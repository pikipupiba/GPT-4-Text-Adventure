import os, json
from loguru import logger

data_folder = os.path.join(os.getcwd(), "data")
game_folder = os.path.join(data_folder, "game_files")
system_message_folder = os.path.join(data_folder, "system_messages")

class FileManager:

    DATA_FOLDER = os.path.join(os.getcwd(), "data")

    def build_path(file_name: str = None, folder: str = None):
        if folder is None:
            return os.path.abspath(os.path.join(FileManager.DATA_FOLDER, file_name))
        else:
            return os.path.abspath(os.path.join(FileManager.DATA_FOLDER, folder, file_name))

    def load_file(file_name: str = None, folder: str = None):

        if file_name is None:
            return {}

        file_path = FileManager.build_path(file_name, folder)

        try:
            with open(file_path, "r") as f:
                file = f.read()
            return json.loads(file)
        except FileNotFoundError:
            logger.error(f"File not found")
            return {}
        except IOError as e:
            logger.error(f"IOError: {e}")
            return {}
        except json.decoder.JSONDecodeError as e:
            logger.error(f"JSONDecodeError: {e}")
            return {}

    def save_file(file_contents = None, file_name: str = None,  folder: str = None):
        if file_name is None:
            return

        if file_contents is None:
            logger.warning(f"File contents is *None*, saving empty file")
            file_contents = {}

        file_path = FileManager.build_path(file_name, folder)

        try:
            with open(file_path, "w") as f:
                f.write(json.dumps(file_contents, indent=4))
        except IOError as e:
            logger.error(f"IOError: {e}")
        except json.decoder.JSONDecodeError as e:
            logger.error(f"JSONDecodeError: {e}")
        
    def delete_file(file_name: str = None, folder: str = None):
        """
        Delete a file from a file path.

        Parameters:
        - file_path (str): The path to the file.

        Returns:
        - dict: An error message if the file could not be deleted, otherwise None.
        """
        if file_path is None:
            logger.error(f"No file_path provided. Unable to delete file.")
            return

        file_path = FileManager.build_path(file_name, folder)

        try:
            os.remove(file_path)
        except FileNotFoundError:
            logger.error(f"{file_name} | File not found")
        except IOError as e:
            logger.error(f"{file_name} | IOError: {e}")