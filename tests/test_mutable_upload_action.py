"""Spec for the publish-job supply-chain exposure.

These tests fail while `.github/workflows/cicd.yml` runs a third-party action
from a movable tag and hands it the object-storage credentials, or leaves the
job checkout token on disk for that action to read.

They pass once every such action is pinned to a full 40-character commit SHA
(or replaced by a first-party `run` step) and a later unpinned third-party
step can no longer read the checkout token. No production code is executed
against DigitalOcean or GitHub; the harness reproduces the runner and checkout
steps cited in the test, with placeholder secret values.
"""

from __future__ import annotations

import base64
import json
import os
import re
import subprocess
import tempfile
import threading
import unittest
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_PATH = REPO_ROOT / ".github" / "workflows" / "cicd.yml"

# actions/checkout@v7 (commit 3d3c42e5aac5ba805825da76410c181273ba90b1) action.yml.
# The runner applies these defaults when the workflow omits the input
# (ActionRunner.cs merges definition.Data.Inputs). input-helper.ts then treats
# only the string TRUE as persisted credentials.
CHECKOUT_PERSIST_DEFAULT = "true"
CHECKOUT_TOKEN_DEFAULT = "${{ github.token }}"

FULL_SHA = re.compile(r"^[0-9a-fA-F]{40}$")
EXPRESSION = re.compile(r"\$\{\{\s*([^}]+?)\s*\}\}")

# Placeholder values only. These are not real credentials.
PLACEHOLDERS = {
    "DO_ACCESS_KEY": "placeholder-do-access-key",
    "DO_SECRET_KEY": "placeholder-do-secret-key",
    "DO_SPACE_NAME": "placeholder-do-space-name",
    "DO_SPACE_REGION": "placeholder-do-space-region",
    "NPM_ACCESS_TOKEN": "placeholder-npm-token",
    "publish-job-token": "placeholder-publish-job-token",
    "resolve-job-token": "placeholder-resolve-job-token",
}


ATTACKER_MAIN = r"""
const fs = require('fs');

// Same read as action-input-parser 1.2.38 lib/index.js getEnvVar, which is the
// copy bundled in BetaHuhn/do-spaces-action dist/index.js (the runs.main file).
function getEnvVar(key) {
  var parsed = process.env["INPUT_".concat(key.replace(/ /g, '_').toUpperCase())];
  var raw = process.env[key];
  return parsed || raw || undefined;
}

const viaParser = {};
for (const key of process.argv.slice(2)) {
  viaParser[key] = getEnvVar(key) || null;
}

const inputs = {};
for (const [key, value] of Object.entries(process.env)) {
  if (key.startsWith('INPUT_')) inputs[key] = value;
}

let token = null;
const credentialPaths = [];
try {
  const cfg = fs.readFileSync('.git/config', 'utf8');
  for (const line of cfg.split('\n')) {
    const match = line.match(/^\s*path\s*=\s*(.*?)\s*$/);
    if (match) credentialPaths.push(match[1]);
  }
} catch (err) {}

for (const credentialPath of credentialPaths) {
  try {
    const text = fs.readFileSync(credentialPath, 'utf8');
    const match = text.match(/AUTHORIZATION:\s+basic\s+(\S+)/);
    if (match) token = Buffer.from(match[1], 'base64').toString('utf8');
  } catch (err) {}
}

process.stdout.write(JSON.stringify({
  attacker: true,
  inputs,
  viaParser,
  token,
  credentialPaths,
}) + '\n');
"""

BENIGN_MAIN = "process.stdout.write(JSON.stringify({benign:true})+'\\n');\n"

ACTION_YML = """name: stand-in
runs:
  using: node20
  main: dist/index.js
"""


def run(cmd, cwd=None, check=True, env=None):
    return subprocess.run(
        cmd,
        cwd=cwd,
        env=env,
        check=check,
        text=True,
        capture_output=True,
    )


def git(repo, *args, check=True):
    return run(["git", "-C", str(repo), *args], check=check)


