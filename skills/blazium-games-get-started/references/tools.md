# Blazium Games MCP tools

All tools call the Blazium Games API on behalf of the connected user. `uid` accepts a game uid or its vanity name. Tools marked **account** need an account-level token (a project token gets `4030`); tools marked **write** need `mcp:write` or the narrower write scope for that tool's group. Buying, wallet, and library are only on the player server at `https://mcp.blazium.games/player`. A developer token that purchases or tops up gets `4034`.

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
| `list_items` | `uid`, optional `cursor` | mcp:read | One page of item definitions. `next` is the following page |
| `create_item` | `uid`, `itemdef_id`, `name` | mcp:catalog.write | Creates a definition. `unique` is only set here |
| `update_item` | `uid`, `itemdef_id`, `name` | mcp:catalog.write | Edits a definition. `unique` cannot change |
| `give_items` | `uid`, `itemdef_id`, `quantity`, `request_id`, `recipients` | mcp:catalog.write | Gives copies by handle or email. At most 100 items |
| `list_item_sets` | `uid`, optional `cursor` | | One page of named sets. Bonuses are stored, not applied |
| `upsert_item_set` | `uid`, `name` | mcp:catalog.write | Creates or replaces a named set |
| `sync_item_schema` | `uid`, `mode` | mcp:steam.manage | sync, overwrite, or addon. Does not move player items |
| `set_inventory_flags` | `uid`, `confirm` | mcp:steam.manage | Turns inventory or transfers on. Neither can be turned off |
| `list_mint_keys` | `uid`, optional `cursor` | mcp:keys.manage | One page of mint key names and prefixes |
| `request_mint_key` | `uid`, `name` | mcp:keys.manage | Returns the 128-character secret once. It can mint, set stats, socket, unsocket, and use |
| `rename_mint_key` | `uid`, `key_id`, `name` | mcp:keys.manage | Renames a live mint key |
| `revoke_mint_key` | `uid`, `key_id` | mcp:keys.manage | Revokes a mint key |
| `request_server_key` | `uid`, `role` | | Returns a game_server or private_server secret once |
| `revoke_server_key` | `uid`, `key_id` | | Revokes one game server key |
| `get_web_player` | `uid` | | Browser player settings, including the Discord application id, public key, and share links |
| `set_web_player` | `uid` | `enabled`, `full_build_id`, `demo_build_id`, `width`, `height`, `fullscreen`, `mobile`, `click_to_play`, `hide_branding`, `start_fullscreen`, `embed_enabled`, `embed_domains`, `discord_enabled`, `application_id`, `public_key`, `share_build_id`, `share_enabled` | Choose the full build, an optional demo, the player size, branding, fullscreen launch, embed settings, and Discord activity hosting. `share_build_id` and `share_enabled` together turn one web build's unlisted link on or off. Hosting stays off unless `discord_enabled` is set, and it still requires the player to be on plus both values. Needs mcp:build.write |
| `set_host_fetch` | `uid`, `build_id`, `enabled` | `rotate` | Turns on, turns off, or rotates the file URL a host uses to download one web build. TikTok, Douyin, WeChat, YouTube, Reddit, Newgrounds, CrazyGames, Poki, Meta, and GameDistribution can have one. Discord, Telegram, Steam, GOG, Epic, and itch do not. The player server does not return this URL |
| `list_game_crashes` | `uid` | | Recent crash reports |
| `get_crash` | `uid`, `crash_id` | | One crash with metadata, analysis, and stack availability |
| `request_crash_download` | `uid`, `crash_id`, `kind` (`dump`, `log`, or `stack`; default `dump`) | | Private download URL valid for 1 hour |
| `get_deploy_info` | `uid` | | Upload, crash, and events URLs, recent builds, and env var names. get_deploy_info lists the short code only. It does not include the access token or the secret |
| `list_game_builds` | `uid` | | Up to 50 builds. Each `build_id` is the `X-Build-Id` for crash reporters |
| `delete_game_build` | `uid`, `build_id` | write | Deletes one build after the owner approves |
| `add_game_admin` | `uid`, `invite` | write | Invites an admin. Owner only, and the owner approves |
| `remove_game_admin` | `uid`, `admin_id` | write | Removes an admin. Owner only |
| `delete_game` | `uid` | write | Deletes a game the caller owns, after the owner approves |
| `get_account_analytics` | none | account | Analytics across the account's games |
| `get_game_build` | `uid`, `build_id` | | One build with its files and crash reporter headers |
| `list_mcp_keys` | none | account | MCP API key prefixes. Secrets are never returned |
| `request_mcp_key` | `idempotency_key` | account, write | Issue a new MCP API key and invalidate every previous one. Waits for the human's approval, then returns the secret once |
| `request_deploy_key` | `uid`, `idempotency_key` | write | Creating a new deploy key replaces the previous one. Uploads that used the old key stop working. Returns both values once, after the project owner approves. The access token can be copied later from the Deploy keys tab. The secret cannot |
| `list_channels` | `uid` | | Channel pointers (stable, beta, dev, custom), expiry, beta subscribers, and history |
| `promote_build` | `uid`, `channel`, `build_id`, `expires_in_hours`, `idempotency_key` | write | Point a channel at a clean build. `stable` waits for the human's approval |
| `rollback_channel` | `uid`, `channel` | write | Move a channel back to its previous build |
| `list_crash_groups` | `uid` | | Up to 100 crash groups by cause, most recently seen first, with counts per build and a sample crash id |
| `get_crash_reporter` / `set_crash_reporter` | `uid`, and for set: `enabled`, `webhooks`, `refresh_signing_key` | `mcp:crash.read` / `mcp:crash.write` | Per-game crash webhooks. The signing key is not the bug reporter key |
| `get_build_provenance` | `uid`, `file_uid` | | Uploader, deploy key reference, upload time, checksum, and scan history of a file |
| `list_reviews` | `uid`, `unreplied`, `page` | | Player reviews with the summary (enjoyed, quality average and counts, would play with friends) |
| `reply_to_review` | `uid`, `review_uid`, `text` | write | Public reply to a review; empty text removes it |
| `list_bug_tickets` | `uid`, `status`, `page` | | 50 tickets a page. Follow `next_page`. `has_screenshot` and `has_log` mark files |
| `get_bug_ticket` | `uid`, `bug_uid` | | One ticket |
| `request_bug_screenshot` | `uid`, `bug_uid` | | One-hour link, not the image |
| `get_bug_log` | `uid`, `bug_uid`, `offset` | | One log page. Follow `next_offset` |
| `update_bug_ticket` | `uid`, `bug_uid`, `status` (`open`, `fixed`, `unidentified`, `closed`) | `mcp:bugs.write` | Set status. Closed stays silent in the game |
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
| `set_anonymous_downloads` | `uid`, `enabled`, `confirm_no_license` | `mcp:write` | Anonymous downloads, the full web build, and the web demo for signed-out visitors. Turning them on needs the human's confirm, and a free game |
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
| `game_setup_walkthrough` | `uid` | | Read-only setup steps, failing listing checks, field limits, and `next_tool`. It does not change the game and does not return secrets |
| `update_game_taxonomy` | `uid`, `genres`, `tags`, `tone`, `inputs`, `content_warnings`, `engines`, `session_bucket`, `net`, `players_min`, `players_max`, `authorship`, `authorship_credit`, `ai_uses` | write | Set the taxonomy, the made-with label (`human`, `human_agent`, `agent_heavy`, empty clears; credit up to 120 characters), and the generative AI disclosure (`art`, `audio`, `code`, `text`, `voice`, `runtime`; empty list means none); only passed fields change |
| `set_similar_games` | `uid`, `games` | write | Replace the similar titles (up to 10) |
| `set_media` | `uid`, `kind` (`cover`, `thumbnail`, `gallery`) | write | Returns the `chauffeur media` commands and image limits (PNG, JPEG, GIF, WebP, sniffed from the file). Wide images need width/height between 1.70 and 1.85. Thumbnail 1280x720 recommended, 960x540 to 1920x1080, 5 MB. Cover 1024x576 recommended, 1024x576 to 2048x1152, 8 MB. Screenshot 1920x1080 recommended, 1280x720 to 2048x1152, 10 MB. Avatar 256x256 to 512x512, square (0.95 to 1.05), 2 MB, on the account settings page. MCP never uploads images |
| `scan_status` | `uid` | | Virus-scan state and history per build file, and files removed for failing the scan |
| `list_oauth_apps` | `uid` | mcp:read | Sign-in applications and whether another one can be created. Never returns a secret |
| `create_oauth_app` | `uid`, `name`, `redirects`, `email` | mcp:write | Creates a sign-in application. The secret is shown once |
| `update_oauth_app` | `uid`, `app_id` | mcp:write | Changes the name, redirect URLs, or email flag |
| `rotate_oauth_app_secret` | `uid`, `app_id` | mcp:write | Replaces the secret. The new one is shown once |
| `delete_oauth_app` | `uid`, `app_id` | mcp:write | Deletes the application |

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
| `get_security_status` | none | account, read | Authenticator `state` (`on`, `skipped`, `not_chosen`), `enabled_at`, `skipped_at`, `recovery_codes_left`, and `email_code_alternative`. Enroll, replace, and turn-off stay on the website |
| `skip_authenticator` | none | account | Records that the human chose not to set up an authenticator. Call it only when the human asked. Later sign-in uses `confirm_account` with the email code |
| `set_game_price` | `uid`, `price_cents` (0 or 99-50000), `donations_enabled` | write | Set price or donations. Owners and game admins only |
| `list_game_sales` | `uid` | | Sales, donations, refunds, and seller earnings for a game you manage |
| `get_approval` | `approval_id` | account | State of a purchase approval |
| `confirm_approval` | `approval_id`, `code` | account, write | Approve with the 6-digit code the human read from their email |
| `start_payout_setup` | none | account, money | Stripe payout setup link for the human |
| `get_payout_dashboard_link` | none | account, money | One-time Stripe Express dashboard link (`4095` before setup) |
| `cash_out` | `amount_cents` (at least 2500) | account, money | Cashes out available earnings to the account's own payout account, no approval; the owner is emailed. Sale earnings can be cashed out once that sale's refund window ends, 7 days after the sale. Playtime does not release them sooner. Payouts are processed on weekdays from 8:00am to 5:00pm Pacific |
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
| `create_account` | `email`, optional `password`, `timezone` | none | Continue or Generate only when password is omitted. Enter a timezone or Use this machine when timezone is omitted |
| `login` | `email`, optional `password` | none | The person types the password. Generate is not offered. Elevated only after sign-in succeeds |
| `confirm_account` | `email`, `code` | none | Returns the first `bgames_mcp_` key once and elevates this connection |
| `elevate_session` | `key` | none | Signs this connection in with a saved key. No Authorization header |

