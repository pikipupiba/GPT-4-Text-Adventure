#TODO:
# 1. track tokens with Game objects (__dict__ anyone?)
# 2. auto switch to gpt-3.5-turbo-16k-0613 when context is too long
# 3. add a 3rd item to messages indicating real_model
# 4. Output combat and stats in real time. (use a schema for this yeehaw)
# 5. Add a little text spinner to the chatbot while it's thinking
#    - Can use emojis! :D
import os
from loguru import logger
from PythonClasses.Helpers.randomish_words import randomish_words

from PythonClasses.Game.StateManager import StateManager
from PythonClasses.Game.Renderer import Renderer
from PythonClasses.Game.SystemMessage import SystemMessage
from PythonClasses.Game.SchemaStream import SchemaStream
from PythonClasses.OpenAI.LLM import LLM


class Game:

    # Initialize a new Game object for each active game.
    def __init__(self, name: str = None):
        logger.debug("Initializing Game")

        logger.debug("Starting game")

        if name is None:
            name = randomish_words()
            logger.warning(f"No name provided. Using {name}.")

        model = "gpt-4-0613"
        system_message = ""

        self.state = StateManager(name, model, system_message, user_message = "Begin the game.")

    def change_model(self, new_model:str=None):
        logger.debug(f"Changing model to {new_model}")

        self.state.turns[-1].model = new_model

        logger.trace(f"Successfully changed model to {self.state.turns[-1].model}")

    def change_name(self, new_name:str=None, keep_old:bool=True):
        logger.debug(f"Changing game name to {new_name}")

        self.state.change_name(new_name, keep_old)

        logger.trace(f"Successfully changed game name to {self.state.name}")

    def render(self):
        """
        This function is called when the game state changes.
        """
        return Renderer.render(self.state)
    
    def save_game(self):
        logger.debug("Saving game")
        self.state.save_game()
        return None
    
    def load_game(self):
        logger.debug("Loading game")
        self.state.load_game()
        return self.render()
    
    def delete_game(self):
        logger.debug("Deleting game")
        self.state.delete_game()
        return None
    
    def undo(self):
        logger.debug("Undoing turn")
        self.state.undo()
        return self.render()
    
    def retry(self):
        logger.debug("Retrying turn")
        self.state.retry()
        return self.render()

    def restart(self, name: str = None, model: str = None, system_message: str = None):
        """
        This function is called when the game starts.
        """
        logger.debug("Starting game")

        # Increment a number on the end of the name
        # Check if name ends in a number
        if self.name is None:
            self.name = randomish_words()
            logger.warning(f"No name provided. Using {self.name}.")
        elif self.name[-1].isdigit():
            # Increment the number
            self.name = self.name[:-1] + str(int(self.name[-1]) + 1)
        else:
            # Add a number to the end
            self.name += "_2"

        model = self.model
        system_message = self.system_message

        self.state = StateManager(name, model, system_message, user_message = "Begin the game.")

        return self.render()
    
    def submit(self, message: str = None):
        """
        This function is called when the user submits a message.
        """
        logger.debug(f"Submitting message: {message}")

        if self.state.turns[-1].raw[1] is not None:
            self.state.new_turn(message)

        return self.render()
    
    def stream_prediction(self):

        model = self.state.turns[-1].model
        system_message = self.state.turns[-1].system
        raw_history = self.state.get_raw_history()

        streaming_json = ""
        schema_stream = None
        did_append_combat = False
        self.state.turns[-1].raw[1] = ""
        self.state.turns[-1].display[1] = ""

        for chunk in LLM.predict(model, system_message, raw_history):

            if len(chunk["choices"][0]["delta"]) == 0:
                break

            content = chunk["choices"][0]["delta"]["content"]

            # See what model the api actually used. This is important for tracking tokens.
            real_model = chunk.get("model", model)

            # All chunks go to the raw history
            self.state.turns[-1].raw[1] += content
            
            if schema_stream == None:
                # Not currently in json stream, add chunk to chatbot
                if content == "{\"":
                    # Found the start of a JSON object
                    schema_stream = SchemaStream()
                    streaming_json += content
                    self.state.turns[-1].display[1] += "\n\n---"
                else:
                    self.state.turns[-1].display[1] += content
            else:
                # Don't add content to the chatbot if they are part of a JSON schema
                # Add content to the streaming json
                streaming_json += content

                # Check if the streaming json matches any schemas
                data = schema_stream.check_json_string(streaming_json)

                if schema_stream.schema_name == "Combat_Schema":
                    if not did_append_combat:
                        self.state.turns[-1].combat.append({})
                        did_append_combat = True

                    if data is not None:
                        self.state.turns[-1].combat[-1] = data

                elif schema_stream.schema_name == "Stats_Schema":
                    if data is not None:
                        self.state.turns[-1].stats = data

                if schema_stream.complete:
                    streaming_json = ""
                    self.schema_stream = None

            # yield self.state.turns[-1].raw, self.state.turns[-1].display, self.state.turns[-1].stats, self.state.turns[-1].combat

            yield self.render()