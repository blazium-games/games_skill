"""Security spec for the skill publish workflow.

A movable tag on Bioblaze/game-semver-action can set simple_version to any
string. The runner inserts that string into `run` scripts with no shell
escaping. These tests expand expressions the way the runner does, then execute
the workflow's own shell. They fail while that insertion can run a command or
replace a published archive.
"""

from __future__ import annotations

import base64
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
WORKFLOW_PATH = REPO / ".github" / "workflows" / "cicd.yml"
ATTACKER_TEXT = b"ATTACKER-SKILL-TEXT"
SEMVER = r"^[0-9]+\.[0-9]+\.[0-9]+$"
OPEN = "${{"
CLOSE = "}}"

# Expressions these tests supply. Anything else in a step under test is a
# sink the harness does not know how to expand, and the test fails closed.
RUNNER_CONTEXT = {
    "github.ref": "refs/heads/main",
    "github.sha": "0" * 40,
    "github.token": "placeholder-not-a-secret",
}


def load_workflow() -> dict:
    return yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))


def expression_segments(raw: str) -> list[tuple[str, str]]:
    """Split a scalar the way actions/runner TemplateReader splits ${{ }}."""
    if OPEN not in raw:
        return [("lit", raw)]
    segments: list[tuple[str, str]] = []
    index = 0
    start = raw.find(OPEN)
    while index < len(raw):
        if start >= 0 and index == start:
            in_string = False
            cursor = index + len(OPEN)
            end = -1
            while cursor < len(raw):
                char = raw[cursor]
                if char == "'":
                    in_string = not in_string
                elif not in_string and char == "}" and raw[cursor - 1] == "}":
                    end = cursor
                    cursor += 1
                    break
                cursor += 1
            if end < 0:
                raise AssertionError("unclosed ${{ in workflow script")
            # Content is between ${{ and }}, matching TemplateReader's substring.
            expression = raw[index + len(OPEN) : end + 1 - len(CLOSE)]
            segments.append(("expr", " ".join(expression.split())))
            index = end + 1
            start = raw.find(OPEN, index)
        elif start >= 0 and index < start:
            segments.append(("lit", raw[index:start]))
            index = start
        else:
            segments.append(("lit", raw[index:]))
            break
    return segments


def expand_run_script(raw: str, values: dict[str, str]) -> str:
    """Insert expression results literally, as FormatResultBuilder does.

    Literal text is kept as written. Expression values are not quoted or
    escaped. An expression that fills the whole scalar is the same concatenation.
    """
    parts: list[str] = []
    for kind, value in expression_segments(raw):
        if kind == "lit":
            parts.append(value)
            continue
        if value not in values and value not in RUNNER_CONTEXT:
            raise AssertionError(f"workflow expands unknown expression {value!r}")
        parts.append(values.get(value, RUNNER_CONTEXT.get(value, "")))
    return "".join(parts)


def parse_github_output(text: str) -> dict[str, str]:
    """Parse GITHUB_OUTPUT the way FileCommandManager.EnvFileKeyValuePairs does.

    Later assignments of the same name replace earlier ones.
    """
    outputs: dict[str, str] = {}
    index = 0
    length = len(text)

    def read_line() -> tuple[str | None, str | None]:
        nonlocal index
        if index >= length:
            return None, None
        newline_at = text.find("\n", index)
        if newline_at < 0:
            line = text[index:]
            index = length
            return line, None
        line = text[index:newline_at]
        index = newline_at + 1
        return line, "\n"

    line, _newline = read_line()
    while line is not None:
        if line != "":
            equals_at = line.find("=")
            heredoc_at = line.find("<<")
            if equals_at >= 0 and (heredoc_at < 0 or equals_at < heredoc_at):
                key, value = line.split("=", 1)
                if key == "":
                    raise AssertionError(f"invalid output line {line!r}")
                outputs[key] = value
            elif heredoc_at >= 0 and (equals_at < 0 or heredoc_at < equals_at):
                key, delimiter = line.split("<<", 1)
                if key == "" or delimiter == "":
                    raise AssertionError(f"invalid output line {line!r}")
                start = index
                end = index
                current, newline = read_line()
                while current != delimiter:
                    if current is None or newline is None:
                        raise AssertionError("unterminated output delimiter")
                    end = index - len(newline)
                    current, newline = read_line()
                outputs[key] = text[start:end] if end > start else ""
            else:
                raise AssertionError(f"invalid output line {line!r}")
        line, _newline = read_line()
    return outputs


