story_function=[
    {
        "name": "continue_adventure",
        "description": "Ingest the player's action and update the story, time, relationships, and items.",
        "required": ["Story", "Time", "Friends", "Items"],
        "parameters": {
            "type": "object",
            "properties": {
                "Story": {
                    "type": "string",
                    "description": "Continue the narrative in an interesting and humorous way. Elaborate on details. When a new day begins, summarize the previous day's events and set the scene for the new day.",
                },
                "Time": {
                    "type": "number",
                    "description": "What is an accurate estimate of how long this action took in minutes.",
                },
                "Relationships": {
                    "type": "object",
                    "description": "Update relationships based on previous user action. If there are no changes, output the same as the input.",
                    "required": ["Acquaintances", "Friends", "Best Friend", "Enemies", "Arch Nemesis"],
                    "properties": {
                        "Acquaintances": {
                            "type": "object",
                            "description": "",
                            "properties": {
                                "count": {
                                    "type": "number",
                                    "description": "The total number of acquaintances"
                                },
                                "info": {
                                    "type": "string",
                                    "description": "important info about changes to the acquaintances this turn"
                                }
                            }
                        },
                        "Friends": {
                            "type": "object",
                            "description": "",
                            "properties": {
                                "count": {
                                    "type": "number",
                                    "description": "The total number of friends"
                                },
                                "info": {
                                    "type": "string",
                                    "description": "important info about changes to the friends this turn"
                                }
                            }
                        },
                        "Best Friend": {
                            "type": "object",
                            "description": "",
                            "properties": {
                                "count": {
                                    "type": "number",
                                    "description": "Number of best friends. Either 0 or 1."
                                },
                                "info": {
                                    "type": "string",
                                    "description": "important info about changes to the best friend this turn"
                                }
                            }
                        },
                        "Enemies": {
                            "type": "object",
                            "description": "",
                            "properties": {
                                "count": {
                                    "type": "number",
                                    "description": "The total number of enemies"
                                },
                                "info": {
                                    "type": "string",
                                    "description": "important info about changes to the enemies this turn"
                                }
                            }
                        },
                        "Arch Nemesis": {
                            "type": "object",
                            "description": "",
                            "properties": {
                                "count": {
                                    "type": "number",
                                    "description": "The number of arch nemesis. Either 0 or 1."
                                },
                                "info": {
                                    "type": "string",
                                    "description": "important info about changes to the arch nemesis this turn"
                                }
                            }
                        }
                    }
                },
                "Items": {
                    "type": "array",
                    "description": "Items remaining after player action. Only remove items if they are used up or given away and cannot be used again.",
                    "items": {
                        "type": "string",
                    },
                },
            },
        },
    }
]