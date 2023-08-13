from typing import List, Union
from enum import Enum

import openai
# from reliablegpt import reliableGPT
import tiktoken

from loguru import logger

from PythonClasses.LLM.openai_helpers import build_openai_history, build_openai_system_message
from PythonClasses.Game.ChatMessage import HistoryFilter, History, ChatMessage

class OpenAIModel(Enum):
    '''Enum for model types.'''
    # ----------------- | Model Name         | Model Version           | Token Max  | Prompt Price | Completion Price | TPM Max |
    GPT_3_5_TURBO =     ( "GPT_3_5_TURBO"    , "gpt-3.5-turbo-0613"    , 4096       , 0.0000015    , 0.000002         ,  90000  )
    GPT_3_5_TURBO_16k = ( "GPT_3_5_TURBO_16k", "gpt-3.5-turbo-16k-0613", 16384      , 0.000003     , 0.000004         , 180000  )
    GPT_4 =             ( "GPT_4"            , "gpt-4-0613"            , 8192       , 0.00003      , 0.00006          ,  40000  )
    GPT_4_32k =         ( "GPT_4_32k"        , "gpt-4-32k-0613"        , 32768      , 0.00006      , 0.00012          ,      0  )

    def __init__(self, model_name, model_version, max_tokens, prompt_price, completion_price, tpm_max):
        self.model_name = model_name
        self.model_version = model_version
        self.max_tokens = max_tokens
        self.prompt_price = prompt_price
        self.completion_price = completion_price
        self.tpm_max = tpm_max
        # Define all attribute in initialization
        self.price = {
            "prompt": self.prompt_price,
            "completion": self.completion_price,
        }
        try:
            self.encoding = tiktoken.encoding_for_model(self.model_name)
        except KeyError:
            logger.warning(f"Model {self.model_name} not found. Using cl100k_base encoding.")
            self.encode = tiktoken.get_encoding("cl100k_base").encode
        self.tokens_per_message = 3
        self.tokens_per_name = 1
        self.tokens_per_response = 3

    def __str__(self):
        return self.model_name

    def cost(self, input: Union[str, list, tuple, dict, ChatMessage, History, HistoryFilter] = None, type: str = None):
        '''
        Needs a tuple with (type, messages)
        type = either "prompt" or "completion"
        messages = any nested list or tuple of strings
        returns a tuple in the same order as the input
        '''
        if input is None:
            logger.warning("Cost | input == None | Returning 0.")
            return 0

        # Handling ChatMessage
        if isinstance(input, ChatMessage):
            return (self.num_tokens(input.context) if input.context else 0) * self.price[type]

        # Handling History
        if isinstance(input, History):
            return sum(self.num_tokens(message.context) for message in input.messages) * self.price[type]

        # Handling HistoryFilter
        if isinstance(input, HistoryFilter):
            return sum(self.num_tokens(item['content']) for item in input.context_history()) * self.price[type]

        if isinstance(input, dict):
            cost_dict = {key: self.cost(value) for key, value in input.items()}
            total = 0
            for val in cost_dict.values():
                if isinstance(val, (int, float)):
                    total += val
                elif val is not None:
                    total += sum(item for item in val if item is not None)
            cost_dict["total"] = total
            return cost_dict

        if input[0] == "prompt" or input[0] == "completion":
            return self.num_tokens(input) * self.price[input[0]]

        if isinstance(input, list) or isinstance(input, tuple):
            return sum(self.cost(message) if self.cost(message) is not None else 0 for message in input)
        
    def total_cost(self, input: Union[str, list, tuple, ChatMessage, History, HistoryFilter] = None):
        '''
        Needs a tuple with (type, messages)
        type = either "prompt" or "completion"
        messages = any nested list of strings
        returns a tuple in the same order as the input
        '''
        # Handling ChatMessage
        if isinstance(input, ChatMessage):
            return self.num_tokens(input.context) * self.price[type]

        # Handling History
        if isinstance(input, History):
            return sum(self.num_tokens(message.context) for message in input.messages) * self.price[type]

        # Handling HistoryFilter
        if isinstance(input, HistoryFilter):
            return sum(self.num_tokens(item['content']) for item in input.context_history()) * self.price[type]

        if isinstance(input, tuple):
            type = input[0]
            return self.num_tokens(input) * self.price[type]

        if isinstance(input, list):
            return sum(self.cost(message) for message in input)
    
    def encode(self, input: Union[str, ChatMessage, List[str], History, HistoryFilter] = None):
        """Return the number of tokens used by a string of text."""
        if input is None:
            logger.warning("Tokenize | input == None | Returning 0.")
            return 0

        # Handling ChatMessage
        if isinstance(input, ChatMessage):
            return self.encoding.encode(input.context) if input.context else []

        # Handling History or HistoryFilter
        elif isinstance(input, (History, HistoryFilter)):
            # Using context_history to get the most recent history content for encoding
            messages = [message["content"] for message in input.context_history()]
            return [self.encode(message) for message in messages] if len(messages) > 0 else []

        elif isinstance(input, str):
            return self.encoding.encode(input)

        elif isinstance(input, list):
            # Recursively encode arrays of messages
            return [self.encode(message) for message in input]

        else:
            return []

    def num_tokens(self, input: Union[str, list, ChatMessage, History, HistoryFilter] = None):
        """Return the number of tokens used by a string of text."""
        token_array = self.encode(input)

        if isinstance(token_array[0], int):
            return len(token_array) + self.tokens_per_message
        if isinstance(token_array[0], list) or isinstance(token_array[0], tuple):
            # Recursively sum arrays of tokens
            return sum([self.num_tokens(message) for message in token_array]) + self.tokens_per_response


