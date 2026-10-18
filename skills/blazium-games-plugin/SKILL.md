---
name: blazium-games-plugin
description: Godot addon for Blazium Games login, lobby, ICE, bugs, ownership, progress, and item transfer.
license: MIT
---

# Blazium Games plugin

Public repo [blazium-games/games_plugin](https://github.com/blazium-games/games_plugin). Install `blazium_games-<version>.zip` from a release, or copy `addons/blazium_games`. Enable the plugin and set the project setting `blazium/game/game_uid` to the project id.

The addon talks to Blazium over HTTP. It does not ship or load `blazium_api64.dll` or `libblazium_api.so`.

Sign in on the login websocket, then use that session for the lobby and for ICE. Inside a Discord activity, the addon proxies login, lobby, and API. Unity and Unreal do not.

`server_progress` is the only call that uses `await`. Every other call returns through a signal. `record_standard_events` posts `session_start`, `session_end`, `boot_ok`, `first_input`, `quit`, and `crash` in one request with zero times. It is not a hook for each of those moments.

The in-game bug call sends `X-Build-Id`, the log, and a screenshot. The screenshot path has to be under `user://` and stops at 32 MiB. The service redacts the log before storage. See [Bug reporter](https://docs.blazium.games/docs/bug-reporter).

`transfer_item` is the player call. `socket_item`, `unsocket_item`, `set_item_stats`, and `use_item` fail on a player session. Those need the owner, an accepted admin, or a mint key.

The long guide is [Engines](https://docs.blazium.games/docs/engines).
