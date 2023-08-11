import os
from contextlib import closing
# import sys
# import subprocess
# from tempfile import gettempdir
# from botocore.exceptions import BotoCoreError, ClientError
import threading
from botocore.config import Config
from PythonClasses.LLM.LLM import LLM
from loguru import logger
import boto3


# EACH GAME HAS ITS OWN INSTANCE OF SPEECH

# arrays and pop
class LLMStreamProcessor:
    """The `LLMStreamProcessor` class is a Python class that provides functionality for converting 
    text to speech using Amazon Polly.

    Returns:
        _type_: _description_

    Raises:
        _type_: _description_

    Examples:
        >>> from app.PythonClasses.LLMStreamProcessor import LLMStreamProcessor
        'Hi, how are you?'

    """

    AUDIO_FOLDER = os.path.join(os.getcwd(), "data", "audio")

    def __init__(self, game_name: str):
        """
        The function initializes a class instance with attributes for buffering text, a list of 
        sentence terminators, a configuration object, a client object for interacting with the 
        Amazon Polly service, and an audio path.

        :param audio_path: The `audio_path` parameter is a string that represents the path to the 
        audio file that you want to process with Amazon Polly
        """
        logger.info(f"Initializing LLMStreamProcessor | {game_name}")
        self.buffer = ""
        self.terminators = ['.', '?', '!']
        self.config = Config(
            region_name="us-east-1",
            signature_version="v4",
            retries={"max_attempts": 10, "mode": "standard"},
        )
        self.client = boto3.client("polly", config=self.config)
        self.audio_path = os.path.join(LLMStreamProcessor.AUDIO_FOLDER, game_name)

        
        if not os.path.exists(self.audio_path):
            os.makedirs(self.audio_path)

    def _split_at_first_terminator(self, text):
        """
        The function `_split_at_first_terminator` splits a given text at the first occurrence of any
        terminator in a list of terminators, and returns the two resulting parts.

        :param text: a string that represents the input text that needs to be split
        :return: The function `_split_at_first_terminator` returns a tuple containing two elements. 
        The first element is the substring of `text` from the beginning up to and including the 
        first occurrence of a terminator character. This substring is stripped of leading and 
        trailing whitespace. The second element is the remaining portion of `text` after the first 
        terminator character.
        """
        positions = [text.find(terminator)
                     for terminator in self.terminators if terminator in text]
        first_position = min(pos for pos in positions if pos != -1)
        return text[:first_position+1].strip(), text[first_position+1:]
    
    def pop_audio(self):
        
        if len(os.listdir(self.audio_path)) > 0:
            logger.info(f"Popping audio file | {self.audio_path}")
            return os.path.join(self.audio_path, os.listdir(self.audio_path)[0])
        else:
            return None

    def _save_audio(self, audio_stream):
        # Save the audio stream to a file
        logger.info(f"Saving audio | {self.audio_path}")
        with open(
            os.path.join(
                self.audio_path,
                f"audio{len(os.listdir(self.audio_path))}.mp3"
            ), "wb"
        ) as file:
            file.write(audio_stream.read())

    def _send_to_api(self, sentence):
        logger.info(f"Sending to API | {sentence}")
        if not sentence.startswith("<speak>"):
            # Use the LLM class to send the request to openai
            system_message = """You convert the user message from plaintext to SSML.
            
            Do not respond stating what you are doing, simply do."""
            sentence = LLM.oneshot(system_message, sentence)
            # Handle the SSML response
            response = self.client.synthesize_speech(
                Engine="standard",
                LanguageCode="en-US",
                OutputFormat="mp3",
                VoiceId="Brian",
                Text=sentence,
                TextType="ssml",
            )
        if "AudioStream" in response:
            with closing(response["AudioStream"]) as stream:
                self._save_audio(stream)

    def process_data(self, data):
        """_summary_

        Args:
            data (_type_): _description_
        """
        logger.debug(f"Processing data | {data}")
        self.buffer += data
        while any(terminator in self.buffer for terminator in self.terminators):
            sentence, self.buffer = self._split_at_first_terminator(
                self.buffer)
            self._send_to_api(sentence)
