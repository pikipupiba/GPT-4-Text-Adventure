import boto3

class Speech:
    config = Config(
        region_name="us-east-1",
        signature_version="v4",
        retries={"max_attempts": 10, "mode": "standard"},
    )

    client = boto3.client("polly", config=config)

    audios = []

    def __init__(self, text: str) -> None:
        self.text = text

    def get_ssml(self):
        system_message = "You are an SSML processor, you trun the user message into a speech response."
        self.ssml = LLM.oneshot(system_message=system_message, user_message=self.text)

    def get_speech_response(self, voice: str = "Brian", type="ssml"):
        text = self.ssml if self.ssml != None else self.text
        if "<speak>" not in text:
            text = f"<speak>{text}</speak>"
        response = self.client.synthesize_speech(
                Engine="standard",
                LanguageCode="en-US",
                OutputFormat="mp3",
                VoiceId=voice,
                Text=text,
                TextType=type
            )
        if "AudioStream" in response:
            with closing(self.response["AudioStream"]) as stream:
                output = os.path.join(gettempdir(), f"speech_{self.audios.count}.mp3")
                try:
                    with open(output, "wb") as file:
                        file.write(stream.read())
                        self.audios.append(file)
                except IOError as error:
                    print(error)

        else:
            print("Could not stream audio")