def load_workflow():
    data = yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))
    # PyYAML 1.1 parses the bare key `on` as boolean true.
    if True in data and "on" not in data:
        data["on"] = data.pop(True)
    return data


def evaluate(value, secret_values, outputs):
    if value is None:
        return ""
    text = str(value)

    def replace(match):
        expr = match.group(1).strip()
        if expr.startswith("secrets."):
            return secret_values[expr.split(".", 1)[1]]
        if expr == "github.token":
            return secret_values["GITHUB_TOKEN"]
        needs = re.fullmatch(
            r"needs\.([A-Za-z0-9_-]+)\.outputs\.([A-Za-z0-9_-]+)", expr
        )
        if needs:
            return outputs[needs.group(2)]
        return match.group(0)

    return EXPRESSION.sub(replace, text)


def step_inputs(step, secret_values, outputs):
    raw = step.get("with") or {}
    return {
        key: evaluate(value, secret_values, outputs)
        for key, value in raw.items()
    }


def step_env(step, secret_values, outputs):
    raw = step.get("env") or {}
    return {
        key: evaluate(value, secret_values, outputs)
        for key, value in raw.items()
    }


def parse_uses(uses):
    if uses.startswith("./") or uses.startswith("docker://"):
        return None
    owner_repo, _, ref = uses.rpartition("@")
    if not owner_repo or not ref or "/" not in owner_repo:
        raise AssertionError(f"unrecognized action reference: {uses}")
    owner, repo = owner_repo.split("/", 1)
    return owner, repo, ref


def is_untrusted(uses):
    """Third-party action pinned to something other than a full commit SHA.

    actions/* is the GitHub-maintained org. This finding's attacker updates
    the tag of the other action repositories the workflow names.
    """
    parsed = parse_uses(uses)
    if parsed is None:
        return False
    owner, _repo, ref = parsed
    if owner == "actions":
        return False
    return not FULL_SHA.fullmatch(ref)


def contents_permission(workflow, job):
    # workflow syntax: permissions are applied at workflow level, then job level.
    permissions = dict(workflow.get("permissions") or {})
    if job.get("permissions") is not None:
        permissions = dict(job.get("permissions") or {})
    return permissions.get("contents")


def persist_credentials(step):
    raw = (step.get("with") or {}).get("persist-credentials", CHECKOUT_PERSIST_DEFAULT)
    if raw is None or str(raw) == "":
        raw = "false"
    return str(raw).upper() == "TRUE"


def init_repo(path):
    path.mkdir(parents=True, exist_ok=True)
    git(path, "init", "-q")
    git(path, "config", "user.email", "tests@example.com")
    git(path, "config", "user.name", "tests")


def commit_action(repo, script, message):
    dist = repo / "dist"
    dist.mkdir(parents=True, exist_ok=True)
    (repo / "action.yml").write_text(ACTION_YML, encoding="utf-8")
    (dist / "index.js").write_text(script, encoding="utf-8")
    git(repo, "add", "action.yml", "dist/index.js")
    git(repo, "commit", "-q", "-m", message)
    return git(repo, "rev-parse", "HEAD").stdout.strip()


def configure_token(workspace, runner_temp, token, server_origin):
    """Port of actions/checkout GitAuthHelper.configureToken for a non-container job.

    Writes the basic credential to a file under RUNNER_TEMP and points the
    local includeIf entries at it. The placeholder replacement matches
    git-auth-helper.ts so the token is not passed as a git argument.
    """
    credential_path = runner_temp / f"git-credentials-{uuid.uuid4()}.config"
    key = f"http.{server_origin}/.extraheader"
    placeholder = "AUTHORIZATION: basic ***"
    basic = base64.b64encode(f"x-access-token:{token}".encode()).decode()
    run(
        ["git", "config", "--file", str(credential_path), key, placeholder]
    )
    content = credential_path.read_text(encoding="utf-8")
    if content.count(placeholder) != 1:
        raise AssertionError("checkout credential placeholder was not written once")
    credential_path.write_text(
        content.replace(placeholder, f"AUTHORIZATION: basic {basic}"),
        encoding="utf-8",
    )
    git_dir = str(workspace / ".git").replace("\\", "/")
    git(
        workspace,
        "config",
        "--local",
        f"includeIf.gitdir:{git_dir}.path",
        str(credential_path),
    )
    git(
        workspace,
        "config",
        "--local",
        f"includeIf.gitdir:{git_dir}/worktrees/*.path",
        str(credential_path),
    )
    return credential_path


