import datetime
from typing import List, Tuple, Dict

from loguru import logger

from PythonClasses.LLM.LilToken import LilToken
from PythonClasses.LLM.OpenAI import OpenAIModel
from PythonClasses.Game.ChatMessage import History, ChatMessage, SystemMessage, UserMessage

class Turn:
# The `Turn` class represents the state of a game turn. It includes attributes such as the
# model, user message, system message, type, display, raw, stats, combat, and execution. The
# class provides methods to initialize a turn object, check if it has stats, and convert the
# object to a dictionary.

    # def __init__(self, model: str = None, user_message = None, system_message: str = None, type: str = "normal"):
    def __init__(self, model: OpenAIModel, system: str, history: History):

        # Token tracker for each turn.
        self.model = model
        self.system_message = system_message
        self.chat_message = chat_message
        self.token_tracker = LilToken(model)


        

        # Fill in stats, combat, and execution after response

    def load(input_obj: dict):
        model_name = input_obj.get("model", None)
        messages = input_obj.get("messages", [None, None])
        system_message = input_obj.get("system_message", None)

        model = OpenAIModel[model_name]
        turn = Turn(model, system_message, messages)
        
        turn.type = input_obj.get("type", None)
        # ChatMessage is a List[List[List[str, str]]]
        # Outer list = list of all ChatMessage types
        # Middle list = list of ChatMessages of one history type
        # Inner list = list containing message pairs
        # OuterList[0] = Display
        # OuterList[1] = Raw (for context for api call)
        # OuterList[2] = Summary, if it exists
        # OuterList[3] = Stats, if it exists

        turn.histories = input_obj.get("history", None)
        turn.stats = input_obj.get("stats", {})
        turn.combat = input_obj.get("combat", [])
        turn.execution = input_obj.get("execution", Turn.DEFAULT_EXECUTION.copy())

        # Remove empty strings. We can handle None.
        for i in range(2):
            if turn.display[i] == "":
                turn.display[i] = None
            if turn.raw[i] == "":
                turn.raw[i] = None

    def has_stats(self):
        return (self.stats is not None) and (self.stats != {})
        

    def __dict__(self):
        return {
            "type": getattr(self, "type", ""),
            "model": getattr(self, "model", ""),
            "system_message": getattr(self, "system_message", ""),
            "display": getattr(self, "display", []),
            "raw": getattr(self, "raw", []),
            "stats": getattr(self, "stats", {}),
            "combat": getattr(self, "combat", []),
            "execution": getattr(self, "execution", Turn.DEFAULT_EXECUTION),
        }
    
    