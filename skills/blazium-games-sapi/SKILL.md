---
name: blazium-games-sapi
description: Write, test, publish, and run Scripted API Luau logic for a game at sapi.blazium.online, with stored data, leaderboards, schedules, secrets, and remote config.
license: MIT
---

# Scripted API

The Scripted API runs a game's own Luau logic at `https://sapi.blazium.online/v1/{game_uid}/{logic}`, so a game needs no server of its own for scores, rewards, inventory rules, season resets, or webhooks. Guide: https://docs.blazium.games/docs/scripted-api. Every function, header, error code, and limit: https://docs.blazium.games/docs/scripted-api-reference.

## Before you start

1. `get_sapi` shows whether it is on, the plan's limits, the active pack per release channel, and the base URL.
2. If it is off, `set_sapi` with `enabled: true` turns it on after the account owner approves. A deploy key cannot turn it on. Set `anonymous_enabled` only if logic marked `auth = "anonymous"` should run without a signed-in player, and `allowed_origins` only for web pages that call it directly.

## Write a pack

A pack is a folder of `.luau` files. Top-level files are routes (1 to 64 characters of `a-z 0-9 _ -`). Files in folders are modules loaded with `require("lib.name")`. `*.test.luau` files are tests. Each logic file returns a table:

```lua
return {
    auth = "user",                       -- anonymous | user | service | signed
    methods = { "POST" },
    uses = { "boards", "progress" },     -- boards, secrets, progress, items, http, webhook
    data = { read = { "user" }, write = { "user" } },  -- global, channel, user
    rate = { per_user = 30, window = 60 },
    handler = function(req)
        local best = math.max(data.user:get("best") or 0, req.body.score)
        data.user:set("best", best)
        board("high"):submit(req.body.score)
        return { best = best }
    end,
}
```

- Declare every data scope and `uses` entry the handler touches. Undeclared access raises `not_declared`.
- Validate input with `std.validate(req.body, schema)` and return `{ status = 400, body = ... }` on failure.
- All writes in a request apply together when the handler returns. An error discards them.
- `http` and `webhook` need `http = { allow = { "api.example.com" } }`.
- Progress writes need `scripted_api` in the achievement, stat, or event writers (`set_achievements`, `set_stats`, `set_funnels`).
- Secrets come from `secrets.get(name)` with `"secrets"` in `uses`. Never put a secret value in the pack.

## Test, then publish

Run these with the game's deploy key configured for chauffeur:

```bash
chauffeur sapi validate --dir sapi --plan free
chauffeur sapi test --dir sapi
chauffeur sapi publish --dir sapi --channel beta --activate
```

`chauffeur sapi dev --dir sapi` serves the pack locally at `http://127.0.0.1:8787/v1/dev/<logic>` with token `dev-user-1` and server key `dev-service`. The emulator is a Linux binary; on Windows run chauffeur in WSL. MCP never uploads a pack.

Promote by activating the same checksum on `stable`: `activate_sapi_pack` with the checksum from `list_sapi_packs`, or `chauffeur sapi activate <checksum> --channel stable`. Over MCP this waits for the owner's approval. Roll back by activating an older checksum. An empty checksum (`none` in chauffeur) stops a channel.

## Run it

- `get_sapi_logs` (filter by `logic`, `level`, or the `request_id` from a failed call) and `get_sapi_usage` for storage. `read_only: true` means the game is over a data limit after its plan changed: reads and deletes work, writes return `4308` until the plan is back or data is deleted.
- `get_sapi_data`, `set_sapi_data`, and `delete_sapi_data` change one key at a time. Deleting all data is website-only.
- `set_sapi_config` sets remote config (`public: true` serves it at `/v1/{game_uid}/_config`). `set_sapi_secret` stores write-only secrets; no tool returns a value.
- `list_sapi_schedules` shows cron logic and recent runs.

## Calling it

- Godot: the `BlaziumSapi` node, `call_logic(logic, args, opts)`, with `call_completed` and `call_failed` signals. It sends the session, channel, and an `Idempotency-Key`, and retries `429` and `503`.
- Any HTTP client: `Authorization: Bearer <session token>` for `auth = "user"`, `X-Sapi-Key` with a game server key (`request_server_key`) for `service`, `X-Blazium-Channel` for the channel, and `Idempotency-Key` on writes that may be retried.
- Unity and Unreal have no Scripted API client; use anonymous or service logic over HTTP.
- Discord activities need the `/blazium/sapi` to `sapi.blazium.online` URL mapping.

## Errors

Codes `4300` to `4322` come from the Scripted API. The common ones: `4302` no such logic or no active pack, `4304` sign-in missing, `4307` rate limited (honor `Retry-After`), `4308` over a plan limit, `4310` script error (read the logs for that request id), `4311` time or memory budget, `4317` unknown release channel.
