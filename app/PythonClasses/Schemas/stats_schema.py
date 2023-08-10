stats_schema={
    "Stats_Schema":{
        "type":"object",
        "description":"Player stats schema. Be realistic, creative, and concise.",
        "properties":{
            "day":{
                "type":"string",
                "description":"Day of the week"
            },
            "time":{
                "type":"integer",
                "description":"Minutes left in the day after the actions this turn. Be realistic and precise."
            },
            "items":{
                "type":"array",
                "description":"Items in the player's inventory. Be as succinct as possible.",
                "items":{
                    "type":"object",
                    "properties":{
                        "name":{
                            "type":"string",
                            "description":"Name of the item"
                        },
                        "status":{
                            "type":"string",
                            "description":"The current status or condition of the item"
                        }
                    }
                }
            },
            "relationships":{
                "type":"array",
                "description":"Relationships with NPCs. May be named or unnamed characters. Be realistic, creative, and concise. Characters should change their relationship with the player based on the player's actions.",
                "items":{
                    "type":"object",
                    "properties":{
                        "relationship":{
                            "type":"string",
                            "description":"Type of relationship. Be creative, precise, and concise.",
                            "examples":[
                                "Acquaintance",
                                "Friend",
                                "Enemy",
                                "Best Friend",
                                "Arch Nemesis",
                                "Frenemy"
                                ]
                        },
                        "count":{
                            "type":"integer",
                            "description":"current number of relationships of this type"
                        },
                        "change":{
                            "type":"integer",
                            "description":"change in the number of relationships of this type"
                        },
                        "rationale":{
                            "type":"string",
                            "description":"rationale for the change in the number of relationships of this type"
                        },
                        "info":{
                            "type":"string",
                            "description":"What has changed about the NPCs in this relationship. Names, sentiments, etc."
                        }
                    }
                }
            }
        }
    }
}

# stats_schema={
#     "Stats_Schema":
#     [
#         ["{strDayOfWeekName}","{intMinsLeft}"],
#         [
#             ["{strItemName}","{strItemStatus}"]
#         ],
#         [
#             ["{intAcquaintanceCount}","{intAcquaintanceChange}","{strAcquaintanceSentiment}"],
#             ["{intFriendCount}","{intFriendChange}","{strFriendSentiment}"],
#             ["{intEnemyCount}","{intEnemyChange}","{strEnemySentiment}"],
#             ["{strBestFriendName}","{strBestFriendSentiment}"],
#             ["{strArchNemesisName}","{strArchNemesisSentiment}"]
#         ]
#     ]
# }