day_schema = {
    "Day_Schema": {
        "type": "object",
        "description": "Current day and time remaining in day.",
        "properties": {
            "day": {"type": "string", "description": "Day of the week"},
            "time": {
                "type": "integer",
                "description": (
                    "Minutes remaining in the day after the actions this turn. Be"
                    " realistic and precise about how long the events described would"
                    " take. For example, high fiving 10 people may only take 5 minutes"
                    " or less, but playing a game of soccer might take more than 20"
                    " minutes. The player asking a question about the game or their"
                    " environment costs no time."
                ),
            },
            "daySummary": {
                "type": "string",
                "description": "Summary of the day's events if time remaining is 0.",
            },
        },
    },
}