class OpenAIInterface:


    def __init__(self):
        from PythonClasses.LLM.LilToken import LilToken
        # Token trackers for each game.
        self.token_trackers = {model.model_name: LilToken(model) for model in OpenAIModel}



    
    def oneshot(system_message: str, user_message: str, model: str = "gpt-4"):
        chat = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
        )
        return chat.choices[0].message["content"]
    
    

    def predict(
        model: str = None, system_message: str = None, raw_history: List[any] = None
    ):
        if model == None:
            logger.warning("No model provided. Returning [].")
            return []

        if system_message == None:
            logger.warning("No system message provided. Returning [].")
            return []

        if raw_history == None:
            logger.warning("No history provided. Returning [].")
            return []

        logger.info(
            f"Predicting with model: {model} | User message: {raw_history[-1][0]}"
        )

        openai_system_message = system_message
        openai_history = raw_history

        messages_openai_format = []
        # Append system message to history
        if openai_system_message != None:
            messages_openai_format.append(openai_system_message)
        if openai_history != None:
            messages_openai_format += openai_history

        # OpenAI API call
        # openai.ChatCompletion.create = reliableGPT(openai.ChatCompletion.create, user_email='ishaan@berri.ai')
        return openai.ChatCompletion.create(
            model=model, messages=messages_openai_format, temperature=1.0, stream=True
        )

    def summarize(self, text: str = None, model: str = "gpt-4"):
        if text == None:
            logger.warning("No text provided. Returning [].")
            return []

        logger.info(f"Summarizing text: {text}")

        return openai.Completion.create(
            engine="davinci",
            prompt=text,
            temperature=0.5,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["\n"],
        )
    
    
    
# AVAILABLE_MODELS = [
#     # GPT-3.5 Turbo
#     "gpt-3.5-turbo",
#     "gpt-3.5-turbo-0301",
#     "gpt-3.5-turbo-0613",

#     # GPT-3.5 Turbo 16k
#     "gpt-3.5-turbo-16k",
#     "gpt-3.5-turbo-16k-0301",
#     "gpt-3.5-turbo-16k-0613",

#     # GPT-4
#     "gpt-4",
#     "gpt-4-0314",
#     "gpt-4-0613",
    
#     # GPT-4 32k models are not currently available
#     "gpt-4-32k",
#     "gpt-4-32k-0314",
#     "gpt-4-32k-0613",

#     # Not implemented yet
#     "text-davinci-003",
#     "code-davinci-002",
# ]