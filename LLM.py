# TODO:
# 1. integrate system message into predict function
# 2. 

import openai
import os,json,uuid,random
from TokenTracker import *
from loguru import logger

# set Open AI API Key
api_key = os.getenv('OPENAI_API_KEY')
assert api_key is not None and len(api_key) > 0, "API Key not set in environment"
openai.api_key = api_key

class LLM:

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

    models = []
    token_trackers = {}

    def __init__(self, models:list):
        LLM.models = models

        for model in models:
            if model not in LLM.AVAILABLE_MODELS:
                raise NotImplementedError(f"num_tokens_from_messages() is not implemented for model {model}.")
                continue
            LLM.token_trackers[model] = TokenTracker(model)


    def predict(self, model, system_message, history):
        # array of dice rolls from 1-20
        dice_rolls = [random.randint(1,20) for i in range(10)]

        history_openai_format = []
        history_openai_format.append({"role": "system", "content": system_message})
        for human, assistant in history:
            if human != None: history_openai_format.append({"role": "user", "content": human })
            if assistant != None: history_openai_format.append({"role": "assistant", "content":assistant})

        response = openai.ChatCompletion.create(
            model=model,
            messages= history_openai_format,         
            temperature=1.0,
            stream=True
        )
        
        history[-1][1] = ""

        for chunk in response:
            if len(chunk['choices'][0]['delta']) != 0:
                history[-1][1] += chunk['choices'][0]['delta']['content']
                yield history

        # Calculate streaming token usage
        LLM.token_trackers[model].add_from_stream(model, history_openai_format, history[-1][1])

        logger.info(f"~~------------------~~ {model}  ~~-------------------~~")
        LLM.token_trackers[model].print()

        # yield self.response

    def get_tokens(self):
        return self.token_tracker
    
    def get_all_tokens():
        return TokenTracker.trackers["gpt-3.5-turbo-0613"], TokenTracker.trackers["gpt-3.5-turbo-16k-0613"], TokenTracker.trackers["gpt-4-0613"], TokenTracker.trackers["gpt-4-32k-0613"]