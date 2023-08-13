#TODO:
# 1. track tokens with Game objects (__dict__ anyone?)
# 2. auto switch to gpt-3.5-turbo-16k-0613 when context is too long
# 3. add a 3rd item to messages indicating real_model
# 4. Output combat and stats in real time. (use a schema for this yeehaw)
# 5. Add a little text spinner to the chatbot while it's thinking
#    - Can use emojis! :D
import json,re,os
from typing import List
from datetime import datetime

import gradio as gr
from loguru import logger
from PythonClasses.Helpers.helpers import randomish_words
from PythonClasses.Helpers.helpers import generate_dice_string

from PythonClasses.LLM.OpenAI import OpenAIModel, OpenAIInterface
from PythonClasses.LLM.LilToken import LilToken, BiglyToken
from PythonClasses.Game.ChatMessage import Role
from PythonClasses.Game.ChatMessage import ChatMessage, SystemMessage
from PythonClasses.Game.History import HistoryFilter, TurnState


# from PythonClasses.Game.Speech import LLMStreamProcessor

from PythonClasses.LLM.OpenAI import OpenAIModel, OpenAIInterface
from PythonClasses.Game.CompleteJson import CompleteJson


class Game:
# The `Game` class  represents a game session. It keeps track of the game
# state, history of turns, and provides methods for interacting with the game. It also includes
# methods for rendering the game story, undoing turns, retrying turns, clearing the history,
# restarting the game, and submitting user messages. Additionally, it includes a method for
# streaming predictions from the language model.

    # Token Trackers for all games.
    TOKEN_TRACKERS = BiglyToken()

    START, STOP, PREDICTING = range(3)
    GAMES = {}

    # Initialize a new Game object for each active game.
    def __init__(self, game_name: str, model_name: str, chatbot: List[List[str]], system_message: str):
        logger.debug(f"Initializing Game: {game_name}")
        self.state = Game.START
        self.game_name = game_name

        # self.audio = LLMStreamProcessor(game_name)
        # Token trackers for each game.
        self.bigly_token = BiglyToken()

        self.history = HistoryFilter({
            "context_distance": 20,
            "summary_distance": 40,
            "display_distance": 60,
        })

        self.model = OpenAIModel.get_model_by_name(model_name)

        self.history += ChatMessage(self.model, Role.SYSTEM, [SystemMessage.inject_schemas(system_message)])
        

        # Intro Assistant Message
        self.history += ChatMessage(self.model, Role.Assistant, [chatbot[0][1]])
        # User entered their character name. Now ask them to choose items.
        choose_items_string = game_name + "\n" + "{Greet me and ask me to choose items}"
        self.history += ChatMessage(self.model, Role.USER, [game_name, choose_items_string])
        
        Game.GAMES[game_name] = self

    def accumulate_tokens(self):
        for model in OpenAIModel:
            self.game_token_trackers[model.model_name].accumulate_tokens()
            self.TOKEN_TRACKERS[model.model_name].accumulate_tokens()

    def start(game_name: str):
        logger.info(f"Starting Game: {game_name}")
        hide = gr.update(visible=False)
        show = gr.update(visible=True)
        # current_game = Game.GAMES[game_name]
        return Game.render_story(game_name) + [game_name, hide, hide, show, show, show]

    def __del__(self):
        logger.debug("Deleting Game")
        del self

    # Access the game object by name
    def _(game_name: str):
        return Game.GAMES[game_name]
    # # Access audio object
    # def _audio(game_name: str):
    #     return Game._(game_name).audio
    # def get_next_audio(game_name: str):
    #     return Game._audio(game_name).get_next_audio()

    def _stats(game_name: str):
        return Game._last_turn(game_name).stats
    def _combat(game_name: str):
        return Game._last_turn(game_name).combat
    
    # Update the interface
    def render_story(game_name: str):
        display_history = Game._(game_name).history.display_history()
        stats = Game._stats(game_name)

        day_box = stats.get("DAY")
        item_box = '\n'.join(stats.get("ITEM"))
        relationship_box = '\n\n'.join(stats.get("RELATIONSHIP"))

        # Sent to config tab for debugging
        turn_dict = Game._(game_name).history.__dict__("summary")

        # Something something LilToken
        # execution_json = Game._last_turn(game_name).execution

        # Speech
        # speech = Game._audio(game_name).get_next_audio()

        return [
            display_history,
            day_box,
            item_box,
            relationship_box,
            turn_dict,
            # execution_json,
            # speech,
        ]
    
    def undo(game_name: str):
        logger.info(f"Undoing last turn: {game_name}")
        if len(Game._history(game_name)) > 1:
            Game._(game_name).history.pop()
        if Game._(game_name).history.turn_state == TurnState.AWAITING_ASSISTANT and len(Game._history(game_name)) > 1:
            Game._(game_name).history.pop()
        return Game.render_story(game_name)
    def retry(game_name: str):
        logger.info("Retrying turn")
        if Game._(game_name).history.turn_state == TurnState.AWAITING_USER:
            Game._(game_name).history.pop()
        return Game.render_story(game_name)
    def clear(game_name: str):
        logger.info("Clearing history")
        # Game._(game_name).history = Game._(game_name).history[:1]
        return Game.render_story(game_name)
    def restart(game_name: str):
        logger.info("Restarting game")
        # Game.clear(game_name)
        return Game.start(game_name)
    
    def submit(game_name: str, user_message: str = "", system_message: str = None, model_name: str = None, type: str = "normal"):
        """
        This function is called when the user submits a message.
        """
        logger.debug(f"Submitting message: {user_message}")

        # Add dice rolls to user message if we are done with the intro
        complete_user_message = user_message
        if len(Game._(game_name).history) > 4:
            complete_user_message += f"\n{{{generate_dice_string(5)}}}"
        if "GPT_3" in Game._(game_name).model.model_name:
            complete_user_message += "\n{Remember to use the schemas exactly as provided}"
        system_message = SystemMessage.inject_schemas(system_message)

        # Update model, system message, and history
        Game._(game_name).model = OpenAIModel.get_model_by_name(model_name)
        Game._(game_name).history += ChatMessage(Game._(game_name).model, Role.SYSTEM, [SystemMessage.inject_schemas(system_message)])
        Game._(game_name).history += ChatMessage(Game._(game_name).model, Role.USER, [user_message, complete_user_message])

        # Clear input box and render story
        return [""] + Game.render_story(game_name)
    
    def new_day(game_name: str):

        logger.info("Starting a new day")
        last_turn = Game._last_turn(game_name)

        next_day_message = "{Begin the next day}"

        Game._(game_name).history += ChatMessage(Game._(game_name).model, Role.USER, ["", next_day_message])

        return Game.stream_prediction(game_name)
    
    def stream_prediction(game_name: str):
        logger.info("Streaming prediction")
       

        response_message = ChatMessage(Game._(game_name).model, Role.ASSISTANT, ["", ""])
        Game._(game_name).history += response_message

        schema_delimiter = r'\.\.[A-Z]+\.\.'  # regex pattern to find schema delimiters
        schema_name = None
        item_index = None
        temp_string = ""
        look_ahead = ""
        look_ahead_distance = 10

        system_message = Game._(game_name).history.current_system_message_openai_format
        context_history = Game._(game_name).history.context_history()
        

        for chunk in OpenAIInterface.predict(Game._(game_name).model.model_version, system_message, context_history):
            if len(chunk["choices"][0]["delta"]) == 0:
                break

            content = chunk["choices"][0]["delta"]["content"]
            response_message.stream_response(["", content, ""])



            # If not streaming, look for opening tag in the unprocessed content
            if not schema_name:
                
                # Buffer the display history so we don't show the schema tag
                look_ahead += content
                if len(look_ahead) > look_ahead_distance:
                    # Calculate the number of items to remove from the beginning
                    num_items_to_remove = len(look_ahead) - look_ahead_distance
                    
                    # Pass the removed items to the function
                    response_message.stream_response([look_ahead[:num_items_to_remove], "", ""])
                    
                    # Keep only the last look_ahead_distance items in the look_ahead list
                    look_ahead = look_ahead[num_items_to_remove:]
                # Game._audio(game_name).process_data(content)

                opening_match = re.search(schema_delimiter, look_ahead)
                if opening_match:
                    schema_name = opening_match.group(0).strip(" .")
                    look_ahead = look_ahead[:opening_match.start()]
                    content = content.rstrip('. \n')
                    if schema_name == "DAY":
                        response_message.stats["DAY"] = ""
                    elif schema_name == "ITEM":
                        if not "ITEM" in response_message.stats:
                            response_message.stats["ITEM"] = []
                    elif schema_name == "RELATIONSHIP":
                        if not "RELATIONSHIP" in response_message.stats:
                            response_message.stats["RELATIONSHIP"] = []
                    elif schema_name == "HIDE":
                        pass
                    else:
                        logger.error(f"Unknown schema: {schema_name}")
                        schema_name = None


            if schema_name == "DAY":
                response_message.stats["DAY"] += content
                closing_match = re.search(schema_delimiter, response_message.stats["DAY"])
                if closing_match:
                    schema_name = None
                    response_message.stats["DAY"] = response_message.stats["DAY"][:closing_match.start()]

                    # Extract the number from the day string
                    response_message.time_left = int(re.findall(r'\d+', response_message.stats["DAY"])[0])
                    if response_message.time_left <= 0:
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
                matching_indices = [index for index, item in enumerate(response_message.stats[schema_name]) if item.startswith(temp_string)]
                if len(matching_indices) == 0:
                    # If no match, append the content to the end of the array
                    item_index = len(response_message.stats[schema_name])
                    response_message.stats[schema_name].append(temp_string)
                elif len(matching_indices) == 1 and len(temp_string) > 4:
                    # If a match is found, replace the item at the first matching index
                    item_index = matching_indices[0]
                    response_message.stats[schema_name][item_index] = temp_string

            elif (schema_name is not None) and (item_index is not None):
                # If we already found the item index, just append the content to the item
                response_message.stats[schema_name][item_index] += content
                closing_match = re.search(schema_delimiter, response_message.stats[schema_name][item_index])
                if closing_match:
                    response_message.stats[schema_name][item_index] = response_message.stats[schema_name][item_index][:closing_match.start()]
                    item_index = None
                    temp_string = ""
                    schema_name = None

            yield Game.render_story(game_name)

        yield Game.render_story(game_name)