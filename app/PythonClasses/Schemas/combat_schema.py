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
                "description":"rationale for roll modifier to allow for positive or negative externalities. Using the right item for a situation or being creative should give a bonus. Using the wrong item for a situation or being distracted or weak should give a penalty",
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
                "description":"+/- to the roll based on modifierRationale"
            },
            "numPreviousRolls":{
                "type":"integer",
                "description":"number of dice rolled so far this turn. Starts at 0 every time and increments by 1 for each roll",
            },
            "roll":{
                "type":"integer",
                "description":"the user will send an array of dice rolls with each turn called rolls[]. use rolls[numPreviousRolls] for this value"
            },
            "result":{
                "type":"integer",
                "description":"roll + modifier"
            },
            "success":{
                "type":"boolean",
                "description":"whether the action succeeds or not. True if result >= dc, False otherwise"
            },
            "elapsedTime":{
                "type":"integer",
                "description":"Minutes consumed by the combat. Be realistic and precise about how long the events described would take. For example, high fiving 10 people may only take 5 minutes or less, but playing a game of soccer might take more than 20 minutes."
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