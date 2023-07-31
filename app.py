import openai
import os,time,json,uuid,sys,signal
from story_chunks import *
from loguru import logger

import gradio as gr
from gm_tab import *
from player_tab import *

def shutdown(signal, frame):
    # Perform any necessary cleanup or shutdown tasks here
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown)

logger.info("Starting")
uid = uuid.uuid4()
logger.remove(0)
logger.add(sys.stdout, level="INFO")
logger.add(f"logs/{uid}"+"_{time:YYYY-MM-DD}_info.log", format="{time:YYYY-MM-DD HH:mm:ss} {level} {message}", level="INFO")
logger.level("md",21)
logger.add(f"logs/{uid}_"+"{time:YYYY-MM-DD}_markdown.md", format="{message}", level="md")

game_area = gr.TabbedInterface([player_tab, gm_tab], ["Player", "Game Master"])
# chat.queue()
# chat.launch(inbrowser=True, show_error=True)
if __name__ == "__main__":
    game_area.queue()
    game_area.launch(inbrowser=True, show_error=True)