import gradio as gr

from PythonClasses.Game.FileManager import FileManager

# GM TAB
with gr.Blocks() as gm_tab:

    with gr.Group():
        # SAVE/LOAD SESSION
        with gr.Row():
            system_message_name = gr.Textbox(
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
                choices=FileManager.get_file_names(FileManager.SYSTEM_MESSAGE_FOLDER),
                show_label=True,
                label="Select System Message",
                scale=2,
            )
            
        # with gr.Row():
        #     example_history_name = gr.Textbox(
        #         value="",
        #         lines=1,
        #         show_label=True,
        #         label="Example History Name",
        #         interactive=True,
        #         scale=2,
        #     )

        #     save_example_history = gr.Button(value="Save", scale=1, size="sm")
        #     load_example_history = gr.Button(value="Load", scale=1, size="sm")

        #     select_example_history = gr.Dropdown(
        #         choices=FileManager.get_file_names(FileManager.EXAMPLE_HISTORY_FOLDER),
        #         show_label=True,
        #         label="Select Example History",
        #         scale=2,
        #     )

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
                        value=FileManager.load_system_message("BEST_system_message"),
                    )
    
    # example_history = gr.Code(
    #                     lines=40,
    #                     label="Example History",
    #                     interactive=True,
    #                     scale=1,
    #                     value="",
    #                     language="json")

    # GM TAB FUNCTIONS
    save_system_message.click(
        fn=FileManager.save_system_message,
        inputs=[system_message_name, system_message],
        outputs=[],
        queue=False
    )
    
    load_system_message.click(
        fn=FileManager.load_system_message,
        inputs=[select_system_message],
        outputs=[system_message],
        queue=False
    )

    select_system_message.change(
        fn=FileManager.load_system_message,
        inputs=[select_system_message],
        outputs=[system_message],
        queue=False
    )

    save_system_message.click(
        fn=FileManager.save_system_message,
        inputs=[system_message_name, system_message],
        outputs=[],
        queue=False
    )
    
    # load_example_history.click(
    #     fn=FileManager.load_example_history,
    #     inputs=[select_example_history],
    #     outputs=[example_history],
    #     queue=False
    # )

    # select_example_history.change(
    #     fn=FileManager.load_example_history,
    #     inputs=[select_example_history],
    #     outputs=[example_history],
    #     queue=False
    # )