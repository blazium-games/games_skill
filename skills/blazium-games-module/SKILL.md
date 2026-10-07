---
name: blazium-games-module
description: Blazium engine games call the games module for login, scripted lobbies, and ICE.
---

# Blazium Games module

Blazium games call the engine module. Official DLL auth stays in the launcher pipe. The other auth is the private login websocket at `wss://login.blazium.online/api/v1/connect` (`getid`, `getlogin`, JWT, then the socket closes). Lobby create and join, and ICE fetch, run only after that token exists.
