# Player server tools

Server: `https://mcp.blazium.games/player`. Scopes: `player:read`, `player:write`, `player:buy`.

## Tools

| Tool | Scope | Purpose |
|------|-------|---------|
| `get_account` | read | Email verification, timezone, balances, what the account may do, and open website sign-in steps (`gate`, `legal_acceptance_required`, `setup_required`, `authenticator`) |
| `create_account` | none | Creates an account. No bearer. Send `accept_legal` only after the person agrees. The account stays a player |
| `confirm_account` | none | Finishes signup with the email code and returns the first `bgames_play_` key once. No bearer |
| `request_email_code` | write | Email a verification code to the human |
| `verify_email` | write | Verify the email with the human's code |
| `set_timezone` | write | Replace the saved timezone with the human's IANA name, when `get_account` timezone is empty or the human asks. Do not use the agent's machine timezone. Unknown names: `4085` |
| `get_security_status` | read | Authenticator `state` (`on`, `skipped`, `not_chosen`), `recovery_codes_left`, and `email_code_alternative`. Enroll, replace, and turn-off stay on the website |
| `skip_authenticator` | write | Records that the human chose not to set up an authenticator. Call it only when the human asked. Later sign-in uses `confirm_account` with the email code |
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
| `get_download_link` | read | 5-minute signed URL for a Windows, Linux, or content-pack file. A web build is hosted and is not downloaded. |
| `get_agent_policy` | read | This agent's spending limit |
| `start_payout_setup` | buy | Start or continue Stripe payout setup; returns a link only the human opens to enter identity, tax, and bank details |
| `get_payout_dashboard_link` | buy | One-time Stripe Express dashboard link for the human (`4095` until setup has started) |
| `cash_out` | buy | Cash out available earnings (`amount_cents`, at least 2500) to the human's own payout account. Sale earnings can be cashed out once that sale's refund window ends, 7 days after the sale. Playtime does not release them sooner. No approval; the owner is emailed. Payouts are processed on weekdays from 8:00am to 5:00pm Pacific. `4021` not enough available, `4057` below the minimum |
| `get_patron_status` | read | The caller's patron memberships: tier, billing, status, period end, and whether the 12 hour check is open. No card data |
| `create_account` | none | Continue or Generate only when password is omitted. Does not turn on developer mode |
| `login` | none | The person types the password. Generate is not offered |
| `confirm_account` | none | Returns the first `bgames_play_` key once and elevates this connection |
| `elevate_session` | none | Signs this connection in with a saved `bgames_play_` key. No Authorization header |
| `search_catalog` | read | Search public games, tools, mods, and assets by text, genres, tags (including community tags), tone, session length, network mode, players, platform, engine and version, renderer, license, made-with label (`authorship`), and `ai_uses`. Several values in one filter match any of them; `exclude_types`, `exclude_genres`, `exclude_tone`, `exclude_tags`, `exclude_warnings`, and `exclude_ai_uses` leave listings out. Adult listings only appear if the human turned on adult content |
| `list_articles` | read | Newest published blog posts. Optional `limit` (1-50) and `query` (title or description). Does not post or delete comments |
| `get_article` | read | One published blog post by `slug`, including the markdown body |
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
| `remove_friend` | write | Removes a friend by username |
| `get_presence` | read | What you are playing, and whether that is shared |
| `set_presence_sharing` | write | `share` true shows friends what you are playing |
| `get_inventory` | read | Items you hold. Page with `cursor` |
| `list_listings` | read | Your marketplace listings |
| `create_listing` | write | Lists items for sale: `uid`, `price_cents`, and `item_ids` or `itemdef_id` with `count` |
| `cancel_listing` | write | Cancels a listing by `listing_id` |
| `send_friend_request` | write | Send a request by username (20 per day, verified email). Accepts theirs if they already asked |
| `respond_friend_request` | write | Accept or decline an incoming request |
| `redeem_key` | write | Redeem a game key or gift link the human gave you; a game they already own leaves the key unused |
| `get_chat_connection` | write | Sign in to game chat yourself: host, TLS port 6697, the browser websocket, and a SASL PLAIN token that works for 10 minutes. Then `GAMEJOIN <game uid>`, or `LFGSUB <game uid>` to read without talking. Commands and replies: https://docs.blazium.games/docs/chat/commands. Chat follows https://blazium.games/chat-rules |
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

## More tools

These tools are listed with the descriptions the live server publishes. Inputs are in each tool's schema, which your client reads when it connects.

### Account, sign-in and privacy

