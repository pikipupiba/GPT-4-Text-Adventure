import gradio as gr

from PythonClasses.Game.FileManager import FileManager
from PythonClasses.player import game


# GM TAB
with gr.Blocks() as gm_tab:

    with gr.Group():
        # SAVE/LOAD SESSION
        with gr.Row():
            system_name = gr.Textbox(
                value="BEST",
                lines=1,
                show_label=True,
                label="System Message Name",
                interactive=True,
                scale=2,
            )

            save_system_message = gr.Button(value="Save", scale=1, size="sm")
            load_system_message = gr.Button(value="Load", scale=1, size="sm")

            select_system_message = gr.Dropdown(
                choices=FileManager.get_file_names(FileManager.SYSTEM_FOLDER),
                show_label=True,
                label="Select System Message",
                scale=2,
            )
            
        with gr.Row():
            example_history_name = gr.Textbox(
                value="",
                lines=1,
                show_label=True,
                label="Example History Name",
                interactive=True,
                scale=2,
            )

            save_example_history = gr.Button(value="Save", scale=1, size="sm")
            load_example_history = gr.Button(value="Load", scale=1, size="sm")

            select_example_history = gr.Dropdown(
                choices=FileManager.get_file_names(FileManager.EXAMPLE_HISTORY_FOLDER),
                show_label=True,
                label="Select Example History",
                scale=2,
            )

    load_mode = gr.Radio(
            choices=["Overwrite", "Prepend", "Append"],
            show_label=False,
            value="Overwrite",
            scale=2)
        
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
    save_system_message.click(
        fn=game.save_system_message,
        inputs=[system_name, system_message],
        outputs=[],
        queue=False
    )
    
    load_system_message.click(
        fn=game.load_system_message,
        inputs=[select_system_message],
        outputs=[system_message],
        queue=False
    )

    select_system_message.change(
        fn=game.load_system_message,
        inputs=[select_system_message],
        outputs=[system_message],
        queue=False
    )

    save_system_message.click(
        fn=game.save_system_message,
        inputs=[system_name, system_message],
        outputs=[],
        queue=False
    )
    
    load_example_history.click(
        fn=game.load_example_history,
        inputs=[select_example_history],
        outputs=[example_history],
        queue=False
    )

    select_example_history.change(
        fn=game.load_example_history,
        inputs=[select_example_history],
        outputs=[example_history],
        queue=False
    )

    
    
    # example_history.change(
    #     fn=game.state.system_message.update_example_history,
    #     inputs=[example_history],
    #     outputs=[],
    #     queue=False
    # )