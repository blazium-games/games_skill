"""Plugin packs for the Blazium Games skills. Games platform only."""

PACKS = {
    "blazium-games-developer": {
        "display": "Blazium Games Developer",
        "description": "Publish on Blazium Games: store pages, builds, crashes, analytics, and keys.",
        "skills": [
            "blazium-games-get-started",
            "blazium-games-store-page",
            "blazium-games-deploy",
            "blazium-games-crash-reporting",
            "blazium-games-debug-crash",
            "blazium-games-analytics",
            "blazium-games-keys",
        ],
        "mcp": False,
    },
    "blazium-games-player": {
        "display": "Blazium Games Player",
        "description": "Play on Blazium Games: search, reviews, friends, and purchases inside a spending limit.",
        "skills": [
            "blazium-games-get-started",
            "blazium-games-player",
            "blazium-games-purchases",
        ],
        "mcp": False,
    },
    "blazium-games": {
        "display": "Blazium Games",
        "description": "Blazium Games developer and player skills, plus the developer and player MCP servers.",
        "skills": [
            "blazium-games-get-started",
            "blazium-games-store-page",
            "blazium-games-deploy",
            "blazium-games-crash-reporting",
            "blazium-games-debug-crash",
            "blazium-games-analytics",
            "blazium-games-keys",
            "blazium-games-player",
            "blazium-games-purchases",
        ],
        "mcp": True,
    },
}
