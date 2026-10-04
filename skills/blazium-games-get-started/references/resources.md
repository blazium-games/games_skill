# Blazium Games MCP resources

JSON resources return JSON. `{uid}` accepts a game uid or vanity name. `ui://` resources return HTML for hosts that support MCP Apps.

## Resources

| URI | Name | Contents |
|-----|------|----------|
| `blazium-games://me` | `me` | Authenticated user (account tokens only) |
| `blazium-games://games` | `games` | Games list |
| `blazium-games://wallet` | `wallet` | Stored balance and payment rules (account tokens only). **Deprecated**: removed from this server after 2026-10-28; use the player server |
| `blazium-games://library` | `library` | Owned games and licenses (account tokens only). **Deprecated**: removed from this server after 2026-10-28; use the player server |
| `ui://blazium-games/account.html` | `account` | Account status, with links to finish sign-in on the website. MIME `text/html;profile=mcp-app` |
| `ui://blazium-games/approval.html` | `approval` | Approval status, confirm link, and the emailed code |
| `ui://blazium-games/dev-game.html` | `dev-game` | Store pages this account can edit |
| `ui://blazium-games/analytics.html` | `analytics` | Visitor analytics |
| `ui://blazium-games/sales.html` | `sales` | Sales, and a price form that saves when the human clicks |
| `ui://blazium-games/crashes.html` | `crashes` | Crash reports and a private download link |
| `ui://blazium-games/checkout.html` | `checkout` | Quote, buy, and donate. **Deprecated** after 2026-10-28 |
| `ui://blazium-games/wallet.html` | `wallet` | Balance and a card top-up link. **Deprecated** after 2026-10-28 |
| `ui://blazium-games/library.html` | `library` | Owned games and download links. **Deprecated** after 2026-10-28 |

A host that supports MCP Apps renders a `ui://` resource beside the tool result. The human confirms a price change in the view. Card payment happens on the Checkout link. Key-issuing tools, payout setup, and cash-out stay text-only.

## Resource templates

| URI template | Name | Contents |
|--------------|------|----------|
| `blazium-games://games/{uid}` | `game` | One game page |
| `blazium-games://games/{uid}/analytics` | `game-analytics` | Visitor analytics for a game |
| `blazium-games://games/{uid}/crashes` | `game-crashes` | Crash reports for a game |
| `blazium-games://games/{uid}/deploy` | `game-deploy` | Non-secret deploy endpoints and key prefixes |
| `blazium-games://games/{uid}/builds` | `game-builds` | Uploaded builds and crash reporter build_ids |
