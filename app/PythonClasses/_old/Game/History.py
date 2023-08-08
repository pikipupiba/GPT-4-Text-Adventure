import os,json
from loguru import logger

from PythonClasses.Helpers.file_helpers import *
from PythonClasses.Helpers.randomish_words import *

from PythonClasses.Game.Turn import Turn
from PythonClasses.Game.SystemMessage import SystemMessage

class History:
    """
    This class is responsible for managing the game state, including loading, saving, undoing, clearing, and retrying game states.
    """

    def __init__(self, name: str = "", model: str = "gpt-3.5-turbo-0613", user_message: str = ""):
        """
        Initialize the StateManager.
        """
        logger.debug("Initializing StateManager")
        
        self.name = name
        self.game_file_path = os.path.join(game_folder, f"{self.name}_game_file.json")

        self.system_message = SystemMessage()
        self.turns = []

        self.turns.append(Turn(user_message, model, self.system_message.build_system_message()))

    def __dict__(self):

        return {
            "name": self.name,
            "game_file_path": self.game_file_path,
            "turns": [turn.__dict__() for turn in self.turns]
        }


    def change_name(self, new_name:str=None, keep_old:bool=True):

        logger.trace(f"Changing game name from {self.name} to {new_name}")

        old_name = self.game_file_path
        old_file_path = self.game_file_path

        if new_name is None:
            new_name = randomish_words()
            logger.warning(f"No system name provided. Using {new_name}.")
        
        self.name = new_name
        self.game_file_path = os.path.join(game_folder, f"{self.name}_game_file.json")

        # if not keep_old and not "error" in self.save_game():
        #     logger.debug(f"Deleting old game: {old_name}")
        #     self.delete_game(old_file_path)

        logger.trace(f"Successfully changed game name from {old_name} to {self.name}")

    
    def new_turn(self, user_message = None, model: str = None, type: str = "normal"):

        logger.debug(f"Adding new turn to game: {self.name} | Turn # {len(self.turns) + 1}")
        
        if model is None:
            model = self.turns[-1].model
        
        self.turns.append(Turn(user_message, model, self.system_message.build_system_message(), type))

        logger.trace(f"Successfully added new turn to game: {self.name} | Turn # {len(self.turns)}")

    
    def get_display_history(self):
        return [turn.display for turn in self.turns]
    
    def get_raw_history(self):
        return [turn.raw for turn in self.turns]

    def last_turn(self):
        return self.turns[-1]
    
    def last_stats(self):

        logger.trace(f"Getting last stats from game: {self.name}")

        # Stats are not guaranteed to be in every message, so we need to find the last one
        for turn in reversed(self.turns):
            if not hasattr(turn, "stats") or turn.stats is None:
                continue

            logger.trace(f"Successfully got last stats from game: {self.name}")

            return turn["stats"]

        logger.trace(f"No stats found in game: {self.name} | Returning None")

        return {}

    

    def undo(self):
        logger.debug("Attempting to undo last action in game")

        if not len(self.turns) > 0:
            logger.info("No history to undo. Leaving game state as is.")
            return None

        self.turns.pop()

        logger.trace("Successfully undid last action in game state")
        return None

    def retry(self):
        
        logger.debug("Attempting to retry last action in game state")

        self.last_turn().display[1] = None
        self.last_turn().raw[1] = None
        self.last_turn().stats = None
        self.last_turn().combat = None
        self.last_turn().tokens = None

        logger.trace("Successfully prepared for retry")
        return None