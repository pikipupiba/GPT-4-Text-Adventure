# TODO:
# 1. dropdown with saved sessions
# 2. 

import gradio as gr
from PythonClasses.Game.SystemMessage import SystemMessage

system = SystemMessage()

# GM TAB
with gr.Blocks() as gm:

    # SAVE/LOAD SESSION
    with gr.Group(): #.style(equal_height=True):
        with gr.Row():
            system_name = gr.Textbox(
                            value="",
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
                        value="")
    
    example_history = gr.Code(
                        lines=40,
                        label="Example History",
                        interactive=True,
                        scale=1,
                        value="",
                        language="json")

    # GM TAB FUNCTIONS
    save.click(
        fn=system.save_system_message,
        inputs=[],
        outputs=[]
    )
    
    load.click(
        fn=system.load_system_message,
        inputs=[mode],
        outputs=[system_message]
    )
    
    system_name.change(
        fn=system.change_name,
        inputs=[system_name],
        outputs=[],
        queue=False
    )

    system_message.change(
        fn=system.update_system_message,
        inputs=[system_message],
        outputs=[],
        queue=False
    )
    
    example_history.change(
        fn=system.update_example_history,
        inputs=[example_history],
        outputs=[],
        queue=False
    )