import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir
from PythonClasses.LLM import LLM


# EACH GAME HAS ITS OWN INSTANCE OF SPEECH

# arrays and pop

# 


class Speech:
    config = Config(
        region_name="us-east-1",
        signature_version="v4",
        retries={"max_attempts": 10, "mode": "standard"},
    )
    client = boto3.client("polly", config=config)

    def __init__(self):
        self.input_stream = ""
        self.sentences = []
        self.audios = []
        self.ssml = []
        
    def add_sentence(self, text: str):
        self.sentences.append(text)



    def get_ssml(self):
        system = "You convert the user message from plaintext to SSML.\n\nDo not respond stating what you are doing, simply do."
        for sentence in self.sentences:
            text = sentence
            self.ssml.append(LLM.oneshot(system_message = system, user_message = text))

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