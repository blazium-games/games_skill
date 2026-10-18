---
name: blazium-games-unreal
description: Unreal plugin BlaziumGames for Blazium Games login, lobby, bugs, progress, and the dedicated server.
license: MIT
---

# Blazium Games Unreal

Public repo [blazium-games/games_unreal](https://github.com/blazium-games/games_unreal). Copy the release zip `BlaziumGames-<version>.zip` into `Plugins/BlaziumGames` and enable Blazium Games. Windows (`Win64`) and Linux are the supported targets.

Put `blazium_api64.dll` from `redistributable-win64.zip`, or `libblazium_api.so` from `redistributable-linux64.zip`, and `game.blaze`, beside the game executable. `UBlaziumSubsystem` is the only callback tick. Do not also call `RunCallbacks` every frame. Blueprint nodes are in the Blazium category.

Do not call client init and dedicated-server init in the same process. There is no macOS player library. This plugin does not proxy a Discord activity. A `templates-*` tag is the engine host, not this library.

`ReportBug` always sends the in-game report. An empty build id and an empty screenshot path omit those parts. The screenshot path check lives in the engine host, not in this plugin. The service redacts the log before storage.

`record_standard_events` is one batch of launch events with zero times, not a hook for each moment. Item calls are forwarded to the library. The server still rejects `socket_item`, `unsocket_item`, `set_item_stats`, and `use_item` on a player session.

The long guide is [Engines](https://docs.blazium.games/docs/engines).