| Tool | What it does |
|------|--------------|
| `open_account_finish` | Returns the website page where the human finishes account setup, accepts changed terms, and sets up, replaces, or turns off an authenticator. An agent never does these steps for the human. When the human asks to skip the authenticator, call `skip_authenticator`. |
| `open_password_settings` | Returns the website page where the human changes the password. Never ask the human for the new password in the chat. |
| `start_email_change` | Email a confirmation code for a new address. The human enters that code on the website. This tool does not confirm the change. |
| `sign_out` | Sign this token's website session out. |
| `sign_out_everywhere` | Sign every session of this account out. Agent keys are not listed here; revoke those separately. |
| `list_connections` | Sign-in accounts linked to this user. Passwords and access tokens are not returned. |
| `start_connection` | Start linking GitHub, Discord, X, or Steam. Give the returned URL to the human. The human finishes it in the browser. |
| `unlink_connection` | Unlink a sign-in account. Keep a password or another link so the account can still sign in. |
| `set_profile_visibility` | Who can see this account's profile: public, private, or hidden. |
| `get_game_display_name` | The display name this account uses inside one game. |
| `set_game_display_name` | Set the display name this account uses inside one game. |
| `unfriend` | Remove a friend, or cancel an outgoing request, by username. |
| `list_mcp_activity` | List the tool calls this account's agents made over MCP, newest first: tool, outcome, error code, duration, `request_id`, client, and arguments with secrets removed. Results are not stored. Kept 30 days. Filters: `game`, `tool`, `status`, `request_id`, `since`, `until`, `limit`, `cursor`. |
| `export_account` | Download this account's portable copy: profile, purchases, licenses, wallet ledger, cash-outs, reviews, friendships, agent key prefixes, patron memberships, your MCP call log, and the API requests your agents made. Secrets are not included. |

### Standing choices

| Tool | What it does |
|------|--------------|
| `list_standing_choices` | Lists every standing allow or deny for this account, with its key, action, and game. Spend limit and developer mode stay on the website. |
| `set_standing_choice` | Stores an allow or a deny for one action on this agent. Always-ask actions (cash-out, payout address, key changes, add admin, delete game, project sign-in apps) cannot be stored as allow. Always no wins. See [Approvals](https://docs.blazium.games/docs/mcp/approvals). |
| `revoke_standing_choice` | Removes one standing choice by `uid`. |

### Wallet, purchases and patrons

| Tool | What it does |
|------|--------------|
| `buy_post` | Buy one patron post. Requires confirm_total_cents from the post price and a unique idempotency_key. Past the spending limit it returns approval_required. |
| `pledge` | Join a developer's patron tier from the wallet or by card. Past this agent's spending limit it returns approval_required. idempotency_key is required. |
| `cancel_membership` | Stop renewing a patron membership. Access lasts until the period already paid for ends. |
| `cancel_cash_out` | Cancel a cash-out that has not been sent and return it to the available balance. Waits for the account owner's approval. |
| `set_payout_currency` | Choose usd or usdc for payouts. A new USDC address always asks the account owner. Waits for the account owner's approval. |
| `request_refund` | Tells the human how to ask for a refund. It does not refund a purchase or send a request. A buyer asks from the Library on the website, or by email to support. |
| `list_spare_copies` | Spare copies this account can send or redeem. |
| `send_spare_copy` | Give a spare copy to another account. Waits for the account owner's approval. |
| `redeem_spare_copy` | Redeem a spare copy onto this account. |
| `get_my_inventory` | Items in this account's inventory. |
| `list_market` | Public item market for a game. |

### Reports and comments

| Tool | What it does |
|------|--------------|
| `report_cheater` | Send a cheater report for a game this account plays. The report is filed as the signed-in player. |
| `report_game` | Report a game page. owner is the page's account username or uid. |
| `report_player` | Report a player profile. The signed-in account is the reporter. |
| `list_my_bug_reports` | Bug reports this account filed. |
| `list_article_comments` | Comments on a blog article. |
| `write_article_comment` | Comment on a blog article. kind is suggestion, critique, question, or praise. |
| `delete_article_comment` | Delete one of this account's article comments. |

### Updates, changelogs and the asset library

| Tool | What it does |
|------|--------------|
| `check_update` | Builds this account should have for a game, on the channel they follow. Compare file_uid and checksum with what is installed. |
| `get_patch_notices` | Patch notices this account has not acknowledged for a game. |
| `ack_patch_notices` | Mark patch notices as seen. |
| `list_changelog` | Public changelog for a game. owner is the developer's username or uid. |
| `list_asset_library` | Search the public asset library the editor uses. |
| `get_asset_library_item` | One asset-library item, including its download when the caller may have it. |

### Admin invites and key revocation

| Tool | What it does |
|------|--------------|
| `accept_invite` | Accept a game admin invite. This asks the account owner first. Turning on developer mode still finishes on the website. |
| `decline_invite` | Decline a game admin invite, or withdraw one you sent. |

### Copyright notices

| Tool | What it does |
|------|--------------|
| `file_dmca_claim` | Files a copyright (DMCA) claim. The filing fee is not refundable. Asks the account owner first, and payment finishes on the checkout page the response returns. |
| `file_counter_notice` | Records a written statement on an open copyright notice that names this account, and emails it to the claimant. It does not restore content or start a waiting period. |
