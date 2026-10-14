---
name: blazium-games-lobby-pack
description: Publish a Luau lobby pack with chauffeur and check it on the Scripted lobby tab.
---

# Lobby packs

`chauffeur lobby publish --dir <path>` packs `.lua` files, refuses any other script, and uploads through the uploader. `chauffeur lobby list` and `chauffeur lobby status` show the stored packs and the checksum the next lobby loads. The game editor Scripted lobby tab shows the same history. The page does not upload the pack.

A seated pack can call these on `lobby`. The host performs them. The pack never sees the host token.

- `unlock_achievement(user, slug)` and `set_stat(user, slug, value)` write progress when that definition lists `scripted_lobby`.
- `record_event(user, name, fields)` stores one registered funnel event. Slug, event, and status strings that are too long are refused before the call. `fields` is at most 4 KiB.
- `analytics(name)` reads count, unique devices, and the daily totals for one event that lists `scripted_lobby`. An optional build filter uses the same shape. It does not return visitor or download numbers.
- `set_presence(user, status)` only notifies that player's lobby connection. The host signs the notice. The launcher applies it.
