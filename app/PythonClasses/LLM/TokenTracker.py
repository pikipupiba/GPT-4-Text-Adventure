from datetime import datetime

from loguru import logger
from PythonClasses.LLM.LLMModel import LLMModel


class LilToken:
    def __init__(self, model: str, prompt: int = None, completion: int = None):
        self.model = LLMModel(model)

        if prompt is not None:
            self.prompt = prompt
        if completion is not None:
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
            self.completion + other.completion,
        )

    def __truediv__(self, number):
        return LilToken(self.model.name, self.prompt / number, self.completion / number)


class TokenTracker(LilToken):
    def __init__(
        self,
        model: str,
        prompt: int = None,
        completion: int = None,
        start: datetime = None,
        end: datetime = None,
    ):
        super().__init__(model, prompt, completion)

        if start is None:
            self.start = datetime.now()

        self.end = end

        self.tokens = LilToken(model, prompt, completion)

    def tpm(self):
        return self.tokens / self.elapsed_time()

    def __add__(self, other):
        if self.model != other.model:
            logger.error("Cannot add tokens from different models.")
            return None

        return TokenTracker(
            model=self.model.name,
            prompt=self.prompt + other.prompt,
            completion=self.completion + other.completion,
            start=min(self.start, other.start),
            end=max(self.end, other.end),
        )

    def stop(self):
        self.end = datetime.now()

    def elapsed_time(self):
        return self.end - self.start
