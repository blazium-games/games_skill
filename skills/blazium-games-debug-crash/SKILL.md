---
name: blazium-games-debug-crash
description: Investigate Blazium Games crash reports. Lists recent crashes, reads the stack excerpt and metadata, downloads dumps, logs, or stackwalk output, maps the crash to a build and source code, and proposes a fix. Use when the user asks to look at crashes, debug a crash, or triage crash reports for a Blazium Games project.
license: MIT
---

# Blazium Games: Debug a Crash

Go from "players are crashing" to a root cause and a fix in the user's code.

## Invoke This Skill When

- "What are my latest crashes?", "debug this crash", "why is my game crashing?"
- The user pastes a crash id from https://blazium.games
- After `blazium-games-crash-reporting` verifies reports arrive

## Prerequisites

- The `blazium-games` MCP server is connected (read access is enough)
- The game's source code is open in the workspace (for step 4, Map to code)

## 1. Find the crash

1. Call `list_crash_groups` with the game `uid`. Each group is one cause (top stack frames, or the crash message and platform before a stackwalk), most recently seen first (up to 100 groups), with counts per build and a `sample_crash_id`.
2. A group whose reports all come from the newest build usually means a regression in that build.
3. Pick the crash the user named, or the `sample_crash_id` of the group with the highest count. `list_game_crashes` lists individual reports when you need more than the sample.
4. Call `list_bug_tickets` for the player's side: what they were doing, in their words. A ticket with an attached dump or log has a `crash_id` you can read like any other crash.

## 2. Read the report

Call `get_crash` with `uid` and `crash_id`. Key fields:

| Field | Meaning |
|-------|---------|
| `build_id`, `os`, `arch` | Which build and platform crashed |
| `user_message` | What the player said they were doing |
| `has_dump`, `has_log`, `has_stack` | Which artifacts can be downloaded |
| `analysis` | Server-side analysis, if already run |
| `metadata` | Reporter metadata (engine version, custom fields) |

Call `get_game_build` with the `build_id` to get the version and channel.

## 3. Download artifacts

Call `request_crash_download` with `kind`:

- `stack`: symbolicated stackwalk output. Start here.
- `log`: the log tail (`log.txt`).
- `dump`: the minidump (`dump.dmp`) for a native debugger.

Each call returns a private `url` valid for 1 hour (`expires_in: 3600`). Fetch it promptly; do not share it or paste it into public places.

## 4. Map to code

1. Take the top frames from the stack that belong to the user's code (skip engine and OS frames).
2. Search the workspace for those functions and files.
3. Check out or inspect the commit matching the build version when possible, so line numbers line up.
4. Read the log tail for the last actions before the crash.

## 5. Report

Give the user:

- One sentence root cause
- The file and function, with a code reference
- The builds and platforms affected, and how many reports
- A proposed fix, and a test or reproduction step
- If the build is live on `stable` and crashing badly, offer `rollback_channel` (needs write access). Players go back to the previous build and nothing is deleted
- Once a fix ships, offer to mark the matching bug tickets with `update_bug_ticket` (`status` `fixed`, or `closed` if it won't be fixed). `open` reopens one

If the dump has no symbols, say so and suggest exporting with debug symbols for the next build.

## Docs

https://docs.blazium.games/docs/crash-reporting#reading-crashes
