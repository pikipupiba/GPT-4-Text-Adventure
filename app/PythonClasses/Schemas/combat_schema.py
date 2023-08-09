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
            "numPreviousRolls":{
                "type":"integer",
                "description":"number of dice rolled so far this turn. Starts at 0 every time and increments by 1 for each roll",
            },
            "dc":{
                "type":"integer",
                "description":"DC for the action. Harder actions have higher DCs"
            },
            "roll":{
                "type":"integer",
                "description":"the user will send an array of dice rolls with each turn called intRollArray[]. use intRollArray[numPreviousRolls] for this value"
            },
            "modifier":{
                "type":"integer",
                "description":"+/- to the roll based on rationale"
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