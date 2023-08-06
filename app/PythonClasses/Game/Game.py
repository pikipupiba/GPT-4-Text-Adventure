#TODO:
# 1. track tokens with Game objects (__dict__ anyone?)
# 2. auto switch to gpt-3.5-turbo-16k-0613 when context is too long
# 3. add a 3rd item to messages indicating real_model
# 4. Output combat and stats in real time. (use a schema for this yeehaw)
# 5. Add a little text spinner to the chatbot while it's thinking
#    - Can use emojis! :D

import os,json,uuid
import openai
from loguru import logger
from ..Helpers import randomish_words
from StateManager import 
from . import StateManager, Renderer, SystemMessage
from ..OpenAI import OpenAIInteractor

# set Open AI API Key
api_key = os.getenv('OPENAI_API_KEY')
assert api_key is not None and len(api_key) > 0, "API Key not set in environment"
openai.api_key = api_key

class Game:

    # Initialize a new Game object for each active game.
    def __init__(self):
        logger.debug("Initializing Game")
        self.renderer = Renderer()
        self.llm = OpenAIInteractor()

    def render(self):
        """
        This function is called when the game state changes.
        """
        logger.debug("Rendering game")

        return self.renderer.render(self.state)

    def start(self, name: str = None, model: str = None, system_message: str = None):
        """
        This function is called when the game starts.
        """
        logger.debug("Starting game")

        if name is None:
            name = randomish_words()
            logger.warning(f"No name provided. Using {name}.")

        self.state = StateManager(name, model, system_message, user_message = "Begin the game.")

        return None
    
    def submit(self, message: str = None):
        """
        This function is called when the user submits a message.
        """
        logger.debug(f"Submitting message: {message}")

        self.state.new_turn(message)
        self.render(self.state)
        return None

    def button(self, button:str=None):
        """
        This function is called when a button is pressed in the chatbot.
        """
        if button is None:
            logger.error("No button provided. Unable to process button.")
            return None

        logger.debug(f"Button pressed: {button}")

        if button == "start":
            return self.start
            self.render(self.state)
            return None
        elif button == "save":
            self.state.save
            self.render(self.state)
            return None
        elif button == "load":
            self.state.load
            self.render(self.state)
            return None
        elif button == "submit":
            self.state.submit
            self.render(self.state)
            return None
        elif button == "retry":
            self.state.retry
            self.render(self.state)
            return None
        elif button == "undo":
            self.state.undo
            self.render(self.state)
            return None
        elif button == "clear":
            self.state.clear
            self.render(self.state)
            return None