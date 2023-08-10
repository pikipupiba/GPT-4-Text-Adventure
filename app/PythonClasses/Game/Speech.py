# import boto3
# from botocore.config import Config
# from botocore.exceptions import BotoCoreError, ClientError
# from contextlib import closing
# import os
# import sys
# import subprocess
# from tempfile import gettempdir
# from PythonClasses.LLM import LLM


# # EACH GAME HAS ITS OWN INSTANCE OF SPEECH

# # arrays and pop

# # 


# class Speech:
# # The `Speech` class is a Python class that provides functionality for converting text to speech
# # using the Amazon Polly service. It initializes with a directory where the audio files will be
# # saved and provides methods for adding sentences, converting the sentences to SSML format, and
# # generating speech responses using the Amazon Polly service.

#     config = Config(
#         region_name="us-east-1",
#         signature_version="v4",
#         retries={"max_attempts": 10, "mode": "standard"},
#     )
# <<<<<<< HEAD

#     client = boto3.client("polly", config=config)

#     def __init__(self, text: str) -> None:
#         pass

#     def get_ssml(self, text: str):
#         LLM.predict(model="gpt-4", system_message=text, raw_history=[])
#         [
#             {
#                 "role": "system",
#                 "content": "You convert the user message from plaintext to SSML.\n\nDo not respond stating what you are doing, simply do.",
#             },
#             {"role": "user", "content": text},
#         ]

#     def get_speech_response(self, text: str, voice: str = "Brian", type="ssml"):
#         if "<speak>" not in text:
#             text = f"<speak>{text}</speak>"
#         self.response = self.client.synthesize_speech(
# =======
#     client = boto3.client("polly", config=config)

# <<<<<<< HEAD
#     def __init__(self):
#         self.input_stream = ""
# =======
#     def __init__(self, directory: str):
#         self.directory = directory
# >>>>>>> c1237ddf7eeb21e2ab37665937d35765b692ae67
#         self.sentences = []
#         self.ssml = []
        
#     def add_sentence(self, text: str):
#         self.sentences.append(text)



#     def get_ssml(self):
#         system = "You convert the user message from plaintext to SSML.\n\nDo not respond stating what you are doing, simply do."
#         for sentence in self.sentences:
#             text = sentence
#             self.ssml.append(LLM.oneshot(system_message = system, user_message = text))

#     def get_speech_response(self, voice: str = "Brian", type="ssml"):
#         text = self.text if self.ssml is None else self.ssml
#         if "<speak>" not in text:
#             text = f"<speak>{text}</speak>"
#         response = self.client.synthesize_speech(
# >>>>>>> 2c449be6a292886c7315715215374e7297d82d04
#             Engine="standard",
#             LanguageCode="en-US",
#             OutputFormat="mp3",
#             VoiceId=voice,
#             Text=text,
# <<<<<<< HEAD
#             TextType="ssml",
#         )

#     def save_speech_response(self):
#         if "AudioStream" in self.response:
# =======
#             TextType=type,
#         )
#         if "AudioStream" in response:
# >>>>>>> 2c449be6a292886c7315715215374e7297d82d04
#             # Note: Closing the stream is important because the service throttles on the
#             # number of parallel connections. Here we are using contextlib.closing to
#             # ensure the close method of the stream object will be called automatically
#             # at the end of the with statement's scope.
# <<<<<<< HEAD
#             with closing(speech["AudioStream"]) as stream:
#                 output = os.path.join(gettempdir(), "speech.mp3")
# =======
#             with closing(response["AudioStream"]) as stream:
#                 output = os.path.join(gettempdir(), self.filename)
# >>>>>>> 2c449be6a292886c7315715215374e7297d82d04

#                 try:
#                     # Open a file for writing the output as a binary stream
#                     with open(output, "wb") as file:
#                         file.write(stream.read())
# <<<<<<< HEAD
#                 except IOError as error:
#                     # Could not write to file, exit gracefully
#                     print(error)
#                     sys.exit(-1)

#         else:
#             # The response didn't contain audio data, exit gracefully
#             print("Could not stream audio")
#             sys.exit(-1)

#         # Play the audio using the platform's default player
#         if sys.platform == "win32":
#             os.startfile(output)
#         else:
#             # The following works on macOS and Linux. (Darwin = mac, xdg-open = linux).
#             opener = "open" if sys.platform == "darwin" else "xdg-open"
#             subprocess.call([opener, output])
# =======
#                         self.audios.append(file.name)
#                 except IOError as error:
#                     # Could not write to file, exit gracefully
#                     print(error)
# >>>>>>> 2c449be6a292886c7315715215374e7297d82d04
