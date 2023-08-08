import os, json
from loguru import logger

data_folder = os.path.join(os.getcwd(), "data")
game_folder = os.path.join(data_folder, "game_files")
system_message_folder = os.path.join(data_folder, "system_messages")

class FileManager:
    def __init__(self):

        pass

    def load_game(self, new_name: str = None):

        if new_name is None:
            logger.warning(f"No game name provided. Unable to load game.")
            return {"error": "No game name provided. Unable to load game."}

        logger.trace(f"Attempting to load game: {new_name}")

        game_file_path = os.path.join(game_folder, f"{new_name}_game_file.json")
        game_data = json.loads(load_file(self.game_file_path, "Load Game"))

        if "error" in game_data:
            logger.error(f"Error loading game: {game_file_path}")
            return game_data

        self.name = game_data["name"]
        if game_file_path is not None:
            self.game_file_path = game_file_path
        self.turns = [Turn(turn) for turn in game_data["turns"]]

        logger.info(f"Successfully loaded game {self.game_file_path}")

        return None
            
    def save_game(self):

        logger.trace(f"Attempting to save game: {self.name}")

        # game_file_path = os.path.join(game_folder, f"{self.name}_game_file.json")

        result = save_file(self.game_file_path, json.dumps(self.__dict__(), indent=4), "Save Game")

        if "error" in result:
            logger.error(f"Error saving game: {self.game_file_path}")
            return result
        
    def delete_game(self):
            
        logger.trace(f"Attempting to delete game: {self.name}")

        # game_file_path = os.path.join(game_folder, f"{self.name}_game_file.json")

        result = delete_file(self.game_file_path, "Delete Game")

        if "error" in result:
            logger.error(f"Error deleting game: {self.name}")
            return result



def load_file(file_path: str = None, log: str = None) -> str:
    """
    Load a file from a file path.

    Parameters:
    - file_path (str): The path to the file.

    Returns:
    - str: The contents of the file.
    """
    if file_path is None:
        logger.error(f"LOAD FILE: {log} | None | No file_path provided. Unable to load file.")
        return {"error": f"LOAD FILE: {log} | None | No file_path provided. Unable to load file."}

    log_string = f"LOAD FILE: {log} | {file_path}"
    logger.trace(log_string)

    file_path = os.path.abspath(file_path)

    try:
        with open(file_path, "r") as f:
            file = f.read()
        logger.trace(f"{log_string} | Successfully loaded file")
        return file
    except FileNotFoundError:
        logger.error(f"{log_string} | File not found")
        return {"error": f"{log_string} | File not found"}
    except IOError as e:
        logger.error(f"{log_string} | IOError: {e}")
        return {"error": f"{log_string} | IOError: {e}"}

def save_file(file_path: str = None, file_contents: str = None, log: str = None):
    """
    Save a file to a file path.

    Parameters:
    - file_path (str): The path to the file.
    - file_contents (str): The contents of the file.

    Returns:
    - dict: An error message if the file could not be saved, otherwise None.
    """
    if file_path is None:
        logger.error(f"SAVE FILE: {log} | None | No file_path provided. Unable to load file.")
        return {"error": f"SAVE FILE: {log} | None | No file_path provided. Unable to load file."}

    log_string = f"SAVE FILE: {log} | {file_path}"
    logger.trace(log_string)

    if file_contents is None:
        logger.warning(f"{log_string} | Saving empty file")
        file_contents = ""

    file_path = os.path.abspath(file_path)

    try:
        with open(file_path, "w") as f:
            f.write(file_contents)
        logger.trace(f"{log} | {file_path} | Successfully saved file")
        return {}
    except IOError as e:
        logger.error(f"{log} | {file_path} | IOError: {e}")
        return {"error": f"{log} | IOError: {e}"}
    
def delete_file(file_path: str = None, log: str = None):
    """
    Delete a file from a file path.

    Parameters:
    - file_path (str): The path to the file.

    Returns:
    - dict: An error message if the file could not be deleted, otherwise None.
    """
    if file_path is None:
        logger.error(f"DELETE FILE: {log} | None | No file_path provided. Unable to delete file.")
        return {"error": f"DELETE FILE: {log} | None | No file_path provided. Unable to delete file."}
    
    log_string = f"DELETE FILE: {log} | {file_path}"
    logger.trace(log_string)

    file_path = os.path.abspath(file_path)

    try:
        os.remove(file_path)
        logger.trace(f"{log_string} | Successfully deleted file")
        return {}
    except FileNotFoundError:
        logger.error(f"{log_string} | File not found")
        return {"error": f"{log_string} | File not found"}
    except IOError as e:
        logger.error(f"{log_string} | IOError: {e}")
        return {"error": f"{log_string} | IOError: {e}"}