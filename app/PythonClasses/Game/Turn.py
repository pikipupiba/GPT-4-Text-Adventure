from typing import List, Tuple, Dict

from loguru import logger

class Turn:
    """
    This class represents the state of a game, including the message, history, raw history, stats, combat, and team name.
    """

    # defaults = {
    #     "type": None,           # enum ["normal", "example", "debug"]
    #     "model": None,          # string
    #     "system_message": None,         # string (full system message or None if unchanged)
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

    # def __init__(self, model: str = None, user_message = None, system_message: str = None, type: str = "normal"):
    def __init__(self, load_obj, *args):

        if load_obj != {}:
            for key, value in load_obj.items():
                setattr(self, key, value)
            return

        if len(args) == 3:
            self.model = args[0]
            self.user_message = args[1]
            self.system_message = args[2]
            self.type = "normal"

        if len(args) == 4:
            self.model = args[0]
            self.user_message = args[1]
            self.system_message = args[2]
            self.type = args[3]

        if self.type == "normal":
            # Normal turn usually takes 2 messages. Shows one thing, does another.
            # For adding dice rolls and such to user messages.
            if isinstance(self.user_message, tuple):
                self.display = [self.user_message[0], None]
                self.raw = [self.user_message[1], None]
            elif isinstance(self.user_message, str):
                self.display = [self.user_message, None]
                self.raw = [self.user_message, None]
            else:
                logger.warning(f"User message is neither tuple or string. Setting to (None, None).")
                self.display = [None, None]
                self.raw = [None, None]
        elif self.type == "example":
            # Example turn requires 1 message. Shows nothing but affects raw history.
            self.display = [None, None]
            self.raw = [self.user_message, None]
        elif self.type == "debug":
            # Debug turn requires 1 message. Shows something but does not affect raw history.
            self.display = [self.user_message, None]
            self.raw = [None, None]

        self.stats = {}
        self.combat = []
        self.execution = {}
        # Fill in stats, combat, and execution after response
        

    def __dict__(self):
        return {
            "type": getattr(self, "type", ""),
            "model": getattr(self, "model", ""),
            "system_message": getattr(self, "system_message", ""),
            "display": getattr(self, "display", []),
            "raw": getattr(self, "raw", []),
            "stats": getattr(self, "stats", {}),
            "combat": getattr(self, "combat", []),
            "execution": getattr(self, "execution", {}),
        }
    
    