---
name: blazium-games-analytics
description: Read and summarize Blazium Games visitor analytics for a game page, including views, unique visitors, countries, and tracked actions. Use when the user asks how their game page is doing, for traffic numbers, or for a weekly analytics summary.
license: MIT
---

# Blazium Games: Analytics

Summarize store page traffic for one game.

## Invoke This Skill When

- "How is my game page doing?", "how many visitors this week?"
- "Which countries are my players from?"
- The user runs the `analytics_summary` prompt

## Prerequisites

- The `blazium-games` MCP server is connected (read access is enough)

## 1. Fetch

1. Resolve the game with `list_games` if the user did not give a `uid`.
2. Call `get_game_analytics` with `uid` (or read `blazium-games://games/{uid}/analytics`).

## 2. Interpret

| Field | Meaning |
|-------|---------|
| `total_views` | Page visits (`visited` actions) |
| `unique_visitors` | Distinct sessions |
| `country_breakdown.countries[]` | `country`, `count`, `percent` |
| `per_game[]` | Visitors and actions per game |
| `actions[]` | Tracked actions such as visits and downloads |
| `downloads.total` | Downloads that went through in the last 30 days |
| `downloads.anonymous` | Downloads with no account (anonymous downloads on) |
| `downloads.by_source[]` | `website`, `asset_library` (Godot or Blazium editor), `api`, `mcp_player`, `mcp_dev` |
| `downloads.by_access[]` | `anonymous`, `owner`, `free`, `purchase`, `grant`, `key`, `bundle` |
| `downloads.by_outcome[]` | Every attempt, including refusals such as `sign_in_required` and `payment_required` |

Analytics are aggregate. Individual visitors are not identifiable through the MCP.

## 3. Summarize

Report in a few sentences:

- Views and unique visitors
- Top three countries with percentages
- Notable actions (for example downloads compared with views)
- Downloads by source, and refusals worth fixing (many `payment_required` or `sign_in_required` attempts from the editor asset library, for example)
- One suggestion, such as improving the tagline if views are high but downloads are low

For crash trends, use `blazium-games-debug-crash` instead.

## Docs

https://docs.blazium.games/docs/mcp/reference
