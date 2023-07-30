import openai
import os,time,json,uuid,sys,signal
from story_chunks import *
from GPTBot import *
from loguru import logger

import gradio as gr
from gradio_gm import *
from gradio_player import *

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

game_area = gr.TabbedInterface([player_tab, game_master_area], ["Player", "Game Master"])
# chat.queue()
# chat.launch(inbrowser=True, show_error=True)
if __name__ == "__main__":
    game_area.queue()
    game_area.launch(inbrowser=True, show_error=True)



# for i in range(5):
#     logger.info("~~-----~~")
#     logger.info(f"Round {i + 1}")
#     logger.info("~~-----~~")

#     logger.log('md',f"\n\n{dm_bot.response}")
#     player_bot.add_message("user", dm_bot.response)
#     player_bot.send_chat()

#     logger.log('md',f"\n\n{player_bot.response}")
#     dm_bot.add_message("user", player_bot.response)   
#     dm_bot.send_chat()

# logger.log('md',f"\n\n{dm_bot.response}")
# GPTBot.log_total_tokens()
