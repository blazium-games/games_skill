# Grok host — Blazium Games skills

How Grok should load these skills. Same files as Claude, Cursor, and Codex. No invented marketplace schema.

These skills are for the store at [blazium.games](https://blazium.games). They are not the Blazium engine skills.

Read [SKILL_TREE.md](SKILL_TREE.md) for which skill to use. The guide is [docs.blazium.games](https://docs.blazium.games), and the short map is [llms.txt](https://docs.blazium.games/llms.txt). Do not invent platform behavior that those pages do not describe.

## Install

Grok routes on each skill's YAML `description`. It reads `SKILL.md` from a skills directory. Grok also auto-reads Claude Code marketplaces, plugins, and skills, so `.claude-plugin/marketplace.json` works when that plugin layout is present. A symlink into `./.grok/skills/` or `~/.grok/skills/` is the explicit path when you are not loading the Claude plugin.

From a clone of this repo:

```bash
python scripts/sync_packs.py
python scripts/validate_packs.py
```

| Method | What to do |
|--------|------------|
| Project skills | Symlink or copy `skills/<name>/` into the workspace skills root Grok already lists |
| User skills | Symlink `skills/` into `~/.grok/skills/` |
| Claude plugin | Leave `.claude-plugin/marketplace.json` in place. Grok reads it automatically |

Do not invent `.grok-plugin/marketplace.json`. If a future Grok marketplace lands, register the existing Claude catalog paths. Do not fork the skill bodies.

## Plugins

- `blazium-games-developer` — publishing
- `blazium-games-player` — playing and buying
- `blazium-games` — both, plus the developer and player MCP servers
