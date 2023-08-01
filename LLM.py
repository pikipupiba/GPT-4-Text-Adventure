import openai
import os,json,uuid,random
from TokenTracker import *
from loguru import logger

# set Open AI API Key
api_key = os.getenv('OPENAI_API_KEY')
assert api_key is not None and len(api_key) > 0, "API Key not set in environment"
openai.api_key = api_key

import os,json,uuid,random

def extract_json_objects(text, decoder=json.JSONDecoder()):
    """Find JSON objects in text, and yield the decoded JSON data

    Does not attempt to look for JSON arrays, text, or other JSON types outside
    of a parent JSON object.

    """
    pos = 0
    while True:
        match = text.find('{', pos)
        if match == -1:
            break
        try:
            result, index = decoder.raw_decode(text[match:])
            yield result
            pos = match + index
        except ValueError:
            pos = match + 1

day_name = ""
time_left = ""
items_array = []
r_array = []
day = ""
items = ""
relationships = ""
stats_schema = ""

def parse_stats(json_grab={}):
    # parse stats from chatbot
    global day_name
    global time_left
    global items_array
    global r_array
    global stats_schema

    global day
    global items
    global relationships
    
    if "Stats_Schema" in json_grab:
        print("Found Stats_Schema")
        stats_schema = json.dumps(json_grab)
        day_name = json_grab["Stats_Schema"][0][0]
        time_left = json_grab["Stats_Schema"][0][1]
        items_array = json_grab["Stats_Schema"][1]
        r_array = json_grab["Stats_Schema"][2]

        day = f'{day_name} --- {time_left} minutes left'
        items = ""
        for item in items_array:
            items += f'{item[0]} ({item[1]})\n'
        relationships = ""
        relationships += f'Acquaintances: {r_array[0][0]} ({r_array[0][1]} {r_array[0][2]})\n'
        relationships += f'Friends: {r_array[1][0]} ({r_array[1][1]} {r_array[1][2]})\n'
        relationships += f'Enemies: {r_array[2][0]} ({r_array[2][1]} {r_array[2][2]})\n'
        relationships += f'Best Friend: {r_array[3][0]} ({r_array[3][1]})\n'
        relationships += f'Arch Nemesis: {r_array[4][0]} ({r_array[4][1]})\n'

    return day, items, relationships
        
        

class LLM:

    AVAILABLE_MODELS = [
        "gpt-4",
        "gpt-4-0314",
        "gpt-4-0613",
        "gpt-4-32k",
        "gpt-4-32k-0314",
        "gpt-4-32k-0613",
        "gpt-3.5-turbo",
        "gpt-3.5-turbo-0301",
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "text-davinci-003",
        "code-davinci-002",
    ]

    models = []
    token_trackers = {}

    def __init__(self, models:list):
        LLM.models = models

        for model in models:
            if model not in LLM.AVAILABLE_MODELS:
                raise NotImplementedError(f"num_tokens_from_messages() is not implemented for model {model}.")
                continue
            LLM.token_trackers[model] = TokenTracker(model)


    def predict(self, model, system_message, example_history, history):
        # array of dice rolls from 1-20
        dice_rolls = [random.randint(1,20) for i in range(10)]

        history_openai_format = []
        history_openai_format.append({"role": "system", "content": system_message + "/n/n" + stats_schema})

        if not example_history or isinstance(example_history, str):
            example_history_json = []
        else:
            try:
                example_history_json = json.loads(example_history)
            except json.JSONDecodeError as e:
                raise ValueError(f"Failed to decode example history: {e}")

        complete_history = example_history_json + history

        for human, assistant in complete_history:
            if human != None: history_openai_format.append({"role": "user", "content": human })
            if assistant != None: history_openai_format.append({"role": "assistant", "content":assistant})

        response = openai.ChatCompletion.create(
            model=model,
            messages= history_openai_format,         
            temperature=1.0,
            stream=True
        )
        
        history[-1][1] = ""

        found_json_array=[]
        inside_json=False
        json_string=""
        for chunk in response:
            real_model = chunk["model"]
            if len(chunk["choices"][0]["delta"]) != 0:
                if inside_json:
                    
                    json_string += chunk["choices"][0]["delta"]["content"]
                    try:
                        found_json_array.append(json.loads(json_string))
                        parse_stats(found_json_array[-1])
                        print(found_json_array[-1])
                        inside_json=False
                        json_string=""
                    except json.JSONDecodeError:
                        continue
                else:
                    if chunk["choices"][0]["delta"]["content"] == "{\"":
                        inside_json=True
                        json_string += chunk["choices"][0]["delta"]["content"]
                        history[-1][1] += "\n---\n"
                        yield history
                    else:
                        history[-1][1] += chunk["choices"][0]["delta"]["content"]
                        yield history

        # Calculate streaming token usage
        LLM.token_trackers[real_model].add_from_stream(real_model, history_openai_format, history[-1][1])

        # logger.info(f"~~--------~~ {model} ~~--------~~")
        LLM.token_trackers[model].print()

        # yield self.response

    def get_tokens(self):
        return self.token_tracker
    
    def get_all_tokens():
        return TokenTracker.trackers["gpt-3.5-turbo-0613"], TokenTracker.trackers["gpt-3.5-turbo-16k-0613"], TokenTracker.trackers["gpt-4-0613"], TokenTracker.trackers["gpt-4-32k-0613"]