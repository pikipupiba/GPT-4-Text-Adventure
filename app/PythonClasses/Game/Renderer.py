from loguru import logger

import gradio as gr

from PythonClasses.Game.StateManager import StateManager
from PythonClasses.player_tab import *

class Renderer:

    def render(state: StateManager):
        """
        This function is called when the game state changes.
        """
        logger.trace("Rendering game")

        # Display history for the chatbot
        display_history = state.get_display_history()
        if display_history is None:
            display_history = []

        # Last available stats
        if hasattr(state.turns[-1], "stats"):
            day_box, item_box, relationship_box = Renderer.render_stats(state.last_stats())
        else:
            day_box, item_box, relationship_box = Renderer.render_stats(None)

        # Combat for last turn
        if hasattr(state.turns[-1], "combat"):
            combat_box = Renderer.render_combat(state.turns[-1].combat)
        else:
            combat_box = ""

        # Execution for last turn
        if hasattr(state.turns[-1], "execution"):
            execution_json = state.turns[-1].execution
        else:
            execution_json = {}

        # Game state for last turn
        game_state_json = state.turns[-1].__dict__()

        logger.trace("Successfully generated render strings")

        return [
            state.name,
            gr.update(),
            gr.update(),
            gr.update(),

            display_history,
            combat_box,
            day_box,
            item_box,
            relationship_box,

            gr.update(),
            gr.update(),
            gr.update(),
            gr.update(),
            gr.update(),
            gr.update(),

            execution_json,
            game_state_json,
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

    def render_stats(stats):

        if stats is None:
            return [
                "??? --- ??? minutes left",
                "???",
                "???",
            ]

        if not "Stats_Schema" in stats:
            return [
                "??? --- ??? minutes left",
                "???",
                "???",
            ]
        
        logger.debug("RENDERING THE STATS!!!")

        stats = stats["Stats_Schema"]

        # DAY/TIME LEFT
        day = stats["day"]
        time = stats["time"]
        day_string = f'{day} --- {time} minutes left'

        # ITEMS
        items_array = stats["items"]
        items_string = ""
        for item in items_array:
            items_string += f'{list(item.items())[0][1]} ({list(item.items())[1][1]})\n'
        
        # RELATIONSHIPS
        r_array = stats["relationships"]
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
    
    def render_combat(combat):
        logger.debug("RENDERING COMBAT!!!")

        if combat is None:
            return []

        if not "Combat_Schema" in combat:
            return []
        
        combat = combat["Combat_Schema"]

        combat_string=""
        for key, value in combat.items():
            combat_string += f'{key}: {value} --- '

        logger.trace("DONE RENDERING COMBAT!!!")

        return combat_string
    