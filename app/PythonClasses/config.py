import gradio as gr

from PythonClasses.Game.FileManager import FileManager

use_models = [
    "gpt-4-0613",
    "gpt-3.5-turbo-0613",
    "gpt-3.5-turbo-16k-0613"
]

with gr.Blocks() as config_tab:

    with gr.Group():
        with gr.Row():
            # SELECT MODEL
            select_model = gr.Radio(
                choices=use_models,
                label="Select Model",
                value=use_models[0],
                scale=1,
            )
            retry = gr.Button(value="Retry", size="sm")
            undo = gr.Button(value="Undo", size="sm")
            clear = gr.Button(value="Clear", size="sm")

    # GAME NAME
    with gr.Group():
        with gr.Row():
            history_name = gr.Textbox(
                value="BAH",
                lines=1,
                label="History Name",
                interactive=True,
                scale=1,
            )
            
            save_game = gr.Button(value="Save", size="sm")
            delete_game = gr.Button(value="Delete", size="sm")
            load_game = gr.Button(value="Load", size="sm")
            
            select_history_name = gr.Dropdown(
                choices=FileManager.get_file_names(FileManager.HISTORY_FOLDER),
                show_label=True,
                label="Select History",
                scale=1,
            )

    # DEBUG AREA
    with gr.Column(variant="compact") as debug_area:
        # with gr.Row():
        #     token_jsons = []
        #     for model_name,tracker in TokenTracker.trackers.items():
        #         token_jsons.append(gr.JSON(label=f"{model_name} Token Tracker", interactive=False))
        execution_json = gr.JSON(label="Execution Info")
        turn_json = gr.JSON(label="Game State")



    config_render_array = [
        execution_json,
        turn_json,
    ]

    # # Click "Retry" button
    # retry.click(
    #     # Remove the last assistant message from the history
    #     fn=game.retry,
    #     inputs=[],
    #     outputs=render_array,
    #     queue=False
    # )

    # # Restart the game
    #     clear.click(
    #     fn=game.clear,
    #     inputs=[],
    #     outputs=render_array,
    # )

    # #--------------------------------------------------------------
    # # AUXILIARY FUNCTIONS
    # #--------------------------------------------------------------
    # # Undo the last user and assistant message
    # undo.click(
    #     fn=game.undo,
    #     inputs=[],
    #     outputs=render_array,
    #     queue=False
    # )

    # # Delete the game
    # delete_game.click(
    #     fn=game.delete_history,
    #     inputs=[game_name],
    #     outputs=render_array,
    #     queue=False
    # )

    # # Load the game on enter
    # game_name.submit(
    #     fn=game.load_history,
    #     inputs=[game_name],
    #     outputs=render_array,
    #     queue=False
    # )

    # # Load the game on button click
    # load_game.click(
    #     fn=game.load_history,
    #     inputs=[game_name],
    #     outputs=render_array,
    #     queue=False
    # )

    # # Save the game on button click
    # save_game.click(
    #     fn=game.save_history,
    #     inputs=[game_name],
    #     outputs=[],
    #     queue=False
    # )