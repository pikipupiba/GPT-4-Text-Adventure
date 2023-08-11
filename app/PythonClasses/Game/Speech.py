import os
from contextlib import closing
import sys
import subprocess
from tempfile import gettempdir
from botocore.exceptions import BotoCoreError, ClientError
from botocore.config import Config
from LLM.LLM import LLM
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
        >>> LLMStreamProcessor.oneshot("You're nice", "Hi")
        'Hi, how are you?'

    """

    def __init__(self, audio_path):
        self.buffer = ""
        self.terminators = ['.', '?', '!']
        self.config = Config(
            region_name="us-east-1",
            signature_version="v4",
            retries={"max_attempts": 10, "mode": "standard"},
        )
        self.client = boto3.client("polly", config=self.config)
        self.audio_path = audio_path

    def process_data(self, data):
        self.buffer += data
        while any(terminator in self.buffer for terminator in self.terminators):
            sentence, self.buffer = self._split_at_first_terminator(
                self.buffer)
            self._send_to_api(sentence)

    def _split_at_first_terminator(self, text):
        positions = [text.find(terminator)
                     for terminator in self.terminators if terminator in text]
        first_position = min(pos for pos in positions if pos != -1)
        return text[:first_position+1].strip(), text[first_position+1:]
    
    def _save_audio(self , audio_stream):
        # Save the audio stream to a file
        with open(self.filename, "wb") as file:
            file.write(audio_stream.read())

    def _send_to_api(self, sentence):
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
                TextType=type,
            )
        if "AudioStream" in response:
            with closing(response["AudioStream"]) as stream:
                output = os.path.join(gettempdir(), self.filename)
                try:
                    # Open a file for writing the output as a binary stream
                    with open(output, "wb") as file:
                        file.write(stream.read())
                        self.audios.append(file.name)
                except IOError as error:
                    # Could not write to file, exit gracefully
                    print(error)
                    
        audio_stream = response.get('AudioStream')
        # Save the audio stream to a file
        with open("response_audio.mp3", "wb") as file:
            file.write(audio_stream.read())
        logger.info("Audio response saved to response_audio.mp3")


class Speech:
    """The `Speech` class is a Python class that provides functionality for converting text to speech
using the Amazon Polly service. It initializes with a directory where the audio files will be
saved and provides methods for adding sentences, converting the sentences to SSML format, and
generating speech responses using the Amazon Polly service."""

    config = Config(
        region_name="us-east-1",
        signature_version="v4",
        retries={"max_attempts": 10, "mode": "standard"},
    )
    client = boto3.client("polly", config=config)

    def __init__(self, directory: str):
        self.directory = directory
        self.sentences = []
        self.ssml = []

    def add_sentence(self, text: str):
        self.sentences.append(text)

    def get_ssml(self):
        system = "You convert the user message from plaintext to SSML.\n\nDo not respond stating what you are doing, simply do."
        for sentence in self.sentences:
            text = sentence
            self.ssml.append(LLM.oneshot(
                system_message=system, user_message=text))

    def get_speech_response(self, voice: str = "Brian", type="ssml"):
        text = self.text if self.ssml is None else self.ssml
        if "<speak>" not in text:
            text = f"<speak>{text}</speak>"
        response = self.client.synthesize_speech(
            Engine="standard",
            LanguageCode="en-US",
            OutputFormat="mp3",
            VoiceId=voice,
            Text=text,
            TextType=type,
        )
        if "AudioStream" in response:
            # Note: Closing the stream is important because the service throttles on the
            # number of parallel connections. Here we are using contextlib.closing to
            # ensure the close method of the stream object will be called automatically
            # at the end of the with statement's scope.
            with closing(response["AudioStream"]) as stream:
                output = os.path.join(gettempdir(), self.filename)

                try:
                    # Open a file for writing the output as a binary stream
                    with open(output, "wb") as file:
                        file.write(stream.read())
                        self.audios.append(file.name)
                except IOError as error:
                    # Could not write to file, exit gracefully
                    print(error)
