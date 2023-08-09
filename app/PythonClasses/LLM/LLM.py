import os
from typing import List, Tuple
from loguru import logger

import openai

# set Open AI API Key
api_key = os.getenv('OPENAI_API_KEY')
assert api_key is not None and len(api_key) > 0, "API Key not set in environment"
openai.api_key = api_key


class LLM:

    def build_openai_history_array(raw_history):

        logger.debug("Building history OpenAI format")

        if raw_history == None:
            logger.warning("No history provided. Returning None.")
            return None
        
        history_openai_format = []

        # Convert history to OpenAI format
        for human, assistant in raw_history:
            if human != None: history_openai_format.append({"role": "user", "content": human })
            if assistant != None: history_openai_format.append({"role": "assistant", "content":assistant})

        logger.trace(f"Successfully built history OpenAI format | Found {len(history_openai_format)} turns")

        return history_openai_format


    def build_openai_system_message(system_message: str = None, model: str = "gpt-4"):

        logger.debug("Building system message OpenAI format")


        if system_message == None:
            logger.warning("No system message provided. Returning None.")
            return None
        
        if "gpt-4" in model:
            system_message_openai_format = {
                "role": "system",
                "content": system_message
            }
        else:
            system_message_openai_format = {
                "role": "user",
                "content": system_message
            }

        logger.trace("Successfully built system message OpenAI format")

        return system_message_openai_format


    def predict(model: str = None, system_message: str = None, raw_history: List[any] = None):

        if model == None:
            logger.warning("No model provided. Returning [].")
            return []
        
        if system_message == None:
            logger.warning("No system message provided. Returning [].")
            return []
        
        if raw_history == None:
            logger.warning("No history provided. Returning [].")
            return []

        logger.info(f"Predicting with model: {model} | User message: {raw_history[-1][0]}")
        
        openai_system_message = LLM.build_openai_system_message(system_message, model)
        openai_history = LLM.build_openai_history_array(raw_history)

        messages_openai_format = []
        # Append system message to history
        if openai_system_message != None:
            messages_openai_format.append(openai_system_message)
        if openai_history != None:
            messages_openai_format += openai_history

        # OpenAI API call
        return openai.ChatCompletion.create(
            model=model,
            messages= messages_openai_format,         
            temperature=1.0,
            stream=True
        )