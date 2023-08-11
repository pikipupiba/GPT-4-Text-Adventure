#TODO:
# 1. track tokens with Game objects (__dict__ anyone?)
# 2. auto switch to gpt-3.5-turbo-16k-0613 when context is too long
# 3. add a 3rd item to messages indicating real_model
# 4. Output combat and stats in real time. (use a schema for this yeehaw)
# 5. Add a little text spinner to the chatbot while it's thinking
#    - Can use emojis! :D
import json,re,os
from datetime import datetime

import gradio as gr
from loguru import logger
from PythonClasses.Helpers.helpers import randomish_words
from PythonClasses.Helpers.helpers import generate_dice_string

from PythonClasses.Game.Turn import Turn
from PythonClasses.Game.SystemMessage import SystemMessage
from PythonClasses.Game.UserMessage import UserMessage
from PythonClasses.LLM.LLMModel import LLMModel

# from PythonClasses.Game.Speech import LLMStreamProcessor

from PythonClasses.LLM.LLM import LLM
from PythonClasses.Game.CompleteJson import CompleteJson


class Game:
# The `Game` class  represents a game session. It keeps track of the game
# state, history of turns, and provides methods for interacting with the game. It also includes
# methods for rendering the game story, undoing turns, retrying turns, clearing the history,
# restarting the game, and submitting user messages. Additionally, it includes a method for
# streaming predictions from the language model.

    START, STOP, PREDICTING = range(3)

    TOTAL_EXECUTION = {
        "model": None,
        "time": {
            "total": {
                "start": None,
                "end": None,
                "elapsed": None,
                "TPM": None,
                "CPM": None,
            },
            "game_average": {
                "total_tokens": 0,
                "elapsed": None,
                "TPM": None,
                "CPM": None,
            },
            "turn_average": {
                "total_tokens": 0,
                "elapsed": None,
                "TPM": None,
                "CPM": None,
            },
        },
        "tokens": {
            "prompt": 0,
            "completion": 0,
            "total": 0,
        },
        "cost": {
            "prompt": 0,
            "completion": 0,
            "total": 0,
        },
    }


    GAMES = {}

    # Initialize a new Game object for each active game.
    def __init__(self, game_name: str, history: [], system_message: str):
        logger.debug(f"Initializing Game: {game_name}")
        self.state = Game.START
        self.game_name = game_name
        # self.audio = LLMStreamProcessor(game_name)

        self.history = []

        intro_json = {
            "type": "normal",
            "model": "gpt-4-0613",
            "system_message": system_message,
            "display": history[0],
            "raw": history[0],
            "stats": {
                "DAY": "Monday",
                "ITEM": [],
                "RELATIONSHIP": [],
            },
            "combat": [],
            "execution": {},
        }

        self.history.append(Turn(intro_json))

        choose_items_string = game_name + "\n" + "{Greet me and ask me to choose items}"

        choose_items_json = {
            "type": "normal",
            "model": "gpt-4-0613",
            "system_message": system_message,
            "display": [game_name, None],
            "raw": [choose_items_string, None],
            "stats": {
                "DAY": "Monday",
                "ITEM": [],
                "RELATIONSHIP": [],
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

    # Access the game object by name
    def _(game_name: str):
        return Game.GAMES[game_name]
    # # Access audio object
    # def _audio(game_name: str):
    #     return Game._(game_name).audio
    # def get_next_audio(game_name: str):
    #     return Game._audio(game_name).get_next_audio()
    
    # Access the game history by name
    def _history(game_name: str):
        return Game.GAMES[game_name].history
    def _history_to_dict(game_name: str):
        return [turn.__dict__() for turn in Game._history(game_name)]
    def _dict_to_history(game_name: str, history_dict_array: []):
        Game.GAMES[game_name].history = [Turn(turn) for turn in history_dict_array]
    def _num_turns(game_name: str):
        return len(Game._history(game_name))
    
    # Chatbot history to display to the player
    def _display_history(game_name: str):
        return [turn.display for turn in Game._history(game_name)]
    # OpenAI history for the language model
    def _raw_history(game_name: str):
        return [turn.raw for turn in Game._history(game_name)]

    # Access the last turn by name
    def _last_turn(game_name: str):
        return Game._history(game_name)[-1]
    def _prev_turn(game_name: str):
        return Game._history(game_name)[-2]
    def _last_display(game_name: str):
        return Game._last_turn(game_name).display
    def _last_raw(game_name: str):
        return Game._last_turn(game_name).raw
    def _stats(game_name: str):
        return Game._last_turn(game_name).stats
    def _combat(game_name: str):
        return Game._last_turn(game_name).combat
    
    # Update the interface
    def render_story(game_name: str):
        display_history = Game._display_history(game_name)
        stats = Game._stats(game_name)

        day_box = stats.get("DAY")
        item_box = '\n'.join(stats.get("ITEM"))
        relationship_box = '\n\n'.join(stats.get("RELATIONSHIP"))

        # Sent to config tab for debugging
        turn_dict = Game._last_turn(game_name).__dict__()

        execution_json = Game._last_turn(game_name).execution

        # Speech
        # speech = Game._audio(game_name).get_next_audio()

        return [
            display_history,
            day_box,
            item_box,
            relationship_box,
            turn_dict,
            execution_json,
            # speech,
        ]
    
    def undo(game_name: str):
        logger.info(f"Undoing last turn: {game_name}")
        if len(Game._history(game_name)) > 0:
            del Game._history(game_name)[-1]
        return Game.render_story(game_name)
    def retry(game_name: str):
        logger.info("Retrying turn")
        Game._last_display(game_name)[1] = None
        Game._last_raw(game_name)[1] = None
        Game._last_turn(game_name).stats = Game._prev_turn(game_name).stats
        Game._last_turn(game_name).combat = []
        Game._last_turn(game_name).tokens = {}
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

        turn_start_time = Game._last_turn(game_name).execution["time"]["turn"]["start"]
        turn_end_time = datetime.now()
        turn_elapsed_time = turn_end_time - turn_start_time
        turn_TPM = Game._last_turn(game_name).execution["tokens"]["total"] / turn_elapsed_time.total_seconds() * 60
        turn_CPM = Game._last_turn(game_name).execution["cost"]["total"] / turn_elapsed_time.total_seconds() * 60

        Game._last_turn(game_name).execution["time"]["turn"]["end"] = turn_end_time
        Game._last_turn(game_name).execution["time"]["turn"]["elapsed"] = turn_elapsed_time
        Game._last_turn(game_name).execution["time"]["turn"]["TPM"] = turn_TPM
        Game._last_turn(game_name).execution["time"]["turn"]["CPM"] = turn_CPM

        if Game._num_turns(game_name) > 2:
            dice_string = generate_dice_string(5)
        else:
            dice_string = ""

        complete_user_message = f'{message}\n{dice_string}'
        if "gpt-3" in model:
            complete_user_message += "\nRemember to use the schemas exactly as provided."
        complete_system_message = SystemMessage.inject_schemas(system_message)

        new_turn_json = {
            "type": type,
            "model": model,
            "system_message": complete_system_message,
            "display": [message, None],
            "raw": [complete_user_message, None],
            "stats": Game._stats(game_name).copy(),
            "combat": [],
            "execution": {},
        }

        if (Game._num_turns(game_name) == 0) or ((Game._last_raw(game_name)[1] is not None) and (len(Game._last_raw(game_name)[1]) > 0)):
            Game._history(game_name).append(Turn(new_turn_json))

        return [""] + Game.render_story(game_name)
    
    def new_day(game_name: str):

        logger.info("Starting a new day")
        last_turn = Game._last_turn(game_name)


        user_message = "{Begin the next day}"

        new_day_json = {
            "type": "normal",
            "model": last_turn.model,
            "system_message": last_turn.system_message,
            "display": [None, None],
            "raw": [user_message, None],
            "stats": Game._stats(game_name).copy(),
            "combat": [],
            "execution": {},
        }

        Game._history(game_name).append(Turn(new_day_json))

        return Game.stream_prediction(game_name)
    
    def stream_prediction(game_name: str):
        logger.info("Streaming prediction")
        current_turn = Game._last_turn(game_name)

        model = current_turn.model
        system_message = current_turn.system_message
        raw_history = Game._raw_history(game_name)

        prompt_tokens = LLMModel.num_tokens_from_messages(model, LLM.build_openai_history_array(Game._raw_history(game_name)))

        api_start_time = datetime.now()

        Game._last_raw(game_name)[1] = ""
        Game._last_display(game_name)[1] = ""

        schema_delimiter = r'\.\.[A-Z]+\.\.'  # regex pattern to find schema delimiters
        schema_name = None
        item_index = None
        temp_string = ""
        

        for chunk in LLM.predict(model, system_message, raw_history):
            if len(chunk["choices"][0]["delta"]) == 0:
                break

            Game._last_turn(game_name).execution["model"] = chunk.get("model", model)
            content = chunk["choices"][0]["delta"]["content"]
            Game._last_raw(game_name)[1] += content

            # If not streaming, look for opening tag in the unprocessed content
            if not schema_name:
                Game._last_display(game_name)[1] += content
                # Game._audio(game_name).process_data(content)

                opening_match = re.search(schema_delimiter, Game._last_display(game_name)[1])
                if opening_match:
                    schema_name = opening_match.group(0).strip(" .")
                    Game._last_display(game_name)[1] = Game._last_display(game_name)[1][:opening_match.start()]
                    content = content.rstrip('. \n')
                    if schema_name == "DAY":
                        Game._last_turn(game_name).stats["DAY"] = ""
                    elif schema_name == "ITEM":
                        if not "ITEM" in Game._last_turn(game_name).stats:
                            Game._last_turn(game_name).stats["ITEM"] = []
                    elif schema_name == "RELATIONSHIP":
                        if not "RELATIONSHIP" in Game._last_turn(game_name).stats:
                            Game._last_turn(game_name).stats["RELATIONSHIP"] = []
                    elif schema_name == "HIDE":
                        pass
                    else:
                        logger.error(f"Unknown schema: {schema_name}")
                        schema_name = None


            if schema_name == "DAY":
                Game._last_turn(game_name).stats["DAY"] += content
                closing_match = re.search(schema_delimiter, Game._last_turn(game_name).stats["DAY"])
                if closing_match:
                    schema_name = None
                    Game._last_turn(game_name).stats["DAY"] = Game._last_turn(game_name).stats["DAY"][:closing_match.start()]

                    # Extract the number from the day string
                    Game._last_turn(game_name).time_left = int(re.findall(r'\d+', Game._last_turn(game_name).stats["DAY"])[0])
                    if Game._last_turn(game_name).time_left <= 0:
                        logger.info("Day over")
                        return Game.new_day(game_name)
                    
            
            elif schema_name == "HIDE":
                temp_string += content
                closing_match = re.search(schema_delimiter, temp_string)
                if closing_match:
                    schema_name = None
                    temp_string = ""

            elif (schema_name is not None) and (item_index is None):
                temp_string += content
                # See if exactly 1 item in items_array matches the content.
                # Check if the start of any item in the array matches the content
                matching_indices = [index for index, item in enumerate(Game._last_turn(game_name).stats[schema_name]) if item.startswith(temp_string)]
                if len(matching_indices) == 0:
                    # If no match, append the content to the end of the array
                    item_index = len(Game._last_turn(game_name).stats[schema_name])
                    Game._last_turn(game_name).stats[schema_name].append(temp_string)
                elif len(matching_indices) == 1 and len(temp_string) > 4:
                    # If a match is found, replace the item at the first matching index
                    item_index = matching_indices[0]
                    Game._last_turn(game_name).stats[schema_name][item_index] = temp_string

            elif (schema_name is not None) and (item_index is not None):
                # If we already found the item index, just append the content to the item
                Game._last_turn(game_name).stats[schema_name][item_index] += content
                closing_match = re.search(schema_delimiter, Game._last_turn(game_name).stats[schema_name][item_index])
                if closing_match:
                    Game._last_turn(game_name).stats[schema_name][item_index] = Game._last_turn(game_name).stats[schema_name][item_index][:closing_match.start()]
                    item_index = None
                    temp_string = ""
                    schema_name = None

            yield Game.render_story(game_name)

        real_model = Game._last_turn(game_name).execution["model"]

        api_end_time = datetime.now()
        api_elapsed_time = api_end_time - api_start_time
        Game._last_turn(game_name).execution["time"]["api_call"]["start"] = api_start_time
        Game._last_turn(game_name).execution["time"]["api_call"]["end"] = api_end_time
        Game._last_turn(game_name).execution["time"]["api_call"]["elapsed"] = api_elapsed_time

        completion_tokens = LLMModel.num_tokens_from_text(real_model, Game._last_raw(game_name)[1])
        total_tokens = prompt_tokens + completion_tokens
        TPM = total_tokens / api_elapsed_time.total_seconds() * 60
        Game._last_turn(game_name).execution["tokens"]["prompt"] = prompt_tokens
        Game._last_turn(game_name).execution["tokens"]["completion"] = completion_tokens
        Game._last_turn(game_name).execution["tokens"]["total"] = total_tokens

        prompt_cost, completion_cost, total_cost = LLMModel.get_cost(model, prompt_tokens, completion_tokens)
        CPM = total_cost / api_elapsed_time.total_seconds() * 60

        Game._last_turn(game_name).execution["cost"]["prompt"] = prompt_cost
        Game._last_turn(game_name).execution["cost"]["completion"] = completion_cost
        Game._last_turn(game_name).execution["cost"]["total"] = total_cost

        Game._last_turn(game_name).execution["time"]["api_call"]["TPM"] = TPM
        Game._last_turn(game_name).execution["time"]["api_call"]["CPM"] = CPM

        yield Game.render_story(game_name)