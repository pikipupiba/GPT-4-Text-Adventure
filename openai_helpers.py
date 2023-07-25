import os, json
import openai
from story_function import *
from stats import *

# set Open AI API Key
api_key = os.getenv('OPENAI_API_KEY')
# print(api_key)
assert api_key is not None, "API Key not set in environment"

openai.api_key = api_key

def submit_message(player_message, gm_message, story):
    messages = build_messages(player_message, gm_message, story)

    # make a call to open ai
    response = openai.ChatCompletion.create(
        model="gpt-4",
        max_tokens=4000,
        n=1,
        messages=messages,
        functions=story_function,
        function_call={"name": "get_story_chunks"},
    )

    print(response)

    # parse JSON output from AI model
    arguments_json = json.loads(response.choices[0]["message"]["function_call"]["arguments"])

    print(json.dumps(arguments_json, indent=2))

    # update stats
    stats.update(arguments_json)

    return [story+"\n\n\n"+arguments_json['Story'], stats.format_day_time(), stats.format_items(), stats.format_relationships()]

def build_system_message(gm_message, story):
    # build system message from GM input
    return gm_message + "\r\n\n" + "STORY:/n" + story + "\n" + "CURRENT STATS:/n" + stats.to_string()

def build_messages(player_message, gm_message, story):
    # submit system message + story + stats + action to model

    system_message = build_system_message(gm_message, story)

    messages = [
        {"role": "system", "content": system_message},
        # {"role": "assistant", "content": story},
        {"role": "user", "content": player_message},
    ]

    return messages