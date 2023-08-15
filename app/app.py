import os,uuid,sys,signal
from loguru import logger

from PythonClasses.Game.Game import Game
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
# # Array to update the interface from the game state. Contains all updatable interface elements.
story_render_array = [
    chatbot,
    day_box,
    item_box,
    relationship_box,
    submit,
    user_message,
    turn_json,
    gm_tab,
    config_tab,
    gpt_4_json,
    gpt_4_32_json,
    gpt_3_5_turbo_json,
    gpt_3_5_turbo_16_json,
    game_average_gpt_4_json,
    game_average_gpt_4_32_json,
    game_average_gpt_3_5_turbo_json,
    game_average_gpt_3_5_turbo_16_json,
    game_gpt_4_json,
    game_gpt_4_32_json,
    game_gpt_3_5_turbo_json,
    game_gpt_3_5_turbo_16_json,

    # audio_box,
]

story_interface_array = [
    history_name,
    game_name,
    start_game,
    user_message,
    submit,
    stats_area,
]


with combined:
# with player_tab:
    
    # audio_box.stop(
    #     fn=Game.get_next_audio,
    #     inputs=[game_name],
    #     outputs=[audio_box],
    #     queue=False,
    #     # every=5,
    # )

    start_game.click(
        fn=Game,
        inputs=[game_name, chatbot, system_message],
        outputs=[],
        queue=False,
    ).then(
        fn= Game.start,
        inputs=[game_name],
        outputs=story_render_array + story_interface_array,
        queue=False,
    ).then(
        # Add the player message to the history
        fn=Game.submit,
        inputs=[game_name, user_message, system_message, select_model],
        outputs=[user_message] + story_render_array,
        queue=False
    ).then(
        fn=Game.stream_prediction,
        inputs=[game_name],
        outputs=story_render_array,
        queue=True
    )

    game_name.submit(
        fn=Game,
        inputs=[game_name, chatbot, system_message],
        outputs=[],
        queue=False,
    ).then(
        fn= Game.start,
        inputs=[game_name],
        outputs=story_render_array + story_interface_array,
        queue=False,
    ).then(
        # Add the player message to the history
        fn=Game.submit,
        inputs=[game_name, user_message, system_message, select_model],
        outputs=[user_message] + story_render_array,
        queue=False
    ).then(
        fn=Game.stream_prediction,
        inputs=[game_name],
        outputs=story_render_array,
        queue=True
    )

    #--------------------------------------------------------------
    # SUBMIT FUNCTIONS
    #--------------------------------------------------------------
    # Click "Do it!" button
    submit.click(
        # Add the player message to the history
        fn=Game.submit,
        inputs=[game_name, user_message, system_message, select_model, system_select, schema_select],
        outputs=[user_message] + story_render_array,
        queue=False
    ).then(
        fn=Game.stream_prediction,
        inputs=[game_name],
        outputs=story_render_array,
        queue=True
    )

    # Press enter key
    user_message.submit(
        # Add the player message to the history
        fn=Game.submit, 
        inputs=[game_name, user_message, system_message, select_model, system_select, schema_select],
        outputs=[user_message] + story_render_array,
        queue=False
    ).then(
        fn=Game.stream_prediction,
        inputs=[game_name],
        outputs=story_render_array,
        queue=True
    )

with combined:
# with config_tab:
    # Click "Retry" button
    retry.click(
        # Remove the last assistant message from the history
        fn=Game.retry,
        inputs=[game_name],
        outputs=story_render_array,
        queue=False,
    )

    undo.click(
        fn=Game.undo,
        inputs=[game_name],
        outputs=story_render_array,
        queue=False
    )

    # Restart the game
    clear.click(
        fn=Game.clear,
        inputs=[game_name],
        outputs=story_render_array,
        queue=False,
    )

    # Restart the game
    restart.click(
        fn=Game.restart,
        inputs=[game_name],
        outputs=story_render_array,
        queue=False,
    )

    render.click(
        fn=Game.render_story,
        inputs=[game_name],
        outputs=story_render_array,
        queue=False,
    )

    #--------------------------------------------------------------
    # AUXILIARY FUNCTIONS
    #--------------------------------------------------------------
    # Undo the last user and assistant message
    

    # Delete the game
    delete_game.click(
        fn=FileManager.delete_history,
        inputs=[select_history_name],
        outputs=[],
        queue=False
    )

    # Load the game on button click
    load_game.click(
        fn=FileManager.load_history,
        inputs=[select_history_name],
        outputs=story_render_array,
        queue=False
    )

    # Save the game on button click
    save_game.click(
        fn=FileManager.save_history,
        inputs=[game_name, game_name],
        outputs=[],
        queue=False
    )

# --------------------------------------------------------------

# game_area = gr.TabbedInterface(
#     [player_tab, gm_tab, config_tab],
#     ["Player", "Game Master", "Config"],
#     title="AI Adventure Academy",
# )

# share_mode_string = os.getenv("SHARE_MODE", "false")
# share_mode = share_mode_string.lower() == 'true'

# if __name__ == "__main__":
#     game_area.queue(
#         concurrency_count=5, 
#         api_open=False,
#     )
#     game_area.launch(
#         inbrowser=True,
#         show_api=False,
#         show_error=True,
#         share=share_mode,
#     )
    

share_mode_string = os.getenv("SHARE_MODE", "false")
share_mode = share_mode_string.lower() == 'true'

if __name__ == "__main__":
    combined.queue(
        concurrency_count=10, 
        api_open=False,
    )
    combined.launch(
        inbrowser=True,
        show_api=False,
        show_error=True,
        share=share_mode,
    )