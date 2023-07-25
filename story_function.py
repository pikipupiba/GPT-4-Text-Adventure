story_function=[
    {
        "name": "get_story_chunks",
        "description": "ingest all aspects of the story",
        "required": ["Story", "Time", "Friends", "Items"],
        "parameters": {
            "type": "object",
            "properties": {
                "Story": {
                    "type": "string",
                    "description": "Continue the story.",
                },
                "Time": {
                    "type": "number",
                    "description": "What is an accurate estimate of how long the previous action took in minutes.",
                },
                "Relationships": {
                    "type": "object",
                    "description": "Update friends based on previous user action.",
                    "required": ["Acquaintances", "Friends", "Best Friend", "Enemies", "Arch Nemesis"],
                    "properties": {
                        "Acquaintances": {
                            "type": "object",
                            "description": "",
                            "properties": {
                                "count": {
                                    "type": "number",
                                    "description": "The number of acquaintances"
                                },
                                "info": {
                                    "type": "string",
                                    "description": "important info about changes to the acquaintances"
                                }
                            }
                        },
                        "Friends": {
                            "type": "object",
                            "description": "",
                            "properties": {
                                "count": {
                                    "type": "number",
                                    "description": "The number of friends"
                                },
                                "info": {
                                    "type": "string",
                                    "description": "important info about changes to the friends"
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
                                    "description": "important info about changes to the best friend"
                                }
                            }
                        },
                        "Enemies": {
                            "type": "object",
                            "description": "",
                            "properties": {
                                "count": {
                                    "type": "number",
                                    "description": "The number of enemies"
                                },
                                "info": {
                                    "type": "string",
                                    "description": "important info about changes to the enemies"
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
                                    "description": "important info about changes to the arch nemesis"
                                }
                            }
                        }
                    }
                },
                "Items": {
                    "type": "array",
                    "description": "Items remaining after previous user action.",
                    "items": {
                        "type": "string",
                    },
                },
            },
        },
    }
]