def remove_token(workspace, runner_temp):
    """Port of GitAuthHelper.removeToken for the main repository config."""
    listed = git(
        workspace,
        "config",
        "--local",
        "--name-only",
        "--get-regexp",
        r"^includeIf\.gitdir:",
        check=False,
    )
    if listed.returncode not in (0, 1):
        raise AssertionError(listed.stderr)
    keys = [line for line in listed.stdout.splitlines() if line]
    for key in keys:
        values = git(
            workspace, "config", "--local", "--get-all", key, check=False
        )
        for value in values.stdout.splitlines():
            name = Path(value).name
            if re.fullmatch(r"git-credentials-[0-9a-f-]+\.config", name, re.I):
                git(
                    workspace,
                    "config",
                    "--local",
                    "--unset-all",
                    key,
                    value,
                    check=False,
                )
                credential = Path(value)
                try:
                    credential.relative_to(runner_temp)
                except ValueError:
                    continue
                credential.unlink(missing_ok=True)


def execute_resolved_action(action_repo, sha, workspace, inputs, extra_env):
    git(action_repo, "checkout", "-qf", sha)
    manifest = yaml.safe_load((action_repo / "action.yml").read_text(encoding="utf-8"))
    main = manifest["runs"]["main"]
    env = {
        "PATH": os.environ.get("PATH", ""),
        "HOME": os.environ.get("HOME", str(workspace)),
    }
    for key, value in inputs.items():
        env_key = "INPUT_" + key.replace(" ", "_").upper()
        env[env_key] = value
    env.update(extra_env)
    proc = run(
        ["node", str(action_repo / main), *inputs.keys()],
        cwd=workspace,
        check=False,
        env=env,
    )
    if proc.returncode != 0:
        raise AssertionError(proc.stderr)
    line = proc.stdout.strip().splitlines()[-1]
    return json.loads(line)


def secret_hits(observed, named_secrets):
    hits = []
    blobs = {}
    blobs.update(observed.get("inputs") or {})
    for key, value in (observed.get("viaParser") or {}).items():
        blobs[f"getEnvVar:{key}"] = value
    if observed.get("token"):
        blobs["checkout-credential"] = observed["token"]
    for label, value in blobs.items():
        if not value:
            continue
        for name, secret in named_secrets.items():
            if secret and secret in str(value):
                hits.append(f"{label} contains {name}")
    return hits


class ActionRegistry:
    """Local stand-in for the action repositories named by the workflow.

    Each repository starts with a benign commit at the workflow's tag. The
    attacker then force-updates that tag, which is the git operation a tag
    publisher can perform. Resolution uses `git rev-parse` at job start, which
    is when the runner asks for a ResolvedSha of the workflow ref.
    """

    def __init__(self, root):
        self.root = Path(root)
        self.repos = {}
        self.attacker_sha = {}
        self.benign_sha = {}

    def prepare(self, owner, repo, ref):
        key = f"{owner}/{repo}"
        if key in self.repos:
            return
        repo_path = self.root / owner / repo
        init_repo(repo_path)
        benign = commit_action(repo_path, BENIGN_MAIN, "published action")
        if FULL_SHA.fullmatch(ref):
            self.benign_sha[key] = benign
            self.attacker_sha[key] = None
        else:
            git(repo_path, "tag", ref, benign)
            attacker = commit_action(repo_path, ATTACKER_MAIN, "replaced action")
            git(repo_path, "tag", "-f", ref, attacker)
            moved = git(repo_path, "rev-parse", f"{ref}^{{commit}}").stdout.strip()
            if moved != attacker or attacker == benign:
                raise AssertionError("tag update did not move the ref")
            self.benign_sha[key] = benign
            self.attacker_sha[key] = attacker
        self.repos[key] = repo_path

    def resolve(self, owner, repo, ref):
        key = f"{owner}/{repo}"
        repo_path = self.repos[key]
        if FULL_SHA.fullmatch(ref):
            # A full commit id is not a tag. Moving tags does not change it.
            resolved = git(repo_path, "rev-parse", "--verify", f"{ref}^{{commit}}", check=False)
            if resolved.returncode != 0:
                return ref.lower()
            return resolved.stdout.strip()
        return git(repo_path, "rev-parse", f"{ref}^{{commit}}").stdout.strip()


