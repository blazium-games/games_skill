---
name: blazium-games-crash-reporting
description: Send crash reports, standard launch events, and custom events from a game to Blazium Games. Configures the Blazium Engine crash reporter or a custom HTTP reporter with X-App-Id and X-Build-Id, adds the session_start, boot_ok, first_input, session_end, and quit events that rate launch health, uploads Breakpad symbols with chauffeur, and verifies reports arrive. Use when the user wants crash reporting, crash dumps, symbols, launch health, error telemetry, or gameplay events for a Blazium Games project.
license: MIT
---

# Blazium Games: Crash Reporting

Wire a game to `POST https://api.blazium.online/api/v1/public/crashes` so crashes show up in `list_game_crashes`.

## Invoke This Skill When

- "Add crash reporting", "send crash dumps to Blazium Games", "why aren't my crashes showing up?"
- The user wants custom gameplay or telemetry events
- A build was just deployed and needs its `build_id` wired in

## Prerequisites

- The `blazium-games` MCP server is connected
- At least one registered build (see `blazium-games-deploy`)

## 1. Resolve identity

1. Call `get_deploy_info` with the game `uid`. Read `auth.crash_headers`:
   - `X-App-Id`: the game uid
   - `X-Build-Id`: the latest build's `build_id`
2. If the user ships several platforms or channels, call `list_game_builds` and pick the `build_id` matching the exact version, OS, arch, and channel. Every combination is its own build.

`X-Build-Id` is a build UID, never a version string. Crash ingest needs no secret, so these values are safe to ship inside the game.

## 2a. Blazium Engine games

Set these in Project Settings under `application/crash_reporter/`:

| Setting | Value |
|---------|-------|
| `enabled` | `true` |
| `upload_mode` | `InEngine`, `Sidecar`, or `Both` |
| `endpoint` | `https://api.blazium.online/api/v1/public/crashes` |
| `app_id` | the game uid (`X-App-Id`) |
| `build_id` | the build UID (`X-Build-Id`) |
| `app_version` | the build version |
| `build_channel` | `stable`, `beta`, etc. |
| `require_user_consent` | `true` (recommended) |
| `privacy_policy_url` | `https://blazium.games/privacy-policy` or your own |

For the sidecar UI, place the [crash_reporter](https://github.com/blazium-games/blazium_crash_reporter) binary next to the game executable. Never put secrets in Project Settings.

In CI, write `build_id` into the project before exporting, so each exported binary reports against its own build.

## 2b. Custom reporter

1. Create the report:

   ```http
   POST https://api.blazium.online/api/v1/public/crashes
   X-App-Id: <game uid>
   X-Build-Id: <build_id>
   Content-Type: application/json

   { "has_dump": true, "has_log": true, "app_name": "My Game", "app_version": "1.0.0",
     "engine_version": "4.8", "os": "windows", "arch": "x86_64",
     "user_message": "It froze on level 3", "anonymous": true, "metadata": {} }
   ```

   The response is `201` with `id` and an `uploads` object containing `dump` and/or `log` entries: `url`, `method` (`PUT`), `expires_at` (24 hours), `max_bytes` (64 MB), and `filename` (`dump.dmp` or `log.txt`).

2. Upload each file to its `url` with `PUT`, sending the raw bytes (or a multipart `file` part). Each URL works once.

| Error code | Meaning |
|------------|---------|
| `4001` | Invalid JSON body |
| `4010` | Missing `X-App-Id` or `X-Build-Id` |
| `4030` | Unknown app id, or a `build_id` that doesn't belong to that app. Use the `build_id` from `list_game_builds`, not a version string |
| `4130` | `metadata` has more than 64 keys (`413`) |
| `4290` | The game hit its daily crash report limit (`429`); retry tomorrow |

Past the daily upload limit the report is still stored but `uploads` is empty.

## 3. Standard events (always add these)

Every game should send the six standard events so its builds get a launch health band on the store page and new games can reach the Unheard of shelf. Add them without being asked whenever you wire crash reporting, and tell the user you did.

| Event | When | Fields |
|-------|------|--------|
| `session_start` | Process started | |
| `boot_ok` | First frame of the main menu or first scene | `device_uid` (required), `ms` since start (optional, 0 to 600000) |
| `first_input` | First key, click, touch or gamepad button | `ms` (optional, 0 to 600000) |
| `session_end` | Normal close | `seconds` (required, whole number 0 to 86400) |
| `quit` | The player chose Quit | |
| `crash` | Crash reporter, or next launch after an unclean exit | `device_uid` (required) |

Send them to the events endpoint below with the same random per-install `device_uid` on every event (store it in `user://`). Clamp `ms` and `seconds` to their ranges: one invalid standard event refuses the whole request with `4158`.

For Blazium and Godot, add an autoload (for example `res://autoload/blazium_events.gd`, registered in Project Settings > Autoload) that sends `session_start` in `_ready`, `boot_ok` after the first processed frame, `first_input` from `_input` once, and `session_end` on `NOTIFICATION_WM_CLOSE_REQUEST`, and exposes a `quit_game()` that sends `quit` and `session_end` before quitting. A complete script is in https://docs.blazium.games/docs/crash-reporting#standard-events. Use the same `app_id` and `build_id` as the crash reporter. For other engines, send the same events at the same moments.

Ask before adding them if the game has no privacy policy or the user needs player consent for telemetry.

## 4. Custom events (optional)

```http
POST https://api.blazium.online/api/v1/public/events
X-App-Id: <game uid>
X-Build-Id: <build_id>
Content-Type: application/json

{ "events": [ { "event": "level_complete", "anonymous": true, "device_uid": "<random per install>" } ] }
```

Up to 100 events per request (more returns `4130`); the response is `202`. Use a random per-install id, not hardware identifiers.

## 5. Symbols

Stacks from minidumps only show addresses until Breakpad symbols are uploaded for that build. Symbols can only be uploaded with the chauffeur CLI and the game's deploy key:

1. Export with debug symbols (the `.pdb` on Windows, an unstripped binary or `.debug` file on Linux, the `.dSYM` on macOS).
2. Make `.sym` files: `cargo install dump_syms`, then `dump_syms <pdb|binary|dSYM> > symbols/<name>.sym`.
3. Upload: `chauffeur symbols --build-id <build_id> symbols/`, or `--symbols symbols/` on `chauffeur addfiles`. `upload_symbols_info` returns the exact command.

Check with `list_build_symbols`. Details: https://docs.blazium.games/docs/cli/symbols

## 6. Verify

1. Trigger a test crash (or send the JSON above with `curl`).
2. Call `list_game_crashes` and confirm the new report and its `build_id`.
3. Run the game once and check that the events arrive with `get_game_analytics`. `get_build_health` rates a build once enough devices have launched it.
4. Hand off to `blazium-games-debug-crash` to read the crash.

If nothing arrives, check that `X-Build-Id` belongs to this game (`get_game_build`) and that the endpoint is the `crash_ingest` URL from `get_deploy_info`.

## Docs

https://docs.blazium.games/docs/crash-reporting
