import json
import os

from loguru import logger
from PythonClasses.Game.Game import Game
from PythonClasses.Game.Turn import Turn


class FileManager:
    # The `FileManager` class is responsible for managing file operations such as saving, loading,
    # and deleting files. It provides methods for saving system messages, saving and loading game
    # history, and performing general file operations like getting file names, building file paths,
    # and deleting files. The class uses the `os` and `json` modules for file operations and the
    # `loguru` module for logging.

    DATA_FOLDER = os.path.join(os.getcwd(), "data")
    HISTORY_FOLDER = os.path.join(os.getcwd(), "data", "history")
    AUDIO_FOLDER = os.path.join(os.getcwd(), "data", "audio")
    SYSTEM_MESSAGE_FOLDER = os.path.join(os.getcwd(), "data", "system_message")
    EXAMPLE_HISTORY_FOLDER = os.path.join(os.getcwd(), "data", "example_history")

    @staticmethod
    def save_system_message(system_message_name: str, system_message: str):
        logger.info(f"Saving system message | {system_message_name}")
        FileManager.save_file(
            FileManager.SYSTEM_MESSAGE_FOLDER,
            f"{system_message_name}.txt",
            system_message,
        )

    @staticmethod
    def load_system_message(system_message_name: str):
        logger.info(f"Loading system message | {system_message_name}")
        system_message = FileManager.load_file(
            FileManager.SYSTEM_MESSAGE_FOLDER, f"{system_message_name}.txt", default=""
        )
        return system_message

    @staticmethod
    def save_history(game_name: str, history_name: str):
        logger.info(f"Saving history | {game_name} -> {history_name}")
        history_dict = Game._history_to_dict(game_name)
        for turn in history_dict[1:]:
            if hasattr(turn, "system_message"):
                del turn["system_message"]
        FileManager.save_file(
            FileManager.HISTORY_FOLDER,
            f"{history_name}.json",
            Game._history_to_dict(game_name),
        )

    @staticmethod
    def load_history(history_name: str):
        logger.info(f"Loading history | {history_name}")
        history_dict_array = FileManager.load_file(
            FileManager.HISTORY_FOLDER, f"{history_name}.json", default=[]
        )
        history = [Turn(turn) for turn in history_dict_array]
        return history

    @staticmethod
    def delete_history(history_name: str):
        if history_name is None:
            return
        logger.info(f"Deleting history | {history_name}")
        FileManager.delete_file(FileManager.HISTORY_FOLDER, f"{history_name}.json")

    @staticmethod
    def get_file_names(folder: str = None):
        return [
            file_name.split(".")[0]
            for file_name in os.listdir(folder)
            if file_name != ""
        ]

    @staticmethod
    def build_path(folder: str, file_name: str):
        return os.path.abspath(os.path.join(folder, file_name))

    @staticmethod
    def load_file(folder: str, file_name: str, default=""):
        if (folder is None) or (file_name is None):
            return default

        full_path = FileManager.build_path(folder, file_name)

        try:
            with open(full_path) as f:
                file = f.read()
            try:
                return json.loads(file)
            except Exception:
                return file
        except FileNotFoundError as e:
            logger.error(f"File not found: {e}")
            return default
        except OSError as e:
            logger.error(f"IOError: {e}")
            return default
        except json.decoder.JSONDecodeError as e:
            logger.error(f"JSONDecodeError: {e}")
            return default

    @staticmethod
    def save_file(folder: str, file_name: str, file_contents=""):
        if (folder is None) or (file_name is None):
            return

        full_path = FileManager.build_path(folder, file_name)

        try:
            # create folder if it doesn't exist
            if not os.path.exists(folder):
                os.makedirs(folder)

            with open(full_path, "w") as f:
                file_extension = file_name.split(".")[-1]
                if file_extension == "json" and not isinstance(file_contents, str):
                    f.write(json.dumps(file_contents, indent=4))
                elif file_extension == "txt" and isinstance(file_contents, str):
                    f.write(file_contents)

        except OSError as e:
            logger.error(f"IOError: {e}")
        except json.decoder.JSONDecodeError as e:
            logger.error(f"JSONDecodeError: {e}")

    @staticmethod
    def delete_file(folder: str, file_name: str):
        if (folder is None) or (file_name is None):
            return

        full_path = FileManager.build_path(folder, file_name)

        try:
            os.remove(full_path)
        except FileNotFoundError as e:
            logger.error(f"{full_path} | File not found error: {e}")
        except OSError as e:
            logger.error(f"{full_path} | IOError: {e}")
