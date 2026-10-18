---
name: blazium-games-unity
description: Unity package com.blazium.games for Blazium Games login, lobby, bugs, progress, and the dedicated server.
license: MIT
---

# Blazium Games Unity

Public repo [blazium-games/games_unity](https://github.com/blazium-games/games_unity). Install the release tarball `com.blazium.games-<version>.tgz` with Package Manager (**Add package from tarball**). The package name is `com.blazium.games`.

Put `blazium_api64.dll` from `redistributable-win64.zip`, or `libblazium_api.so` from `redistributable-linux64.zip`, in `Assets/Plugins/x86_64`. Put `game.blaze` beside the built player. Add one `BlaziumTick`. It calls `RunCallbacks` from `Update`. Do not also call `RunCallbacks` every frame.

Do not call `BlaziumApi.Init` and `BlaziumGameServer.Init` in the same process. There is no macOS player library. This package does not proxy a Discord activity. A `templates-*` tag is the engine host, not this library.

The public `ReportBug` method always sends the in-game report. An empty build id and an empty screenshot path omit those parts. The screenshot path check lives in the engine host, not in this package. The service redacts the log before storage.

`record_standard_events` is one batch of launch events with zero times, not a hook for each moment. Item calls are forwarded to the library. The server still rejects `socket_item`, `unsocket_item`, `set_item_stats`, and `use_item` on a player session.

The long guide is [Engines](https://docs.blazium.games/docs/engines).
