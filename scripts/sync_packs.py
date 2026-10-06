"""Link each pack's skills into plugins/<pack>/skills for Cursor and Codex zips."""

import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from packs import PACKS  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.1.0"
HOMEPAGE = "https://docs.blazium.games"
REPOSITORY = "https://github.com/blazium-games/games_skill"
CODEXIGNORE = """.env
.env.*
*.local
__pycache__/
"""


def copy_tree(dest: Path, src: Path) -> None:
    if dest.exists() or dest.is_symlink():
        if dest.is_dir() and not dest.is_symlink():
            shutil.rmtree(dest)
        else:
            dest.unlink()
    if src.is_dir():
        shutil.copytree(src, dest, symlinks=False)
    else:
        shutil.copy2(src, dest)


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def write_pack_surface(plugin: Path, name: str, pack: dict) -> None:
    desc = pack["description"]
    interface = {
        "displayName": pack["display"],
        "shortDescription": desc,
        "longDescription": desc,
        "developerName": "Blazium Games",
        "category": "Developer Tools",
        "capabilities": ["Read", "Write"],
        "websiteURL": HOMEPAGE,
        "defaultPrompt": [
            "Use Blazium Games skills for the store at blazium.games.",
            desc,
        ],
    }
    manifest = {
        "name": name,
        "version": VERSION,
        "description": desc,
        "author": {"name": "Blazium Games"},
        "homepage": HOMEPAGE,
        "repository": REPOSITORY,
        "license": "MIT",
        "keywords": ["blazium", "blazium-games", "skills"],
    }
    write_json(plugin / "plugin.json", manifest)
    write_json(plugin / ".codex-plugin" / "plugin.json", {**manifest, "interface": interface})
    (plugin / "README.md").write_text(
        f"# {pack['display']}\n\n{desc}\n\n"
        f"Install this pack from the [games_skill]({REPOSITORY}) marketplace.\n",
        encoding="utf-8",
    )
    shutil.copyfile(ROOT / "SECURITY.md", plugin / "SECURITY.md")
    shutil.copyfile(ROOT / "LICENSE", plugin / "LICENSE")
    (plugin / ".codexignore").write_text(CODEXIGNORE, encoding="utf-8")


def main() -> int:
    for name, pack in PACKS.items():
        plugin = ROOT / "plugins" / name
        write_pack_surface(plugin, name, pack)
        skills_dir = plugin / "skills"
        if skills_dir.exists() and not skills_dir.is_symlink():
            shutil.rmtree(skills_dir)
        skills_dir.mkdir(parents=True, exist_ok=True)
        for skill in pack["skills"]:
            src = ROOT / "skills" / skill
            if not (src / "SKILL.md").is_file():
                print(f"missing {src / 'SKILL.md'}", file=sys.stderr)
                return 1
            copy_tree(skills_dir / skill, src)
        if pack["mcp"]:
            copy_tree(plugin / "mcp.json", ROOT / "mcp.json")
    print(f"copied {len(PACKS)} packs")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except OSError as exc:
        print(exc, file=sys.stderr)
        raise SystemExit(1)
