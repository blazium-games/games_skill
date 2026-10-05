---
name: blazium-games-player
description: Connect an agent to a Blazium Games account as a player through the player MCP server at mcp.blazium.games/player. Checks the account and email, reads the wallet and library, recommends games with cited reasons, searches the catalog, writes reviews and bug reports, shows what friends are playing, explains player scopes and spending limits, and routes to purchases, installs, or launches. Use when the user wants an agent to act for them as a player on Blazium Games, find a game to play, review a game, report a bug, set up the player MCP server, or check what they own or can spend.
license: MIT
---

# Blazium Games: Player

The player server acts for one player. It sees the account, wallet, and library, and with `player:buy` it can top up and buy within the human's spending limit. It never touches game pages, builds, or keys; those need the developer server (`blazium-games`, see [get-started](../blazium-games-get-started/SKILL.md)).

## Invoke This Skill When

- "Connect my Blazium Games account as a player", "set up the Blazium Games player server"
- "What games do I own on Blazium Games?", "how much can this agent spend?"
- Before [purchases](../blazium-games-purchases/SKILL.md) when the player server isn't connected

## 1. Connect

1. Check whether a `blazium-games-player` server is connected. If not, ask the human to add it:

   ```json
   { "mcpServers": { "blazium-games-player": { "url": "https://mcp.blazium.games/player" } } }
   ```

2. On the consent page the human ticks **Allow purchases** only if you should buy for them. A player key (`bgames_play_...`) from https://blazium.games/settings/mcp works too.
3. A developer key (`bgames_mcp_...`) or developer OAuth token is refused here, and a player token is refused by the developer server. Never try to reuse one for the other.

## 2. Check the account

1. Call `get_account`. If `email_verified` is false, call `request_email_code`, ask the human for the code from their inbox, and call `verify_email`. Downloading and buying need a verified email. If `timezone` is empty and you know the human's IANA timezone, call `set_timezone`. Do not use the timezone of the machine you are running on. If `gate` is not empty, tell the human to finish that step at https://blazium.games/account/finish (accept changed terms, finish setup, or choose about an authenticator app). Never do those steps for them.
2. Call `get_agent_policy` to see this agent's limit: `unset` (every purchase needs approval), `unlimited`, `monthly`, `yearly`, or `one_time`. Only the human changes it, on the website.
3. Call `get_wallet` for the available balance.

## 3. Route

| The human wants to | Do |
|---|---|
| Buy, donate, or top up | [purchases](../blazium-games-purchases/SKILL.md) |
| See what they own | `get_library` |
| Set up payouts or cash out earnings | Only when the human asks. `start_payout_setup` (or `get_payout_dashboard_link` once set up) and give them the Stripe link; never enter their details yourself. `cash_out` with the amount they asked for, from the available earnings in `get_wallet`. Tell them it can take up to 72 business hours to reach the bank and that they will get an email |
| Something to play, and they haven't said what | `get_shelf` with `tonight`, `unheard_of` when they want something new, or `browser_playable` when they can't install anything, before a wide `recommend` |
| Something to play right now | `recommend` with what they told you (`minutes`, `party_size`, `intent` in their words, `like_uid`, `os`). Give each pick with its `reasons` and `cautions`; don't add reasons of your own. If the results are empty, relay the `hint` and ask for one more constraint |
| Why a game was or wasn't suggested | `why_this` with the same inputs; its `blockers` say what kept it out |
| Find something specific | `search_catalog` with their constraints (for example `session_bucket: 15m`, `players: 2`, `os: windows`, `genres: [puzzle, strategy]`, or `exclude_tone: [dark]` for what they want to avoid), then `get_game_details` on the best matches. Say why each one fits using `why_short` |
| "More like this" / "not for me" | `taste_feedback` with `more_like` true or false |
| Mods or tools for a game | `list_game_addons` with the game's `uid` (`kind: mods` or `tools`) |
| Tag a game they play | `suggest_tag` with the tag they chose. It needs an hour of play (`4237`); `remove` takes it back |
| Review a game they own | Ask whether they enjoyed it and, separately, its quality from 1 to 5, then `write_review` with their words. Never write a review they didn't give you |
| Report a bug | `report_bug` with what happened and how to reproduce it. If they have a crash dump or log, set `include_dump` / `include_log` and upload the file with `PUT` to the returned URL |
| "What are my friends playing?" | `games_friends_play`; live games come first, then the last 14 days |
| Add or answer a friend | `send_friend_request` with the username they gave you, or `list_friends` then `respond_friend_request`. Only send requests the human asked for |
| Redeem a key or gift link | `redeem_key` with the code or link they gave you. `4084` means they already own it and the key is still unused |
| Install a game they own or a free game | `why_should_i_trust_this` first. Pass its facts on, and do not call a file safe. Then `install_build` and give them the `blazium://install/<uid>` link. If it fails because the scan isn't clean, don't offer another way to download that file |
| Join or leave a beta | `set_channel` (`beta` or `stable`), then `install_build` |
| Play a game | `launch_game`, then give them the `blazium://game/<uid>` link. The desktop launcher is Windows and Linux and listens on port 39220. Hand over the link; do not fetch the installer unless they ask. `blazium://buy/<uid>` opens the store page and does not install. Game chat is IRC on `irc.blazium.online` port 6697 |
| Download a game they own or a free game | Step 5 (Download) of [purchases](../blazium-games-purchases/SKILL.md) |

## Errors

| Code | Meaning |
|------|---------|
| `4212` | The token has no `player:buy`. The human reconnects and ticks **Allow purchases**, or creates a key with purchases allowed |
| `4031` | The token is read-only |
| `4033` | That route isn't available to player tokens. Use the developer server for game management |
| `4032` | The token mixes developer and player scopes. Reconnect |
| `4076` | Reviews and bug reports need a copy of the game: buy it, or download it if it's free |
| `4077` | The human is a developer of this game and can't review it |
| `4291` | Too many bug reports today; try tomorrow |
| `4078` | Already friends, or the request was already sent |
| `4292` | Too many friend requests today; try tomorrow |
| `4042` / `4079` | The key isn't valid, or was already redeemed |

## References

- [Tools](./references/tools.md)
- https://docs.blazium.games/docs/mcp/player
