from typing import Dict, List
from loguru import logger

import gradio as gr

from PythonClasses.Game.Turn import Turn
from PythonClasses.player_tab import *

class Render:

    def render_history(history = []):
        """
        This function is called when the game state changes.
        """
        logger.trace("Rendering game")

        if len(history) == 0:
            return [
                [],

                "",
                "??? --- ??? minutes left",
                "???",
                "???",

                {},
                {},
            ]

        # Display history for the chatbot
        display_history = [turn.__dict__().get("display", ["", ""]) for turn in history]

        # Last available stats
        day_box, item_box, relationship_box = Render.render_stats(Render.last_stats(history))

        # Combat for last turn
        combat_box = Render.render_combat(history[-1].__dict__().get("combat", []))

        # Execution for last turn
        execution_json = history[-1].__dict__().get("execution", {})

        # Last turn json
        turn_json = history[-1].__dict__()

        logger.trace("Successfully generated render strings")

        return [
            display_history,

            combat_box,
            day_box,
            item_box,
            relationship_box,

            execution_json,
            turn_json,
        ]
    
    def last_stats(history = []):

        # Stats are not guaranteed to be in every message, so we need to find the last one
        for turn in reversed(history):
            if not hasattr(turn, "stats") or turn.stats == {}:
                continue

            return turn.__dict__()["stats"]

        return {}

    def render_stats(stats = {}):

        if (stats == {}):
            return [
                "??? --- ??? minutes left",
                "???",
                "???",
            ]
        
        logger.trace("RENDERING THE STATS!!!")

        # DAY/TIME LEFT
        day = stats.get("day", "???")
        time = stats.get("time", "???")
        day_string = f'{day} --- {time} minutes left'

        # ITEMS
        items_array = stats.get("items", [])
        items_string = ""
        for item in items_array:
            items_string += f'{list(item.items())[0][1]} ({list(item.items())[1][1]})\n'
        
        # RELATIONSHIPS
        r_array = stats.get("relationships", [])
        relationships_string = ""
        for relationship in r_array:

            relationship.setdefault("relationship", "")
            relationship.setdefault("count", "")
            relationship.setdefault("rationale", "")
            relationship.setdefault("names", [])

            relationships_string += f'{relationship["relationship"]}: {relationship["count"]} ({relationship["rationale"]})\n'
            
            for name in relationship["names"]:
                relationships_string += f'{name},'

            relationships_string = relationships_string[:-1] + '\n\n'

        return [
            day_string,
            items_string,
            relationships_string,
        ]
    
    def render_combat(combat_array: List = []):
        logger.trace("RENDERING COMBAT!!!")

        if len(combat_array) == 0:
            return ""

        combat_string=""
        for combat in combat_array:
            for key, value in combat.items():
                combat_string += f'{key}: {value} --- '
            combat_string = combat_string[:-4] + '\n'

        logger.trace("DONE RENDERING COMBAT!!!")

        return combat_string
    