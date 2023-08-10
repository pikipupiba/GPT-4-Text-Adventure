import json

from typing import Dict, List
from loguru import logger

import gradio as gr

from PythonClasses.Game.Turn import Turn
from PythonClasses.player import *

class Render:

    def render_story(chatbot: [], stats: {}):
        """
        This function is called when the game state changes.
        """
        logger.trace("Rendering game")

        if len(chatbot) == 0 and stats == {}:
            return [
                [],
                "??? --- ??? minutes left",
                "???",
                "???",
            ]

        # Last available stats
        day_box, item_box, relationship_box = Render.render_stats(stats)

        # # Execution for last turn
        # execution_json = history[-1].__dict__().get("execution", {})

        # # Last turn json
        # turn_json = history[-1].__dict__()

        logger.trace("Successfully generated render strings")

        return [
            chatbot,
            day_box,
            item_box,
            relationship_box,
        ]

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
            status = item.get("status", "???")
            items_string += f'{name} ({status})\n'
        
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
    
    def render_combat(combat: {}):
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