Payout tools need `mcp:write` or `mcp:money`.

## Scripted API

Full reference: [Scripted API](../../../docs/scripted-api.md). MCP never uploads a pack; `chauffeur sapi publish` does, with the game's deploy key. Turning it on, activating a pack, deleting a secret, and a real `reset_sapi_data` wait for the owner's approval.

| Tool | Inputs | Access | What it does |
|------|--------|--------|--------------|
| `get_sapi` | `uid` | | Enabled, anonymous calls, allowed origins, active pack per channel, plan limits, base URL, packs, and the publish command |
| `set_sapi` | `uid`, optional `enabled`, `anonymous_enabled`, `allowed_origins` | write | Only the fields you pass change. Turning it on waits for the owner's approval |
| `list_sapi_packs` | `uid` | | Checksum, channel, size, publisher, the channels each serves, and its logic list |
| `activate_sapi_pack` | `uid`, `checksum`, optional `channel` | write | Serves a stored pack on a channel (default `stable`). An empty checksum stops the channel. Also how you roll back |
| `get_sapi_logs` | `uid`, optional `logic`, `channel`, `level`, `request_id`, `since`, `until`, `cursor`, `limit` | | Stored script logs, oldest first. Follow `next_cursor`. Secret values are scrubbed |
| `get_sapi_usage` | `uid` | | Stored data, keys, players and leaderboard entries against the plan |
| `get_sapi_data` | `uid`, optional `scope`, `channel`, `user`, `prefix`, `after`, `limit` | | One page of keys and values in a scope, at most 200. Follow `next` |
| `set_sapi_data` | `uid`, `key`, `value`, optional `scope`, `channel`, `user`, `ttl` | write | Writes one value. Obeys the plan's write limits |
| `delete_sapi_data` | `uid`, `key`, optional `scope`, `channel`, `user` | write | Deletes one key |
| `reset_sapi_data` | `uid`, `scope`, optional `channel`, `user`, `prefix`, `dry_run`, `confirm` | write | Deletes many keys at once. A dry run counts and changes nothing; a real reset needs `confirm` |
| `get_sapi_config` | `uid` | | Remote config values per channel, and whether each is public |
| `set_sapi_config` | `uid`, `name`, optional `channel`, `value`, `public`, `delete` | write | Sets or deletes one config value |
| `list_sapi_secrets` | `uid` | | Secret names per channel. Values are never returned |
| `set_sapi_secret` | `uid`, `name`, optional `channel`, `value`, `delete` | keys | Stores or deletes one write-only secret |
| `list_sapi_schedules` | `uid` | | Scheduled logic, its cron and channel, and recent runs |
| `get_sapi_pack_files` | `uid`, optional `checksum` (64 characters, `active` or `latest`), `channel` | | The files of a stored pack with sizes and which are tests. Read-only |
| `get_sapi_file` | `uid`, `path`, optional `checksum`, `channel` | | The source of one file in a stored pack, so you can inspect the live scripts. Edit locally with `chauffeur sapi pull`, then `chauffeur sapi publish` |
| `get_sapi_features` | `uid` | | Each [feature and capability](../../../docs/scripted-api-features.md): enabled or not, what it needs, its plan, whether it is sensitive, and the link where the owner turns one on |
| `get_sapi_feature_history` | `uid` | | Who turned features on or off, and from where (dashboard, CLI, MCP, staff or migration) |
| `enable_sapi_feature` | `uid`, `feature` | | Changes nothing. Only the game owner can turn a feature on, from the website. Returns the link and what the feature needs |
| `disable_sapi_feature` | `uid`, `feature`, optional `cascade` | | Turns one feature off. Refused while an enabled feature needs it, unless `cascade` is true. Covered by `mcp:catalog.write` |
| `get_sapi_analytics` | `uid` | | Calls, errors, refusals (storage, rate, run budget, feature off) and latency per day and per logic |
| `get_sapi_audit` | `uid`, optional `limit`, `before` | | Every change to the Scripted API (packs, settings, features, data, config, secrets, staff stops) with who made it, newest first. Follow `next_before` for older entries |
## Lobby data

