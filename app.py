import gradio as gr
from gm import *
from player import *

game_area = gr.TabbedInterface([player_area, game_master_area], ["Player", "Game Master"]).launch()