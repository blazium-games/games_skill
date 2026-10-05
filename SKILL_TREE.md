# Blazium Games skill tree

Blazium Games is the platform for playing and publishing games, applications, mods, and assets. A token belongs to one server: `blazium-games` (developer, `https://mcp.blazium.games/mcp`, keys `bgames_mcp_`) publishes pages, builds, crashes, analytics, and keys. `blazium-games-player` (player, `https://mcp.blazium.games/player`, keys `bgames_play_`) finds, reviews, installs, and buys.

The guide is [docs.blazium.games](https://docs.blazium.games). This file is the skill index. The docs site remains the source for how the platform works.

## Read this first

- Docs map: https://docs.blazium.games/llms.txt
- Platform map: https://blazium.games/llms.txt
- Which files exist, and which do not: https://docs.blazium.games/docs/discovery
- Introduction: https://docs.blazium.games/docs/intro
- Developer server card: https://mcp.blazium.games/.well-known/mcp/server-card.json
- Player server card: https://mcp.blazium.games/.well-known/mcp/player-server-card.json

## Start here

New to Blazium Games? Start with [blazium-games-get-started](skills/blazium-games-get-started/SKILL.md). It connects the right server, verifies the account, and routes to the skill that matches the goal. The plugin guide is [Cursor plugin](https://docs.blazium.games/docs/cursor-plugin).

## Skills

| Skill | Use it to | Docs |
|-------|-----------|------|
| [blazium-games-get-started](skills/blazium-games-get-started/SKILL.md) | Connect, verify, and pick a workflow | [MCP](https://docs.blazium.games/docs/mcp), [OAuth](https://docs.blazium.games/docs/mcp/oauth), [Cursor plugin](https://docs.blazium.games/docs/cursor-plugin) |
| [blazium-games-store-page](skills/blazium-games-store-page/SKILL.md) | Create or edit a store page, set a price or donations, fill the press kit | [Listings](https://docs.blazium.games/docs/listings), [Content rules](https://docs.blazium.games/docs/content-rules), [Press kit](https://docs.blazium.games/docs/press-kit), [Images](https://docs.blazium.games/docs/graphical_assets_guidelines), [Media CLI](https://docs.blazium.games/docs/cli/media), [Selling](https://docs.blazium.games/docs/payments/selling) |
| [blazium-games-deploy](skills/blazium-games-deploy/SKILL.md) | Ship builds from CI or `npm install -g @blazium-games/cli` | [Deploy builds](https://docs.blazium.games/docs/deploy), [CLI](https://docs.blazium.games/docs/cli), [CI](https://docs.blazium.games/docs/cli/ci) |
| [blazium-games-crash-reporting](skills/blazium-games-crash-reporting/SKILL.md) | Send crashes and events from a game | [Crash reporting](https://docs.blazium.games/docs/crash-reporting), [Symbols](https://docs.blazium.games/docs/cli/symbols) |
| [blazium-games-debug-crash](skills/blazium-games-debug-crash/SKILL.md) | Triage crashes and map them to code | [Reading crashes](https://docs.blazium.games/docs/crash-reporting#reading-crashes) |
| [blazium-games-analytics](skills/blazium-games-analytics/SKILL.md) | Summarize page traffic and downloads | [Download analytics](https://docs.blazium.games/docs/download-analytics), [MCP reference](https://docs.blazium.games/docs/mcp/reference) |
| [blazium-games-keys](skills/blazium-games-keys/SKILL.md) | Inspect and rotate MCP and deploy keys | [Access and keys](https://docs.blazium.games/docs/mcp/access-and-keys), [Permissions](https://docs.blazium.games/docs/legal/permissions) |
| [blazium-games-player](skills/blazium-games-player/SKILL.md) | Recommendations, catalog search, reviews, bug reports, friends, launcher links, game chat, and chat tokens for IRC clients | [Player MCP](https://docs.blazium.games/docs/mcp/player), [Game chat](https://docs.blazium.games/docs/storefront/chat), [Chat Rules](https://blazium.games/chat-rules) |
| [blazium-games-purchases](skills/blazium-games-purchases/SKILL.md) | Buy, donate, and top up within a spending limit | [Agent purchases](https://docs.blazium.games/docs/payments/agent-purchases), [Top up](https://docs.blazium.games/docs/payments/top-up), [Buying](https://docs.blazium.games/docs/payments/buying) |

## Typical paths

- **New game:** get-started, store-page, deploy, crash-reporting
- **Sell a game:** store-page, deploy. Selling rules: https://docs.blazium.games/docs/payments/selling
- **Buy a game:** player, purchases
- **Existing game, new build:** deploy, crash-reporting
- **Players report crashes:** debug-crash
- **Find something to play:** player
- **Leaked key:** keys
- **Use chat in an IRC client, or a chat token leaked:** player
- **Moderate a game's chat:** get-started (chat tools)

## More of the guide

- [Developer mode](https://docs.blazium.games/docs/developer-mode)
- [Public API](https://docs.blazium.games/docs/api-reference)
- [Payments](https://docs.blazium.games/docs/payments)
- [Account security](https://docs.blazium.games/docs/account-security)
- [Linked accounts](https://docs.blazium.games/docs/linked-accounts)
- [DMCA](https://docs.blazium.games/docs/storefront/dmca)
- [Report a page](https://docs.blazium.games/docs/storefront/report)

## References in this repo

- [Tools](skills/blazium-games-get-started/references/tools.md)
- [Resources](skills/blazium-games-get-started/references/resources.md)
- [Prompts](skills/blazium-games-get-started/references/prompts.md)
- [Authentication](skills/blazium-games-get-started/references/auth.md)
- Player tools: [tools.md](skills/blazium-games-player/references/tools.md)
