# Blazium Games skills

Agent skills for [Blazium Games](https://blazium.games), the store operated by Divine Games, Inc. They cover store pages, deploys, crash reporting, analytics, keys, and playing or buying games.

This package is the store. It is not the engine skills at [`@blazium-engine/skills`](https://www.npmjs.com/package/@blazium-engine/skills), and it does not install Hub, the engine CLI, or the toolchain. A game on Blazium Games does not have to be made with the Blazium engine. The upload command is `chauffeur` from [`@blazium-games/cli`](https://www.npmjs.com/package/@blazium-games/cli).

The guide and the in-repo Cursor plugin source stay in [games_docs](https://github.com/blazium-games/games_docs). This repo is the versioned release. The skill index, with links into the guide, is [SKILL_TREE.md](SKILL_TREE.md).

## Documentation

Read these before guessing how the platform works:

- [docs.blazium.games](https://docs.blazium.games)
- Docs map: [llms.txt](https://docs.blazium.games/llms.txt)
- Platform map: [blazium.games/llms.txt](https://blazium.games/llms.txt)
- [Discovery files](https://docs.blazium.games/docs/discovery)
- [Introduction](https://docs.blazium.games/docs/intro)

| Skill | Guide |
|-------|--------|
| `blazium-games-get-started` | [MCP](https://docs.blazium.games/docs/mcp), [OAuth](https://docs.blazium.games/docs/mcp/oauth), [Cursor plugin](https://docs.blazium.games/docs/cursor-plugin) |
| `blazium-games-store-page` | [Listings](https://docs.blazium.games/docs/listings), [Content rules](https://docs.blazium.games/docs/content-rules), [Press kit](https://docs.blazium.games/docs/press-kit), [Images](https://docs.blazium.games/docs/graphical_assets_guidelines), [Selling](https://docs.blazium.games/docs/payments/selling) |
| `blazium-games-deploy` | [Deploy builds](https://docs.blazium.games/docs/deploy), [chauffeur CLI](https://docs.blazium.games/docs/cli) |
| `blazium-games-crash-reporting` | [Crash reporting](https://docs.blazium.games/docs/crash-reporting) |
| `blazium-games-debug-crash` | [Reading crashes](https://docs.blazium.games/docs/crash-reporting#reading-crashes) |
| `blazium-games-analytics` | [Download analytics](https://docs.blazium.games/docs/download-analytics) |
| `blazium-games-keys` | [Access and keys](https://docs.blazium.games/docs/mcp/access-and-keys) |
| `blazium-games-player` | [Player MCP](https://docs.blazium.games/docs/mcp/player) |
| `blazium-games-purchases` | [Agent purchases](https://docs.blazium.games/docs/payments/agent-purchases) |

Support is [blazium.games/support](https://blazium.games/support). Status is [status.blazium.games](https://status.blazium.games). Platform bugs go to [blazium-games/support](https://github.com/blazium-games/support/issues).

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
