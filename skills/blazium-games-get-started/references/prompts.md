# Blazium Games MCP prompts

| Prompt | Arguments | Purpose |
|--------|-----------|---------|
| `draft_game_page` | `pitch` (required) | Draft a name, one-line tagline, and two-paragraph description from a short pitch |
| `improve_game_copy` | `description` (required) | Rewrite an existing store description while keeping the facts |
| `analytics_summary` | `uid` (required) | Summarize the week's visitors using `get_game_analytics` |
| `bootstrap_game` | `pitch`, `uid` (both optional) | Create or find a store page, read deploy info and builds, and issue rotated deploy keys so an agent can ship from CI |

## `bootstrap_game` steps

1. `get_setup`
2. `create_game` from the pitch with `draft` visibility if no matching game exists
3. `get_deploy_info`
4. `list_game_builds` for existing `build_id` values
5. `request_deploy_key` (invalidates previous upload keys; returns `X-Access-Token` and `X-Secret-Key` once)
6. After `POST /api/v1/tool/upload/build`, store the returned `build_id` as `BLAZIUM_GAMES_BUILD_ID` and send it as `X-Build-Id` from crash reporters
7. Print env var names and URLs. Do not echo secrets after the user has stored them
