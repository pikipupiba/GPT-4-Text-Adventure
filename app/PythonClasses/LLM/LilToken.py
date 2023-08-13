# from __future__ import annotations
from typing import List
from datetime import datetime

from loguru import logger
# from PythonClasses.LLM.OpenAI import OpenAIModel

from PythonClasses.Helpers.helpers import min_max_or_none


class LilToken:
    def __init__(self, model, system: int = 0, history: int = 0, completion: int = 0, start: datetime = None, end: datetime = None):
        self.model = model
        self.system = system
        self.history = history
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
        return [self.system, self.history, self.completion]
    
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
    def total_tokens(self):
        return sum(self.tokens)
    
    @property
    def tpm(self):
        return self._values_per_minute(self.tokens)
    
    @property
    def cost(self):
        # Assuming the model has a cost method with the given signature
        system_cost = self.model.cost(["prompt", self.system])
        history_cost = self.model.cost(["prompt", self.history])
        completion_cost = self.model.cost(["completion", self.completion])
        return [system_cost, history_cost, completion_cost]
    
    @property
    def cpm(self):
        return self._values_per_minute(self.cost)
    
    @property
    def tpm_total(self):
        return self._values_per_minute([sum(self.tokens)])[0]
    
    @property
    def cpm_total(self):
        return self._values_per_minute([sum(self.cost)])[0]

    def _values_per_minute(self, values: List[int]) -> List[float]:
        return [value / self.elapsed_time * 60 for value in values]

    def __add__(self, other):
        if self.model.model_name != other.model.model_name:
            raise ValueError("Cannot add tokens from different models.")

        combined_start, combined_end = min_max_or_none(self.start, self.end, other.start, other.end)
        combined_system = (self.system or 0) + (other.system or 0)
        combined_history = (self.history or 0) + (other.history or 0)
        combined_completion = (self.completion or 0) + (other.completion or 0)

        return LilToken(
            model=self.model,
            system=combined_system,
            history=combined_history,
            completion=combined_completion,
            start=combined_start,
            end=combined_end
        )
    
class BiglyToken:

    def __init__(self, start: datetime = None, end: datetime = None):
        from PythonClasses.LLM.OpenAI import OpenAIModel

        self.start = datetime.now() if start is None else start
        self.end = end

        self.total_token_trackers = {model.model_name: LilToken(model) for model in OpenAIModel}
        self.lil_tokens = []

    def stop(self, end: datetime = None):
        self.end = datetime.now() if end is None else end
    
    @property
    def elapsed_time(self):
        self.end = self.end or datetime.now()
        return (self.end - self.start).total_seconds()
    
    @property
    def total_tokens(self):
        # return sum([lil_token.total_tokens for lil_token in self.lil_tokens])
        pass
    
    @property
    def total_tpm(self):
        # return self._values_per_minute([self.total_tokens])[0]
        pass

    @property
    def total_cpm(self):
        # return self._values_per_minute([self.total_cost])[0]
        pass

    @property
    def total_cost(self):
        # return sum([lil_token.cost for lil_token in self.lil_tokens])
        pass

    def _values_per_minute(self, values: List[int]) -> List[float]:
        return [value / self.elapsed_time * 60 for value in values]
    
    def add_lil_token(self, lil_token: LilToken):
        self.lil_tokens.append(lil_token)
        self.total_token_trackers[lil_token.model.model_name] += lil_token

    def __add__(self, other):
        if not isinstance(other, BiglyToken):
            raise ValueError("Cannot add tokens from different models.")

        combined_start, combined_end = min_max_or_none(self.start, self.end, other.start, other.end)

        combined_bigly_token = BiglyToken(start=combined_start, end=combined_end)
        combined_bigly_token.lil_tokens = self.lil_tokens + other.lil_tokens

        for model_name, lil_token in self.total_token_trackers.items():
            combined_bigly_token.total_token_trackers[model_name] = lil_token + other.total_token_trackers[model_name]

        return combined_bigly_token
    
    def __iadd__(self, other):
        if not isinstance(other, BiglyToken):
            raise ValueError("Cannot add tokens from different models.")

        self.lil_tokens += other.lil_tokens

        for model_name, lil_token in self.total_token_trackers.items():
            self.total_token_trackers[model_name] += other.total_token_trackers[model_name]

        return self