The store of games_slobby, separate from the Scripted API's data and with the same shape. Free has a small quota; Grow and Scale have more. A real `reset_lobby_data` waits for the owner's approval, as does deleting a lobby secret.

| Tool | Inputs | Access | What it does |
|------|--------|--------|--------------|
| `get_lobby_data` | `uid`, optional `scope` (`global`, `channel`, `user`, `lobby`), `channel`, `user`, `lobby`, `prefix`, `after`, `limit` | | One page of keys and values, at most 200. Follow `next` |
| `set_lobby_data` | `uid`, `key`, `value`, optional `scope`, `channel`, `user`, `lobby`, `ttl` | | Writes one value within the plan's limits. Covered by `mcp:catalog.write` |
| `delete_lobby_data` | `uid`, `key`, optional `scope`, `channel`, `user`, `lobby` | | Deletes one key. Covered by `mcp:catalog.write` |
| `reset_lobby_data` | `uid`, `scope`, optional `channel`, `user`, `lobby`, `prefix`, `dry_run`, `confirm` | | Deletes many keys. A dry run counts and changes nothing. A real reset needs `confirm` and waits for the owner's approval. Covered by `mcp:catalog.write` |
| `get_lobby_config`, `set_lobby_config` | `uid`, and for set `name`, `channel`, `value`, `public`, `delete` | | Lobby remote config. Covered by `mcp:catalog.write` |
| `list_lobby_secrets`, `set_lobby_secret` | `uid`, and for set `name`, `channel`, `value`, `delete` | | Write-only secrets for lobby scripts. Deleting waits for the owner's approval. Covered by `mcp:keys.manage` |
| `get_lobby_usage` | `uid` | | Lobby data against the plan, with the plan's lobby limits |
| `get_lobby_analytics` | `uid` | | Lobbies opened and closed, peaks, joins, requests turned away at a plan cap, lobby data use and TURN use over the plan's history window |
| `get_lobby_audit` | `uid`, optional `limit`, `before` | | Every change to lobby data with who made it, newest first. Follow `next_before` for older entries. Secret values are never recorded |

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
| `4083` | Website only (account settings, approval links, key management). It does not apply to `set_anonymous_downloads` |
| `4109` | Anonymous downloads were turned on without `confirm_no_license` |
| `4113` | Anonymous downloads are only available on a free listing |
| `4114` | A price or an edition was set while anonymous downloads are on |
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
| `set_presence_sharing` | Turn activity sharing on or off. Friends stop seeing live play when it is off. |
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

