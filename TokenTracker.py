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
        # print("Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
    elif "gpt-4" in model:
        # print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
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

    def __add__(self, other):
        return LLMToken(
            self.prompt + other.prompt,
            self.completion + other.completion,
            self.total + other.total
            )

class TokenTracker:

    trackers = {}

    def __init__(self, model:str):
        if model not in AVAILABLE_MODELS:
            raise NotImplementedError(f"Model {model} not implemented.")
        if model in TokenTracker.trackers:
            raise NotImplementedError(f"Model {model} already has a token tracker.")

        self.model = model
        self.TPM = 0
        self.total_tokens = LLMToken(0,0,0)
        self.last_tokens = LLMToken(0,0,0)
        self.start_time = time.time()
        TokenTracker.trackers[model] = self

    def add(self, token:LLMToken):
        self.last_tokens = token
        self.total_tokens += token
        self.TPM = (self.total_tokens.total)/(time.time()-self.start_time)*60
        return self.total_tokens

    def add_from_stream(self, model:str, history:list, response:str):
        # Calculate streaming token usage
        encoding = tiktoken.encoding_for_model(model)
        prompt = num_tokens_from_messages(history, model=model)
        completion = len(encoding.encode(response))
        total = prompt + completion

        self.last_tokens = LLMToken(prompt, completion, total)
        self.add(self.last_tokens)
    
    def log_all_token_trackers():
        logger.info("----------------------------------------------------------")
        logger.info("----------------------------------------------------------")
        logger.info("             LOGGING ALL TOKEN TRACKERS")
        logger.info("----------------------------------------------------------")
        logger.info("----------------------------------------------------------")
        for model, tracker in TokenTracker.trackers.items():
            tracker.print()

    def print(self):
        logger.info(f"{self.model} | TPM: {round(self.TPM, 4)}")

        last = self.last_tokens
        logger.info(f"LAST  P:{last.prompt} | C:{last.completion} | T:{last.total}")

        total = self.total_tokens
        logger.info(f"TOTAL P:{total.prompt} | C:{total.completion} | T:{total.total}")
    
    # def to_json(self):
    #     return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