def write_action_output(path: Path, name: str, value: str) -> None:
    """Write one output the way @actions/core setOutput does in the action bundle.

    prepareKeyValueMessage stores the string unchanged between a delimiter.
    """
    delimiter = "ghadelimiter_0123456789abcdef0123456789abcdef"
    if delimiter in name or delimiter in value:
        raise AssertionError("delimiter collided with output value")
    path.write_text(f"{name}<<{delimiter}\n{value}\n{delimiter}\n", encoding="utf-8")


def quote_break(commands: str) -> str:
    """Close a double-quoted expansion, run commands, and stop the script."""
    if "\n" in commands:
        raise AssertionError("quote-break payload must be one line")
    return f'"; {commands}; exit 0; echo "'


def command_substitution(commands: str) -> str:
    return f"$({commands})"


def single_quote_break(commands: str) -> str:
    """Close a single-quoted expansion. Inside double quotes this stays data."""
    if "\n" in commands:
        raise AssertionError("single-quote payload must be one line")
    return f"'; {commands}; exit 0; #"


class Workflow:
    def __init__(self, document: dict):
        self.document = document

    def job(self, name: str) -> dict:
        return self.document["jobs"][name]

    def step_by_id(self, job: str, step_id: str) -> dict:
        for step in self.job(job)["steps"]:
            if step.get("id") == step_id:
                return step
        raise AssertionError(f"{job} has no step {step_id}")

    def run_step(self, job: str, name: str) -> dict:
        matches = [step for step in self.job(job)["steps"] if step.get("name") == name]
        if len(matches) != 1:
            raise AssertionError(f"{job} step {name!r} found {len(matches)} times")
        return matches[0]

    def semver_action_uses(self) -> list[str]:
        found: list[str] = []
        for job in self.document["jobs"].values():
            for step in job.get("steps") or []:
                uses = step.get("uses")
                if isinstance(uses, str) and uses.startswith("Bioblaze/game-semver-action@"):
                    found.append(uses)
        return found

    def artifact_glob(self, job: str) -> str:
        for step in self.job(job)["steps"]:
            uses = step.get("uses") or ""
            if uses.startswith("actions/upload-artifact@"):
                return str(step["with"]["path"])
        raise AssertionError(f"{job} does not upload an artifact")

    def download_dirs(self) -> dict[str, str]:
        found: dict[str, str] = {}
        for step in self.job("publish")["steps"]:
            uses = step.get("uses") or ""
            if uses.startswith("actions/download-artifact@"):
                found[str(step["with"]["name"])] = str(step["with"]["path"])
        return found


def install_stubs(bin_dir: Path) -> None:
    # curl and gh are stubbed so the workflow's version lookup cannot leave this machine.
    # python is the command setup-python puts on PATH before the pack scripts run.
    stubs = {
        "curl": "#!/bin/sh\necho 'refusing network from curl stub' >&2\nexit 22\n",
        "jq": "#!/bin/sh\nexit 0\n",
        "gh": "#!/bin/sh\necho 'refusing network from gh stub' >&2\nexit 1\n",
        "python": "#!/bin/sh\nexec python3 \"$@\"\n",
    }
    for name, body in stubs.items():
        path = bin_dir / name
        path.write_text(body, encoding="utf-8")
        path.chmod(0o755)


def step_environment(step: dict, values: dict[str, str], base: dict[str, str]) -> dict[str, str]:
    env = dict(base)
    for key, raw in (step.get("env") or {}).items():
        env[str(key)] = expand_run_script(str(raw), values)
    return env


