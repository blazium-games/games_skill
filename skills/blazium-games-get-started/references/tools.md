# Blazium Games MCP tools

All tools call the Blazium Games API on behalf of the connected user. `uid` accepts a game uid or its vanity name. Tools marked **account** need an account-level token (a project token gets `4030`); tools marked **write** need `mcp:write` or the narrower write scope for that tool's group. Tools marked **deprecated** are removed from this server on 2026-10-28; use the player server at `https://mcp.blazium.games/player` instead.

| Tool | Inputs | Access | What it does |
|------|--------|--------|--------------|
| `get_profile` | none | account | Authenticated user profile |
| `get_setup` | none | account | Account, games, public URLs, and key prefixes. No secrets |
| `list_games` | none | | Games the user owns or admins, plus pending admin invites |
| `get_game` | `uid` | | One game's settings and store page fields |
| `get_lobby` | `uid` | | Lobby settings and published packs: enabled, relay or scripted, TURN, the active checksum, and pack history |
| `set_lobby` | `uid` (required), `enabled`, `lobby_type` (`relay` or `scripted`), `ice_enabled` | write | Only the fields you pass change |
| `create_game` | `name` (required), `tagline`, `description`, `visibility`, `asset_type`, `vanity_name`, `adult`, `indexable`, `parent` | account, write | Create a store page. Tools, mods and plugins need a `parent` before they can go public. Needs developer mode on the account (`4105`) |
| `update_game` | `uid` (required), `name`, `tagline`, `description`, `visibility`, `asset_type`, `adult`, `indexable`, `parent` | write | Update a store page; only passed fields change. An empty `parent` object clears it |
| `get_game_analytics` | `uid`, optional `build` | | Visitor analytics plus registered funnel events: count, unique devices, and a daily series |
| `get_achievements` | `uid` | | Achievement definitions and writers |
| `set_achievements` | `uid`, `achievements` | mcp:catalog.write | Replaces the achievement list |
| `get_stats` | `uid` | | Integer stats, op, and writers |
| `set_stats` | `uid`, `stats` | mcp:catalog.write | Replaces the stat list |
| `get_funnels` | `uid` | | Registered analytics events and writers |
| `set_funnels` | `uid`, `funnels` | mcp:catalog.write | Replaces the funnel list |
| `get_presence_writers` | `uid` | | Who may set the short presence status |
| `set_presence_writers` | `uid`, `writers` | mcp:catalog.write | Replaces that list |
| `list_server_keys` | `uid` | | Game server key prefixes and roles. No secrets |
| `request_server_key` | `uid`, `role` | | Returns a game_server or private_server secret once |
| `revoke_server_key` | `uid`, `key_id` | | Revokes one game server key |
| `get_web_player` | `uid` | | Browser player settings, including the Discord application id, public key, and share links |
| `set_web_player` | `uid` | `enabled`, `full_build_id`, `demo_build_id`, `width`, `height`, `fullscreen`, `mobile`, `click_to_play`, `hide_branding`, `start_fullscreen`, `embed_enabled`, `embed_domains`, `discord_enabled`, `application_id`, `public_key`, `share_build_id`, `share_enabled` | Choose the full build, an optional demo, the player size, branding, fullscreen launch, embed settings, and Discord activity hosting. `share_build_id` and `share_enabled` together turn one web build's unlisted link on or off. Hosting stays off unless `discord_enabled` is set, and it still requires the player to be on plus both values. Needs mcp:build.write |
| `list_game_crashes` | `uid` | | Recent crash reports |
| `get_crash` | `uid`, `crash_id` | | One crash with metadata, analysis, and stack availability |
| `request_crash_download` | `uid`, `crash_id`, `kind` (`dump`, `log`, or `stack`; default `dump`) | | Private download URL valid for 1 hour |
| `get_deploy_info` | `uid` | | Upload, crash, and events URLs, recent builds, env var names, deploy key prefixes. No secrets |
| `list_game_builds` | `uid` | | Up to 50 builds. Each `build_id` is the `X-Build-Id` for crash reporters |
| `delete_game_build` | `uid`, `build_id` | write | Deletes one build after the owner approves |
| `add_game_admin` | `uid`, `invite` | write | Invites an admin. Owner only, and the owner approves |
| `remove_game_admin` | `uid`, `admin_id` | write | Removes an admin. Owner only |
| `delete_game` | `uid` | write | Deletes a game the caller owns, after the owner approves |
| `get_account_analytics` | none | account | Analytics across the account's games |
| `get_game_build` | `uid`, `build_id` | | One build with its files and crash reporter headers |
| `list_mcp_keys` | none | account | MCP API key prefixes. Secrets are never returned |
| `request_mcp_key` | `idempotency_key` | account, write | Issue a new MCP API key and invalidate every previous one. Waits for the human's approval, then returns the secret once |
| `request_deploy_key` | `uid`, `idempotency_key` | write | Issue a new upload `access_token` and `secret_key` for a game and invalidate the previous ones. Waits for the human's approval, then returns secrets once |
| `list_channels` | `uid` | | Channel pointers (stable, beta, dev, custom), expiry, beta subscribers, and history |
| `promote_build` | `uid`, `channel`, `build_id`, `expires_in_hours`, `idempotency_key` | write | Point a channel at a clean build. `stable` waits for the human's approval |
| `rollback_channel` | `uid`, `channel` | write | Move a channel back to its previous build |
| `list_crash_groups` | `uid` | | Up to 100 crash groups by cause, most recently seen first, with counts per build and a sample crash id |
| `get_crash_reporter` / `set_crash_reporter` | `uid`, and for set: `enabled`, `webhooks`, `refresh_signing_key` | `mcp:crash.read` / `mcp:crash.write` | Per-game crash webhooks. The signing key is not the bug reporter key |
| `get_build_provenance` | `uid`, `file_uid` | | Uploader, deploy key reference, upload time, checksum, and scan history of a file |
| `list_reviews` | `uid`, `unreplied`, `page` | | Player reviews with the summary (enjoyed, quality average and counts, would play with friends) |
| `reply_to_review` | `uid`, `review_uid`, `text` | write | Public reply to a review; empty text removes it |
| `list_bug_tickets` | `uid`, `status` | | Player bug tickets with counts by status; attachments carry a `crash_id` |
| `update_bug_ticket` | `uid`, `bug_uid`, `status` (`open`, `fixed`, `closed`) | `mcp:bugs.write` | Mark a ticket fixed or closed, or reopen it |
| `get_bug_reporter` / `set_bug_reporter` | `uid`, and for set: `enabled`, `daily_cap`, `webhooks`, `refresh_signing_key` | `mcp:bugs.read` / `mcp:bugs.write` | Per-game in-game reporter. The signing key is unique to the game |
| `get_review_reporter` | `uid` | `mcp:read` | New-review webhooks: enabled, webhook URLs, and that game's signing key. The key is not the sale, crash, or bug reporter key |
| `set_review_reporter` | `uid`, optional `enabled`, `webhooks`, `refresh_signing_key` | `mcp:catalog.write` | Turns new-review webhooks on, replaces up to five https URLs, or refreshes the signing key. An edit or a delete does not send |
| `get_sale_reporter` | `uid` | `mcp:money` | Sale and refund webhooks: enabled, webhook URLs, and that game's signing key. The key is not the review, crash, or bug reporter key |
| `set_sale_reporter` | `uid`, optional `enabled`, `webhooks`, `refresh_signing_key` | `mcp:money` | Turns sale and refund webhooks on, replaces up to five https URLs, or refreshes the signing key |
| `get_steam_auth` / `set_steam_auth` | `uid`, and for set: `app_id`, `web_api_key`, `ticket_secret`, `enabled`, `confirm` | `mcp:steam.manage` | Write-only Web API key and ticket secret. Disable deletes both only when `confirm` is true |
| `unlink_steam` | `uid`, `confirm` | `mcp:steam.manage` | Unlinks Steam. `confirm` only after the human agrees |
| `rotate_steam_key` | `uid`, `confirm` | `mcp:steam.manage` | Replaces the Web API key. The new key is returned once |
| `resync_steam` | `uid`, `confirm`, optional `groups`, `web_api_key` | `mcp:steam.manage` | Imports the chosen groups again |
| `import_steam_game` | `app_id`, `web_api_key`, `confirm`, optional `groups`, `uid` | developer | Imports a Steam page. `confirm` only after the human agrees |
| `set_anonymous_downloads` | `uid`, `enabled`, `confirm_no_license` | write | Anonymous downloads. Turning them on needs the human's confirm, and a free game |
| `set_adult_content` | `show`, `confirm_18` | account, write | Adult listings. Turning them on needs the human to confirm they are 18 or older |
| `list_copyright_notices` | none | | Paid copyright (DMCA) notices about the account's content, with status and how many of its links each names |
| `get_copyright_notice` | `uid` | | One notice: claimant, work, statements, the account's named links, staff messages, decision, and `reply_to`. Read only; the human replies by email with the reference in the subject |
| `get_game_chat` | `uid` | | The game's IRC channel (`irc_channel`), whether guests may join (`chat_guests`), and who is banned or muted with when each mute ends |
| `set_chat_guests` | `uid`, `guests` | write | Let people without a license join the channel; they can read but can't talk until they own the game |
| `ban_chat_user` | `uid`, `username` | write | Ban a user from the channel until unbanned; they are removed right away. The owner, admins, and `blazium` can't be banned. Only when the human asked |
| `unban_chat_user` | `uid`, `username` | write | Lift a chat ban |
| `suspend_chat_user` | `uid`, `username`, `minutes` (1-43200) | write | Mute a user for up to 30 days; they can still read. Only when the human asked |
| `unsuspend_chat_user` | `uid`, `username` | write | Lift a chat mute |
| `declare_dependency` | `uid`, `target_uid`, `kind`, `remove` | write | Link to another public listing: `uses`, `supports`, or `made_with` |
| `list_dependents` | `uid` | | What a listing uses and which listings use it, plus license kind and compatibility |
| `declare_engine_compat` | `uid`, `compat` | write | Replace the engine version ranges (engine, min/max version, renderer, platform) |
| `declare_license` | `uid`, `license_kind` | write | `cc0`, `cc-by`, `cc-by-sa`, `paid`, `source-available`, or `proprietary` |
| `create_key_pool` | `uid`, `name`, `campaign` | write | A named pool for redeemable game keys |
| `grant_keys` | `uid`, `pool`, `n`, `campaign`, `idempotency_key` | write | Create 1-5000 keys; returns a one-time `csv_url` (1 hour). Over 100 needs the owner's approval |
| `create_gift_link` | `uid`, `pool`, `note` | write | A single-use redeem link for one person, shown once |
| `list_key_pools` | `uid` | | Pools with size, redeemed, unredeemed, and gift link counts |
| `validate_listing` | `uid` | | Listing check (errors block going public), current taxonomy, and allowed values |
| `update_game_taxonomy` | `uid`, `genres`, `tags`, `tone`, `inputs`, `content_warnings`, `engines`, `session_bucket`, `net`, `players_min`, `players_max`, `authorship`, `authorship_credit`, `ai_uses` | write | Set the taxonomy, the made-with label (`human`, `human_agent`, `agent_heavy`, empty clears; credit up to 120 characters), and the generative AI disclosure (`art`, `audio`, `code`, `text`, `voice`, `runtime`; empty list means none); only passed fields change |
| `set_similar_games` | `uid`, `games` | write | Replace the similar titles (up to 10) |
| `set_media` | `uid`, `kind` (`cover`, `thumbnail`, `gallery`) | write | Returns the `chauffeur media` commands and image limits (PNG, JPEG, GIF, WebP, sniffed from the file). Wide images need width/height between 1.70 and 1.85. Thumbnail 1280x720 recommended, 960x540 to 1920x1080, 5 MB. Cover 1024x576 recommended, 1024x576 to 2048x1152, 8 MB. Screenshot 1920x1080 recommended, 1280x720 to 2048x1152, 10 MB. Avatar 256x256 to 512x512, square (0.95 to 1.05), 2 MB, on the account settings page. MCP never uploads images |
| `scan_status` | `uid` | | Virus-scan state and history per build file, and files removed for failing the scan |

