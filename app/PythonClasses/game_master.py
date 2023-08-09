# TODO:
# 1. dropdown with saved sessions
# 2. 

from PythonClasses.player import game

import gradio as gr

# GM TAB
with gr.Blocks() as gm_tab:

    # SAVE/LOAD SESSION
    with gr.Group(): #.style(equal_height=True):
        with gr.Row():
            with gr.Row():
                system_name = gr.Textbox(
                    value="BEST",
                    lines=1,
                    show_label=False,
                    interactive=True,
                    scale=7,
                )
                select_system = gr.Dropdown(
                    choices=["BEST", "BAH"],
                    label="System",
                    scale=1,
                )
            with gr.Row():
                example_name = gr.Textbox(
                    value="BEST",
                    lines=1,
                    show_label=False,
                    interactive=True,
                    scale=7,
                )
                select_example = gr.Dropdown(
                    choices=["BEST", "BAH"],
                    label="System",
                    scale=1,
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
        fn=game.save_system_message,
        inputs=[system_name],
        outputs=[]
    )
    
    load.click(
        fn=game.load_system_message,
        inputs=[system_name],
        outputs=[system_message]
    )
    
    # example_history.change(
    #     fn=game.state.system_message.update_example_history,
    #     inputs=[example_history],
    #     outputs=[],
    #     queue=False
    # )