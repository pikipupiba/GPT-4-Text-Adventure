import time, json
from loguru import logger

AVAILABLE_MODELS = [
    "gpt-4",
    "gpt-4-0314",
    "gpt-4-32k",
    "gpt-4-32k-0314",
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-0301",
    "text-davinci-003",
    "code-davinci-002",
]

class ChatToken:

    def __init__(self, usage):
        self.prompt_tokens = usage["prompt_tokens"]
        self.completion_tokens = usage["completion_tokens"]
        self.total_tokens = usage["total_tokens"]

    def __add__(self, other):
        return ChatToken(usage = {
            "prompt_tokens": self.prompt_tokens + other.prompt_tokens,
            "completion_tokens": self.completion_tokens + other.completion_tokens,
            "total_tokens": self.total_tokens + other.total_tokens})

class ChatTokenCounter:
    def __init__(self, model:str):
        self.model = model
        self.token_history = []
        self.total_tokens = ChatToken(usage = {"prompt_tokens":0,"completion_tokens":0,"total_tokens":0})
        self.start_time = time.time()
        self.TPM = 0

    # def __repr__(self):
    #     return f"ChatTokenCounter({self.model},{self.token_history},{self.total_tokens},{self.start_time},{self.TPM})"

    # def __dict__(self):
    #     return self.to_json()
        # return {"model": self.model, "token_history":self.token_history,"total_tokens":self.total_tokens,"start_time":self.start_time,"TPM":self.TPM}

    def __add__(self, other):
        total = ChatTokenCounter(model = self.model)
        total.total_tokens += self.total_tokens
        total.total_tokens += other.total_tokens
        return total

    def add(self, token:ChatToken):
        self.token_history.append(token)
        self.total_tokens += token
        self.TPM = (self.total_tokens.total_tokens)/(time.time()-self.start_time)*60

    def print(self, name):
        if self.token_history != []:
            current = self.token_history[-1]
            logger.info(f"Bot: {name} | Model: {self.model} | Prompt: {current.prompt_tokens} | Completion: {current.completion_tokens} | Total: {current.total_tokens}")

        total = self.total_tokens
        logger.info(f"TPM: {self.TPM} | Prompt: {total.prompt_tokens} | Completion: {total.completion_tokens} | Total: {total.total_tokens}")
    
    # def to_json(self):
    #     return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