## Tools, mods and press

A tool, mod or plugin names the game it is for with `parent` on `create_game` or `update_game`: `{"game": "uid-or-vanity"}` for a listing on Blazium Games, or `{"external_name": "...", "external_url": "https://..."}` for one that isn't. The parent's store page lists it under **Tools and utilities** or **Mods and plugins**.

| Tool | Inputs | Access | What it does |
|------|--------|--------|--------------|
| `set_mod_settings` | `uid`, `install_path`, `loader`, `instructions` | write | Mods and plugins only (`4234` otherwise). Relative install path, lowercase loader slug (for example `bepinex`), markdown instructions up to 8000 characters. Replaces all three |
| `get_press_kit` | `uid` | | The press kit behind the listing's `/press` page and `press.zip` |
| `set_press_kit` | `uid`, `release_date`, `website_url`, `press_email`, `trailer_url`, `history`, `features`, `awards`, `links`, `quotes`, `credits` | write | Replace the whole press kit; omitted fields are cleared, so read it with `get_press_kit` first. https links only; up to 20 features, awards, links and quotes, and 50 credits |
| `hide_community_tag` | `uid`, `tag`, `show` | write | Hide a player-suggested tag from the store page, or show it again with `show`. Without `tag`, lists every suggestion with its vote count |
| `get_store_links` | `uid` | | The listing's links to its pages on other stores (shown as "Also on"), and every supported store with its allowed hosts |
| `set_store_links` | `uid`, `store_links` (`platform`, `url`) | write | Replace every store link; omitted stores are removed, so read them with `get_store_links` first. One per store (`steam`, `gog`, `epic`, `itch`, `humble`, `microsoft`, `playstation`, `nintendo`, `apple`, `google_play`, `gamejolt`), each an https link on that store's own site |

