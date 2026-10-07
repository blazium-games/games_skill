---
name: blazium-games-plugin
description: Godot-based engines other than Blazium use the public games_plugin addon.
---

# games_plugin

Other Godot engines vendor `addons/blazium_games/`. Auth is the login websocket only. The addon never loads the official DLL. After the JWT arrives, `BlaziumLobby` and `BlaziumIce` use that token. Set project setting `blazium/game/game_uid`.
