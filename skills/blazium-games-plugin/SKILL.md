---
name: blazium-games-plugin
description: Godot-based engines other than Blazium use the public games_plugin addon.
license: MIT
---

# games_plugin

Other Godot engines vendor `addons/blazium_games/`. Auth is the login websocket only. The addon never loads the official DLL. After the JWT arrives, `BlaziumLobby` and `BlaziumIce` use that token. Set project setting `blazium/game/game_uid`.

Inside a Discord activity, the addon sends API, login, and lobby traffic through `{applicationId}.discordsays.com`. Unity and Unreal do not.

`transfer_item` can move the signed-in player's items to Steam when that game allows it. `socket_item`, `unsocket_item`, `set_item_stats`, and `use_item` fail locally. Those actions belong to the game owner, an accepted admin, or a mint key on the owner's server, never a player session.