## Builds, health and editions

MCP never uploads files: builds, symbols and store images go through the chauffeur CLI with the game's deploy key.

| Tool | Inputs | Access | What it does |
|------|--------|--------|--------------|
| `get_build_health` | `uid` | | Per-build devices, boot-ok and crash-on-boot counts, median session and band over 30 days (`excellent`, `healthy`, `mixed`, `problematic`, or `unrated` until enough devices report) |
| `list_build_symbols` | `uid`, `build_id` | | Breakpad symbol files for a build, plus the `chauffeur symbols` command |
| `delete_build_symbols` | `uid`, `build_id`, `symbol_uid` | write | Delete one symbol file, or all of them when `symbol_uid` is empty |
| `upload_symbols_info` | `uid`, `build_id` | | The exact `chauffeur symbols` command and limits for a build. Uploads nothing |
| `bundle_check` | `uid`, `build_id` | | Informational: store asset packs found inside the build and whether each is `owned`, `licensed`, `attribution`, or `unlicensed` |
| `mod_compat` | `uid` (a mod), `game` | | The mod's engine compatibility against each supported game's current builds: `compatible`, `incompatible`, or `unknown` |
| `list_skus` | `uid` | | Editions with slug, kind, price, active flag, order, and bundle listings |
| `upsert_sku` | `uid`, `sku_uid`, `slug`, `name`, `description`, `kind`, `price_cents`, `bundle_asset_uids`, `active`, `sort_order` | write | Create an edition, or replace one when `sku_uid` is set. Kinds: `standard`, `deluxe`, `beta_access`, `bundle`. Up to 8; the listed price follows the cheapest active one |
| `delete_sku` | `uid`, `sku_uid` | write | Retire an edition; owners keep it |

