---
name: blazium-games-purchases
description: Buy games and donate on Blazium Games from the account's stored balance. Quotes the price and tax, confirms with the human, buys with an idempotency key, handles per-agent spending limits and emailed approvals, low balance, tops up by card link or x402 USDC, and fetches download links. Use when the user wants to buy, purchase, donate to, or download a game on Blazium Games, check their balance or library, or add balance.
license: MIT
---

# Blazium Games: Purchases

Agents buy only from the stored balance and only after telling the human the exact total. Within the limit the human set for this agent a purchase completes at once; anything else waits for the human to approve it by emailed link or code.

## Invoke This Skill When

- "Buy <game> on Blazium Games", "donate $5 to <game>"
- "What's my Blazium Games balance?", "add $20 to my balance"
- "Download <game>", "what games do I own?"

## Prerequisites

- The `blazium-games-player` MCP server (`https://mcp.blazium.games/player`) is connected with `player:buy` (the human ticked **Allow purchases**). See [player](../blazium-games-player/SKILL.md). The developer server still has these tools until 2026-10-28, marked deprecated; prefer the player server
- The account email is verified
- Optional: the human set a spending mode for this agent at https://blazium.games/settings/mcp (unlimited, monthly, yearly, or one-time limit). Without one, every purchase needs their approval

## 1. Check the account

1. Call `get_account`. If `email_verified` is false, call `request_email_code`, ask the human for the code from their inbox, and call `verify_email`.
2. Call `get_agent_policy`. `limit_mode` is `unset` (every purchase needs approval), `unlimited`, `monthly`, `yearly`, or `one_time`; `limit_cents` minus `spent_in_period_cents` is what you can spend without approval. Only the human changes it, at https://blazium.games/settings/mcp.
3. Call `get_library` (`list_library` on the developer server) to see whether the game is already owned. If it is, skip to step 5 (Download).

## 2. Quote

Call `quote_purchase` with the game `uid` (or vanity name). For a donation to a free game, pass `kind: "donation"` and `amount_cents` (100 to 50000).

If `get_game_details` lists `skus` (editions such as deluxe, beta access, or a bundle), ask the human which one and pass its slug as `sku` to both `quote_purchase` and `purchase_game`. Without `sku` the cheapest edition is bought. Owners of a cheaper edition pay only the difference.

The quote returns price, tax, and `total_cents`. Tax depends on the human's saved address.

## 3. Confirm with the human

Show the game, price, tax, and total in dollars, and say it will come from their Blazium Games balance. Wait for an explicit yes. Never buy on an assumed or earlier approval.

## 4. Buy

Call `purchase_game` (or `donate_to_game` with the same `amount_cents`) with:

| Field | Value |
|-------|-------|
| `uid` | The game |
| `sku` | Optional edition slug, the same one you quoted |
| `confirm_total_cents` | `total_cents` the human approved |
| `idempotency_key` | A new unique string, for example a UUID. Reuse it only to retry this same purchase after a network error |

| Code | What to do |
|------|------------|
| `4094` | The total changed. Show the new total from the error and ask again, then retry with a new idempotency key |
| `4020` | Not enough balance. Go to step 6 (Add balance) |
| `4221` | No billing address for tax. The human must top up by card once (`create_top_up_link`) or buy on the website |
| `4214` | Not an error: `approval_required`. Go to step 4b (Approval) |
| `4215` | The human denied it. Do not retry |
| `4095` | That idempotency key was used for a different purchase. Use a new key |
| `4212` | This token can't buy: no `player:buy`, or a project token. The human reconnects the player server with **Allow purchases** |
| `4096` | Email not verified. Go back to step 1 (Check the account) |
| `4090` | The human already owns the game. Skip to step 5 (Download) |
| `4091` | It's the human's own game; they can't buy it |
| `4092` | The game is free; no purchase needed. Skip to step 5 (Download) |
| `4093` | The game doesn't accept donations |
| `4155` | Unknown edition. Check `skus` in `get_game_details` |
| `4157` | The human already owns this edition or a higher one |
| `4165` | Beta access is sold as an edition. Offer the `beta_access` edition from `data.skus` |
| `4030` | A project-bound developer token. Use the player server instead |
| `4034` | Buying moved to the player server; the developer copies no longer work. Use `blazium-games-player` |

## 4b. Approval

The result has `approval_required: true` and an `approval` with its `uid`. The human got an email with a link and a 6-digit code.

1. Tell the human: approve with the link in the email, or read you the code.
2. If they give you the code, call `confirm_approval` with `approval_id` and `code`. `4216` means the code is wrong or expired.
3. Otherwise call `get_approval` after they say they approved. `status` is `pending`, `approved`, `denied`, `expired`, or `used`.
4. Once `approved`, call `purchase_game` (or `donate_to_game`) again with the same `idempotency_key` and `confirm_total_cents`. The approval covers only that purchase and expires after 30 minutes; if it expired, the retry sends a new email.

## 5. Download

1. Take `developer` and `vanity_name` (or `game_uid`) from `get_library`.
2. Read the public page data (no auth): `GET https://api.blazium.online/api/v1/public/user/<developer>/games/<vanity_name>`. Pick the file for the human's OS and arch from `data.files[]` and keep its `uid`.
3. Call `get_download_link` with `file_id` set to that `uid`. The link lasts 5 minutes; give it to the human right away.

Free games can be downloaded the same way without buying. If the error is `4099`, the file is still being scanned; try again later.

## 6. Add balance

Call `get_wallet` and `get_payment_options`, then either:

- **Card:** `create_top_up_link` with `amount_cents` (500 to 50000). Give the URL to the human; you cannot pay by card. Check `get_wallet` after they say it is done.
- **USDC over x402:** only if you have your own wallet and the human agreed. Call `create_x402_top_up` (`amount_cents`, optional `network`), sign a payment for exactly the returned requirements, then call `pay_with_x402` with `top_up_id` and the signed `payment_payload`. Credit appears after settlement.

Top-ups add a processing fee (shown by `get_payment_options`). Credit can be spent but never cashed out.

## Rules to tell the human when relevant

- Refunds are only through support@blazium.games: purchases within 7 days and before 2 hours of play. Donations are not refundable.
- With `player:buy` you can set up payouts (`start_payout_setup`, `get_payout_dashboard_link`; the human opens the Stripe link) and cash out available earnings (`cash_out`, $25 minimum) without approval. Money only goes to the account's own payout account, the owner is emailed after each cash-out, and it can take up to 72 business hours to reach the bank.

## Docs

- https://docs.blazium.games/docs/payments/agent-purchases
- https://docs.blazium.games/docs/payments/top-up
