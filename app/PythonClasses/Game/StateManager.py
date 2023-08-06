import os,json,uuid,array
from typing import List, Tuple
from loguru import logger

from ..Helpers import file_helpers, randomish_words

from Turn import Turn

class GameStateManager:
    """
    This class is responsible for managing the game state, including loading, saving, undoing, clearing, and retrying game states.
    """

    def __init__(self, name: str = None, model: str = None, system_message: str = None, user_message: str = None):
        """
        Initialize the GameStateManager.
        """
        logger.debug("Initializing GameStateManager")
        
        self.name = name
        self.game_file_path = os.path.join("sessions", "game_files", f"{name}_game_file.json")
        self.turns = array.array("Turn", [])

        self.turns.append(Turn(user_message, model, system_message))


    def change_name(self, new_name:str=None, keep_old:bool=True):

        old_name = self.game_file_path

        if new_name is None:
            new_name = randomish_words()
            logger.warning(f"No name provided. Using {new_name}.")
        
        self.name = new_name
        self.game_file_path = os.path.join("sessions", "game_files", f"{self.name}_game_file.json")

        if not keep_old and not "error" in self.save_game():
            self.delete_game(old_name)

    
    def new_turn(self, user_message = None, model: str = None, system_message: str = None, type: str = "normal"):
        
        if model is None:
            model = self.turns[-1].model
        if system_message is None:
            system_message = self.turns[-1].system
        
        self.turns.append(Turn(user_message, model, system_message, type))

        return None
    
    def get_display_history(self):
        return [turn.display for turn in self.turns]
    
    def get_raw_history(self):
        return [turn.raw for turn in self.turns]

    def get_last_turn(self):
        return self.turns[-1]
    
    def last_stats(self):
        # Stats are not guaranteed to be in every message, so we need to find the last one
        for turn in reversed(self.turns):
            if not "stats" in turn:
                continue

            return turn["stats"]

    def load_game(self, game_file_path: str = None):

        logger.debug(f"Attempting to load game: {game_file_path}")

        game_data = file_helpers.load_file(game_file_path, "Load Game")

        if "error" in game_data:
            logger.error(f"Error loading game: {game_file_path}")
            return game_data

        self.name = game_data.name
        self.game_file_path = game_file_path
        self.turns = [Turn(turn) for turn in game_data.turns]

        logger.info(f"Successfully loaded game {self.game_file_path}")

        return None
            
    def save_game(self):

        logger.debug(f"Attempting to save game: {self.game_file_path}")

        result = file_helpers.save_file(self.game_file_path, self, "Save Game")

        if "error" in result:
            logger.error(f"Error saving game: {self.game_file_path}")
            return result
        
    def delete_game(self, game_file_path: str = None):
            
        logger.debug(f"Attempting to delete game: {game_file_path}")

        result = file_helpers.delete_file(game_file_path, "Delete Game")

        if "error" in result:
            logger.error(f"Error deleting game: {game_file_path}")
            return result

    def undo(self):
        logger.debug("Attempting to undo last action in game")

        if not len(self.turns) > 0:
            logger.info("No history to undo. Leaving game state as is.")
            return None

        self.turns.pop()

        logger.trace("Successfully undid last action in game state")
        return None

    def clear(self):
        logger.debug("Clearing game state")

        self.turns = []

        logger.trace("Successfully cleared game state")
        return None

    def retry(self):
        
        logger.debug("Attempting to retry last action in game state")

        self.turns[-1].display[1] = None
        self.turns[-1].raw[1] = None
        self.turns[-1].stats = None
        self.turns[-1].combat = None
        self.turns[-1].tokens = None

        logger.trace("Successfully prepared for retry")
        return None