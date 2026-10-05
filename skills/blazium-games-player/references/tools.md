# Player server tools

Server: `https://mcp.blazium.games/player`. Scopes: `player:read`, `player:write`, `player:buy`.

## Tools

| Tool | Scope | Purpose |
|------|-------|---------|
| `get_account` | read | Email verification, timezone, balances, what the account may do, and open website sign-in steps (`gate`, `legal_acceptance_required`, `setup_required`, `authenticator`) |
| `request_email_code` | write | Email a verification code to the human |
| `verify_email` | write | Verify the email with the human's code |
| `set_timezone` | write | Replace the saved timezone with the human's IANA name, when `get_account` timezone is empty or the human asks. Do not use the agent's machine timezone. Unknown names: `4085` |
| `get_security_status` | read | Authenticator `state` (`on`, `skipped`, `not_chosen`), `recovery_codes_left`, and `email_code_alternative`. Changes happen only on the website |
| `get_wallet` | read | Balances, fee and refund rules, payout status (`payouts`), recent `cash_outs`, and `rules.payout_arrival` |
| `list_wallet_transactions` | read | Ledger entries, newest first |
| `get_payment_options` | read | Card and x402 USDC top-up options with fees |
| `create_top_up_link` | buy | Card Checkout link for the human |
| `create_x402_top_up` | buy | x402 payment requirements for a USDC top-up |
| `pay_with_x402` | buy | Submit the signed x402 payment |
| `quote_purchase` | read | Price, tax, and total |
| `purchase_game` | buy | Buy a license from the balance |
| `donate_to_game` | buy | Donate to a free game from the balance |
| `get_approval` | read | State of an approval |
| `confirm_approval` | write | Approve with the human's emailed code |
| `get_library` | read | Owned games, refund windows, play time |
| `get_download_link` | read | 5-minute signed download URL |
| `get_agent_policy` | read | This agent's spending limit |
| `start_payout_setup` | buy | Start or continue Stripe payout setup; returns a link only the human opens to enter identity, tax, and bank details |
| `get_payout_dashboard_link` | buy | One-time Stripe Express dashboard link for the human (`4095` until setup has started) |
| `cash_out` | buy | Cash out available earnings (`amount_cents`, at least 2500) to the human's own payout account. No approval; the owner is emailed. Up to 72 business hours to reach the bank. `4021` not enough available, `4057` below the minimum |
| `search_catalog` | read | Search public games, tools, mods, and assets by text, genres, tags (including community tags), tone, session length, network mode, players, platform, engine and version, renderer, license, made-with label (`authorship`), and `ai_uses`. Several values in one filter match any of them; `exclude_types`, `exclude_genres`, `exclude_tone`, `exclude_tags`, `exclude_warnings`, and `exclude_ai_uses` leave listings out. Adult listings only appear if the human turned on adult content |
| `list_game_addons` | read | Mods and plugins, or tools and applications, made for a game (`kind`: `mods`, `tools`, or empty for both); `same_creator` marks the developer's own |
| `suggest_tag` | write | Suggest a tag for a game the human owns and played for an hour (`4237` before that), or `remove` it; up to 5 per game. Without `tag`, returns their suggestions. Only suggest tags the human chose |
| `get_shelf` | read | A home page shelf for the human's `os` (`limit` 1-24): `tonight` (short sessions with a healthy build), `unheard_of` (recent listings few people have found), `featured`, `new`, `recently_updated`, `made_with_blazium`, `in_development`, `browser_playable`, `community`, or `tools_and_assets`. `has_browser_build` and `has_downloads` say how each one plays |
| `get_game_details` | read | One listing: taxonomy, price, files with scan state and checksum, similar titles, links to its pages on other stores (`store_links`), ownership |
| `install_build` | read | License and scan check, checksum, 5-minute download URL, and a `blazium://install/<uid>` hand-off. Uses the channel the human follows unless `channel` is given. Fails unless the file is clean |
| `launch_game` | read | `blazium://game/<uid>` hand-off. The launcher remote is port 39220. `blazium://buy/<uid>` does not install. Chat is IRC on `irc.blazium.online:6697` |
| `set_channel` | write | Join (`beta`) or leave (`stable`) a game's beta |
| `why_should_i_trust_this` | read | Developer, upload provenance, scan history, checksums, and cautions for the current files. Never claims a file is safe |
| `recommend` | read | Listings of one `asset_type` (default `game`) for right now from `minutes`, `party_size`, `intent`, `like_uid`, and platform. Deterministic; every result has `reasons` citing listing fields. Pass the reasons on instead of inventing your own |
| `why_this` | read | One game against the same inputs: score, reasons, cautions, and the `blockers` that keep it out of `recommend` |
| `write_review` | write | Create, update, or `delete` the human's review of a game they own: `enjoyed` and `quality` (1-5) are separate, plus `would_play_with_friends` and `text`. Only write what the human said |
| `taste_feedback` | write | `more_like` true or false for a game, or `clear` |
| `report_bug` | write | File a bug ticket with the developers (10 per day); `include_dump` / `include_log` return one-time upload URLs |
| `games_friends_play` | read | What friends are playing now, then what they played in the last 14 days; `live_only` skips the recent list |
| `list_friends` | read | Friends with presence, plus incoming and sent requests with their `request_uid` |
| `send_friend_request` | write | Send a request by username (20 per day, verified email). Accepts theirs if they already asked |
| `respond_friend_request` | write | Accept or decline an incoming request |
| `redeem_key` | write | Redeem a game key or gift link the human gave you; a game they already own leaves the key unused |
| `get_chat_connection` | write | Sign in to game chat yourself: host, TLS port 6697, the browser websocket, and a SASL PLAIN token that works for 10 minutes. Then `GAMEJOIN <game uid>`. Chat follows https://blazium.games/chat-rules |
| `get_chat_token_status` | read | Whether the human has a chat token for IRC clients (prefix and times, never the token), whether the account is locked out of chat, and the client settings |
| `request_chat_token` | write | Only when the human asks, with `confirm: true`: creates or replaces their IRC client chat token. It comes back once; hand it straight to the human. Replacing it disconnects clients using the old one. Up to 10 changes an hour (`4290`) |
| `revoke_chat_token` | write | Only when the human asks, with `confirm: true`: revokes the chat token and disconnects clients using it |

## Resources

| URI | Contents |
|-----|----------|
| `blazium-games://me` | Account status |
| `blazium-games://wallet` | Stored balance and payment rules |
| `blazium-games://library` | Owned games and licenses |
| `ui://blazium-games/checkout.html` | Quote, buy, and donate. The purchase runs when the human clicks |
| `ui://blazium-games/game.html` | Game information and trust checks |
| `ui://blazium-games/results.html` | Search, recommendations, shelves, add-ons, and what friends are playing |
| `ui://blazium-games/wallet.html` | Balance, ledger, spending limit, and a card top-up link |
| `ui://blazium-games/approval.html` | Approval status, confirm link, and the emailed code |
| `ui://blazium-games/library.html` | Owned games, redeem, and download links |
| `ui://blazium-games/handoff.html` | `blazium://` hand-off for BlaziumLauncher |
| `ui://blazium-games/account.html` | Verification, timezone, and links to finish sign-in on the website |
| `ui://blazium-games/feedback.html` | Reviews, bug reports, taste, and tag suggestions. Send only what the human wrote |
| `ui://blazium-games/friends.html` | Friends and requests. Send and answer only from a click |
