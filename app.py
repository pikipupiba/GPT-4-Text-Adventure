import gradio as gr
import openai
from openai_helpers import *
from gm import *
from player import *


openai.organization = "org-ziA2BQ1zJxVrlYV5I6mcTUwN"
openai.api_key = os.getenv('OPENAI_API_KEY')

user = openai.ChatMessageRoleUser
messages = []

# Initialize messages with system message and example turns.

# 


game_area = gr.TabbedInterface([player_area, game_master_area], ["Player", "Game Master"]).launch()