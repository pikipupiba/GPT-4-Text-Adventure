import os,uuid,sys,signal
from loguru import logger

from PythonClasses.Game.FileManager import FileManager

import gradio as gr
from PythonClasses.player import *
from PythonClasses.game_master import *
from PythonClasses.config import *

def shutdown(signal, frame):
    # Perform any necessary cleanup or shutdown tasks here
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown)

logger.info("Starting app.py")
uid = uuid.uuid4()
logger.remove(0)
logger.add(sys.stdout, level="INFO")
logger.add(f"logs/{uid}"+"_{time:YYYY-MM-DD}_info.log", format="{time:YYYY-MM-DD HH:mm:ss} {level} {message}", level="INFO")
logger.level("md",21)
logger.add(f"logs/{uid}_"+"{time:YYYY-MM-DD}_markdown.md", format="{message}", level="md")

# --------------------------------------------------------------

# #--------------------------------------------------------------
# #                      PLAYER TAB FUNCTIONS
# #--------------------------------------------------------------
# # Array to update the interface from the game state. Contains all changeable interface elements.
player_render_array = [
    display_history,
    day_box,
    item_box,
    relationship_box,
]

# #--------------------------------------------------------------
# # SUBMIT FUNCTIONS
# #--------------------------------------------------------------
# Click "Do it!" button
# submit.click(
#     # Add the player message to the history
#     fn=game.submit, 
#     inputs=[user_message, system_message, select_model],
#     outputs=[user_message] + player_render_array,
#     queue=False
# ).then(
#     fn=game.stream_prediction,
#     inputs=[],
#     outputs=player_render_array,
#     queue=True
# )

# # Press enter key
# user_message.submit(
#     # Add the player message to the history
#     fn=game.submit, 
#     inputs=[user_message, system_message, select_model],
#     outputs=[user_message] + player_render_array,
#     queue=False
# ).then(
#     fn=game.stream_prediction,
#     inputs=[],
#     outputs=player_render_array,
#     queue=True
# )









# --------------------------------------------------------------

game_area = gr.TabbedInterface([player_tab, gm_tab, config_tab], ["Player", "Game Master", "Config"])
share_mode_string = os.getenv("SHARE_MODE", "false")
share_mode = share_mode_string.lower() == 'true'

if __name__ == "__main__":
    game_area.queue(
        concurrency_count=5, 
        api_open=False,
    )
    game_area.launch(
        inbrowser=True,
        show_api=False,
        show_error=True,
        share=share_mode,
    )