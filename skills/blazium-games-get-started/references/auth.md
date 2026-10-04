# Authentication

The server at `https://mcp.blazium.games/mcp` accepts OAuth 2.1 access tokens or MCP API keys, both sent as `Authorization: Bearer <token>`.

## OAuth (recommended)

- Discovery: `https://mcp.blazium.games/.well-known/oauth-protected-resource/mcp` and `/.well-known/oauth-authorization-server` (player server: the same paths ending in `/player`)
- PKCE `S256` (verifier 43-128 characters), dynamic client registration, and client ID metadata documents are supported
- Scopes: `mcp:read`, `mcp:write`, and the narrower `mcp:catalog.write`, `mcp:build.write`, `mcp:crash.read`, `mcp:analytics.read`, `mcp:keys.manage`, `mcp:money`
- Access tokens last 1 hour. Refresh tokens rotate on every use, so the client renews silently, but the sign-in still ends 30 days after it started
- Each refresh token works once. Reusing a spent one revokes the whole sign-in; the user then reconnects
- Details: https://docs.blazium.games/docs/mcp/oauth

On the consent page the user picks:

| Choice | Effect |
|--------|--------|
| Account | All games the user owns or admins, plus account tools |
| Single project | Only that game. Account tools (`get_profile`, `get_setup`, `list_mcp_keys`, `request_mcp_key`, `create_game`, `get_account`, approvals, payments, `blazium-games://me`) and other games return `403` code `4030` |
| Preset | **Store page**, **CI**, **Crash triage**, **Keys**, **Money**, or **Full access**. A tool outside the preset returns `4073` |
| Read-only access | Only `mcp:read` is granted. Any write returns `403` code `4031` "This token is read-only" |

Revoke grants at https://blazium.games/settings/mcp.

## API keys

For headless agents and CI:

1. Create a key at https://blazium.games/settings/mcp, or call `request_mcp_key` from an existing account session.
2. Configure the client:

```json
{
  "mcpServers": {
    "blazium-games": {
      "type": "http",
      "url": "https://mcp.blazium.games/mcp",
      "headers": { "Authorization": "Bearer bgames_mcp_YOUR_KEY" }
    }
  }
}
```

Keys start with `bgames_mcp_`. Issuing a new account key invalidates every previous account key. The owner and each admin can also create their own project key bound to one game from that game's MCP tab. Player keys start with `bgames_play_` and only work on `https://mcp.blazium.games/player`.

## Rules for agents

- Never print a full key or secret after the user has stored it. Refer to prefixes only.
- Never commit keys. Store them in CI secrets or a local `.env` that is gitignored.
- Rotating is destructive: warn before calling `request_mcp_key` or `request_deploy_key`.

## Server card

`https://mcp.blazium.games/.well-known/mcp/server-card.json` lists every tool, prompt, and resource the server currently exposes.
