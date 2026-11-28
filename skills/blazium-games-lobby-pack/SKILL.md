---
name: blazium-games-lobby-pack
description: Publish a Luau lobby pack with chauffeur and check it on the Scripted lobby tab.
license: MIT
---

# Lobby packs

`chauffeur lobby set` turns the lobby on, chooses `relay` or `scripted`, and switches TURN. Pass at least one of `--enabled`, `--type`, or `--ice`.

`chauffeur lobby publish --dir <path>` packs `.lua` files, refuses any other script, and uploads through the uploader. `chauffeur lobby list` and `chauffeur lobby status` show the stored packs and the checksum the next lobby loads. The game editor Scripted lobby tab shows the same history. The page does not upload the pack.

A seated pack can call these on `lobby`. The host performs them. The pack never sees the host token.

- `unlock_achievement(user, slug)` and `set_stat(user, slug, value)` write progress when that definition lists `scripted_lobby`.
- `record_event(user, name, fields)` stores one registered funnel event. Slug, event, and status strings that are too long are refused before the call. `fields` is at most 4 KiB.
- `analytics(name)` reads count, unique devices, and the daily totals for one event that lists `scripted_lobby`. An optional build filter uses the same shape. It does not return visitor or download numbers.
- `set_presence(user, status)` only notifies that player's lobby connection. The host signs the notice. The launcher applies it.

## Lobby data

On every plan a lobby script can keep data in its own store (4 KiB per lobby on Free, 16 KiB on Grow, 64 KiB on Scale), with `data.global`, `data.channel`, `data.user` and `data.lobby`, `board(name)`, `config.get` and `secrets.get`. Declare what it reads and writes in `blazium.json` (`"data": { "read": [...], "write": [...] }`). The store is separate from the Scripted API's data. Reach the Scripted API with `sapi.read(scope, key, user, fn)` and `sapi.call(logic, { action, body, user }, fn)` after adding `"sapi"` to `uses`. The owner turns on the `lobby` and `lobby_data` capabilities for the game first, otherwise calls answer `feature_disabled`. `chauffeur lobby data|config|secret|usage` and the MCP tools `get_lobby_data`, `set_lobby_data`, `get_lobby_config` and `get_lobby_usage` read and change it. Guide: https://docs.blazium.games/docs/multiplayer#lobby-data.