## Account and payments

Amounts are integer US cents. Agents pay only from the stored balance, and only after the human approves the quoted total. Workflow: [blazium-games-purchases](../../blazium-games-purchases/SKILL.md).

| Tool | Inputs | Access | What it does |
|------|--------|--------|--------------|
| `get_account` | none | account | Email verification, timezone, balances, what the account may do (publish, upload, download, buy), and open website sign-in steps (`gate`, `legal_acceptance_required`, `legal_changes`, `setup_required`, `authenticator`) |
| `create_account` | `email`, `password`, optional `username`, `accept_legal`, `accept_developer_terms` | none | Creates an account. No bearer. On this server, `accept_legal` and `accept_developer_terms` (only after the human agrees) turn developer mode on |
| `confirm_account` | `email`, `code` | none | Finishes signup with the email code and returns the first `bgames_mcp_` key once. No bearer |
| `enable_developer_mode` | `accept_terms` | account, write | Turns developer mode on after the human agrees. Turning it off stays on the website |
| `request_email_code` | none | account, write | Email a verification code to the human |
| `verify_email` | `code` | account, write | Verify the email with the code the human read from their inbox |
| `set_timezone` | `timezone` | account, write | Replace the saved timezone with the human's IANA name, when it is empty or the human asks. Do not send the timezone of the machine running the agent. Unknown names: `4085` |
| `get_security_status` | none | account, read | Authenticator `state` (`on`, `skipped`, `not_chosen`), `enabled_at`, `skipped_at`, `recovery_codes_left`, and `email_code_alternative`. Changes happen only on the website |
| `get_wallet` | none | account | Credit, pending, and available balances with fee, refund, and cash-out rules, payout status, and recent cash-outs. **Deprecated** |
| `list_wallet_transactions` | `limit` (1-200, default 50), `before` | account | Ledger entries, newest first. **Deprecated** |
| `get_payment_options` | none | account | Card top-up link option and x402 USDC networks with fees. **Deprecated** |
| `create_top_up_link` | `amount_cents` (500-50000) | account, write | Card Checkout link for the human; agents cannot pay by card. **Deprecated** |
| `create_x402_top_up` | `amount_cents`, `network` (default Base) | account, write | x402 payment requirements to sign with the agent's own wallet. **Deprecated** |
| `pay_with_x402` | `top_up_id`, `payment_payload` | account, write | Submit the signed payment; credit is added after on-chain settlement. **Deprecated** |
| `quote_purchase` | `uid`, `kind` (`purchase` or `donation`), `amount_cents` (donations), `sku` (edition; empty quotes the cheapest) | account, write | Price, tax, and `total_cents` to show the human. **Deprecated** |
| `purchase_game` | `uid`, `confirm_total_cents`, `idempotency_key`, `sku` (same as the quote) | account, write | Buy a license from the balance; beyond the agent's limit returns `approval_required`. **Deprecated** |
| `donate_to_game` | `uid`, `amount_cents`, `confirm_total_cents`, `idempotency_key` | account, write | Donate to a free game from the balance. **Deprecated** |
| `list_library` | none | account | Owned games with refund windows and playtime. **Deprecated** |
| `get_download_link` | `file_id` | account | 5-minute signed URL for a build file; needs a verified email and, for paid games, a license. **Deprecated** |
| `set_game_price` | `uid`, `price_cents` (0 or 99-50000), `donations_enabled` | write | Set price or donations. Owners and game admins only |
| `list_game_sales` | `uid` | | Sales, donations, refunds, and seller earnings for a game you manage |
| `get_agent_policy` | none | account | This agent's limit mode, limit, and spend in the period; only the human changes them, on the website. **Deprecated** |
| `get_approval` | `approval_id` | account | State of a purchase approval |
| `confirm_approval` | `approval_id`, `code` | account, write | Approve with the 6-digit code the human read from their email |
| `start_payout_setup` | none | account, money | Stripe payout setup link for the human |
| `get_payout_dashboard_link` | none | account, money | One-time Stripe Express dashboard link (`4095` before setup) |
| `cash_out` | `amount_cents` (at least 2500) | account, money | Cashes out available earnings to the account's own payout account, no approval; the owner is emailed. Payouts are processed on weekdays from 8:00am to 5:00pm Pacific |
| `get_patron_status` | `developer` (optional) | read | The caller's patron memberships. No card data |
| `list_patrons` | `page` (optional) | read | Patrons of this developer |
| `get_patron` | `username` | read | One patron of this developer |
| `list_tiers` | none | read | Tiers and proposed game links |
| `create_tier` | `name`, `rank`, `price_cents`, `billing` | write | Rank, billing, and unlock stay fixed after create |
| `update_tier` | `uid`, optional `name`, `price_cents`, `active` | write | Hide a tier with `active` false |
| `delete_tier` | `uid` | write | Refused while a membership is pending or active |
| `list_posts` | `page` (optional) | read | Drafts and published posts |
| `create_post` | `title`, `status`, `visibility`, `tier_uids` | write | `visibility` is `public` or `tiers` |
| `update_post` | `uid` plus the create fields | write | Edit a post |
| `delete_post` | `uid` | write | Remove a post |
| `create_account` | `email`, `password` | none | No bearer. Follow the `setup_account` prompt |
| `login` | `email`, `password` | none | No bearer. Follow the `sign_in` prompt |
| `confirm_account` | `email`, `code` | none | Returns the first `bgames_mcp_` key once |

