import gradio as gr

from PythonClasses.Game.FileManager import FileManager

use_models = [
    "gpt-4-0613",
    "gpt-3.5-turbo-0613",
    "gpt-3.5-turbo-16k-0613"
]

with gr.Blocks() as config_tab:
    debug_mode = gr.Checkbox(label="Debug Mode", default=True)

    # SELECT MODEL
    select_model = gr.Dropdown(
        choices=use_models,
        label="Select Model",
        value=use_models[0],
        scale=1,
    )

    with gr.Group():
        retry = gr.Button(value="Retry", size="sm")
        undo = gr.Button(value="Undo", size="sm")
        clear = gr.Button(value="Clear", size="sm")