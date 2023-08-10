import tiktoken
from loguru import logger

class LLMModel:
# The `LLMModel` class is a class for looking up information about language models (LLMs). It
# provides methods for getting the price of a specific LLM model, getting information about a
# specific LLM model, and calculating the number of tokens used by a string of text or a list of
# messages for a specific LLM model. The class also defines a list of available LLM models and
# their corresponding prices.
    # Class for looking up information about LLM models

    AVAILABLE_MODELS = [
        # GPT-3.5 Turbo
        "gpt-3.5-turbo",
        "gpt-3.5-turbo-0301",
        "gpt-3.5-turbo-0613",

        # GPT-3.5 Turbo 16k
        "gpt-3.5-turbo-16k",
        "gpt-3.5-turbo-16k-0301",
        "gpt-3.5-turbo-16k-0613",

        # GPT-4
        "gpt-4",
        "gpt-4-0314",
        "gpt-4-0613",
        
        # # GPT-4 32k models are not currently available
        # "gpt-4-32k",
        # "gpt-4-32k-0314",
        # "gpt-4-32k-0613",

        # # Not implemented yet
        # "text-davinci-003",
        # "code-davinci-002",
    ]

    prices = [
        {
            "models": ["gpt-3.5-turbo", "gpt-3.5-turbo-0301", "gpt-3.5-turbo-0613"],
            "prompt": 0.0000015,
            "completion": 0.000002,
        },
        {
            "models": ["gpt-3.5-turbo-16k", "gpt-3.5-turbo-16k-0301", "gpt-3.5-turbo-16k-0613"],
            "prompt": 0.000003,
            "completion": 0.000004,
        },
        {
            "models": ["gpt-4", "gpt-4-0314", "gpt-4-0613"],
            "prompt": 0.00003,
            "completion": 0.00006,
        },
        {
            "models": ["gpt-4-32k", "gpt-4-32k-0314", "gpt-4-32k-0613"],
            "prompt": 0.00006,
            "completion": 0.00012,
        },
    ]

    def get_price(model:str):

        logger.trace(f"Getting price for model {model}")

        for price in LLMModel.prices:
            if model in price["models"]:
                logger.trace(f"Found price for model {model}")
                return price
            
        logger.error(f"Model {model} not found in price list.")
        return None
    
    def get_model_info(model:str):
        logger.trace(f"Getting model info for model {model}")
        if model is None:
            logger.error("Model not specified.")
            return None
        if model not in LLMModel.AVAILABLE_MODELS:
            logger.error(f"Model {model} not implemented.")
            return None
        
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            print("Warning: model not found. Using cl100k_base encoding.")
            encoding = tiktoken.get_encoding("cl100k_base")

        # Set number of tokens used for message headers
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
            return LLMModel.get_model_info(model="gpt-3.5-turbo-0613")
        elif "gpt-4" in model:
            # print("Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613.")
            return LLMModel.get_model_info(model="gpt-4-0613")
        else:
            raise NotImplementedError(
                f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
            )
        
        logger.trace(f"Found model info for model {model}")
        
        return {
            "encoding": encoding,
            "tokens_per_message": tokens_per_message,
            "tokens_per_name": tokens_per_name,
        }
    
    def num_tokens_from_text(model:str = None, text:str = None):
        """Return the number of tokens used by a string of text."""
        logger.trace(f"Getting number of tokens from messages for model {model}")

        if text is None:
            logger.error("Text not specified.")
            return None

        encoding, tokens_per_message, tokens_per_name = LLMModel.get_model_info(model)

        if encoding is None:
            logger.error(f"Encoding not found for model {model}")
            return None

        num_tokens = len(encoding.encode(text))

        logger.trace(f"Found {num_tokens} tokens for model {model}")

        return num_tokens

    def num_tokens_from_messages(messages, model:str = None):
        """Return the number of tokens used by a list of messages."""

        logger.trace(f"Getting number of tokens from messages for model {model}")

        encoding, tokens_per_message, tokens_per_name = LLMModel.get_model_info(model)

        if None in (encoding, tokens_per_message, tokens_per_name):
            logger.error(f"Model info not found for model {model}")
            return None
        
        # Count tokens
        num_tokens = 0
        for message in messages:
            num_tokens += tokens_per_message
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":
                    num_tokens += tokens_per_name
        num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>

        logger.trace(f"Found {num_tokens} tokens for model {model}")
        return num_tokens