"""Link each pack's skills into plugins/<pack>/skills for Cursor and Codex zips."""

import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from packs import PACKS  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


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


def main() -> int:
    for name, pack in PACKS.items():
        plugin = ROOT / "plugins" / name
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
