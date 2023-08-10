import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir
from PythonClasses.LLM import LLM


class Speech:
    config = Config(
        region_name="us-east-1",
        signature_version="v4",
        retries={"max_attempts": 10, "mode": "standard"},
    )

    client = boto3.client("polly", config=config)

    def __init__(self, text: str) -> None:
        pass

    def get_ssml(self, text: str):
        LLM.predict(model="gpt-4", system_message=text, raw_history=[])
        [
            {
                "role": "system",
                "content": "You convert the user message from plaintext to SSML.\n\nDo not respond stating what you are doing, simply do.",
            },
            {"role": "user", "content": text},
        ]

    def get_speech_response(self, text: str, voice: str = "Brian", type="ssml"):
        if "<speak>" not in text:
            text = f"<speak>{text}</speak>"
        self.response = self.client.synthesize_speech(
            Engine="standard",
            LanguageCode="en-US",
            OutputFormat="mp3",
            VoiceId=voice,
            Text=text,
            TextType="ssml",
        )

    def save_speech_response(self):
        if "AudioStream" in self.response:
            # Note: Closing the stream is important because the service throttles on the
            # number of parallel connections. Here we are using contextlib.closing to
            # ensure the close method of the stream object will be called automatically
            # at the end of the with statement's scope.
            with closing(speech["AudioStream"]) as stream:
                output = os.path.join(gettempdir(), "speech.mp3")

                try:
                    # Open a file for writing the output as a binary stream
                    with open(output, "wb") as file:
                        file.write(stream.read())
                except IOError as error:
                    # Could not write to file, exit gracefully
                    print(error)
                    sys.exit(-1)

        else:
            # The response didn't contain audio data, exit gracefully
            print("Could not stream audio")
            sys.exit(-1)

        # Play the audio using the platform's default player
        if sys.platform == "win32":
            os.startfile(output)
        else:
            # The following works on macOS and Linux. (Darwin = mac, xdg-open = linux).
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, output])
