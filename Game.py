import openai
import os,json,random
from TokenTracker import *
from helpers import *
from loguru import logger

# set Open AI API Key
api_key = os.getenv('OPENAI_API_KEY')
assert api_key is not None and len(api_key) > 0, "API Key not set in environment"
openai.api_key = api_key

import os,json,uuid,random

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

combat_schema={
    "Combat_Schema":
    ["{strCharacter}","{strAction}","{strDcReason}","{intDC}","{intRoll}"]
}

stats_schema={
    "Stats_Schema":
    [
        ["{strDayName}","{intMinsLeft}"],
        [
            ["{strItemName}","{strItemStatus}"]
        ],
        [
            ["{intAcquaintanceCount}","{strAcquaintanceChange}","{strAcquaintanceReason}"],
            ["{intFriendCount}","{strFriendChange}","{strFriendReason}"],
            ["{intEnemyCount}","{strEnemyChange}","{strEnemyReason}"],
            ["{strBestFriendName}","{strBestFriendStatus}"],
            ["{strArchNemesisName}","{strArchNemesisStatus}"]
        ]
    ]
}



class Game:

    AVAILABLE_MODELS = [
        "gpt-4",
        "gpt-4-0314",
        "gpt-4-0613",
        # GPT-4 32k models are not currently available
        # "gpt-4-32k",
        # "gpt-4-32k-0314",
        # "gpt-4-32k-0613",
        "gpt-3.5-turbo",
        "gpt-3.5-turbo-0301",
        "gpt-3.5-turbo-0613",
        "gpt-3.5-turbo-16k-0613",
        "text-davinci-003",
        "code-davinci-002",
    ]

    # Initialize a new Game object for each active game.
    def __init__(self, models:list=[], prev_game_state:dict=None):
        if not prev_game_state is None:
            self.state = prev_game_state
            self.models = prev_game_state["models"]
        else:
            self.models = models

        # Create a token tracker for each model
        self.token_trackers = []
        for model in models:
            if model not in Game.AVAILABLE_MODELS:
                raise NotImplementedError(f"num_tokens_from_messages() is not implemented for model {model}.")
                continue
            self.token_trackers.append(TokenTracker(model))


    def predict(self, model, system_message, example_history, history):
        
        history_openai_format = []
        
        # Append strings to system message
        dice_string = generate_dice_string()
        combat_schema_string = json.dumps(combat_schema)
        stats_schema_string = json.dumps(stats_schema)

        complete_system_message = f'{system_message}\n\n{combat_schema_string}\n{stats_schema_string}\n\n{dice_string}'
        
        # Append system message to history
        history_openai_format.append({"role": "system", "content": f'{system_message}\n\n{stats_schema}'})

        # Check for example history
        # Example history helps the model understand the desired flow of the conversation
        if not example_history or isinstance(example_history, str):
            example_history_json = []
        else:
            # Example history is input as a string
            try:
                example_history_json = json.loads(example_history)
            except json.JSONDecodeError as e:
                raise ValueError(f"Failed to decode example history: {e}")

        # Append history to example history
        complete_history = example_history_json + history

        # Convert history to OpenAI format
        for human, assistant in complete_history:
            if human != None: history_openai_format.append({"role": "user", "content": human })
            if assistant != None: history_openai_format.append({"role": "assistant", "content":assistant})

        # OpenAI API call
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
        self.token_trackers[real_model].add_from_stream(real_model, history_openai_format, history[-1][1])

        # logger.info(f"~~--------~~ {model} ~~--------~~")
        self.token_trackers[model].print()

    def get_tokens(self):
        return self.token_tracker
    
    def get_all_tokens():
        return TokenTracker.trackers["gpt-3.5-turbo-0613"], TokenTracker.trackers["gpt-3.5-turbo-16k-0613"], TokenTracker.trackers["gpt-4-0613"], TokenTracker.trackers["gpt-4-32k-0613"]