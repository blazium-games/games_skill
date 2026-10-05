# Blazium Games skills

Agent skills for [Blazium Games](https://blazium.games), the store operated by Divine Games, Inc. They are not the engine skills at [`@blazium-engine/skills`](https://www.npmjs.com/package/@blazium-engine/skills), and they do not install Hub or the engine.

## Install

```bash
npm install @blazium-games/skills
```

Cursor: add `blazium-games/games_skill` from **Cursor Settings > Plugins**, then enable **Blazium Games**.

## Platform

- Docs: [docs.blazium.games](https://docs.blazium.games) and the map [llms.txt](https://docs.blazium.games/llms.txt)
- Skills: `npm install @blazium-games/skills`, or Cursor Settings > Plugins > `blazium-games/games_skill`. Index: [SKILL_TREE.md](https://github.com/blazium-games/games_skill/blob/master/SKILL_TREE.md)
- MCP: [developer server](https://docs.blazium.games/docs/mcp) at `https://mcp.blazium.games/mcp`, and [player server](https://docs.blazium.games/docs/mcp/player) at `https://mcp.blazium.games/player`
- CLI: `npm install -g @blazium-games/cli` (`chauffeur`), guide at [docs.blazium.games/docs/cli](https://docs.blazium.games/docs/cli)
- Launcher: Windows setup from [Releases](https://github.com/blazium-games/games_launcher/releases), guide at [desktop app](https://docs.blazium.games/docs/storefront/desktop-app)
- Support: [blazium-games/support](https://github.com/blazium-games/support/issues). Status: [status.blazium.games](https://status.blazium.games)

## This repo

This package is the versioned release. The guide and the in-repo plugin source stay in [games_docs](https://github.com/blazium-games/games_docs). The skill index, with links into the guide, is [SKILL_TREE.md](SKILL_TREE.md). The catalog is [https://cdn.blazium.app/games-skills/skills.json](https://cdn.blazium.app/games-skills/skills.json).

A game on Blazium Games does not have to be made with the Blazium engine. The upload command is `chauffeur` from [`@blazium-games/cli`](https://www.npmjs.com/package/@blazium-games/cli).

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

| Plugin | What it covers |
|--------|----------------|
| `blazium-games-developer` | Get started, store page, deploy, crash reporting, debug crash, analytics, keys |
| `blazium-games-player` | Get started, player, purchases |
| `blazium-games` | Every skill, plus `mcp.json` |

`mcp.json` points at `https://mcp.blazium.games/mcp` and `https://mcp.blazium.games/player`. A token belongs to one server.

- Claude Code reads `.claude-plugin/marketplace.json`.
- Cursor reads `.cursor-plugin/marketplace.json`.
- Codex reads `.agents/plugins/marketplace.json`.
- Grok reads the Claude marketplace and `./.grok/skills/`. See [GROK.md](GROK.md).

Platform bugs go to [blazium-games/support](https://github.com/blazium-games/support/issues), not this repository's issue tracker.

## License

Licensed under the MIT License — see [LICENSE](LICENSE).
