# from __future__ import annotations
from typing import List
from datetime import datetime

from loguru import logger
# from PythonClasses.LLM.OpenAI import OpenAIModel




class LilToken:
    def __init__(self, model: OpenAIModel, system: int = None, history: int = None, completion: int = None, start: datetime = None, end: datetime = None):
        self.model = model

        if system is not None:
            self.system = system
        if history is not None:
            self.history = history
        if completion is not None:
            self.completion = completion

        self.start = datetime.now() if start is None else start
        self.end = end

    def stop(self, end: datetime = None):
        self.end = datetime.now() if end is None else end
        return self

    @property
    def elapsed_time(self):
        self.end = self.end or datetime.now()
        return (self.end - self.start).total_seconds()
    
    @property
    def tokens(self):
        return (self.system, self.history, self.completion)
    
    @property
    def token_dict(self):
        return {
            "system": self.system,
            "history": self.history,
            "completion": self.completion
        }
    
    @property
    def prompt_tokens(self):
        return self.system + self.history
    
    @property
    def completion_tokens(self):
        return self.completion
    
    @property
    def total_tokens(self):
        return sum(self.tokens)
    
    @property
    def tpm(self):
        return (tokens / self.elapsed_time * 60 for tokens in self.tokens)
    
    @property
    def tpm_total(self):
        return sum(self.tpm)

    @property
    def cost(self):
        return self.model.cost(self.token_dict)
    
    @property
    def cpm(self):
        return (cost / self.elapsed_time * 60 for cost in self.cost)
    
    @property
    def cpm_total(self):
        return sum(self.cpm)


    def __add__(self, other):
        if self.model.name != other.model.name:
            logger.error("Cannot add tokens from different models.")
            return None

        return LilToken(
            model = self.model,
            system = self.system + other.system,
            history = self.history + other.history,
            completion = self.completion + other.completion,
            start = min(self.start, other.start),
            end = max(self.end, other.end)
        )