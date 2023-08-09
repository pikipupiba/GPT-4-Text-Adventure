import json

from typing import Dict, List
from loguru import logger

import gradio as gr

from PythonClasses.Game.Turn import Turn
from PythonClasses.player import *

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
        display_history = [getattr(turn, "display", ["", ""]) for turn in history]

        # Last available stats
        day_box, item_box, relationship_box = Render.render_stats(Render.last_stats(history))

        # Combat for last turn
        # combat_box = Render.render_combat(history[-1].__dict__().get("combat", []))

        # Execution for last turn
        execution_json = history[-1].__dict__().get("execution", {})

        # Last turn json
        turn_json = history[-1].__dict__()

        logger.trace("Successfully generated render strings")

        return [
            display_history,

            # player_message,
            # combat_box,
            day_box,
            item_box,
            relationship_box,

            execution_json,
            turn_json,
        ]
    
    def last_stats(history = []):

        # Stats are not guaranteed to be in every message, so we need to find the last one
        # i = len(history)-1
        for turn in reversed(history):
            # logger.info(f"Checking turn {i}")
            # i -= 1
            if not hasattr(turn, "stats") or turn.stats == {} or turn.stats is None:
                continue

            # last_stats_yee = turn.stats
            # logger.info("Last stats:")
            # logger.info(json.dumps(last_stats_yee, indent=4))
            return turn.stats

        # logger.info("No stats found in history. Returning {}.")
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
            name = item.get("name", "???")
            description = item.get("description", "???")
            items_string += f'{name} ({description})\n'
        
        # RELATIONSHIPS
        r_array = stats.get("relationships", [])
        relationships_string = ""
        for relationship in r_array:

            type = relationship.get("relationship", "")
            count = relationship.get("count", "")
            rationale = relationship.get("rationale", "")
            names = relationship.get("names", [])

            relationships_string += f'{type}: {count} ({rationale})\n'
            
            for name in names:
                relationships_string += f'{name}, '

            relationships_string = relationships_string[:-2] + '\n\n'

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
    
    def render_combat_new(combat: {}):
        logger.trace("RENDERING COMBAT!!!")

        combat_string=""
        
        if "name" in combat:
            combat_string += f'---> {combat["name"]}'
        if "action" in combat:
            combat_string += f' is trying to {combat["action"]}'
        if "dcRationale" in combat:
            combat_string += f'\n---> {combat["dcRationale"]}'
        if "modifierRationale" in combat:
            combat_string += f'\n---> {combat["modifierRationale"]}'
        if "dc" in combat:
            combat_string += f'\n---> Need: {combat["dc"]}'
        if "roll" in combat:
            combat_string += f' | Got: {combat["roll"]}'
        if "modifier" in combat and "roll" in combat:
            combat_string += f' + {combat["modifier"]}'
        if "result" in combat:
            combat_string += f' = {combat["result"]}'
        if "success" in combat:
            if combat["success"] == True:
                combat_string += f' | Success!'
            else:
                combat_string += f' | Failure!'
        

        logger.trace("DONE RENDERING COMBAT!!!")

        return combat_string