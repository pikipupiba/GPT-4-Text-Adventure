from loguru import logger
from PythonClasses.LLM.LLMModel import LLMModel

class LLMToken:
# The `LLMToken` class is a Python class that represents a token in a language model. It has
# attributes such as `prompt`, `completion`, and `total` which represent the number of tokens in
# the prompt, completion, and the total number of tokens respectively.

    def __init__(self, *args, **kwargs):
        if "usage" in kwargs:
            self.prompt = kwargs["usage"]["prompt_tokens"]
            self.completion = kwargs["usage"]["completion_tokens"]
            self.total = kwargs["usage"]["total_tokens"]
        else:
            self.prompt = args[0]
            self.completion = args[1]
            if len(args) > 2:
                self.total = args[2]
            else:
                self.total = self.prompt + self.completion

        self.model = kwargs.get("model", None)

        self.calculate_cost()
        

    def __add__(self, other):
        logger.trace(f"Adding tokens from models {self.model} and {other.model}")
        if self.model != other.model:
            logger.error("Cannot add tokens from different models.")
            return None
        
        return LLMToken(
            self.prompt + other.prompt,
            self.completion + other.completion,
            self.total + other.total
            )
    
    def calculate_cost(self, model: LLMModel = None):
        if model is None:
            model = self.model

        
        return model.cost(self.total)