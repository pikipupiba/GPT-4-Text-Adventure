from typing import List, Tuple, Dict

from loguru import logger

class Turn:
    """
    This class represents the state of a game, including the message, history, raw history, stats, combat, and team name.
    """

    # defaults = {
    #     "type": None,           # enum ["normal", "example", "debug"]
    #     "model": None,          # string
    #     "system": None,         # string (full system message or None if unchanged)
    #     "display": None,        # tuple (string, string)
    #     "raw": None,            # tuple (string, string)
    #     "stats": None,          # dict
    #     "combat": None,         # array of dicts
    #     "execution":
    #     {  
    #         "model": None,
    #         "time": {
    #             "start": None,      # datetime
    #             "end": None,        # datetime
    #             "elapsed": None,    # HH:MM:SS
    #         },
    #         "tokens": {
    #             "prompt": {
    #                 "system": None,
    #                 "history": None,
    #                 "user": None,
    #                 "total": None,
    #             },
    #             "completion": None,
    #             "total": None,
    #         },
    #         "cost": {
    #             "prompt": {
    #                 "system": None,
    #                 "history": None,
    #                 "user": None,
    #                 "total": None,
    #             },
    #             "completion": None,
    #             "total": None,
    #         },
    #     },
    # }

    def __init__(self, user_message = None, model: str = None, system_message: str = None, type: str = "normal"):

        self.model = model
        self.system = system_message
        self.type = type

        if self.type == "normal":
            # Normal turn usually takes 2 messages. Shows one thing, does another.
            # For adding dice rolls and such to user messages.
            if isinstance(user_message, tuple):
                self.display = (user_message[0], None)
                self.raw = (user_message[1], None)
            elif isinstance(user_message, str):
                self.display = (user_message, None)
                self.raw = (user_message, None)
            else:
                logger.warning(f"User message is neither tuple or string. Setting to None.")
                self.display = None
                self.raw = None
        elif self.type == "example":
            # Example turn requires 1 message. Shows nothing but affects raw history.
            self.display = None
            self.raw = (user_message, None)
        elif self.type == "debug":
            # Debug turn requires 1 message. Shows something but does not affect raw history.
            self.display = (user_message, None)
            self.raw = None

        # Fill in stats, combat, and execution after response
        

    def __dict__(self):
        return {
            "type": self.type,
            "model": self.model,
            "system": self.system,
            "display": self.display,
            "raw": self.raw,
            "stats": self.stats,
            "combat": self.combat,
            "execution": self.execution,
        }
    
    