import re
from enum import Enum, auto
from typing import List, Union, Optional, Tuple, Dict
from loguru import logger

from PythonClasses.LLM.OpenAI import OpenAIModel
from PythonClasses.Helpers.helpers import generate_dice_string, get_nth_or_value
from PythonClasses.LLM.LilToken import LilToken



class Role(Enum):
    USER = auto()
    ASSISTANT = auto()
    SYSTEM = auto()
    ANY = auto()

    def __repr__(self):
        return f"DisplayType.{self.name}"

class ChatMessage:
    def __init__(self, model, role: Role, content: List[str] = [""]):
        '''
        USER/ASSISTANT: [display, context, summary]
        SYSTEM: [system]
        '''
        self.role = role
        self.content = content

        if self.role == Role.USER or self.role == Role.ASSISTANT:
             content = content[:3] + [''] * (3 - len(content))
             # Context is king
             
        self.num_tokens = model.num_tokens(content[1] if len(content[1]) > 0 else content[0])
        
        self.combat = []
        self.stats = {}


    @property
    def display(self) -> Optional[str]:
        return self.content[0]
    @display.setter
    def display(self, content: str) -> None:
        self.content[0] = content
    @property
    def context(self) -> Optional[str]:
        return self.content[1]
    @context.setter
    def context(self, content: str) -> None:
        self.content[1] = content
    @property
    def summary(self) -> Optional[str]:
        return self.content[2]
    @summary.setter
    def summary(self, content: str) -> None:
        self.content[2] = content

    def __getitem__(self, key: int) -> str:
        return self.content[key]
    def __setitem__(self, key: int, content: str) -> None:
        self.content[key] = content

    @property
    def day_string(self) -> str:
        return self.content[3]