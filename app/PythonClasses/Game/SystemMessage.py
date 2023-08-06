import os,json,re
from typing import List
from loguru import logger

from ..Helpers import file_helpers, randomish_words

from ...Schemas import schema_strings

class SystemMessage:
    def __init__(self, name, system_message: str = None):
        self.system_message = system_message
        self.system_message_file_path = os.path.join("sessions", "system_messages", f"{name}_system_message.txt")
        self.parts = []
    
    def message_to_parts(self):
        pass
    
    def build_system_message(self, new_system_message: str = None):
        # if self.parts is None:
        #     self.parts = []

        # system_message = ""
        # for part in self.parts:
        #     system_message += part + "\n\n"

        if new_system_message is not None:
            self.system_message = new_system_message

        # Function to replace matched pattern with schema string
        def replacer(match):
            schema_name = match.group(1)  # Extract the schema_name from the matched pattern
            return schema_strings.get(schema_name, match.group(0))  # Return variable value or original if not found
        
        # /*\schema_name*/\  # Pattern to match schema placeholders
        schema_matcher = re.compile(r'/\*\\(.*?)\*/\\')  # Compile regex pattern to match schema placeholders

        # Replace schema placeholders with schema strings in system message
        complete_system_message = re.sub(schema_matcher, replacer, self.system_message)

        return complete_system_message
    
    def save_system_message(self, file_name, system_message):
        logger.debug(f"Saving '{file_name}.txt' SYSTEM message!")

        try:
            session_file_path = os.path.join("sessions", "system_messages", f"{self.system_message_file_path}.txt")

            with open(session_file_path, "w") as f:
                f.write(system_message)
        except IOError as e:
            print(f"Error: {e}")

    def load_system_message(self, file_name, mode: str = "Overwrite"):

        logger.debug(f"Attempting to load system message: {self.game_file_path}")

        result = file_helpers.load_file(self.system_message_file_path, "Load System Message")

        if "error" in result:
            logger.error(f"Error saving game: {self.system_message_file_path}")
            return result

        if mode == "Overwrite":
            self.system_message = result
        elif mode == "Prepend":
            self.system_message = result + "/n/n" + self.system_message
        elif mode == "Append":
            self.system_message = self.system_message + "/n/n" + result

        return None

def save_current_example_history(example_history):
    logger.debug("Saving CURRENT EXAMPLE HISTORY!")
    session_file_path = os.path.join("sessions", "current", "example_history.json")

    try:
        with open(session_file_path, "w") as f:
            f.write(example_history)
    except IOError as e:
        print(f"Error: {e}")

def load_current_example_history():
    logger.debug("Loading CURRENT EXAMPLE HISTORY!")

    try:
        session_file_path = os.path.join("sessions", "current", "example_history.json")

        with open(session_file_path, "r") as f:
            example_history = f.read()
    except FileNotFoundError:
        print(f"Error: File '{session_file_path}' not found. Creating.")
        example_history = []
        save_current_example_history(example_history)
    except IOError as e:
        print(f"Error: {e}")
        example_history = []

    return example_history