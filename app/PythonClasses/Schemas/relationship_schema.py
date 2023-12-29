relationship_schema = {
    "Relationship_Schema": {
        "type": "array",
        "description": (
            "Relationships with NPCs. May be named or unnamed characters. Be realistic,"
            " creative, and concise. Characters should change their relationship with"
            " the player based on the player's actions."
        ),
        "items": {
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "description": (
                        "Type of relationship. Be creative, precise, and concise. The"
                        " type should logically follow from the player's actions."
                    ),
                    "examples": [
                        "Accepted Birthday Invite",
                        "Acquaintance",
                        "Friend",
                        "Enemy",
                        "Best Friend",
                        "Arch Nemesis",
                        "Frenemy",
                    ],
                },
                "info": {
                    "type": "string",
                    "description": (
                        "What has changed about the NPCs in this relationship. Names,"
                        " sentiments, etc."
                    ),
                },
                "changeRationale": {
                    "type": "string",
                    "description": (
                        "rationale for the change in the number of relationships of"
                        " this type"
                    ),
                },
                "change": {
                    "type": "integer",
                    "description": (
                        "change in the number of relationships of this type based on"
                        " the change rationale"
                    ),
                },
                "count": {
                    "type": "integer",
                    "description": (
                        "previous number of relationships of this type +/- change"
                    ),
                },
            },
        },
    }
}
