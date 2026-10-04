---
name: blazium-games-keys
description: Inspect and rotate Blazium Games credentials, including MCP API keys and per-game deploy keys, with warnings before destructive rotation and the owner's approval, and create redeemable game keys and gift links. Use when the user wants to rotate, revoke, list, or replace a Blazium Games key, suspects a key leaked, or wants to hand out game keys.
license: MIT
---

# Blazium Games: Keys

Blazium Games has two kinds of credentials:

| Credential | Used by | Rotate with | List with |
|------------|---------|-------------|-----------|
| MCP API key (`bgames_mcp_...`) | MCP clients without OAuth | `request_mcp_key` | `list_mcp_keys` |
| Deploy key (`access_token` + `secret_key`) | chauffeur CLI and CI uploads (builds, symbols, store images) | `request_deploy_key` | `get_deploy_info` (`keys[]`) |

## Invoke This Skill When

- "Rotate my Blazium Games key", "my deploy key leaked", "list my keys"
- A CI upload fails with an authentication error after someone rotated keys

## Prerequisites

- The `blazium-games` MCP server is connected with write access
- MCP key tools need an account-level token

## 1. Inspect

- MCP keys: call `list_mcp_keys`. Only prefixes are returned.
- Deploy keys: call `get_deploy_info` with the game `uid` and read `keys[]` (`uid`, `prefix`, `created_at`).

## 2. Warn

Rotation is immediate and destructive:

- `request_mcp_key` invalidates **every** previous MCP API key on the account. Any client using an old key stops working. OAuth connections are not affected.
- `request_deploy_key` invalidates **every** previous deploy key for that game. Any pipeline using an old key fails its next upload.

Ask the user to confirm and to name where the new secret will be stored.

## 3. Rotate

Call the matching tool with an `idempotency_key` you make up (for example `rotate-deploy-<uid>-<date>`). Over MCP the first call returns HTTP 202 with `approval_required: true` (code `4214`), `email_sent`, and an `approval` object. Pass `approval.uid` as `approval_id`, and give the human `approval.confirm_url`; the account owner also gets an email with the link and a 6-digit code. Ask the human to approve, then either call `confirm_approval` with the code they read to you or poll `get_approval` until `approved`. A project-bound token can't call either (`4030`), so wait for the human to say they approved from the email. Call the rotation tool again with the same `idempotency_key`. Each approval works once. If the human denies it you get `4215`; stop.

The secret is returned once. Tell the user to store it (CI secret, password manager, or a gitignored `.env`) and then stop repeating it.

## 4. Update consumers

- MCP key: update the `Authorization: Bearer` header in each MCP client config.
- Deploy key: update `BLAZIUM_ACCESS_TOKEN` and `BLAZIUM_SECRET_KEY` in every CI system, for example with `gh secret set BLAZIUM_ACCESS_TOKEN`.

## Revoking OAuth access

OAuth grants and project-bound MCP keys are managed at https://blazium.games/settings/mcp and in each game's settings. Revoking there does not require rotating API keys.

## Project keys and admins

- Each owner and admin creates their own project key. Creating one replaces only your own previous key for that project.
- Adding an admin over MCP waits for the owner's approval, and deleting a deploy key does too. Only the owner can add admins or remove other admins (`4034`).
- Removing an admin revokes their key for the project.
- The owner can turn off MCP access for admins on the project's MCP tab (website only). That revokes admins' keys and blocks their account keys and OAuth for that project.

## Game keys (redeemable codes)

Redeemable game keys are not credentials; they give players a copy of the game. They need a token with `mcp:money` (or full access).

1. `create_key_pool` with the game `uid` and a `name`.
2. `grant_keys` with `pool`, `n` (1 to 5000), and an `idempotency_key`. The codes come back once, as a `csv_url` that downloads one time within an hour. More than 100 at once returns `approval_required` like a rotation.
3. `create_gift_link` makes a single-use redeem link for one person, shown once.
4. `list_key_pools` shows size, redeemed, unredeemed, and gift link counts. Codes can't be shown again.

## Read-only tokens

If the user approved the connection with **Read-only access**, the token only has `mcp:read`. Rotation tools then fail with HTTP 403, code 4031 ("This token is read-only"). Ask the user to reconnect without the read-only option, or to rotate on the website. A token from a narrower preset without `mcp:keys.manage` gets `4073`; reconnect with the **Keys** or **Full access** preset.

## Docs

- https://docs.blazium.games/docs/mcp/access-and-keys
- Permissions, scopes, and error codes: https://docs.blazium.games/docs/legal/permissions
