# import gradio as gr

# from PythonClasses.player import *

# from PythonClasses.Game.FileManager import FileManager
# from PythonClasses.Game.Game import Game

# use_models = [
#     "gpt-4-0613",
#     "gpt-3.5-turbo-0613",
#     "gpt-3.5-turbo-16k-0613"
# ]

# with combined:
#     with gr.Tab("Config") as config_tab:

#         with gr.Group():
#             with gr.Row():
#                 # SELECT MODEL
#                 select_model = gr.Radio(
#                     choices=use_models,
#                     label="Select Model",
#                     value=use_models[0],
#                     scale=1,
#                 )
#                 retry = gr.Button(value="Retry", size="sm")
#                 undo = gr.Button(value="Undo", size="sm")
#                 clear = gr.Button(value="Clear", size="sm")
#                 restart = gr.Button(value="Restart", size="sm")

#         # GAME NAME
#         with gr.Group():
#             with gr.Row():
#                 history_name = gr.Textbox(
#                     value="BAH",
#                     lines=1,
#                     label="History Name",
#                     interactive=True,
#                     scale=1,
#                 )

#                 save_game = gr.Button(value="Save", size="sm")
#                 delete_game = gr.Button(value="Delete", size="sm")
#                 load_game = gr.Button(value="Load", size="sm")

#                 select_history_name = gr.Dropdown(
#                     choices=FileManager.get_file_names(FileManager.HISTORY_FOLDER),
#                     show_label=True,
#                     label="Select History",
#                     scale=1,
#                 )

#         # DEBUG AREA
#         with gr.Column(variant="compact") as debug_area:
#             # with gr.Row():
#             #     token_jsons = []
#             #     for model_name,tracker in TokenTracker.trackers.items():
#             #         token_jsons.append(gr.JSON(label=f"{model_name} Token Tracker", interactive=False))
#             execution_json = gr.JSON(label="Execution Info")
#             turn_json = gr.JSON(label="Game State")


#         config_render_array = [
#             execution_json,
#             turn_json,
#         ]
