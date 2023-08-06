from loguru import logger

class LLMToken:

    def __init__(self, *args, **kwargs):
        if "usage" in kwargs:
            self.prompt = kwargs["usage"]["prompt_tokens"]
            self.completion = kwargs["usage"]["completion_tokens"]
            self.total = kwargs["usage"]["total_tokens"]
        else:
            self.prompt = args[0]
            self.completion = args[1]
            self.total = args[2]

        self.model = kwargs.get("model", None)

        self.get_cost()
        

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