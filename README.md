# Blazium Games skills

Agent skills for [Blazium Games](https://blazium.games), the store operated by Divine Games, Inc. They cover store pages, deploys, crash reporting, analytics, keys, and playing or buying games.

This package is the store. It is not the engine skills at [`@blazium-engine/skills`](https://www.npmjs.com/package/@blazium-engine/skills), and it does not install Hub, the engine CLI, or the toolchain. A game on Blazium Games does not have to be made with the Blazium engine.

The guide and the in-repo Cursor plugin source stay in [games_docs](https://github.com/blazium-games/games_docs). This repo is the versioned release.

## Install

```bash
npm install @blazium-games/skills
```

Cursor: add `blazium-games/games_skill` from **Cursor Settings > Plugins**.

The catalog is [https://cdn.blazium.app/games-skills/skills.json](https://cdn.blazium.app/games-skills/skills.json).

## Plugins

| Plugin | What it covers |
|--------|----------------|
| `blazium-games-developer` | Get started, store page, deploy, crash reporting, debug crash, analytics, keys |
| `blazium-games-player` | Get started, player, purchases |
| `blazium-games` | Every skill, plus `mcp.json` |

`mcp.json` points at `https://mcp.blazium.games/mcp` and `https://mcp.blazium.games/player`. A token belongs to one server.

## Hosts

- Claude Code reads `.claude-plugin/marketplace.json`.
- Cursor reads `.cursor-plugin/marketplace.json`.
- Codex reads `.agents/plugins/marketplace.json`.
- Grok reads the Claude marketplace and `./.grok/skills/`. See [GROK.md](GROK.md).