Payout tools are not deprecated and need `mcp:write` or `mcp:money`.

## Field values

- `visibility`: `draft` (owner and admins), `owner` (owner only), `invisible` (link only), or `public`
- `asset_type`: `game`, `application`, `tool`, `mod`, `plugin`, `game_asset`, `dev_asset`, or `rom`
- `adult`: marks 18+ content (sexual content or nudity); hidden from search, recommendations and search engines
- `indexable`: `false` keeps the store page out of search engines and AI crawlers
- `build_id`: the build UID (for example `004e044e-...`), not a version string

## Errors

Tool errors come back as `API <status>: <body>`. Common bodies:

| Code | Meaning |
|------|---------|
| `4010` | Not authenticated |
| `4030` | Not allowed: the game isn't yours, or a project token called an account-level tool or another game. Reconnect with **Account** |
| `4031` | Token is read-only |
| `4034` | Buying moved to the player server, or only the project owner can manage admins |
| `4040` | Not found (the message says what) |
| `4090` | Already done: the game is already owned, or the crash has no such file to download |
| `4091` | You can't buy your own game |
| `4092` | The game is free |
| `4093` | The game doesn't accept donations |
| `4006` | Build not found |
| `4096` | Email not verified; use `request_email_code` and `verify_email` |
| `4085` | Not an IANA timezone name |
| `4020` | Not enough balance; top up first |
| `4221` | No billing address for tax; top up by card once or buy on the website |
| `4023` | Buy the game before downloading it |
| `4094` | Total changed since the quote; confirm again with the human |
| `4099` | File still being scanned |
| `4212` | This token can't make purchases |
| `4214` | Waiting for the human's approval (a normal result, not an error) |
| `4215` | The human denied the request |
| `4216` | Wrong or expired approval code |
| `4083` | Website only (account settings, approval links, key management) |
| `4071` | Taxonomy value not allowed |
| `4072` | Similar title isn't a public game, or is this game |
| `4225` | Listing check failed, so the page can't go public. Run `validate_listing` |
| `4073` | The token's scopes don't cover this tool; reconnect with a wider preset |
| `4074` | File isn't on a channel this account can see |
| `4075` | Nothing to roll back to |
| `4226` | Invalid channel name or expiry |
| `4155` | Invalid edition |
| `4156` | The game already has 8 editions |
| `4164` | The price comes from the editions; change them with `upsert_sku` |
| `4105` | Developer mode is off; the human turns it on at blazium.games/settings |
| `4233` | Invalid parent |
| `4234` | Invalid mod settings |
| `4235` | Invalid press kit |
| `4238` | Invalid store link: wrong site, not https, or a store listed twice |

