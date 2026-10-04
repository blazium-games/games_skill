"""Check skill front matter and that every marketplace path exists."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from packs import PACKS  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def front_matter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{path}: missing front matter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError(f"{path}: unclosed front matter")
    data = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data


def main() -> int:
    errors = []
    declared = set()
    for name, pack in PACKS.items():
        for skill in pack["skills"]:
            declared.add(skill)
            skill_md = ROOT / "skills" / skill / "SKILL.md"
            if not skill_md.is_file():
                errors.append(f"{name}: missing {skill_md.relative_to(ROOT)}")
                continue
            meta = front_matter(skill_md)
            if meta.get("name") != skill:
                errors.append(f"{skill}: name is {meta.get('name')!r}")
            if not meta.get("description"):
                errors.append(f"{skill}: missing description")
        plugin_json = ROOT / "plugins" / name / "plugin.json"
        if not plugin_json.is_file():
            errors.append(f"missing {plugin_json.relative_to(ROOT)}")
    on_disk = {p.name for p in (ROOT / "skills").iterdir() if p.is_dir()}
    extra = on_disk - declared
    if extra:
        errors.append("skills not in a pack: " + ", ".join(sorted(extra)))
    for manifest in (
        ROOT / ".claude-plugin" / "marketplace.json",
        ROOT / ".cursor-plugin" / "marketplace.json",
        ROOT / ".agents" / "plugins" / "marketplace.json",
    ):
        if not manifest.is_file():
            errors.append(f"missing {manifest.relative_to(ROOT)}")
            continue
        data = json.loads(manifest.read_text(encoding="utf-8"))
        names = {item.get("name") for item in data.get("plugins", [])}
        missing = set(PACKS) - names
        if missing:
            errors.append(f"{manifest.relative_to(ROOT)}: missing {', '.join(sorted(missing))}")
        for item in data.get("plugins", []):
            for skill_path in item.get("skills", []):
                skill_md = ROOT / skill_path / "SKILL.md"
                if not skill_md.is_file():
                    errors.append(f"{manifest.relative_to(ROOT)}: missing {skill_path}")
            source = item.get("source")
            if isinstance(source, str) and source not in ("./", ".") and source.startswith("./"):
                if not (ROOT / source).exists():
                    errors.append(f"{manifest.relative_to(ROOT)}: missing {source}")
            if isinstance(source, dict) and source.get("path", "").startswith("./"):
                if not (ROOT / source["path"]).exists():
                    errors.append(f"{manifest.relative_to(ROOT)}: missing {source['path']}")
    if not (ROOT / "mcp.json").is_file():
        errors.append("missing mcp.json")
    pkg = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    if pkg.get("name") != "@blazium-games/skills":
        errors.append(f"package name is {pkg.get('name')!r}")
    for doc in ("README.md", "SKILL_TREE.md", "GROK.md"):
        text = (ROOT / doc).read_text(encoding="utf-8") if (ROOT / doc).is_file() else ""
        if "docs.blazium.games" not in text:
            errors.append(f"{doc}: missing docs.blazium.games")
        if doc == "SKILL_TREE.md":
            for skill in declared:
                if skill not in text:
                    errors.append(f"SKILL_TREE.md: missing {skill}")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"ok {len(declared)} skills, {len(PACKS)} packs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
