from datetime import datetime

from loguru import logger
from PythonClasses.LLM.LLMModel import LLMModel

class LilToken:
    def __init__(self, prompt: int = None, completion: int = None):
        self.prompt = prompt
        self.completion = completion

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

class TokenTracker:
# The `LLMToken` class is a Python class that represents a token in a language model. It has
# attributes such as `prompt`, `completion`, and `total` which represent the number of tokens in
# the prompt, completion, and the total number of tokens respectively.

    def __init__(self, model: str, prompt: int = None, completion: int = None):
        self.model = LLMModel(model)

        self.time = {
            "start": datetime.now(),
            "end": None,
            "elapsed": None,
        }

        # Total amounts of each token type
        self.tokens = {
            "prompt": prompt,
            "completion": completion,
        }
        self.cost = {
            "prompt": None,
            "completion": None,
        }
        self.tpm = {
            "prompt": None,
            "completion": None,
        }
        self.cpm = {
            "prompt": None,
            "completion": None,
        }


        
        if self.prompt and self.completion:
            self.total = self.prompt + self.completion

        self.calculate_cost()
    
    def total(self):

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
    
    def calculate_cost(self, model: LLMModel = None):
        if model is None:
            model = self.model

        
        return model.cost(self.total)