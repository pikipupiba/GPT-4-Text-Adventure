import os,json
from typing import List, Tuple
from loguru import logger
from PythonClasses.LLM.LLMModel import LLMModel

import openai

# set Open AI API Key
# api_key = os.getenv('OPENAI_API_KEY')

# if (api_key is None) or (len(api_key) == 0):
#     api_key = os.environ['OPENAI_API_KEY']
# assert api_key is not None and len(api_key) > 0, "API Key not set in environment"

# openai.api_key = api_key
if os.getenv('AZURE_OPENAI_API_KEY') is not None:
    logger.info("Using Azure OpenAI API")
    use_azure = True
else:
    logger.info("Using OpenAI API")
    use_azure = False

if use_azure:
    openai.api_type = "azure"
    openai.api_version = "2023-05-15"
    openai.api_key = os.getenv('AZURE_OPENAI_API_KEY')
    openai.api_base = os.getenv('AZURE_OPENAI_API_BASE')
    model_deployment_name_35 = "Q3-dpt-meeting-35"
    model_deployment_name_4 = "Q3-dpt-meeting-4"
else:
    openai.api_key = os.getenv('OPENAI_API_KEY')

assert openai.api_key is not None and len(openai.api_key) > 0, "API Key not set in environment"

history_length = 50

def set_history_length(new_history_length: int):
    global history_length
    history_length = new_history_length

# `LLM` is a class that provides methods for interacting with the OpenAI API. It includes
# methods for generating responses in a chat-like format (`oneshot`), building the history array
# in the required OpenAI format (`build_openai_history_array`), building the system message in
# the required OpenAI format (`build_openai_system_message`), predicting the next response based
# on the model, system message, and history (`predict`), and summarizing text (`summarize`).
class LLM:

    def __init__(self):
        tokens = {
            "gpt-3.5-turbo-0613" : {
                "prompt": 0,
                "completion": 0,
                "tpm": 0,
            },
            "gpt-3.5-turbo-16k-0613" : {
                "prompt": 0,
                "completion": 0,
                "tpm": 0,
            },
            "gpt-4-0613": {
                "prompt": 0,
                "completion": 0,
                "tpm": 0,
            },
            "gpt-4-32k-0613": {
                "prompt": 0,
                "completion": 0,
                "tpm": 0,
            },
        }

    def oneshot(system_message: str, user_message: str, model: str = "gpt-4"):
        if use_azure:
            if "gpt-4" in model:
                model = model_deployment_name_4
            elif "gpt-3.5" in model:
                model = model_deployment_name_35
        chat = openai.ChatCompletion.create(
            engine = model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ]
        )
        return chat.choices[0].message["content"]

    def build_openai_history_array(raw_history):
        logger.debug("Building history OpenAI format")

        if raw_history == None:
            logger.warning("No history provided. Returning None.")
            return None

        history_openai_format = []

        # Convert history to OpenAI format
        for human, assistant in raw_history:
            if human != None:
                history_openai_format.append({"role": "user", "content": human})
            if assistant != None:
                history_openai_format.append(
                    {"role": "assistant", "content": assistant}
                )

        logger.trace(
            f"Successfully built history OpenAI format | Found {len(history_openai_format)} turns"
        )

        return history_openai_format

    def build_openai_system_message(system_message: str = None, model: str = "gpt-4"):
        logger.debug("Building system message OpenAI format")

        if system_message == None:
            logger.warning("No system message provided. Returning None.")
            return None

        if "gpt-4" in model:
            system_message_openai_format = {"role": "system", "content": system_message}
        else:
            system_message_openai_format = {"role": "user", "content": system_message}

        logger.trace("Successfully built system message OpenAI format")

        return system_message_openai_format



    def predict(
        model: str = None, system_message: str = None, raw_history: List[any] = None, llm_model: LLMModel = None
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

        openai_system_message = LLM.build_openai_system_message(system_message, model)
        openai_history = LLM.build_openai_history_array(raw_history)

        messages_openai_format = []
        # Append system message to history
        if openai_system_message != None:
            messages_openai_format.append(openai_system_message)
        if openai_history != None:
            messages_openai_format += openai_history[-history_length:]

        llm_model.num_tokens_from_messages(model, messages_openai_format)

        if use_azure:
            if "gpt-4" in model:
                model = model_deployment_name_4
            elif "gpt-3.5" in model:
                model = model_deployment_name_35

            # OpenAI API call
            return openai.ChatCompletion.create(
                engine=model,
                messages=messages_openai_format,
                temperature=0.9,
                stream=True,
                max_tokens=1000,
            )
        else:
            # OpenAI API call
            return openai.ChatCompletion.create(
                model=model,
                messages=messages_openai_format,
                temperature=0.9,
                stream=True,
                max_tokens=1000,
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