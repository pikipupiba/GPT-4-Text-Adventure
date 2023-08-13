from typing import List, Union
from enum import Enum

import openai
import tiktoken

from loguru import logger

from PythonClasses.LLM.openai_helpers import build_openai_history, build_openai_system_message
from PythonClasses.Game.ChatMessage import HistoryFilter, History, ChatMessage


class OpenAIModelMetadata:
    def __init__(self, model_name, model_version, max_tokens, prompt_price, completion_price, tpm_max):
        self.model_name = model_name
        self.model_version = model_version
        self.max_tokens = max_tokens
        self.prompt_price = prompt_price
        self.completion_price = completion_price
        self.tpm_max = tpm_max

    def __str__(self):
        return self.model_name


class OpenAIModel(Enum):
    GPT_3_5_TURBO = OpenAIModelMetadata("GPT_3_5_TURBO", "gpt-3.5-turbo-0613", 4096, 0.0000015, 0.000002, 90000)
    GPT_3_5_TURBO_16k = OpenAIModelMetadata("GPT_3_5_TURBO_16k", "gpt-3.5-turbo-16k-0613", 16384, 0.000003, 0.000004, 180000)
    GPT_4 = OpenAIModelMetadata("GPT_4", "gpt-4-0613", 8192, 0.00003, 0.00006, 40000)
    GPT_4_32k = OpenAIModelMetadata("GPT_4_32k", "gpt-4-32k-0613", 32768, 0.00006, 0.00012, 0)

    def __init__(self, metadata: OpenAIModelMetadata):
        self.metadata = metadata


class ChatMessageHandler:
    @staticmethod
    def cost(input: ChatMessage, price: float):
        return OpenAIModel.num_tokens(input.context) * price


class HistoryHandler:
    @staticmethod
    def cost(input: History, price: float):
        return sum(OpenAIModel.num_tokens(message.context) for message in input.messages) * price


class HistoryFilterHandler:
    @staticmethod
    def cost(input: HistoryFilter, price: float):
        return sum(OpenAIModel.num_tokens(item['content']) for item in input.context_history()) * price
