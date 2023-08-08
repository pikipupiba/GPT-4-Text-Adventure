import os, json
from loguru import logger

data_folder = os.path.join(os.getcwd(), "data")
game_folder = os.path.join(data_folder, "game_files")
system_message_folder = os.path.join(data_folder, "system_messages")

    
import os
import json

class FileManager:
    DATA_DIR = os.path.join(os.getcwd(), "data")
    
    def __init__(self):
        if not os.path.exists(self.DATA_DIR):
            os.makedirs(self.DATA_DIR)
    
    def save(self, filename, data):
        with open(os.path.join(self.DATA_DIR, filename), "w") as file:
            json.dump(data, file)
    
    def load(self, filename):
        with open(os.path.join(self.DATA_DIR, filename), "r") as file:
            return json.load(file)