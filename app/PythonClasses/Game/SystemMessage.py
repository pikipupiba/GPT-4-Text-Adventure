import os,json,re
from typing import List
from loguru import logger

from PythonClasses.Helpers.file_helpers import *
from PythonClasses.Helpers.randomish_words import *

from PythonClasses.Schemas import schema_strings

class SystemMessage:
    def __init__(self, name: str = None, system_message: str = None):
        logger.debug("Initializing SystemMessage")

        self.name = name
        self.system_message = system_message
        self.system_message_file_path = os.path.abspath(os.path.join(os.getcwd(), "data", "system_messages", f"{self.name}_system_message.txt"))
        # self.parts = []

        logger.debug(f"Successfully initialized SystemMessage: {self.name}")
    

    def message_to_parts(self):
        pass

    def update_system_message(self, new_system_message: str = None):

        self.system_message = new_system_message

    def update_example_history(self, new_example_history: str = None):

        self.example_history = json.loads(new_example_history)
    
    
    def change_name(self, new_name:str=None, keep_old:bool=True):
        logger.debug(f"Changing system message name from {self.name} to {new_name}")

        old_name = self.name
        old_file_path = self.system_message_file_path

        if new_name is None:
            new_name = randomish_words()
            logger.warning(f"No system name provided. Using {new_name}.")
        
        self.name = new_name
        self.system_message_file_path = os.path.abspath(os.path.join(os.getcwd(), "data", "system_messages", f"{self.name}_system_message.txt"))

        # if not keep_old and not "error" in self.save_system_message():
        #     logger.debug(f"Deleting old system message: {old_file_path}")
        #     self.delete_system_message(old_file_path)

        logger.trace(f"Successfully changed system message name from {old_name} to {self.name}")


    def build_system_message(self):

        logger.debug(f"Building system message: {self.name}")

        # if self.parts is None:
        #     self.parts = []

        # system_message = ""
        # for part in self.parts:
        #     system_message += part + "\n\n"

        # Function to replace matched pattern with schema string
        num_found_schemas = 0
        def replacer(match):
            num_found_schemas += 1
            schema_name = match.group(1)  # Extract the schema_name from the matched pattern
            return schema_strings.get(schema_name, match.group(0))  # Return variable value or original if not found
        
        # /*\schema_name*/\  # Pattern to match schema placeholders
        schema_matcher = re.compile(r'/\*\\(.*?)\*/\\')  # Compile regex pattern to match schema placeholders

        # Replace schema placeholders with schema strings in system message
        complete_system_message = re.sub(schema_matcher, replacer, self.system_message)

        logger.trace(f"Successfully built system message: {self.name} | Replaced {num_found_schemas} schema placeholders")

        return complete_system_message
    

    def save_system_message(self):

        logger.debug(f"Attempting to save the system message: {self.system_message_file_path}")

        result = save_file(self.system_message_file_path, self.system_message, "Save System Message")

        if "error" in result:
            logger.error(f"Error saving system message: {self.system_message_file_path}")
            return result

        logger.trace(f"Successfully saved system message: {self.system_message_file_path}")


    def load_system_message(self, mode: str = "Overwrite"):

        logger.debug(f"Attempting to load system message: {self.system_message_file_path}")

        result = load_file(self.system_message_file_path, "Load System Message")

        if "error" in result:
            logger.error(f"Error loading system message: {self.system_message_file_path}")
            return result

        if mode == "Overwrite":
            self.system_message = result
        elif mode == "Prepend":
            self.system_message = result + "/n/n" + self.system_message
        elif mode == "Append":
            self.system_message = self.system_message + "/n/n" + result

        logger.trace(f"Successfully loaded system message: {self.system_message_file_path}")

        return self.system_message
    
    def delete_system_message(self, system_message_file_path: str = None):

        logger.debug(f"Attempting to delete system message: {system_message_file_path}")

        if system_message_file_path is None:
            system_message_file_path = self.system_message_file_path

        result = delete_file(system_message_file_path, "Delete System Message")

        if "error" in result:
            logger.error(f"Error deleting system message: {system_message_file_path}")
            return result

        logger.trace(f"Successfully deleted system message: {system_message_file_path}")

    # def save_current_example_history(example_history):
    #     logger.debug("Saving CURRENT EXAMPLE HISTORY!")
    #     session_file_path = os.path.join("sessions", "current", "example_history.json")

    #     try:
    #         with open(session_file_path, "w") as f:
    #             f.write(example_history)
    #     except IOError as e:
    #         print(f"Error: {e}")

    # def load_current_example_history():
    #     logger.debug("Loading CURRENT EXAMPLE HISTORY!")

    #     try:
    #         session_file_path = os.path.join("sessions", "current", "example_history.json")

    #         with open(session_file_path, "r") as f:
    #             example_history = f.read()
    #     except FileNotFoundError:
    #         print(f"Error: File '{session_file_path}' not found. Creating.")
    #         example_history = []
    #         save_current_example_history(example_history)
    #     except IOError as e:
    #         print(f"Error: {e}")
    #         example_history = []

    #     return example_history