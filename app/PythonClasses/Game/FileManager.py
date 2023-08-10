import os, json
from loguru import logger

from PythonClasses.Game.Turn import Turn
class FileManager:

    DATA_FOLDER = os.path.join(os.getcwd(), "data")
    HISTORY_FOLDER = os.path.join(os.getcwd(), "data", "history")
    SYSTEM_MESSAGE_FOLDER = os.path.join(os.getcwd(), "data", "system_message")
    EXAMPLE_HISTORY_FOLDER = os.path.join(os.getcwd(), "data", "example_history")

    def save_system_message(system_message_name: str):
        logger.info(f"Saving system message | {system_message_name}")
        FileManager.save_file(FileManager.SYSTEM_MESSAGE_FOLDER, f"{system_message_name}.txt")

    def load_system_message(system_message_name: str):
        logger.info(f"Loading system message | {system_message_name}")
        system_message = FileManager.load_file(FileManager.SYSTEM_MESSAGE_FOLDER, f"{system_message_name}.txt", default="")
        return system_message
    
    def save_history(history_name: str, history: list):
        logger.info(f"Saving history | {history_name}")
        history_dict_array = [turn.__dict__() for turn in history]
        FileManager.save_file(FileManager.HISTORY_FOLDER, f"{history_name}.json", history_dict_array)
    
    def load_history(history_name: str):
        logger.info(f"Loading history | {history_name}")
        history_dict_array = FileManager.load_file(FileManager.HISTORY_FOLDER, f"{history_name}.json", default=[])
        history = [Turn(turn) for turn in history_dict_array]
        return history
    
    def delete_history(history_name: str):
        if history_name is None: return
        logger.info(f"Deleting history | {history_name}")
        FileManager.delete_file(FileManager.HISTORY_FOLDER, f"{history_name}.json")

    def get_file_names(folder: str = None):
        return [file_name.split(".")[0] for file_name in os.listdir(folder) if file_name != ""]

    def build_path(folder: str, file_name: str):
        return os.path.abspath(os.path.join(folder, file_name))

    def load_file(folder: str, file_name: str, default = ""):

        if (folder is None) or (file_name is None):
            return default

        full_path = FileManager.build_path(folder, file_name)

        try:
            with open(full_path, "r") as f:
                file = f.read()
            try:
                return json.loads(file)
            except:
                return file
        except FileNotFoundError as e:
            logger.error(f"File not found: {e}")
            return default
        except IOError as e:
            logger.error(f"IOError: {e}")
            return default
        except json.decoder.JSONDecodeError as e:
            logger.error(f"JSONDecodeError: {e}")
            return default

    def save_file(folder: str, file_name: str, file_contents = ""):
        if (folder is None) or (file_name is None):
            return

        full_path = FileManager.build_path(folder, file_name)

        try:
            # create folder if it doesn't exist
            if not os.path.exists(folder):
                os.makedirs(folder)

            with open(full_path, "w") as f:
                if (file_name.split(".")[-1] == "json") and (type(file_contents) != str):
                    f.write(json.dumps(file_contents, indent=4))
                elif (file_name.split(".")[-1] == "txt") and (type(file_contents) == str):
                    f.write(file_contents)
        except IOError as e:
            logger.error(f"IOError: {e}")
        except json.decoder.JSONDecodeError as e:
            logger.error(f"JSONDecodeError: {e}")
        
    def delete_file(folder: str, file_name: str):

        if (folder is None) or (file_name is None):
            return

        full_path = FileManager.build_path(folder, file_name)

        try:
            os.remove(full_path)
        except FileNotFoundError as e:
            logger.error(f"{full_path} | File not found error: {e}")
        except IOError as e:
            logger.error(f"{full_path} | IOError: {e}")