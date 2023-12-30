import json
import os
import re
from typing import List

from loguru import logger
from PythonClasses.Schemas import schema_strings

schemas_full = {
    "day": {
        "use": "When time passes in a measurable way. Always use after an action.",
        "description": (
            "Use this format to describe the day of the week and the amount of time"
            " remaining. Each day begins with 60 minutes. Always display the number of"
            " minutes remaining in the day as an integer. Do not start the next day"
            " without being told."
        ),
        "variables": {
            "day": "Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday",
            "time": (
                "time remaining in the day in minutes, must include the integer number"
                " even if it's 0: int between 0 and 60"
            ),
            "quip": "short quip about the amount of time remaining: <5 words",
        },
        "format": "..DAY..{day} with {time} minutes left. {quip}..DAY..",
    },
    "item": {
        "use": "When an item is used, gained, or changes status.",
        "description": (
            "Use this format to describe an item and its condition. Items can be used"
            " or gained."
        ),
        "variables": {
            "name": "name of the item - <5 words",
            "status": (
                "the current condition, status, or amount remaining of the item: <10"
                " words"
            ),
            "format": "..ITEM..{name} ({status})..ITEM..",
        },
        "relationship": {
            "use": (
                "When the number or attitude of NPCs of a certain relationship level"
                " changes."
            ),
            "description": (
                "Use this format to describe my relationships with NPCs. Relationships"
                " can be gained, lost and change but cannot be negative. Don't forget"
                " to subtract friends from one level when adding them to another."
            ),
            "variables": {
                "level": (
                    "Creative relationship levels. Indicates the level of closeness"
                    " with the player. Arch Nemesis, Enemy, Rival, Neutral, Ally,"
                    " Friend, Best Friend, Family, Lover, Soulmate, Spouse, etc."
                ),
                "change": (
                    "change to the number of NPCs in this level, includes the sign:"
                    " +/- int"
                ),
                "count": (
                    "number of NPCs of this type after change, should remain self"
                    " consistent: int"
                ),
                "rationale": (
                    "rationale for the change in the number of NPCs of this type: <20"
                    " words"
                ),
                "info": (
                    "current relevant information about NPCs of this type such as"
                    " names, sentiment, and/or reasoning: <20 words"
                ),
            },
            "format": (
                "..RELATIONSHIP..{type} | Change: {change} |  Total: {count}\n--->"
                " {rationale}\n---> {info}..RELATIONSHIP.."
            ),
        },
        "action": {
            "use": "When an action is taken.",
            "description": (
                "Use this format to describe an action taken by a character. Actions"
                " can succeed or fail."
            ),
            "variables": {
                "name": "name of character: <5 words",
                "action": "attempted action: <20 words",
                "difficulty": "level of difficulty, be creative: 1 word",
                "dcRationale": "rationale for the DC: <20 words",
                "dc": (
                    "DC for the action. Harder actions have higher DCs: int between 1"
                    " and 20"
                ),
                "modifierRationale": (
                    "rationale for roll modifier to allow for positive or negative"
                    " externalities. Using the right item for a situation or being"
                    " creative should give a bonus. Using the wrong item for a"
                    " situation or being distracted or weak should give a penalty: <20"
                    " words"
                ),
                "modifier": (
                    "+/- to the roll based on rationale, show the +/- sign: int between"
                    " -10 and +10"
                ),
                "numRolls": (
                    "number of dice rolls so far this turn. Starts at 0 every turn and"
                    " increments by 1 for each roll: int"
                ),
                "roll": (
                    "the user will send dice rolls with each turn called rolls[]. use"
                    " rolls[numRolls] for this value: int"
                ),
                "result": "roll + modifier: int",
                "success": (
                    "SUCCESS if {result} >= {dc}, else FAILURE. Add an adjective"
                    " indicating the level of success or failure depending on the"
                    " difference between the result and DC: string"
                ),
                "elapsedTime": (
                    "realistic and precise estimate of how long the action took: int"
                ),
            },
            "format": (
                "---> {name} is trying to {action}.\n---> Difficulty: {difficulty} -"
                " {dcRationale} ({dc})\n---> {'Bonus' or 'Penalty'}:"
                " {modifierRationale} ({modifier})\n---> Result: {rolls[numRolls]}"
                " {modifier sign: + or -} {modifier} {<, >, or =} {dc}  |  {adjective}"
                " {SUCCESS or FAILURE}\n---> Elapsed Time: {elapsedTime} minutes"
            ),
        },
    },
}

