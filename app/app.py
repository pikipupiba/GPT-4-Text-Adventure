import os,uuid,sys,signal
from loguru import logger

import gradio as gr

from PythonClasses.player import *
from PythonClasses.game_master import *

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

game_area = gr.TabbedInterface([player_tab, gm_tab], ["Player", "Game Master"])
# chat.queue()
# chat.launch(inbrowser=True, show_error=True)
share_mode_string = os.getenv("SHARE_MODE", "false")
share_mode = share_mode_string.lower() == 'true'

if __name__ == "__main__":
    game_area.queue(
        concurrency_count=5, 
        api_open=False,
    )
    game_area.launch(
        inbrowser=True,
        show_error=True,
        share=share_mode,
    )