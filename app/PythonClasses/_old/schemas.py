# combat_schema={
#     "Combat_Schema":
#     [
#         "{strCharacter}",
#         "{strAction}",
#         "{strDcReasoning}",
#         "{intDc}",
#         "{intRoll}",
#         "{intBonus}",
#         "{intResult}"
#     ]
# }

combat_schema={
    "Combat_Schema":{
        "type":"object",
        "description":"Combat thought process schema. Be realistic, creative, and concise.",
        "properties":{
            "name":{
                "type":"string",
                "description":"name of the character performing the action",
                "examples":[
                    "Player",
                    "Jolly Jimbo Jones",
                    "Counselor Craggy"
                ]
            },
            "action":{
                "type":"string",
                "description":"action taken by the character"
            },
            "dcRationale":{
                "type":"string",
                "description":"the rationale for the DC"
            },
            "dc":{
                "type":"integer",
                "description":"DC for the action. Harder actions have higher DCs"
            },
            "modifierRationale":{
                "type":"string",
                "description":"rationale for roll modifier to allow for positive or negative externalities.",
                # "examples":[
                #     "character is distracted",
                #     "The character is very weak",
                #     "The character is very smart",
                #     "The character is very dumb",
                #     "The character is very lucky",
                #     "The character is very unlucky",
                #     "The character is very skilled",
                # ]
            },
            "modifier":{
                "type":"integer",
                "description":"+/- to the roll based on rationale"
            },
            "numPreviousRolls":{
                "type":"integer",
                "description":"number of dice rolled so far this turn. Starts at 0 every time and increments by 1 for each roll",
            },
            "roll":{
                "type":"integer",
                "description":"the user will send an array of dice rolls with each turn called intRollArray[]. use intRollArray[numPreviousRolls] for this value"
            },
            "result":{
                "type":"integer",
                "description":"roll + modifier"
            },
            "success":{
                "type":"boolean",
                "description":"whether the action succeeds or not. True if result >= dc, False otherwise"
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
