schemas_short = {
    "day": {
        "use": "When time passes in a measurable way. Always use after an action.",
        "description": (
            "Use this format to describe the day of the week and the amount of time"
            " remaining. Each day begins with 60 minutes."
        ),
        "variables": {
            "day": "day name",
            "time": "time remaining in day: int between 0 and 60",
            "quip": "short quip time remaining: <5 words",
        },
        "format": "..DAY..{day} with {time} minutes left. {quip}..DAY..",
    },
    "item": {
        "use": "Every time an item is used or mentioned.",
        "description": "Use this format to describe an item and its condition.",
        "variables": {
            "name": "name of the item - <5 words",
            "status": (
                "the current condition, status, or amount remaining of the item: <10"
                " words"
            ),
        },
        "format": "..ITEM..{name} ({status})..ITEM..",
    },
    "relationship": {
        "use": (
            "Every time you do something that could possibly affect your relationship"
            " with any NPC."
        ),
        "description": (
            "Use this format to describe my relationships with NPCs. Relationships can"
            " be gained, lost and change but cannot be negative. Don't forget to"
            " subtract friends from one level when adding them to another."
        ),
        "variables": {
            "level": (
                "Creative relationship levels. Indicates the level of closeness with"
                " the player. Arch Nemesis, Enemy, Rival, Neutral, Ally, Friend, Best"
                " Friend, Family, Lover, Soulmate, Spouse, etc."
            ),
            "change": "change to the number of NPCs in this level: +/- int",
            "count": "count after change, should remain self consistent: int",
            "rationale": "rationale for the change: <20 words",
            "info": (
                "current relevant information about NPCs of this type such as names,"
                " sentiment, reasoning, etc: <20 words"
            ),
        },
        "format": (
            "..RELATIONSHIP..{type} | Change: {change} |  Total: {count}\n--->"
            " {rationale}\n---> {info}..RELATIONSHIP.."
        ),
    },
    "action": {
        "use": "When an action is taken.",
        "description": (
            "Use this format to describe an action taken by a character. Actions can"
            " succeed or fail."
        ),
        "format": (
            "---> {name} is trying to {action}.\n---> Difficulty: {difficulty} -"
            " {dcRationale} ({dc})\n---> {'Bonus' or 'Penalty'}: {modifierRationale}"
            " ({modifier})\n---> Result: {rolls[numRolls]} {modifier sign: + or -}"
            " {modifier} {<, >, or =} {dc}  |  {adjective} {SUCCESS or FAILURE}\n--->"
            " Elapsed Time: {elapsedTime} minutes"
        ),
    },
}

special_turns = """Special Turns:
Turn 0: Game introduction & ask user's name.
Turn 1: User selects 5 items from a list of 10 items: treasure map to somewhere mischievous, magical rubber ducky, Ouija board, 7 random (you pick, some can have magical properties)"""


class SystemMessage:
    # The `SystemMessage` class is providing a method called `inject_schemas` that is used to inject
    # schema strings into a given system message. It does this by searching for schema placeholders
    # in the system message and replacing them with the corresponding schema string. The schema
    # placeholders are identified using a specific pattern (`/*\schema_name*/\`) and are replaced
    # using the `re.sub` function. If a schema string is not found for a particular schema name, the
    # original placeholder is retained in the system message. The method returns the complete system
    # message with the injected schemas.

    def inject_schemas(system_message: str, turn_num: int = 0):
        # The `inject_schemas` method is used to inject schema strings into a given system message. It
        # searches for schema placeholders in the system message and replaces them with the
        # corresponding schema string. The schema placeholders are identified using a specific pattern
        # (`/*\schema_name*/\`) and are replaced using the `re.sub` function. If a schema string is
        # not found for a particular schema name, the original placeholder is retained in the system
        # message. The method returns the complete system message with the injected schemas.

        from PythonClasses.Game.FileManager import FileManager

        logger.debug("Injecting schemas into system message")

        if turn_num > 15:
            with open(
                os.path.join(FileManager.SYSTEM_MESSAGE_FOLDER, "medium.txt"), "r"
            ) as f:
                system_message = f.read()
                complete_system_message = (
                    f"{system_message}\n\n{json.dumps(schemas_short, separators=(',', ':'))}"
                )
        else:
            # load full.txt from folder
            with open(
                os.path.join(FileManager.SYSTEM_MESSAGE_FOLDER, "long.txt"), "r"
            ) as f:
                system_message = f.read()
                complete_system_message = (
                    f"{system_message}\n\n{json.dumps(schemas_full, separators=(',', ':'))}"
                )

        # # Function to replace matched pattern with schema string
        # num_found_schemas = 0
        # def replacer(match):
        #     nonlocal num_found_schemas
        #     num_found_schemas += 1
        #     schema_name = match.group(1)  # Extract the schema_name from the matched pattern
        #     return schema_strings.get(schema_name, match.group(0))  # Return variable value or original if not found

        # # /*\schema_name*/\  # Pattern to match schema placeholders
        # schema_matcher = re.compile(r'\/\*\\(.*?)\/\*\\')  # Compile regex pattern to match schema placeholders

        # # Replace schema placeholders with schema strings in system message
        # complete_system_message = re.sub(schema_matcher, replacer, system_message)
        # if schema_select == None:
        #     complete_system_message = system_message
        # elif schema_select == "full":
        #     complete_system_message = f"{system_message}\n\n{json.dumps(schemas_full, separators=(',', ':'))}"
        # elif schema_select == "short":
        #     complete_system_message = f"{system_message}\n\n{json.dumps(schemas_short, separators=(',', ':'))}"
        # elif schema_select == "none":
        #     complete_system_message = system_message

        # logger.info(f"Successfully injected *{num_found_schemas}* schemas")

        return complete_system_message