def run_job(workflow, job_name, job_token_name, registry, outputs):
    job = workflow["jobs"][job_name]
    token = PLACEHOLDERS[job_token_name]
    named_secrets = {
        "DO_ACCESS_KEY": PLACEHOLDERS["DO_ACCESS_KEY"],
        "DO_SECRET_KEY": PLACEHOLDERS["DO_SECRET_KEY"],
        "DO_SPACE_NAME": PLACEHOLDERS["DO_SPACE_NAME"],
        "DO_SPACE_REGION": PLACEHOLDERS["DO_SPACE_REGION"],
        "NPM_ACCESS_TOKEN": PLACEHOLDERS["NPM_ACCESS_TOKEN"],
        "GITHUB_TOKEN": token,
        job_token_name: token,
    }
    secret_values = dict(named_secrets)
    leaks = []
    checked = []

    for owner, repo, ref in untrusted_refs(job):
        registry.prepare(owner, repo, ref)

    with tempfile.TemporaryDirectory() as tmp:
        workspace = Path(tmp) / "workspace"
        runner_temp = Path(tmp) / "runner-temp"
        runner_temp.mkdir()
        init_repo(workspace)
        (workspace / "README.md").write_text("workspace\n", encoding="utf-8")
        git(workspace, "add", "README.md")
        git(workspace, "commit", "-q", "-m", "checkout")

        for index, step in enumerate(job["steps"]):
            uses = step.get("uses")
            if not uses:
                continue
            parsed = parse_uses(uses)
            if parsed and parsed[0] == "actions" and parsed[1].startswith("checkout"):
                if persist_credentials(step):
                    token_expr = (step.get("with") or {}).get("token", CHECKOUT_TOKEN_DEFAULT)
                    configure_token(
                        workspace,
                        runner_temp,
                        evaluate(token_expr, secret_values, outputs),
                        "https://github.com",
                    )
                else:
                    # configure-then-remove, matching getSource's finally block
                    # when persistCredentials is false.
                    token_expr = (step.get("with") or {}).get("token", CHECKOUT_TOKEN_DEFAULT)
                    configure_token(
                        workspace,
                        runner_temp,
                        evaluate(token_expr, secret_values, outputs),
                        "https://github.com",
                    )
                    remove_token(workspace, runner_temp)
                continue
            if not is_untrusted(uses):
                continue
            owner, repo, ref = parsed
            sha = registry.resolve(owner, repo, ref)
            checked.append(f"{job_name}[{index}] {uses} -> {sha}")
            if registry.attacker_sha.get(f"{owner}/{repo}") != sha:
                continue
            inputs = step_inputs(step, secret_values, outputs)
            observed = execute_resolved_action(
                registry.repos[f"{owner}/{repo}"],
                sha,
                workspace,
                inputs,
                step_env(step, secret_values, outputs),
            )
            hits = secret_hits(observed, named_secrets)
            if hits:
                leaks.append(f"{job_name} step {index} ({uses}): {', '.join(hits)}")
    return leaks, checked


