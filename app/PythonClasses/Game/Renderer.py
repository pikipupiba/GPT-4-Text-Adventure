from loguru import logger

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
        day, items, relationships = Renderer.render_stats(state.last_stats())

        # Combat for last turn
        combat = Renderer.render_combat(state.turn[-1].combat)

        # Execution for last turn
        execution = Renderer.render_token_tracker(state[-1].execution)

        logger.trace("Successfully generated render strings")

        return {
            "name": state.name,
            "display_history": display_history,
            "day": day,
            "items": items,
            "relationships": relationships,
            "combat": combat,
            "execution": execution,
        }

    def render_stats(self):
        if not "Stats_Schema" in self.stats:
            return {
                "day_string": "??? --- ??? minutes left",
                "items_string": "???",
                "relationships_string": "???",
            }
        
        logger.debug("RENDERING THE STATS!!!")
        stats = self.stats["Stats_Schema"]

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

        logger.debug("DONE RENDERING THE STATS!!!")

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

        logger.debug("DONE RENDERING COMBAT!!!")

        return combat_string

    # Break game state apart for rendering
    def render_game_state(self):
        logger.debug("RENDERING THE GAME STATE!!!")
        stats_strings = self.render_stats()
        combat_string = self.render_combat()

        logger.debug("DONE RENDERING THE GAME STATE!!!")
        logger.debug(self.team_name)
        logger.debug(self.history)
        logger.debug(stats_strings["day_string"])
        logger.debug(stats_strings["items_string"])
        logger.debug(stats_strings["relationships_string"])
        logger.debug(combat_string)
        return (
            self.team_name,
            self.history,
            stats_strings["day_string"],
            stats_strings["items_string"],
            stats_strings["relationships_string"],
            combat_string
        )