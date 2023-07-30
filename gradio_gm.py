# TODO:
# 1. dropdown with saved sessions
# 2. 

import gradio as gr
from session import *

with gr.Blocks() as game_master_area:
    with gr.Row().style(equal_height=True):
        file_name = gr.Textbox(
                        value="current_system_message",
                        lines=1,
                        show_label=False,
                        interactive=True,
                        scale=8,
                        )
        save = gr.Button(value="Save", scale=1)
        load = gr.Button(value="Load", scale=1)
        mode = gr.Radio(["Overwrite", "Prepend", "Append"], show_label=False, value="Overwrite", scale=3)

    system_message = gr.Textbox(lines=40, label="System", interactive=True, scale=1, value=load_current_system_message)

    save.click(fn=save_session, inputs=[file_name, system_message], outputs=[])
    load.click(fn=load_session, inputs=[file_name, system_message, mode], outputs=[system_message])

    system_message.change(fn=save_current_system_message, inputs=[system_message], outputs=[])