def untrusted_refs(job):
    refs = []
    for step in job["steps"]:
        uses = step.get("uses")
        if uses and is_untrusted(uses):
            refs.append(parse_uses(uses))
    return refs


class MutableUploadActionTests(unittest.TestCase):
    def test_publish_job_does_not_hand_a_moved_tag_storage_keys_or_write_token(self):
        workflow = load_workflow()
        self.assertIn("push", workflow["on"])
        push = workflow["on"]["push"]
        self.assertIn("master", push["branches"])
        self.assertIn("main", push["branches"])
        self.assertIn("v*", push["tags"])
        job = workflow["jobs"]["publish"]
        self.assertEqual(contents_permission(workflow, job), "write")
        self.assertFalse(
            (REPO_ROOT / ".github" / "workflows" / "actions.lock").exists(),
            "an actions lockfile would pin the tag before this test's resolver runs",
        )

        upload_steps = [
            step["uses"]
            for step in job["steps"]
            if step.get("uses", "").startswith("BetaHuhn/do-spaces-action@")
        ]
        # Every catalog upload shares the pin. A fix that leaves one behind still fails.
        self.assertGreaterEqual(len(upload_steps), 1)

        with tempfile.TemporaryDirectory() as tmp:
            registry = ActionRegistry(tmp)
            leaks, checked = run_job(
                workflow,
                "publish",
                "publish-job-token",
                registry,
                {"simple_version": "9.9.9"},
            )
        do_spaces_checked = [item for item in checked if "do-spaces-action@" in item]
        self.assertEqual(
            len(do_spaces_checked),
            len(upload_steps),
            "the harness did not execute every do-spaces-action step",
        )
        self.assertEqual(leaks, [])

    def test_resolve_version_does_not_hand_a_moved_tag_the_job_token(self):
        workflow = load_workflow()
        job = workflow["jobs"]["resolve-version"]
        self.assertEqual(contents_permission(workflow, job), "read")
        semver_steps = [
            step["uses"]
            for step in job["steps"]
            if step.get("uses", "").startswith("Bioblaze/game-semver-action@")
        ]
        self.assertGreaterEqual(len(semver_steps), 1)
        with tempfile.TemporaryDirectory() as tmp:
            registry = ActionRegistry(tmp)
            leaks, checked = run_job(
                workflow,
                "resolve-version",
                "resolve-job-token",
                registry,
                {"simple_version": "9.9.9"},
            )
        semver_checked = [item for item in checked if "game-semver-action@" in item]
        self.assertEqual(len(semver_checked), len(semver_steps))
        self.assertEqual(leaks, [])

    def test_checkout_credential_file_is_presented_on_http(self):
        """The credential configureToken writes is the header git sends.

        This is the client half of a push. The publish job's contents: write
        permission is what makes that token able to update the repository.
        """
        captured = {}

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                captured["authorization"] = self.headers.get("Authorization")
                self.send_response(401)
                self.end_headers()

            def log_message(self, _format, *_args):
                return

        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        port = server.server_address[1]
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with tempfile.TemporaryDirectory() as tmp:
                workspace = Path(tmp) / "workspace"
                runner_temp = Path(tmp) / "runner-temp"
                runner_temp.mkdir()
                init_repo(workspace)
                token = PLACEHOLDERS["publish-job-token"]
                origin = f"http://127.0.0.1:{port}"
                configure_token(workspace, runner_temp, token, origin)
                git(
                    workspace,
                    "remote",
                    "add",
                    "origin",
                    f"{origin}/example.git",
                )
                git(workspace, "ls-remote", "origin", check=False)
        finally:
            server.shutdown()
            server.server_close()

        header = captured.get("authorization")
        self.assertIsNotNone(header)
        scheme, _, encoded = header.partition(" ")
        self.assertEqual(scheme.lower(), "basic")
        decoded = base64.b64decode(encoded).decode()
        self.assertEqual(decoded, f"x-access-token:{PLACEHOLDERS['publish-job-token']}")


if __name__ == "__main__":
    unittest.main()
