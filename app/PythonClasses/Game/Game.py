#TODO:
# 1. track tokens with Game objects (__dict__ anyone?)
# 2. auto switch to gpt-3.5-turbo-16k-0613 when context is too long
# 3. add a 3rd item to messages indicating real_model
# 4. Output combat and stats in real time. (use a schema for this yeehaw)
# 5. Add a little text spinner to the chatbot while it's thinking
#    - Can use emojis! :D
import json

import gradio as gr
from loguru import logger
from PythonClasses.Helpers.helpers import randomish_words
from PythonClasses.Helpers.helpers import generate_dice_string

from PythonClasses.Game.Render import Render
from PythonClasses.Game.Turn import Turn
from PythonClasses.Game.SystemMessage import SystemMessage
from PythonClasses.Game.UserMessage import UserMessage

from PythonClasses.LLM.LLM import LLM
from PythonClasses.Game.CompleteJson import CompleteJson


class Game:
# The `Game` class  represents a game session. It keeps track of the game
# state, history of turns, and provides methods for interacting with the game. It also includes
# methods for rendering the game story, undoing turns, retrying turns, clearing the history,
# restarting the game, and submitting user messages. Additionally, it includes a method for
# streaming predictions from the language model.

    START, STOP, PREDICTING = range(3)

    GAMES = {}

    # Initialize a new Game object for each active game.
    def __init__(self, game_name: str, history: [], system_message: str):
        logger.debug(f"Initializing Game: {game_name}")
        self.state = Game.START
        self.game_name = game_name

        self.history = []

        intro_json = {
            "type": "normal",
            "model": "gpt-4-0613",
            "system_message": system_message,
            "display": history[0],
            "raw": history[0],
            "stats": {
                "day": "Monday",
            },
            "combat": [],
            "execution": {},
        }

        self.history.append(Turn(intro_json))

        choose_items_string = f"{game_name}\nLet's choose items now."

        choose_items_json = {
            "type": "normal",
            "model": "gpt-4-0613",
            "system_message": system_message,
            "display": [game_name, None],
            "raw": [choose_items_string, None],
            "stats": {
                "day": "Monday",
            },
            "combat": [],
            "execution": {},
        }

        self.history.append(Turn(choose_items_json))
        
        Game.GAMES[game_name] = self


    def start(game_name: str):
        logger.info(f"Starting Game: {game_name}")
        hide = gr.update(visible=False)
        show = gr.update(visible=True)
        # current_game = Game.GAMES[game_name]
        return Game.render_story(game_name) + [game_name, hide, hide, show, show, show]

    def __del__(self):
        logger.debug("Deleting Game")
        del self
        # delete any empty games
        for game_name, game in Game.GAMES.items():
            if game is None:
                del Game.GAMES[game_name]

    def _(game_name: str):
        return Game.GAMES[game_name]
    
    def _last_turn(game_name: str):
        return Game._history(game_name)[-1]
    def _history(game_name: str):
        return Game.GAMES[game_name].history
    
    def _history_to_dict(game_name: str):
        return [turn.__dict__() for turn in Game._history(game_name)]
    
    def _dict_to_history(game_name: str, history_dict_array: []):
        Game.GAMES[game_name].history = [Turn(turn) for turn in history_dict_array]
    
    def _stats(game_name: str):
        # Stats are not guaranteed to be in every message, so we need to find the last one
        for turn in reversed(Game._history(game_name)):
            if not turn.has_stats():
                continue
            return turn.stats
        return {}
    
    def _last_stats(game_name: str):
        return Game._last_turn(game_name).stats
    def _combat(game_name: str):
        return Game._last_turn(game_name).combat
    def _last_display(game_name: str):
        return Game._last_turn(game_name).display
    def _last_raw(game_name: str):
        return Game._last_turn(game_name).raw   


    def render_story(game_name: str):
        """
        This function is called when the game state changes.
        """
        display_history = Game._display_history(game_name)
        stats = Game._stats(game_name)
        
        return Render.render_story(display_history, stats)
    
    def undo(game_name: str):
        logger.info(f"Undoing last turn: {game_name}")
        if len(Game._history(game_name)) > 0:
            del Game._history(game_name)[-1]
        return Game.render_story(game_name)
    
    def retry(game_name: str):
        logger.info("Retrying turn")
        Game._last_display(game_name)[1] = None
        Game._last_raw(game_name)[1] = None
        Game._last_turn(game_name).stats = None
        Game._last_turn(game_name).combat = None
        Game._last_turn(game_name).tokens = None
        return Game.render_story(game_name)

    def clear(game_name: str):
        logger.info("Clearing history")
        for turn in Game._history(game_name):
            del turn
        return Game.render_story(game_name)
    
    def restart(game_name: str):
        logger.info("Restarting game")
        Game.clear(game_name)
        return Game.start(game_name)
    
    def submit(game_name: str, message: str = "", system_message: str = None, model: str = None, type: str = "normal"):
        """
        This function is called when the user submits a message.
        """
        logger.debug(f"Submitting message: {message}")

        # TODO: USER MESSAGE CLASS TO FORMAT IT WITH DICE ROLLS AND SUCH??
        # # Add dice roll to the end of the user message
        # if "intRollArray" not in self.raw_history[-1][0]:
        #     self.raw_history[-1][0] += f'\n\n{generate_dice_string(10)}'
        dice_string = generate_dice_string(5)
        complete_user_message = f'{message}\n{dice_string}'
        if "gpt-3" in model:
            complete_user_message += "\nRemember to use the schemas exactly as provided."
        complete_system_message = SystemMessage.inject_schemas(system_message)

        if (len(Game._history(game_name)) == 0) or (Game._last_raw(game_name)[1] == None) or (len(Game._last_raw(game_name)[1]) > 0):
            Game._history(game_name).append(Turn({}, model, [message, complete_user_message], complete_system_message, type))

        return [""] + Game.render_story(game_name)
    
    def _raw_history(game_name: str):
        return [turn.raw for turn in Game._history(game_name)]
    def _display_history(game_name: str):
        return [turn.display for turn in Game._history(game_name)]
    
    def stream_prediction(game_name: str):

        current_turn = Game._last_turn(game_name)

        model = current_turn.model
        system_message = current_turn.system_message
        raw_history = Game._raw_history(game_name)

        streaming_json = ""
        in_streaming_json = False
        found_schema = False
        did_append_combat = False
        last_combat_string = ""
        Game._last_raw(game_name)[1] = ""
        Game._last_display(game_name)[1] = ""
        setattr(Game._last_turn(game_name), "combat", [])
        setattr(Game._last_turn(game_name), "stats", {})
        setattr(Game._last_turn(game_name), "execution", {})

        for chunk in LLM.predict(model, system_message, raw_history):

            if len(chunk["choices"][0]["delta"]) == 0:
                break

            content = chunk["choices"][0]["delta"]["content"]

            # See what model the api actually used. This is important for tracking tokens.
            real_model = chunk.get("model", model)

            # All chunks go to the raw history
            Game._last_raw(game_name)[1] += content
            
            if not in_streaming_json:
                # Not currently in json stream, add chunk to chatbot
                if content == "{\"":
                    # Found the start of a JSON object
                    in_streaming_json = True
                    streaming_json += content
                    Game._last_display(game_name)[1] += "\n\n"
                else:
                    Game._last_display(game_name)[1] += content
            else:
                # Don't add content to the chatbot if they are part of a JSON schema
                # Add content to the streaming json
                streaming_json += content

                if "\n" in streaming_json:
                    pass
                # Check if the streaming json matches any schemas
                data, complete = CompleteJson.complete_json(streaming_json)

                if data is None:
                    # Parsing json failed for some reason. Such is life.
                    continue

                if "Combat_Schema" in data:
                    if not did_append_combat:
                        Game._last_turn(game_name).combat.append({})
                        did_append_combat = True

                    Game._last_turn(game_name).combat[-1] = data["Combat_Schema"]

                    combat_string = Render.render_combat(Game._last_turn(game_name).combat[-1])

                    if combat_string != last_combat_string:
                        delta = len(combat_string) - len(last_combat_string)
                        delta_string = combat_string[-delta:]
                        Game._last_display(game_name)[1] += delta_string
                        last_combat_string = combat_string

                elif "Stats_Schema" in data:
                    Game._last_turn(game_name).stats = data["Stats_Schema"]

                if complete:
                    logger.info(json.dumps(data, indent=4))
                    if did_append_combat == True:
                        did_append_combat = False
                    streaming_json = ""
                    in_streaming_json = False
                    Game._last_display(game_name)[1] += "\n\n"

            # yield self.history[-1].raw, self.history[-1].display, self.history[-1].stats, self.history[-1].combat

            yield Game.render_story(game_name)