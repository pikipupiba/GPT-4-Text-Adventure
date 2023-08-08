from typing import Dict, List, Union
from loguru import logger

import gradio as gr

from PythonClasses.Game.StateManager import StateManager
from PythonClasses.player_tab import *

class Renderer:

    def __init__(self):
        self.game_name = ""
        self.load_game = gr.update()
        self.save_game = gr.update()
        self.delete_game = gr.update()

        self.display_history = ""
        self.combat_box = ""
        self.day_box = ""
        self.item_box = ""
        self.relationship_box = ""

        self.model_select = gr.update()
        self.player_message = gr.update()
        self.submit = gr.update()
        self.retry = gr.update()
        self.undo = gr.update()
        self.restart = gr.update()

        self.execution_json = {}
        self.game_state_json = {}

    def render(self, state: StateManager):
        """
        This function is called when the game state changes.
        """
        logger.trace("Rendering game")

        # Display history for the chatbot
        self.display_history = state.get_display_history()

        # Last available stats
        self.day_box, self.item_box, self.relationship_box = Renderer.render_stats(state.last_stats())

        # Combat for last turn
        self.combat_box = Renderer.render_combat(state.last_turn().__dict__().get("combat", []))


        # Execution for last turn
        if hasattr(state.last_turn(), "execution"):
            self.execution_json = state.last_turn().execution
        else:
            self.execution_json = {}

        # Game state for last turn
        self.game_state_json = state.last_turn().__dict__()

        logger.trace("Successfully generated render strings")

        return [
            self.game_name,
            self.load_game,
            self.save_game,
            self.delete_game,

            self.display_history,
            self.combat_box,
            self.day_box,
            self.item_box,
            self.relationship_box,

            self.model_select,
            self.player_message,
            self.submit,
            self.retry,
            self.undo,
            self.restart,

            self.execution_json,
            self.game_state_json,
        ]

        # return {
        #     render_dict.game_name: state.name,
        #     render_dict.load_game: gr.update(),
        #     render_dict.save_game: gr.update(),
        #     render_dict.delete_game: gr.update(),

        #     render_dict.display_history: display_history,
        #     render_dict.combat_box: combat_box,
        #     render_dict.day_box: day_box,
        #     render_dict.item_box: item_box,
        #     render_dict.relationship_box: relationship_box,

        #     render_dict.model_select: gr.update(),
        #     render_dict.player_message: gr.update(),
        #     render_dict.submit: gr.update(),
        #     render_dict.retry: gr.update(),
        #     render_dict.undo: gr.update(),
        #     render_dict.restart: gr.update(),

        #     render_dict.execution_json: execution_json,
        #     render_dict.game_state_json: game_state_json,
        # }

    def render_stats(_stats: Dict = {}):

        if not (stats := _stats.get("Stats_Schema")):
            return [
                "??? --- ??? minutes left",
                "???",
                "???",
            ]
        
        logger.trace("RENDERING THE STATS!!!")

        # DAY/TIME LEFT
        day = stats["day"]
        time = stats["time"]
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

        logger.trace("DONE RENDERING THE STATS!!!")

        return [
            day_string,
            items_string,
            relationships_string,
        ]
    
    def render_combat(_combat: List = []):
        logger.trace("RENDERING COMBAT!!!")

        if _combat is None:
            return []

        if not "Combat_Schema" in _combat:
            return []
        
        combat = _combat["Combat_Schema"]

        combat_string=""
        for key, value in combat.items():
            combat_string += f'{key}: {value} --- '

        logger.trace("DONE RENDERING COMBAT!!!")

        return combat_string
    