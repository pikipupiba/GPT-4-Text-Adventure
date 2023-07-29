import gradio as gr
from session import *

with gr.Blocks() as game_master_area:
    with gr.Row():
        with gr.Row():
            file_name = gr.Textbox(lines=1, show_label=False, interactive=True, scale=10, value="YeeYeeBaby")
            save = gr.Button(value="Save", scale=1)
            load = gr.Button(value="Load", scale=1)
        mode = gr.Radio(["Overwrite", "Prepend", "Append"], show_label=False, value="Overwrite")

    system_message = gr.Textbox(lines=10, label="System", interactive=True, scale=10, value="")

    save.click(fn=save_session, inputs=[file_name, system_message], outputs=[])
    load.click(fn=load_session, inputs=[file_name, system_message, mode], outputs=[system_message])