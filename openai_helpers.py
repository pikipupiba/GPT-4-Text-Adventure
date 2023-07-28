import os, json, time
import openai
from story_function import *
from stats import *

# set Open AI API Key
api_key = os.getenv('OPENAI_API_KEY')
# print(api_key)
assert api_key is not None and len(api_key) > 0, "API Key not set or invalid"

openai.api_key = api_key
openai.organization = "org-ziA2BQ1zJxVrlYV5I6mcTUwN"

start_time = 0

def submit_message(player_message, gm_message, story, total_tokens, dice_rolls):

    global start_time
    if start_time == 0:
        start_time = time.time()
        
    messages = build_messages(player_message, gm_message, story, dice_rolls)
    # make a call to open ai
    response = openai.ChatCompletion.create(
        model="gpt-4",
        max_tokens=3000,
        n=1,
        messages=messages,
        functions=story_function,
        function_call={"name": "continue_adventure"},
    )

    # print(response)

    # parse JSON output from AI model
    arguments_json = json.loads(response.choices[0]["message"]["function_call"]["arguments"])

    print(json.dumps(arguments_json, indent=2))

    # update stats
    stats.update(arguments_json)

    if total_tokens == "": total_tokens="0"

    tokens_per_minute = (int(total_tokens)+response.usage.total_tokens)/(time.time()-start_time)*60

    return [story+"\n----------------------------------------------\n"+arguments_json['Story'], stats.format_day_time(), stats.format_items(), stats.format_relationships(), response.usage.total_tokens, response.usage.total_tokens+int(total_tokens), tokens_per_minute]

def build_system_message(gm_message, dice_rolls):
    # build system message from GM input
    return gm_message + "\n\n" + "CURRENT STATS:\n" + stats.to_string() + "\n\n" + "CURRENT DICE ROLLS: " + dice_rolls

def build_messages(player_message, gm_message, story, dice_rolls):
    # submit system message + story + stats + action to model

    system_message = build_system_message(gm_message, dice_rolls)

    messages = [
        {"role": "system", "content": system_message},
        {"role": "assistant", "content": story},
        {"role": "user", "content": player_message},
    ]

    return messages