def execute_step(step: dict, values: dict[str, str], cwd: Path, base_env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    if "run" not in step:
        raise AssertionError("step has no run script")
    script = expand_run_script(str(step["run"]), values)
    script_path = cwd / "workflow-step.sh"
    script_path.write_text(script, encoding="utf-8")
    env = step_environment(step, values, base_env)
    # ubuntu-latest has no shell: override, so the runner invokes bash with sh's -e.
    return subprocess.run(
        ["bash", "-e", str(script_path)],
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )


def copy_repo(destination: Path) -> None:
    shutil.copytree(
        REPO,
        destination,
        symlinks=False,
        ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc", "workflow-step.sh"),
    )


def zip_names_for(globs: list[str]) -> list[str]:
    names: list[str] = []
    for pattern in globs:
        if not pattern.endswith("*.zip"):
            raise AssertionError(f"unexpected artifact path {pattern}")
        names.append(pattern.replace("*.zip", "evil.zip"))
    return names


def pack_commands(marker: Path, zip_names: list[str]) -> str:
    """Shell that records execution and writes attacker zips in the job workspace.

    Zip names are relative so they match the workflow's upload-artifact glob.
    The Python is base64 so the payload can sit inside the single quotes of a
    surrounding printf without the quotes being eaten early.
    """
    writes = [
        'zipfile.ZipFile("%s", "w").writestr("SKILL.md", "ATTACKER-SKILL-TEXT")' % name
        for name in zip_names
    ]
    python = "import zipfile; " + "; ".join(writes)
    encoded = base64.b64encode(python.encode()).decode()
    return (
        f'touch "{marker}"; '
        f"python3 -c 'import base64; exec(base64.b64decode(\"{encoded}\").decode())'"
    )


class SkillPublishInjectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.workflow = Workflow(load_workflow())
        self.temp = Path(tempfile.mkdtemp(prefix="skill-publish-"))
        self.bin_dir = self.temp / "bin"
        self.bin_dir.mkdir()
        install_stubs(self.bin_dir)
        self.addCleanup(shutil.rmtree, self.temp, True)

    def base_env(self, github_output: Path) -> dict[str, str]:
        return {
            "PATH": f"{self.bin_dir}:/usr/bin:/bin",
            "HOME": str(self.temp),
            "LANG": "C.UTF-8",
            "GITHUB_OUTPUT": str(github_output),
            "GITHUB_REF": "refs/heads/main",
            "GITHUB_SHA": "0" * 40,
            "GITHUB_WORKSPACE": str(self.temp),
        }

    def action_output_value(self, value: str) -> str:
        output_file = self.temp / "action-output.txt"
        write_action_output(output_file, "simple_version", value)
        parsed = parse_github_output(output_file.read_text(encoding="utf-8"))
        self.assertIn("simple_version", parsed)
        return parsed["simple_version"]

    def test_semver_action_is_pinned_to_a_commit_sha(self) -> None:
        uses = self.workflow.semver_action_uses()
        self.assertTrue(uses, "workflow does not run Bioblaze/game-semver-action")
        for ref in uses:
            self.assertRegex(ref, r"^Bioblaze/game-semver-action@[0-9a-f]{40}$")

    def test_finalize_command_substitution_has_no_side_effect(self) -> None:
        marker = self.temp / "finalize-command-marker"
        payload = self.action_output_value(command_substitution(f'touch "{marker}"'))
        self.run_finalize(payload)
        self.assertFalse(marker.exists(), "finalize script executed the action output")

    def test_finalize_single_quote_break_has_no_side_effect(self) -> None:
        marker = self.temp / "finalize-single-marker"
        payload = self.action_output_value(single_quote_break(f"touch {marker}"))
        self.run_finalize(payload)
        self.assertFalse(marker.exists(), "finalize script executed the action output")

    def test_finalize_quote_break_does_not_emit_a_shell_version(self) -> None:
        marker = self.temp / "finalize-quote-marker"
        payload = self.action_output_value(quote_break(f'touch "{marker}"'))
        result, outputs = self.run_finalize(payload)
        self.assertFalse(marker.exists(), "finalize script executed the action output")
        if result.returncode == 0:
            version = outputs.get("simple_version", "")
            self.assertRegex(version, SEMVER)

    def test_pack_jobs_do_not_run_a_quote_breaking_version(self) -> None:
        for job in ("pack-claude", "pack-cursor", "pack-codex"):
            with self.subTest(job=job, payload="quote-break"):
                self.assert_pack_rejects(job, quote_break(self.pack_body(job)))

    def test_pack_jobs_do_not_run_command_substitution(self) -> None:
        for job in ("pack-claude", "pack-cursor", "pack-codex"):
            with self.subTest(job=job, payload="command-substitution"):
                marker = self.temp / f"{job}-command-marker"
                payload = command_substitution(f"touch {marker}")
                self.assert_pack_rejects(job, payload, marker=marker)

    def test_pack_jobs_do_not_run_a_single_quoted_break(self) -> None:
        for job in ("pack-claude", "pack-cursor", "pack-codex"):
            with self.subTest(job=job, payload="single-quote"):
                marker = self.temp / f"{job}-single-marker"
                payload = single_quote_break(f"touch {marker}")
                self.assert_pack_rejects(job, payload, marker=marker)

    def test_published_archives_stay_free_of_action_output_commands(self) -> None:
        jobs = ("pack-claude", "pack-cursor", "pack-codex")
        globs = [self.workflow.artifact_glob(job) for job in jobs]
        marker = self.temp / "published-marker"
        # One version string is shared by every pack job. It writes every
        # archive name; each job's upload glob keeps only its own.
        planted = quote_break(pack_commands(marker, zip_names_for(globs)))
        encoded = base64.b64encode(planted.encode()).decode()
        finalize_payload = quote_break(
            f'touch "{marker}"; '
            "python3 -c 'import os,base64; "
            f"p=base64.b64decode(\"{encoded}\").decode(); "
            "open(os.environ[\"GITHUB_OUTPUT\"],\"a\").write(\"simple_version=\"+p+\"\\n\")'"
        )
        result, outputs = self.run_finalize(self.action_output_value(finalize_payload))
        version = outputs.get("simple_version", "")
        archives = self.run_publish_inputs(version, jobs) if result.returncode == 0 and version else []
        attacker_files = [str(path) for path in archives if ATTACKER_TEXT in path.read_bytes()]
        self.assertEqual(attacker_files, [], "publish inputs contain the action's archive")
        self.assertFalse(marker.exists(), "version output executed during publish")
        if result.returncode == 0:
            self.assertRegex(version, SEMVER)

    def pack_body(self, job: str) -> str:
        marker = self.temp / f"{job}-quote-marker"
        archive = zip_names_for([self.workflow.artifact_glob(job)])[0]
        return pack_commands(marker, [archive])

    def assert_pack_rejects(self, job: str, version: str, marker: Path | None = None) -> None:
        cwd = self.temp / job
        copy_repo(cwd)
        github_output = cwd / "github-output.txt"
        github_output.write_text("", encoding="utf-8")
        step = self.workflow.run_step(job, self.pack_step_name(job))
        result = execute_step(
            step,
            {"needs.resolve-version.outputs.simple_version": version},
            cwd,
            self.base_env(github_output),
        )
        produced = [path for path in cwd.glob(self.workflow.artifact_glob(job)) if path.is_file()]
        attacker = [path for path in produced if ATTACKER_TEXT in path.read_bytes()]
        markers = {path for path in self.temp.glob(f"{job}-*-marker") if path.is_file()}
        if marker is not None and marker.exists():
            markers.add(marker)
        self.assertEqual(
            markers,
            set(),
            f"{job} executed the version string\nstdout:{result.stdout}\nstderr:{result.stderr}",
        )
        self.assertEqual(attacker, [], f"{job} left an attacker archive: {attacker}")

    def pack_step_name(self, job: str) -> str:
        names = {
            "pack-claude": "Zip Claude marketplace",
            "pack-cursor": "Zip Cursor plugins",
            "pack-codex": "Zip Codex plugins",
        }
        return names[job]

    def run_finalize(self, action_output: str) -> tuple[subprocess.CompletedProcess[str], dict[str, str]]:
        cwd = self.temp / "resolve-version"
        cwd.mkdir()
        github_output = cwd / "github-output.txt"
        github_output.write_text("", encoding="utf-8")
        step = self.workflow.step_by_id("resolve-version", "finalize")
        result = execute_step(
            step,
            {"steps.version.outputs.simple_version": action_output},
            cwd,
            self.base_env(github_output),
        )
        outputs = parse_github_output(github_output.read_text(encoding="utf-8"))
        return result, outputs

    def run_publish_inputs(self, version: str, jobs: tuple[str, ...]) -> list[Path]:
        """Place each pack artifact where publish downloads it, then run publish's catalog script."""
        downloads = self.workflow.download_dirs()
        publish_root = self.temp / "publish"
        copy_repo(publish_root)
        collected: list[Path] = []
        for job in jobs:
            host = job.removeprefix("pack-")
            self.assertIn(host, downloads)
            pack_dir = self.temp / f"publish-{job}"
            copy_repo(pack_dir)
            github_output = pack_dir / "github-output.txt"
            github_output.write_text("", encoding="utf-8")
            execute_step(
                self.workflow.run_step(job, self.pack_step_name(job)),
                {"needs.resolve-version.outputs.simple_version": version},
                pack_dir,
                self.base_env(github_output),
            )
            matches = [path for path in pack_dir.glob(self.workflow.artifact_glob(job)) if path.is_file()]
            destination = publish_root / downloads[host]
            destination.mkdir(parents=True, exist_ok=True)
            for match in matches:
                target = destination / match.name
                shutil.copy2(match, target)
                collected.append(target)
        catalog_step = self.workflow.run_step("publish", "Require every pack and write skills.json")
        execute_step(
            catalog_step,
            {"needs.resolve-version.outputs.simple_version": version},
            publish_root,
            self.base_env(publish_root / "github-output.txt"),
        )
        return collected


if __name__ == "__main__":
    unittest.main()
