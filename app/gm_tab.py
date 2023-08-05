# TODO:
# 1. dropdown with saved sessions
# 2. 

import gradio as gr
from session import *

# GM TAB
with gr.Blocks() as gm_tab:

    # SAVE/LOAD SESSION
    with gr.Group(): #.style(equal_height=True):
        with gr.Row():
            file_name = gr.Textbox(
                            value="current_system_message",
                            lines=1,
                            show_label=False,
                            interactive=True,
                            scale=7,
                            )
            save = gr.Button(value="Save", scale=1, size="sm")
            load = gr.Button(value="Load", scale=1, size="sm")
            mode = gr.Radio(
                    choices=["Overwrite", "Prepend", "Append"],
                    show_label=False,
                    value="Overwrite",
                    scale=3)
        
    # SYSTEM MESSAGE
    system_message = gr.Textbox(
                        lines=40,
                        label="System",
                        interactive=True,
                        scale=1,
                        value=load_current_system_message)
    
    example_history = gr.Code(
                        lines=40,
                        label="Example History",
                        interactive=True,
                        scale=1,
                        value=load_current_example_history,
                        language="json")

    # GM TAB FUNCTIONS
    save.click(
        fn=save_session,
        inputs=[file_name, system_message],
        outputs=[]
        )
    
    load.click(
        fn=load_session,
        inputs=[file_name, system_message, mode],
        outputs=[system_message]
        )

    system_message.change(
        fn=save_current_system_message,
        inputs=[system_message],
        outputs=[],
        queue=False
        )
    
    example_history.change(
        fn=save_current_example_history,
        inputs=[example_history],
        outputs=[],
        queue=False
        )