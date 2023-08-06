from typing import List

class SystemMessage:
    def __init__(self, parts: List[str] = None):

        self.parts = []
        return None
    
    def build_system_message(self, parts: List[str] = None):
        if parts is None:
            parts = self.parts

        system_message = ""
        for part in parts:
            system_message += part + "\n\n"

        return system_message