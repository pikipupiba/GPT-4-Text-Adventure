from typing import List
from datetime import datetime

from loguru import logger
from PythonClasses.LLM.LLMModel import LLMModel




class LilToken:
    def __init__(self, model: str, prompt: int = None, completion: int = None):
        self.model = LLMModel(model)

        self.prompt = prompt
        self.completion = completion

    def set(self, prompt: int = None, completion: int = None):
        if prompt is not None:
            self.prompt = prompt
        if completion is not None:
            self.completion = completion

    def tokens(self):
        return self.prompt, self.completion
    
    def total_tokens(self):
        return self.prompt + self.completion

    def cost(self):
        return self.model.cost(self.prompt, self.completion)
    
    def total_cost(self):
        prompt_cost, completion_cost = self.model.cost(self.prompt, self.completion)
        return prompt_cost + completion_cost

    def __add__(self, other):
        logger.trace(f"Adding tokens from models {self.model} and {other.model}")
        if self.model != other.model:
            logger.error("Cannot add tokens from different models.")
            return None
        
        return LilToken(
            self.model.name,
            self.prompt + other.prompt,
            self.completion + other.completion
        )

class TokenTracker:


    def __init__(self, model: str, prompt: int = None, completion: int = None):
        self.model = LLMModel(model)

        self.start = datetime.now()
        self.end = None

        # Total amounts of each token type
        self.tokens = LilToken(model, prompt, completion)

    
    def _rate(self):

        total_time = self.time["end"] - self.time["start"]
        total_tokens = self.tokens["prompt"] + self.tokens["completion"]
        total_cost = self.cost["prompt"] + self.cost["completion"]

        TPM = total_tokens / total_time.total_seconds() * 60
        CPM = total_cost / total_time.total_seconds() * 60

        return {
            "time": total_time,
            "tokens": total_tokens,
            "cost": total_cost,
            "TPM": TPM,
            "CPM": CPM,
        }

    def __add__(self, other):
        logger.trace(f"Adding tokens from models {self.model} and {other.model}")
        if self.model != other.model:
            logger.error("Cannot add tokens from different models.")
            return None
        
        return TokenTracker(
            self.prompt + other.prompt,
            self.completion + other.completion,
            self.total + other.total
        )
    
    def __stop__(self, prompt: int = None,  completion: int = None):
        if self.prompt is not None:
            self.tokens["prompt"] = prompt
        if self.completion is not None:
            self.tokens["completion"] = completion

        self.tokens["total"] = self.prompt + self.completion

        prompt_cost, completion_cost, total_cost  = LLMModel.get_cost(self.model, self.tokens["prompt"], self.tokens["completion"])

        self.cost["prompt"] = prompt_cost
        self.cost["completion"] = completion_cost
        self.cost["total"] = total_cost



        self.calculate_cost()
    
    def calculate_cost(self):
        
        self.model.
        
        return model.cost(self.total)