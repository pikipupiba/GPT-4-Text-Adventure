from loguru import logger
from PythonClasses.LLM.LLMModel import LLMModel

class LLMToken:
    """`LLMToken` is for tracking model token usage"""
    def __init__(self, *args, **kwargs):
        if "usage" in kwargs:
            self.prompt = kwargs["usage"]["prompt_tokens"]
            self.completion = kwargs["usage"]["completion_tokens"]
            self.total = kwargs["usage"]["total_tokens"]
        else:
            self.prompt = args[0]
            self.completion = args[1]
            self.total = args[2] if len(args) > 2 else self.prompt + self.completion
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
        """
        Calculates the cost using a given model or the default model if none is provided.
        
        :param model: an instance of the `LLMModel` class. It is an optional parameter 
        and has a default value of `None`. If no value is provided for `model`, the method will
        use the `self.model` attribute as the default value
        :type model: LLMModel
        :return: the cost calculated by the model.
        """
        if model is None:
            model = self.model
        return model.cost(self.total)
