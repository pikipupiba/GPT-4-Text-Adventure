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


    def build_openai_system_message(system_message: str = None):

        logger.debug("Building system message OpenAI format")

        if system_message == None:
            logger.warning("No system message provided. Returning None.")
            return None

        system_message_openai_format = {
            "role": "system",
            "content": system_message
        }

        logger.trace("Successfully built system message OpenAI format")

        return system_message_openai_format

    def predict(model, system_message: str = None, raw_history: List[Tuple[str, str]] = None):

        logger.debug(f"Predicting with model: {model} | User message: {raw_history[-1][0]}")
        
        messages_openai_format = []
        # Append system message to history
        messages_openai_format.append(LLM.build_openai_system_message(system_message))
        messages_openai_format += LLM.build_openai_history_array(raw_history)

        # OpenAI API call
        yield openai.ChatCompletion.create(
            model=model,
            messages= messages_openai_format,         
            temperature=1.0,
            stream=True
        )