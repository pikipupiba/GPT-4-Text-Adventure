import os
import asyncio
import aioboto3
from contextlib import closing
from botocore.config import Config
from loguru import logger
from PythonClasses.LLM.OpenAI import OpenAIInterface

class LLMStreamProcessor:

    AUDIO_FOLDER = os.path.join(os.getcwd(), "data", "audio")

    def __init__(self, game_name: str):
        logger.info(f"Initializing LLMStreamProcessor | {game_name}")
        self.buffer = ""
        self.terminators = ['.', '?', '!']
        self.config = Config(
            region_name="us-east-1",
            signature_version="v4",
            retries={"max_attempts": 10, "mode": "standard"},
        )
        self.client = aioboto3.client("polly", config=self.config)
        self.audio_path = os.path.join(LLMStreamProcessor.AUDIO_FOLDER, game_name)

        if not os.path.exists(self.audio_path):
            os.makedirs(self.audio_path)

    def _split_at_first_terminator(self, text):
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
        logger.info(f"Saving audio | {self.audio_path}")
        with open(
            os.path.join(
                self.audio_path,
                f"audio{len(os.listdir(self.audio_path))}.mp3"
            ), "wb"
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