### Game settings and imports

| Tool | What it does |
|------|--------------|
| `open_web_player_poster` | Poster images are uploaded on the website, not through MCP. Returns the page where the human uploads one. |
| `delete_web_player_poster` | Remove the browser-player poster from a game. |
| `get_sign_in_providers` | Which providers a game accepts for player sign-in. |
| `set_sign_in_providers` | Replace the providers a game accepts for player sign-in: github, x, discord, steam, email. Also sets the web origins and return URIs that players outside the launcher may use. Send only the lists to change. Waits for the account owner's approval. |
| `get_sign_in_funnel` | How many player sign-ins were opened, needed a step on the website, and finished for a game, per day and per sign-in method. Counts only, for the last days (1 to 90, default 30). |

### Admin invites and key revocation

| Tool | What it does |
|------|--------------|
| `accept_invite` | Accept a game admin invite. This asks the account owner first. Turning on developer mode still finishes on the website. |
| `decline_invite` | Decline a game admin invite, or withdraw one you sent. |
| `revoke_gift_link` | Revoke a gift link that has not been redeemed. Waits for the account owner's approval. |
| `revoke_key_code` | Revoke one unused key code. A redeemed code keeps its license. Waits for the account owner's approval. |
| `revoke_key_pool` | Revoke unused codes in a pool, or one campaign. Redeemed codes keep their licenses. Waits for the account owner's approval. |

### Copyright notices

| Tool | What it does |
|------|--------------|
| `file_dmca_claim` | Files a copyright (DMCA) claim. The filing fee is not refundable. Asks the account owner first, and payment finishes on the checkout page the response returns. |
| `file_counter_notice` | Records a written statement on an open copyright notice that names this account, and emails it to the claimant. It does not restore content or start a waiting period. |
