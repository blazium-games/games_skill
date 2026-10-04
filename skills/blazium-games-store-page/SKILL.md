---
name: blazium-games-store-page
description: Create or update a Blazium Games store page. Drafts the name, tagline, and description from a pitch, creates the page as a draft, updates copy, fills in the taxonomy, images, and similar titles until the listing check passes, sets a price or donations, and changes visibility. Use when the user wants to create a game page, write store copy, rename a game, price a game, accept donations, or publish a page on Blazium Games.
license: MIT
---

# Blazium Games: Store Page

Create and edit the public page at `https://<username>.blazium.games/<vanity_name>`.

## Invoke This Skill When

- "Create a Blazium Games page for my game", "write my store description"
- "Make my game public", "change the tagline"
- "Sell my game for $4.99", "let players donate"
- The `bootstrap_game` prompt needs a page to exist

## Prerequisites

- The `blazium-games` MCP server is connected with write access
- Creating a page needs an account-level token (a project-bound token can only edit its own game) and developer mode on the account. `4105` means it's off: the human turns it on at https://blazium.games/settings and accepts the developer terms. Never turn it on for them
- Going public, setting a price, and uploading need the owner's email verified. Check with `get_account`; if `email_verified` is false, call `request_email_code`, ask the human for the code from their inbox, then call `verify_email`. Updates that set `visibility` to `public` fail with code `4096` until then

## 1. Find or create

1. Call `list_games`. If a game matches the user's project, use its `uid` and go to step 3 (Update).
2. Otherwise draft copy. Use the `draft_game_page` prompt with a short `pitch`, or write:
   - `name`
   - `tagline`: one factual line. This is the share-card description on Discord, X, and Google. Do not put private contacts, keys, or unreleased URLs in it
   - `description`: markdown, two short paragraphs, facts only. Its first plain line is the share description when there is no tagline
3. Confirm the copy with the user.

## 2. Create

Call `create_game`:

| Field | Notes |
|-------|-------|
| `name` | Required |
| `tagline` | One line |
| `description` | Markdown |
| `visibility` | Start with `draft`. Options: `draft` (owner and admins), `owner` (owner only), `invisible` (link only), `public` |
| `asset_type` | `game`, `application`, `tool`, `mod`, `plugin`, `game_asset`, or `dev_asset` |
| `vanity_name` | URL slug, lowercase with dashes |
| `parent` | Required for `tool`, `mod`, and `plugin` before they can go public: `{"game": "uid-or-vanity"}` for a listing on Blazium Games, or `{"external_name": "...", "external_url": "https://..."}` for a game that isn't. Ask the user which game it's for |
| `adult` | `true` only if the user says it has sexual content or nudity. Adult pages are hidden from search, recommendations, and search engines, and need the player's opt-in |
| `indexable` | `false` keeps the page out of search engines and AI crawlers. Default `true` |

Keep the returned `uid`.

## 3. Update

Call `update_game` with `uid` and any of `name`, `tagline`, `description`, `visibility`, `asset_type`, `adult`, `indexable`, `parent`. An empty `parent` object clears it. To polish existing copy, run the `improve_game_copy` prompt with the current description first.

For mods and plugins, set how to install them with `set_mod_settings` (`install_path` relative to the game folder, `loader` such as `bepinex`, markdown `instructions`). For press coverage, fill the press kit with `set_press_kit`; it powers the page's `/press` page and `press.zip`. If the game is also on Steam, GOG, Epic Games Store, itch.io or another store, read the current links with `get_store_links`, then pass the full list to `set_store_links` (one https link per store, on that store's own site); they show as "Also on". Players can suggest tags; list them with `hide_community_tag` without a `tag`, and hide one only when the user asks.

Before switching to `public`, confirm with the user and make sure the owner is verified. `invisible` keeps the page reachable by link but out of listings.

## 3b. Listing (required before public)

A page can't go public until the listing check passes (`4225` otherwise).

1. Call `validate_listing`. It returns `errors`, `warnings`, and the allowed values.
2. Fix the taxonomy with `update_game_taxonomy`: at least 3 `tags`; for games also `genres`, `session_bucket`, `players_min`/`players_max`, `net`, and `inputs`; for mods and assets `engines`. Only use values from the check's vocabulary (`4071` otherwise). Ask the user rather than guessing player counts, network mode, or content warnings. Ask whether to set `authorship` (`human`, `human_agent`, or `agent_heavy`) and an optional `authorship_credit`; never pick it for them. Ask which parts used generative AI and set `ai_uses` (`art`, `audio`, `code`, `text`, `voice`, `runtime`, or an empty list for none) from their answer. Tools, mods, and plugins also need a `parent`, and plugins an engine.
3. Images: PNG, JPEG, GIF, or WebP, sniffed from the file bytes. Wide images need width/height between 1.70 and 1.85. Recommended, and the accepted range: thumbnail 1280x720 (960x540 to 1920x1080, 5 MB), cover 1024x576 (1024x576 to 2048x1152, 8 MB), screenshot 1920x1080 (1280x720 to 2048x1152, 10 MB). A public page needs a cover, a thumbnail, and 4 to 20 screenshots. Add at most 10 at a time. A game can change images 60 times an hour. The account avatar is uploaded on the settings page, not here. MCP never uploads images. Give the user the `chauffeur media` commands (`set_media` returns them), for example `chauffeur media cover art/cover.png` and `chauffeur media add shots/*.png`, run with the game's deploy key, or point them to the game's edit page on the website. See https://docs.blazium.games/docs/cli/media
4. A clean build: ship one with `blazium-games-deploy`, then check `scan_status` until a file is `clean`. If a file is `infected` or `error`, tell the user; it was removed and must be rebuilt and uploaded again.
5. Optionally `set_similar_games` with up to 10 public titles the user names.
6. Call `validate_listing` again; when `ready` is true, set `visibility` to `public`.

## 4. Price or donations (optional)

Call `set_game_price` with `uid` and:

| Field | Notes |
|-------|-------|
| `price_cents` | `0` for free, or `99` to `50000` ($0.99 to $500) |
| `donations_enabled` | Free games only. Donations are $1 to $500 |

To sell several editions (standard, deluxe, beta access, or a bundle with the user's other listings), use `upsert_sku` instead; up to 8 per listing. The listing price then follows the cheapest edition and `set_game_price` returns `4164`.

Tell the user what they will receive before setting it: each sale or donation pays the price minus $0.25 + 8% (a $10 game pays $8.95). Earnings unlock 7 days after each sale, and cash-out (8% plus Stripe's payout fee, $25 minimum) is on the website or through `cash_out`; payouts can take up to 72 business hours to reach the bank. Paid games can only be downloaded by buyers. Sales are listed by `list_game_sales`.

Details: https://docs.blazium.games/docs/payments/selling

## 5. Verify

Call `get_game` and give the user the page URL (`page_url` from `get_deploy_info`, or `https://<owner>.blazium.games/<vanity_name>`).

Videos and changelogs are managed on the website or through builds (`blazium-games-deploy`). Image sizes: https://docs.blazium.games/docs/graphical_assets_guidelines

## Docs

- https://docs.blazium.games/docs/listings
- https://docs.blazium.games/docs/content-rules
- https://docs.blazium.games/docs/press-kit
- https://docs.blazium.games/docs/seo-and-indexing
- https://docs.blazium.games/docs/developer-mode
- https://docs.blazium.games/docs/mcp/reference
