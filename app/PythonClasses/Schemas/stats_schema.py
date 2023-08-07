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
                "description":"Items in the player's inventory",
                "items":{
                    "type":"object",
                    "properties":{
                        "name":{
                            "type":"string",
                            "description":"Name of the item"
                        },
                        "description":{
                            "type":"string",
                            "description":"Information about and/or status of the item"
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
                            "description":"Type of relationship",
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
                        "names":{
                            "type":"array",
                            "description":"names of important characters in this type of relationship. Only for named characters",
                            "items":{
                                "type":"string",
                                "description":"Name of the character"
                            }
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