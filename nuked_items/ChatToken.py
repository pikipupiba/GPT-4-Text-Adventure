import time, json
import tiktoken

from loguru import logger

AVAILABLE_MODELS = [
    "gpt-4",
    "gpt-4-0314",
    "gpt-4-0613",
    "gpt-4-32k",
    "gpt-4-32k-0314",
    "gpt-4-32k-0613",
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-0301",
    "gpt-3.5-turbo-0613",
    "gpt-3.5-turbo-16k-0613",
    "text-davinci-003",
    "code-davinci-002",
]

def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613"):
    """Return the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model in {
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "gpt-4-0314",
        "gpt-4-32k-0314",
        "gpt-4-0613",
        "gpt-4-32k-0613",
        }:
        tokens_per_message = 3
        tokens_per_name = 1
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif "gpt-3.5-turbo" in model:
        print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
        return num_tokens_from_messages(messages, model="gpt-4-0613")
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens

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
        self.start_time = time.time()
        self.total_tokens = ChatToken(usage = {"prompt_tokens":0,"completion_tokens":0,"total_tokens":0})
        self.TPM = 0
        self.token_history = []

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

    def add_from_stream(self, model:str, history:list, response:str):
        # Calculate streaming token usage
        encoding = tiktoken.encoding_for_model(model)
        usage = {}
        usage["prompt_tokens"] = num_tokens_from_messages(history, model=model)
        usage["completion_tokens"] = len(encoding.encode(response))
        usage["total_tokens"] = usage["prompt_tokens"] + usage["completion_tokens"]
        self.add(ChatToken(usage))
        return usage


    def print(self, name):
        logger.info(f"Bot: {name} | {self.model} | {round(self.TPM, 4)} TPM")
        if self.token_history != []:
            current = self.token_history[-1]
            logger.info(f"LAST  P:{current.prompt_tokens} | C:{current.completion_tokens} | T:{current.total_tokens}")

        total = self.total_tokens
        logger.info(f"TOTAL P:{total.prompt_tokens} | C:{total.completion_tokens} | T:{total.total_tokens}")
    
    # def to_json(self):
    #     return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
