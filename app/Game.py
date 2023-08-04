#TODO:
# 1. track tokens with Game objects (__dict__ anyone?)
# 2. auto switch to gpt-3.5-turbo-16k-0613 when context is too long
# 3. add a 3rd item to messages indicating real_model
# 4. add a 4th item to messages indicating real_model models

import os,json
import openai
from loguru import logger
from TokenTracker import *
from helpers import *
from schemas import *

# set Open AI API Key
api_key = os.getenv('OPENAI_API_KEY')
assert api_key is not None and len(api_key) > 0, "API Key not set in environment"
openai.api_key = api_key

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

        # Default values for the game state
        default_values = {
            'team_name': team_name,
            'models': models,
            'system_message': "",
            'history': [],
            'raw_history': [],
            'combat': {},
            # 'message': "",
            'stats': {},
            'token_trackers': {}
        }

        # Load previous game state
        prev_game_state = self.load_game_state(team_name)

        # Copy previous game state into the new game object, or use the default value if the attribute does not exist
        for key, default_value in default_values.items():
            value = getattr(prev_game_state, key, default_value)
            setattr(self, key, value)
                    
        # Initialize token trackers
        for model in self.models:
            if model not in Game.AVAILABLE_MODELS:
                raise NotImplementedError(f"num_tokens_from_messages() is not implemented for model {self.models}.")
                continue
            self.token_trackers[model] = TokenTracker(model)

    def build_openai_history_array(self, history, example_history):
        if len(self.history) == 0:
            self.history.append(history[-1].copy())
            self.raw_history.append(history[-1].copy())
        elif self.history[-1][1] is not None:
            self.history.append(history[-1].copy())
            self.raw_history.append(history[-1].copy())

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

        # Add dice roll to the end of the user message
        if "intRollArray" not in self.raw_history[-1][0]:
            self.raw_history[-1][0] += f'\n\n{generate_dice_string(10)}'

        history_array_openai_format = []

        # Convert history to OpenAI format
        for human, assistant in complete_history:
            if human != None: history_array_openai_format.append({"role": "user", "content": human })
            if assistant != None: history_array_openai_format.append({"role": "assistant", "content":assistant})

        return history_array_openai_format


    def build_openai_system_message(self, system_message):

        # Append schema strings to system message
        combat_schema_string = json.dumps(combat_schema, separators=(',', ':'))
        stats_schema_string = json.dumps(stats_schema, separators=(',', ':'))
        
        complete_system_message = f'{system_message}\n\n{combat_schema_string}\n{stats_schema_string}\n\n'
        
        self.system_message = complete_system_message

        system_message_openai_format = {
            "role": "system",
            "content": complete_system_message
        }

        return system_message_openai_format

    def predict(self, model, system_message, example_history, history):
        
        messages_openai_format = []

        # Append system message to history
        messages_openai_format.append(self.build_openai_system_message(system_message))
        messages_openai_format += self.build_openai_history_array(history, example_history)

        # OpenAI API call
        response = openai.ChatCompletion.create(
            model=model,
            messages= messages_openai_format,         
            temperature=1.0,
            stream=True
        )
        

        # Variables to capture JSON objects in the response
        inside_json=False
        json_string=""
        found_json_schema=None

        # Parse the response one chunk at a time
        self.history[-1][1] = ""
        self.raw_history[-1][1] = ""
        for chunk in response:
            # print(self.raw_history[-1][1])
            # See what model the api actually used. This is important for tracking tokens.
            real_model = chunk.get("model", model)
            if len(chunk["choices"][0]["delta"]) != 0:
                content = chunk["choices"][0]["delta"]["content"]

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
                            self.history[-1][1] += " COMPLETE!!!\n\n"
                        elif "Combat_Schema" in new_json:
                            self.combat = new_json
                            if self.combat["Combat_Schema"]["success"] == True:
                                self.history[-1][1] += " SUCCESS!!!\n\n"
                            else:
                                self.history[-1][1] += " FAILURE!!!\n\n"
                        logger.info(new_json)

                        inside_json=False
                        json_string=""
                        found_json_schema=None
                            
                    except json.JSONDecodeError:
                    
                        if found_json_schema == None:
                            if "Stats_Schema" in json_string:
                                logger.info("Found Stats_Schema!")
                                found_json_schema="Stats_Schema"
                                self.history[-1][1] += " Calculating stats "
                            elif "Combat_Schema" in json_string:
                                logger.info("Found Combat_Schema!")
                                found_json_schema="Combat_Schema"
                                self.history[-1][1] += " Calculating combat "
                        else:
                            if len(json_string)%5 == 0:
                                self.history[-1][1] += "-"
                else:
                    # Found the start of a JSON object
                    if content == "{\"":
                        inside_json=True
                        json_string += content
                        self.history[-1][1] += "\n\n---"
                    # Send response chunks to the chatbot
                    else:
                        # print(content)
                        self.history[-1][1] += content
                    
                yield self.history

        # print(self.raw_history[-1][1])
        # Calculate streaming token usage
        self.token_trackers[real_model].add_from_stream(real_model, messages_openai_format, self.raw_history[-1][1])

        # logger.info(f"~~--------~~ {model} ~~--------~~")
        # self.token_trackers[real_model].print()

    def get_tokens(self):
        return self.token_tracker
    
    def get_all_tokens(self):
        return list(self.token_trackers.values())
    
    def render_stats(self):
        if not "Stats_Schema" in self.stats:
            return {
                "day_string": "??? --- ??? minutes left",
                "items_string": "???",
                "relationships_string": "???",
            }
        
        logger.debug("RENDERING THE STATS!!!")
        stats = self.stats["Stats_Schema"]

        # DAY/TIME LEFT
        day = stats["day"]
        time = stats["time"]
        day_string = f'{day} --- {time} minutes left'

        # ITEMS
        items_array = stats["items"]
        items_string = ""
        for item in items_array:
            items_string += f'{list(item.items())[0][1]} ({list(item.items())[1][1]})\n'
        
        # RELATIONSHIPS
        r_array = stats["relationships"]
        relationships_string = ""
        for relationship in r_array:
            relationships_string += f'{relationship["relationship"]}: {relationship["count"]} ({relationship["rationale"]})\n'
            
            for name in relationship["names"]:
                relationships_string += f'{name},'

            relationships_string = relationships_string[:-1] + '\n\n'

        logger.debug("DONE RENDERING THE STATS!!!")

        return {
            "day_string": day_string,
            "items_string": items_string,
            "relationships_string": relationships_string,
        }
    
    def render_combat(self):
        logger.debug("RENDERING COMBAT!!!")

        if not "Combat_Schema" in self.combat:
            return [""]
        
        combat = self.combat["Combat_Schema"]

        combat_string=""
        for key, value in combat.items():
            combat_string += f'{key}: {value} --- '

        logger.debug("DONE RENDERING COMBAT!!!")

        return combat_string

    # Break game state apart for rendering
    def render_game_state(self):
        logger.debug("RENDERING THE GAME STATE!!!")
        stats_strings = self.render_stats()
        combat_string = self.render_combat()

        logger.debug("DONE RENDERING THE GAME STATE!!!")
        logger.debug(self.team_name)
        logger.debug(self.history)
        logger.debug(stats_strings["day_string"])
        logger.debug(stats_strings["items_string"])
        logger.debug(stats_strings["relationships_string"])
        logger.debug(combat_string)
        return (
            self.team_name,
            self.history,
            stats_strings["day_string"],
            stats_strings["items_string"],
            stats_strings["relationships_string"],
            combat_string
         )
    
    def update_team_name(self, team_name:str=None):
        logger.info(f"Updating team name to {team_name}!")
        if team_name is not None:
            self.team_name = team_name
    
    def save_game_state(self, team_name:str=None):

        logger.debug(f"SAVING GAME STATE {team_name}!")

        if team_name is not None:
            self.team_name = team_name

        attributes = {
            "team_name": "",
            "models": [],
            "system_message": "",
            "history": [],
            "raw_history": [],
            "combat": {},
            "stats": {},
            "token_trackers": {}
        }

        game_state = {key: getattr(self, key, default) for key, default in attributes.items()}
        # Cannot print these yet... need a good __dict__ 0_o
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
            return {"error": f"Error saving game state: {e}"}
    
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
                    logger.info(f"---- Loading State Key -- {key} ----")
                    logger.debug(key, value)
                    setattr(self, key, value)
            # Initialize token trackers
            for model in self.models:
                if model not in Game.AVAILABLE_MODELS:
                    raise NotImplementedError(f"num_tokens_from_messages() is not implemented for model {self.models}.")
                    continue
                self.token_trackers[model] = TokenTracker(model)
        except FileNotFoundError:
            print(f"Error: File '{game_state_file_path}' not found")
            game_state = {"error": f"Error loading game state: File '{game_state_file_path}' not found"}
        except IOError as e:
            print(f"Error: {e}")
            game_state = {"error": f"Error loading game state: {e}"}

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
        if not self.history:
            return game_state

        # Pop last entries from history
        self.history.pop()
        self.raw_history.pop()

        # Update game_state with current history
        game_state["history"] = self.history
        game_state["raw_history"] = self.raw_history
        # game_state["message"] = self.message

        # Find and update stats
        self.find_last_stats()
        game_state["stats"] = self.stats

        return game_state
    
    def clear(self, game_state):
        """
        Clears the message, history, and stats attributes of the current game state object.
        
        Parameters:
        - self: The current instance of the game state object.
        - game_state: A dictionary representing the current state of the game.
        
        Returns:
        - game_state: The updated game state dictionary with cleared values for history and stats.
        """
        self.message = ""  # Clear the message attribute
        self.history = []  # Clear the history attribute
        self.raw_history = []  # Clear the raw_history attribute
        self.stats = {}  # Clear the stats attribute
        self.combat = {}  # Clear the combat attribute
        self.team_name = ""  # Clear the team_name attribute
        
        # Assign the cleared values to the corresponding keys in the game_state dictionary
        game_state["history"] = self.history
        game_state["raw_history"] = self.raw_history
        game_state["stats"] = self.stats
        game_state["combat"] = self.combat
        game_state["team_name"] = self.team_name
        
        return game_state  # Return the updated game state dictionary

    
    def retry(self, game_state):

        if not self.history:
            return {}, []
        
        self.history[-1][1] = None
        self.raw_history[-1][1] = None
        game_state["history"] = self.history
        game_state["raw_history"] = self.raw_history

        self.find_last_stats()
        game_state["stats"] = self.stats
        return game_state, self.history