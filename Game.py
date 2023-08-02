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
            ["{intAcquaintanceCount}","{strAcquaintanceChange}","{strAcquaintanceSentiment}"],
            ["{intFriendCount}","{strFriendChange}","{strFriendSentiment}"],
            ["{intEnemyCount}","{strEnemyChange}","{strEnemySentiment}"],
            ["{strBestFriendName}","{strBestFriendSentiment}"],
            ["{strArchNemesisName}","{strArchNemesisSentiment}"]
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
    def __init__(self, team_name:str=None, models:list=[]):

        # Copy previous game state into the new game object
        prev_game_state = self.load_game_state(team_name)

        if not hasattr(prev_game_state, 'team_name'):
            self.team_name = team_name
        if not hasattr(prev_game_state, 'models'):
            self.models = models
        if not hasattr(prev_game_state, 'system_message'):
            self.system_message = ""
        if not hasattr(prev_game_state, 'history'):
            self.history = []
        if not hasattr(prev_game_state, 'raw_history'):
            self.raw_history = []
        if not hasattr(prev_game_state, 'message'):
            self.message = ""
        if not hasattr(prev_game_state, 'stats'):
            self.stats = {}
        if not hasattr(prev_game_state, 'token_trackers'):
            self.token_trackers = {}
            
        # Initialize token trackers
        for model in self.models:
            if model not in Game.AVAILABLE_MODELS:
                raise NotImplementedError(f"num_tokens_from_messages() is not implemented for model {self.models}.")
                continue
            self.token_trackers[model] = TokenTracker(model)


    def predict(self, model, system_message, example_history, history):
        
        history_openai_format = []

        if len(self.history) == 0:
            self.history.append(history[-1].copy())
            self.raw_history.append(history[-1].copy())
        elif self.history[-1][1] is not None:
            self.history.append(history[-1].copy())
            self.raw_history.append(history[-1].copy())
        
        
        # Append strings to system message
        dice_string = generate_dice_string(5)
        # dice_string = f'intRoll={random.randint(1,20)}'
        combat_schema_string = json.dumps(combat_schema)
        stats_schema_string = json.dumps(stats_schema)
        
        complete_system_message = f'{system_message}\n\n{combat_schema_string}\n{stats_schema_string}\n\n{dice_string}'
        
        self.system_message = complete_system_message
        # Append system message to history
        history_openai_format.append({"role": "system", "content": f'{complete_system_message}\n\n'})

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
        complete_history = example_history_json + self.raw_history

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
        
        # Variables to capture JSON objects in the response
        inside_json=False
        json_string=""


        # Parse the response one chunk at a time
        self.history[-1][1] = ""
        self.raw_history[-1][1] = ""
        for chunk in response:
            # print(self.raw_history[-1][1])
            # See what model the api actually used. This is important for tracking tokens.
            real_model = chunk.get("model", model)
            if len(chunk["choices"][0]["delta"]) != 0:
                content = chunk["choices"][0]["delta"]["content"]
                # print(content)
                # Add everything to raw history
                self.raw_history[-1][1] += content
                # Don't add chunks to the chatbot if they are part of a JSON object
                # Continue until the JSON object is complete
                if inside_json:
                    json_string += content
                    try:
                        new_json = json.loads(json_string)
                        if "Stats_Schema" in new_json:
                            self.stats = new_json
                        print(new_json)

                        inside_json=False
                        json_string=""
                    except json.JSONDecodeError:
                        continue
                else:
                    # Found the start of a JSON object
                    if content == "{\"":
                        inside_json=True
                        json_string += content
                        self.history[-1][1] += "\n\n---\n"
                    # Send response chunks to the chatbot
                    else:
                        # print(content)
                        self.history[-1][1] += content
                    
                    yield self.history

        # print(self.raw_history[-1][1])
        # Calculate streaming token usage
        self.token_trackers[real_model].add_from_stream(real_model, history_openai_format, self.raw_history[-1][1])

        # logger.info(f"~~--------~~ {model} ~~--------~~")
        # self.token_trackers[real_model].print()

    def get_tokens(self):
        return self.token_tracker
    
    def get_all_tokens(self):
        return list(self.token_trackers.values())
    
    def render_stats(self):
        if not "Stats_Schema" in self.stats:
            return ["","",""]
        
        logger.debug("RENDERING THE STATS!!!")
        stats_array = self.stats["Stats_Schema"]

        day_name = stats_array[0][0]
        time_left = stats_array[0][1]
        items_array = stats_array[1]
        r_array = stats_array[2]

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

        return [day, items, relationships]

    # Break game state apart for rendering
    def render_game_state(self):
        logger.debug("RENDERING THE GAME STATE!!!")
        stats_strings = self.render_stats()

        return (self.team_name, self.history, self.message, stats_strings[0], stats_strings[1], stats_strings[2])
    
    def save_game_state(self, team_name:str=None):

        # print(vars(self))
        logger.debug(f"SAVING GAME STATE {self.team_name}!")

        game_state = {}
        self.team_name = team_name
        if hasattr(self, 'team_name'):
            game_state["team_name"] = self.team_name
        else:
            game_state["team_name"] = ""
        if hasattr(self, 'models'):
            game_state["models"] = self.models
        else:
            game_state["models"] = []
        if hasattr(self, 'system_message'):
            game_state["system_message"] = self.system_message
        else:
            game_state["system_message"] = ""
        if hasattr(self, 'history'):
            game_state["history"] = self.history
        else:
            game_state["history"] = []
        if hasattr(self, 'raw_history'):
            game_state["raw_history"] = self.raw_history
        else:
            game_state["raw_history"] = []
        if hasattr(self, 'stats'):
            game_state["stats"] = self.stats
        else:
            game_state["stats"] = {}
        if hasattr(self, 'message'):
            game_state["message"] = self.message
        else:
            game_state["message"] = ""
        if hasattr(self, 'token_trackers'):
            # Cannot print these yet... need a good __dict__ 0_o
            game_state["token_trackers"] = {}
            # game_state.token_trackers = self.token_trackers
        else:
            game_state["token_trackers"] = {}

        # Check if the "sessions/game_states" directory exists
        if not os.path.isdir(os.path.join("sessions", "game_states")):
            os.makedirs("sessions/game_states")

        game_state_file_path = os.path.join("sessions", "game_states", f"{self.team_name}_game_state.json")

        try:
            with open(game_state_file_path, "w") as f:
                f.write(json.dumps(game_state, indent=4))
            return game_state
        except IOError as e:
            game_state = None
            print(f"Error: {e}")
            return {}
    
    def load_game_state(self, team_name:str=None):

        print(team_name)
        if team_name is None:
            return None
        
        logger.info(f"Loading GAME STATE {team_name}!")

        # Check if the "sessions/game_states" directory exists
        if not os.path.isdir(os.path.join("sessions", "game_states")):
            os.makedirs("sessions/game_states")

        game_state_file_path = os.path.join("sessions", "game_states", f"{team_name}_game_state.json")

        try:
            with open(game_state_file_path, "r") as f:
                game_state = json.load(f)
                for key, value in game_state.items():
                    setattr(self, key, value)
            # Initialize token trackers
            for model in self.models:
                if model not in Game.AVAILABLE_MODELS:
                    raise NotImplementedError(f"num_tokens_from_messages() is not implemented for model {self.models}.")
                    continue
                self.token_trackers[model] = TokenTracker(model)
        except FileNotFoundError:
            print(f"Error: File '{game_state_file_path}' not found")
            game_state = {}
        except IOError as e:
            print(f"Error: {e}")
            game_state = {}

        return game_state
    
    def find_last_stats(self):
        # Search the second element of each raw history item for the last message that contained stats by use the extract_json_objects() helper function
        # This is a hacky way to do this, but it works for now
        self.stats = {}
        for msg_pair in reversed(self.raw_history):
            if msg_pair[1] == None:
                continue
            msg_json_array = extract_json_objects(msg_pair[1])
            for msg_json in msg_json_array:
                if "Stats_Schema" in msg_json:
                    self.stats = msg_json
                    return

    def undo(self, game_state):
        if len(self.history) > 0:
            # Need to figure out when I should reload teh user message
            # self.message = self.history[-1][0]
            self.history.pop()
            self.raw_history.pop()
            game_state["message"] = self.message
            game_state["history"] = self.history
            game_state["raw_history"] = self.raw_history

            self.find_last_stats()
            
            game_state["stats"] = self.stats
            return game_state
        else:
            return {}
    
    def clear(self, game_state):
        self.message = ""
        self.history = []
        self.raw_history = []
        self.stats = {}
        game_state["message"] = self.message
        game_state["history"] = self.history
        game_state["raw_history"] = self.raw_history
        game_state["stats"] = self.stats
        return game_state
    
    def retry(self, game_state):
        if len(self.history) > 0:
            self.history[-1][1] = None
            self.raw_history[-1][1] = None
            game_state["history"] = self.history
            game_state["raw_history"] = self.raw_history

            self.find_last_stats()
            
            game_state["stats"] = self.stats
            return game_state, self.history
        else:
            return {}, []