import os
from contextlib import closing

import boto3
from botocore.config import Config
from loguru import logger
from PythonClasses.LLM.LLM import LLM

# import asyncio
# import aioboto3


class LLMStreamProcessor:
    AUDIO_FOLDER = os.path.join(os.getcwd(), "data", "audio")

    def __init__(self, game_name: str):
        logger.info(f"Initializing LLMStreamProcessor | {game_name}")
        self.buffer = ""
        self.terminators = [".", "?", "!"]
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
        positions = [
            text.find(terminator)
            for terminator in self.terminators
            if terminator in text
        ]
        first_position = min(pos for pos in positions if pos != -1)
        return text[: first_position + 1].strip(), text[first_position + 1 :]

    def pop_audio(self):
        if len(os.listdir(self.audio_path)) > 0:
            logger.info(f"Popping audio file | {self.audio_path}")
            return os.path.join(self.audio_path, os.listdir(self.audio_path)[0])
        else:
            return None

    def _save_audio(self, audio_stream):
        logger.info(f"Saving audio | {self.audio_path}")
        with open(
            os.path.join(
                self.audio_path, f"audio{len(os.listdir(self.audio_path))}.mp3"
            ),
            "wb",
        ) as file:
            file.write(audio_stream.read())

    async def _send_to_api(self, sentence):
        logger.info(f"Sending to API | {sentence}")
        if not sentence.startswith("<speak>"):
            system_message = """You convert the user message from plaintext to SSML.
                                Do not respond stating what you are doing, simply do."""
            sentence = LLM.oneshot(system_message, sentence)
            async with self.client.synthesize_speech(
                Engine="standard",
                LanguageCode="en-US",
                OutputFormat="mp3",
                VoiceId="Brian",
                Text=sentence,
                TextType="ssml",
            ) as response:
                if "AudioStream" in response:
                    with closing(response["AudioStream"]) as stream:
                        self._save_audio(stream)

    async def process_data(self, data):
        logger.debug(f"Processing data | {data}")
        self.buffer += data
        while any(terminator in self.buffer for terminator in self.terminators):
            sentence, self.buffer = self._split_at_first_terminator(self.buffer)
            await self._send_to_api(sentence)


class LLMChunker:
    AUDIO_FOLDER = os.path.join(os.getcwd(), "data", "audio")

    def __init__(self, game_name: str):
        self.config = Config(
            region_name="us-east-1",
            signature_version="v4",
            retries={"max_attempts": 10, "mode": "standard"},
        )
        self.client = boto3.client("polly", config=self.config)
        self.audio_path = os.path.join(LLMStreamProcessor.AUDIO_FOLDER, game_name)
        self.index = 0

        if not os.path.exists(self.audio_path):
            os.makedirs(self.audio_path)

    def _save_audio(self, audio_stream):
        logger.info(f"Saving audio | {self.audio_path}")

        if os.path.exists(os.path.join(self.audio_path, f"audio{self.index}.mp3")):
            os.remove(os.path.join(self.audio_path, f"audio{self.index}.mp3"))

        self.index += 1

        with open(
            os.path.join(self.audio_path, f"audio{self.index}.mp3"), "wb"
        ) as file:
            file.write(audio_stream.read())
        return file.name

    def _to_ssml(self, text):
        system_message = """You convert the user message from plaintext to SSML.
If a line starts with "--->", it is an action line. Interpret action lines to the best of your ability.
Do not respond by stating what you are doing, simply do."""
        return LLM.oneshot(
            system_message=system_message, user_message=text, model="gpt-3.5"
        )

    def _to_audio(self, text):
        converted_text = self._to_ssml(text)
        with self.client.synthesize_speech(
            Engine="standard",
            LanguageCode="en-US",
            OutputFormat="mp3",
            VoiceId="Brian",
            Text=converted_text,
            TextType="ssml",
        ) as response:
            if "AudioStream" in response:
                with closing(response["AudioStream"]) as stream:
                    self._save_audio(stream)

    def speak(self, text):
        """
        The function "speak" takes in a text input and returns the audio representation of that text.
        This method uses GPT-4, so it costs more tokens than the `no_ssml` method.

        :param text: The text parameter is a string that represents the text that you want to convert to
        audio
        :return: the result of the `_to_audio` method.
        """
        return self._to_audio(text)

    def no_ssml(self, text, voice_id="Brian", rate=100):
        """
        The `no_ssml` function takes in a text and voice_id as parameters, and uses the AWS Polly client to
        synthesize speech without using SSML.

        :param text: The `text` parameter is the input text that you want to convert to speech. It can be a
        plain text or SSML (Speech Synthesis Markup Language) formatted text
        :param voice_id: The `voice_id` parameter is used to specify the voice that will be used for
        synthesizing the speech. In this case, the default value is set to "Brian", which is a specific
        voice available in the text-to-speech service. However, you can change it to any other valid voice,
        defaults to Brian (optional)
        """

        text = f'<speak><prosody rate="{str(rate)}%">{text}</prosody></speak>'
        response = self.client.synthesize_speech(
            Engine="neural",
            LanguageCode="en-US",
            OutputFormat="mp3",
            VoiceId=voice_id,
            Text=text,
            TextType="ssml",
        )
        if "AudioStream" in response:
            with closing(response["AudioStream"]) as stream:
                return self._save_audio(stream)
