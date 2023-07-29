import openai
import os,json,uuid
from ChatToken import *
from loguru import logger

logger.level("msg",22)

# set Open AI API Key
api_key = os.getenv('OPENAI_API_KEY')
assert api_key is not None and len(api_key) > 0, "API Key not set in environment"
openai.api_key = api_key

AVAILABLE_MODELS = [
    "gpt-4",
    "gpt-4-0314",
    "gpt-4-32k",
    "gpt-4-32k-0314",
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-0301",
    "text-davinci-003",
    "code-davinci-002",
]

class GPTBot:

    bots = []

    def __init__(self, name:str):
        self.uuid = uuid.uuid4()
        logger.add(f"logs/{self.uuid}"+"_{time:YYYY-MM-DD}_message.log", format="{message}", level="msg")
        self.name = name
        self.messages = []
        self.model = "gpt-4"
        self.tokens = ChatTokenCounter(self.model)
        GPTBot.bots.append(self)
        
    def add_message_from_file(self, role:str, file_name:str):
        with open(file_name, "r") as file:
            self.messages.append({"role": role, "content":file.read()})
            
    def add_message(self, role:str, message:str):
        self.messages.append({"role": role, "content":message})
        logger.log('msg',f'{self.messages[-1]}')
        
    def send_chat(self):
        self.response_object = openai.ChatCompletion.create(
            model = self.model,
            messages = self.messages
        )
        self.response = self.response_object.choices[0].message.content
        self.add_message("assistant",self.response)
        self.tokens.add(ChatToken(usage = self.response_object.usage))

        logger.info(f"~~------------------~~ {self.name}  ~~-------------------~~")
        self.log_tokens()
        logger.info("\n" + self.response)


        self.log()

    def send_message(self, message, history):

        if history is None: history = []

        self.response_object = openai.ChatCompletion.create(
            model = self.model,
            messages = [{"role": "user", "content": message}]
        )
        self.response = self.response_object.choices[0].message.content
        self.tokens.add(ChatToken(usage = self.response_object.usage))

        # logger.info(f"~~------------------~~ {self.name}  ~~-------------------~~")
        # self.log_tokens()

        return self.response
        

    def log_tokens(self):
        self.tokens.print(self.name)

    def log_all_tokens():
        for bot in GPTBot.bots:
            bot.log_tokens()
    
    def log_total_tokens():
        total = ChatTokenCounter("total")
        for bot in GPTBot.bots:
            total += bot.tokens

        logger.info(f"~~----------------~~ TOKEN TOTALS  ~~-----------------~~")
        total.print("total")

    def log(self):
        pass
        # name = self.response_object.id
        # msg_name = f'{self.response_object.id}_messages'
        # with open(f'log/{name}.txt','w') as f:
        #     f.write(json.dumps(self.response_object.__dict__))
        # with open(f'log/{msg_name}.txt','w') as f:
        #     f.write(json.dumps(self.messages))