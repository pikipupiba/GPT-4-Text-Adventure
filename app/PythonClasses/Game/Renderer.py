from loguru import logger

import gradio as gr

from . import StateManager

class Renderer:

    def render(state: StateManager):
        """
        This function is called when the game state changes.
        """
        logger.debug("Rendering game")

        # Display history for the chatbot
        display_history = state.get_display_history()

        # Last available stats
        day_box, item_box, relationship_box = Renderer.render_stats(state.last_stats())

        # Combat for last turn
        combat_box = Renderer.render_combat(state.turn[-1].combat)

        # Execution for last turn
        execution_json = state.turn[-1].execution

        # Game state for last turn
        game_state_json = state.turn[-1].game_state

        logger.trace("Successfully generated render strings")

        return {
            "game_name": state.name,
            "load_game": gr.update(),
            "save_game": gr.update(),
            "delete_game": gr.update(),

            "display_history": display_history,
            "combat_box": combat_box,

            "day_box": day_box,
            "item_box": item_box,
            "relationship_box": relationship_box,

            "model_select": gr.update(),
            "player_message": gr.update(),
            "submit": gr.update(),
            "retry": gr.update(),
            "undo": gr.update(),
            "clear": gr.update(),

            "execution_json": execution_json,
            "game_state_json": game_state_json,
        }

    def render_stats(self):
        if not "Stats_Schema" in self.stats:
            return {
                "day_string": "??? --- ??? minutes left",
                "items_string": "???",
                "relationships_string": "???",
            }
        
        logger.debug("RENDERING THE STATS!!!")
        stats = self.stats

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

        return {
            "day_string": day_string,
            "items_string": items_string,
            "relationships_string": relationships_string,
        }
    
    def render_combat(self):
        logger.debug("RENDERING COMBAT!!!")

        if not "Combat_Schema" in self.combat:
            return [""]
        
        combat = self.combat["Combat_Schema"]

        combat_string=""
        for key, value in combat.items():
            combat_string += f'{key}: {value} --- '

        logger.trace("DONE RENDERING COMBAT!!!")

        return combat_string
    