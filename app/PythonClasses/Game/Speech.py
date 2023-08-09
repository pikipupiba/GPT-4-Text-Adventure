import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
import os
import sys
import subprocess
from tempfile import gettempdir

class Speech:
    
    config = Config(
        region_name='us-east-1',
        signature_version='v4',
        retries={
            'max_attempts': 10,
            'mode': 'standard'
        }
    )
    
    client = boto3.client('polly', config=config)
    
    def __init__(self, text: str) -> None:
        pass
    
    def get_ssml(self, text: str):
        pass
    
    def get_speech_response(self, text: str, voice: str = 'Brian', type = 'ssml'):
        if "<speak>" not in text:
            text = f"<speak>{text}</speak>"
        self.response = self.client.synthesize_speech(
        Engine='standard',
        LanguageCode='en-US',
        OutputFormat='mp3',
        VoiceId=voice,
        Text=text,
        TextType='ssml'
        )
    
    def save_speech_response():
        pass
    
    