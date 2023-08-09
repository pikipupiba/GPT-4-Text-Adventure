#TODO:
# 1. track tokens with Game objects (__dict__ anyone?)
# 2. auto switch to gpt-3.5-turbo-16k-0613 when context is too long
# 3. add a 3rd item to messages indicating real_model
# 4. Output combat and stats in real time. (use a schema for this yeehaw)
# 5. Add a little text spinner to the chatbot while it's thinking
#    - Can use emojis! :D
import json
from typing import List
from loguru import logger
from PythonClasses.Helpers.randomish_words import randomish_words
from PythonClasses.Helpers.helpers import generate_dice_string

from PythonClasses.Game.Turn import Turn
from PythonClasses.Game.Render import Render
from PythonClasses.Game.SystemMessage import SystemMessage
from PythonClasses.Game.FileManager import FileManager

from PythonClasses.LLM.LLM import LLM
from PythonClasses.Game.SchemaStream import SchemaStream
from PythonClasses.Game.CompleteJson import CompleteJson

class Game:

    # Initialize a new Game object for each active game.
    def __init__(self, history_name: str = None, system_name: str = None, ):
        logger.debug("Initializing Game")

        self.load_history(history_name)
        self.load_system_message(system_name)

        self.history_name = history_name
        self.system_name = system_name

        self.state = "START"
    
    def load_system_message(self, system_name: str):
        if system_name is None:
            system_name = randomish_words()
            logger.warning(f"No system name provided. Using {system_name}.")
            self.system_message = ""
        else:
            logger.info(f"Loading system message | {system_name}")
            self.system_message = FileManager.load_file(f"{system_name}_system_message.txt", "system_message")

        return self.system_message

    def save_system_message(self, system_name: str):
        logger.info(f"Saving system message | {system_name}")
        FileManager.save_file(self.system_message, f"{system_name}_system_message.txt", "system_message")
        self.system_name = system_name


    def render_history(self):
        """
        This function is called when the game state changes.
        """
        return Render.render_history(self.history)
    
    def save_history(self, history_name: str):
        logger.info(f"Saving game | {history_name}")

        history_json = [turn.__dict__() for turn in self.history]

        FileManager.save_file(history_json, f"{history_name}_history.json", "history")
        self.history_name = history_name
    
    def load_history(self, history_name: str):
        if history_name is None:
            history_name = randomish_words()
            logger.warning(f"No history name provided. Using {history_name}.")
            self.history = []
        else:
            logger.info(f"Loading history | {history_name}")
            history_json = FileManager.load_file(f"{history_name}_history.json", "history")
            # TODO: this def doesn't work
            self.history = [Turn(turn) for turn in history_json]
        
        return self.render_history()
    
    def delete_history(self, name: str):

        if name is None:
            name = self.name
        logger.info(f"Deleting game | {name}")
        FileManager.delete_file(f"{self.name}_history.json", "history")
    
    def undo(self):
        logger.info("Undoing turn")
        if len(self.history) > 0:
            self.history.pop()

        return self.render_history()
    
    def retry(self):
        logger.info("Retrying turn")
        self.history[-1].display[1] = None
        self.history[-1].raw[1] = None
        self.history[-1].stats = None
        self.history[-1].combat = None
        self.history[-1].tokens = None
        return self.render_history()

    def clear(self):
        logger.info("Clearing history")
        self.history = []
        return self.render_history()
    
    def submit(self, model: str = None, message: str = "", system_message: str = None, type: str = "normal"):
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

        if len(self.history) == 0 or len(self.history[-1].raw[1]) > 0:
            self.history.append(Turn({}, model, [message, complete_user_message], complete_system_message, type))

        return [""] + self.render_history()
    
    def get_raw_history(self):
        return [turn.raw for turn in self.history]
    
    def stream_prediction(self):

        current_turn = self.history[-1]

        model = current_turn.model
        system_message = current_turn.system_message
        raw_history = self.get_raw_history()

        streaming_json = ""
        in_streaming_json = False
        did_append_combat = False
        last_combat_string = ""
        self.history[-1].raw[1] = ""
        self.history[-1].display[1] = ""
        setattr(self.history[-1], "combat", [])
        setattr(self.history[-1], "stats", {})
        setattr(self.history[-1], "execution", {})

        for chunk in LLM.predict(model, system_message, raw_history):

            if len(chunk["choices"][0]["delta"]) == 0:
                break

            content = chunk["choices"][0]["delta"]["content"]

            # See what model the api actually used. This is important for tracking tokens.
            real_model = chunk.get("model", model)

            # All chunks go to the raw history
            self.history[-1].raw[1] += content
            
            if not in_streaming_json:
                # Not currently in json stream, add chunk to chatbot
                if content == "{\"":
                    # Found the start of a JSON object
                    in_streaming_json = True
                    streaming_json += content
                    self.history[-1].display[1] += "\n\n---\n\n"
                else:
                    self.history[-1].display[1] += content
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
                        self.history[-1].combat.append({})
                        did_append_combat = True

                    self.history[-1].combat[-1] = data["Combat_Schema"]

                    combat_string = Render.render_combat_new(self.history[-1].combat[-1])

                    if combat_string != last_combat_string:
                        delta = len(combat_string) - len(last_combat_string)
                        delta_string = combat_string[-delta:]
                        self.history[-1].display[1] += delta_string
                        last_combat_string = combat_string

                elif "Stats_Schema" in data:
                    self.history[-1].stats = data["Stats_Schema"]

                if complete:
                    if did_append_combat == True:
                        did_append_combat = False
                    streaming_json = ""
                    in_streaming_json = False
                    self.history[-1].display[1] += "\n\n"

            # yield self.history[-1].raw, self.history[-1].display, self.history[-1].stats, self.history[-1].combat

            yield self.render_history()