## Anticheat

These tools need `mcp:anticheat`. `mcp:read`, `mcp:write`, and **Full access** do not include them. They are not on the player server. Reports, keys, and settings stay closed until staff record a signed NDA and a signed contract for that game. `request_anticheat` is the exception: the owner uses it to start that request. Do not describe how a check decides. Profiles are `generic`, `platformer`, and `fps`. Public description: [Anticheat](https://docs.blazium.games/docs/anticheat).

| Tool | Inputs | Access | What it does |
|------|--------|--------|--------------|
| `request_anticheat` | `uid`, contact email, `confirm` | `mcp:anticheat` | Owner only. `confirm` must be true. Staff write to that email |
| `get_anticheat` | `uid` | `mcp:anticheat` | Request status, then the profile and its settings after access is granted |
| `update_anticheat` | `uid`, `profile`, settings for that profile | `mcp:anticheat` | Rejects a setting from the other profile. Shutting admins out is owner-only |
| `list_anticheat_keys` | `uid` | `mcp:anticheat` | Names and prefixes. Never the secret |
| `create_anticheat_key` | `uid`, name, `confirm` | `mcp:anticheat` | `confirm` must be true. Secret once, for the dedicated server only |
| `rotate_anticheat_key` | `uid`, key id, `confirm` | `mcp:anticheat` | `confirm` must be true. New secret once |
| `revoke_anticheat_key` | `uid`, key id, `confirm` | `mcp:anticheat` | `confirm` must be true |
| `list_anticheat_events` | `uid`, optional origin | `mcp:anticheat` | Reports. Origin is the client or a server key's name |
| `list_anticheat_bans` | `uid` | `mcp:anticheat` | Bans for that game |
| `ban_anticheat_player` | `uid`, player | `mcp:anticheat` | Ban a player on that game |
| `unban_anticheat_player` | `uid`, player | `mcp:anticheat` | Lift that ban |
| `list_anticheat_mutes` | `uid` | `mcp:anticheat` | Mutes for that game |
| `mute_anticheat_player` | `uid`, player | `mcp:anticheat` | Mute a player on that game |
| `unmute_anticheat_player` | `uid`, player | `mcp:anticheat` | Lift that mute |
| `list_anticheat_notes` | `uid` | `mcp:anticheat` | Notes the game's developers kept |
| `add_anticheat_note` | `uid`, note | `mcp:anticheat` | Add a note |
| `enqueue_anticheat_action` | `uid`, action, player id, `confirm` | `mcp:anticheat` | `confirm` must be true. Warn, mute, kick, ban, or a screenshot |
| `list_anticheat_audit` | `uid` | `mcp:anticheat` | Who changed settings, keys, or actions |
