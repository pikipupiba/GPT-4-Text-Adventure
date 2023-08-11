# import os
from typing import List #, Tuple
from loguru import logger

import openai

# # set Open AI API Key
# api_key = os.getenv('OPENAI_API_KEY')

# if (api_key is None) or (len(api_key) == 0):
#     api_key = os.environ['OPENAI_API_KEY']

# assert api_key is not None and len(api_key) > 0, "API Key not set in environment"
# openai.api_key = api_key


class LLM:
    """`LLM` is a class that provides methods for interacting with the OpenAI API. It includes
    methods for generating responses in a chat-like format (`oneshot`), building the history array
    in the required OpenAI format (`build_openai_history_array`), building the system message in
    the required OpenAI format (`build_openai_system_message`), predicting the next response based
    on the model, system message, and history (`predict`), and summarizing text (`summarize`).

    Returns:
        _type_: _description_

    Raises:
        _type_: _description_

    Examples:
        >>> from app.PythonClasses.LLM import LLM
        >>> LLM.oneshot("You're nice", "Hi")
        'Hi, how are you?'

    """
    @staticmethod
    def oneshot(system_message: str, user_message: str, model: str = "gpt-3.5"):
        """Send a single message to the OpenAI API and return the response.

        Args:
            system_message (str): system message
            user_message (str): user message
            model (str, optional): _description_. Defaults to "gpt-3.5".

        Returns:
            (str): OpenAi response"""
        chat = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
        )
        return chat.choices[0].message["content"]

    @staticmethod
    def build_openai_history_array(raw_history):
        """Build the history array in the required OpenAI format.

        Args:
            raw_history (List[Tuple[str, str]]): raw history

        Returns:
            (List[Dict[str, str]]): history in OpenAI format"""

        logger.debug("Building history OpenAI format")

        if raw_history is None:
            logger.warning("No history provided. Returning None.")
            return None

        history_openai_format = []

        # Convert history to OpenAI format
        for human, assistant in raw_history:
            if human is not None:
                history_openai_format.append(
                    {"role": "user", "content": human})
            if assistant is not None:
                history_openai_format.append(
                    {"role": "assistant", "content": assistant})

        logger.trace(
            f"Successfully built history OpenAI format | Found {len(history_openai_format)} turns")

        return history_openai_format

    @staticmethod
    def build_openai_system_message(system_message: str = None, model: str = "gpt-4"):
        """
        The `build_openai_system_message` function takes in a system message and a model name, and 
        returns the system message in OpenAI format.

        :param system_message: a string that represents the message for the system.
        It is an optional parameter, so it can be None if no system message is provided
        :type system_message: str
        :param model: The `model` parameter is a string that specifies the OpenAI model to be used.
        In this case, the default value is set to "gpt-4", defaults to gpt-4
        :type model: str (optional)
        :return: message in OpenAI format. If no system message is provided, it returns None.
        """

        logger.debug("Building system message OpenAI format")
        if system_message is None:
            logger.warning("No system message provided. Returning None.")
            return None
        logger.trace("Successfully built system message OpenAI format")
        return (
            {"role": "system", "content": system_message}
            if "gpt-4" in model
            else {"role": "user", "content": system_message}
        )

    @staticmethod
    def predict(model: str = None, system_message: str = None, raw_history: List[any] = None):
        """
        The `predict` function takes in a model, system message, and history, and uses OpenAI's
        ChatCompletion API to generate a response based on the given inputs.
        
        :param model: The `model` parameter is a string that represents the name or ID of the 
        language model that will be used for prediction
        :type model: str
        :param system_message: The `system_message` parameter is a string that represents a message 
        from the system or bot. It can be used to provide context/instructions to the model before 
        generating a response
        :type system_message: str
        :param raw_history: The `raw_history` parameter is a list of previous conversation messages.
        Each message in the list is represented as a tuple, where the first element is the user 
        message and the second element is the assistant's response. The list represents the
        conversation history in chronological order
        :type raw_history: List[any]
        :return: The function `predict` returns the result of the OpenAI API call, which is an 
        instance of the `ChatCompletion` class.
        """
        if model is None:
            logger.warning("No model provided. Returning [].")
            return []
        if system_message is None:
            logger.warning("No system message provided. Returning [].")
            return []
        if raw_history is None:
            logger.warning("No history provided. Returning [].")
            return []
        logger.info(
            f"Predicting with model: {model} | User message: {raw_history[-1][0]}")
        openai_system_message = LLM.build_openai_system_message(
            system_message, model)
        openai_history = LLM.build_openai_history_array(raw_history)
        messages_openai_format = []
        # Append system message to history
        if openai_system_message is not None:
            messages_openai_format.append(openai_system_message)
        if openai_history is not None:
            messages_openai_format += openai_history
        # OpenAI API call
        return openai.ChatCompletion.create(
            model=model,
            messages=messages_openai_format,
            temperature=1.0,
            stream=True
        )

    # def summarize(self, text: str = None, model: str = "gpt-4"):

    #     if text == None:
    #         logger.warning("No text provided. Returning [].")
    #         return []

    #     logger.info(f"Summarizing text: {text}")

    #     return openai.Completion.create(
    #         engine="davinci",
    #         prompt=text,
    #         temperature=0.5,
    #         max_tokens=1000,
    #         top_p=1,
    #         frequency_penalty=0,
    #         presence_penalty=0,
    #         stop=["\n"]
    #     )
