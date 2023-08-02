import gradio as gr
from session import *



with gr.Blocks() as message_area:
    with gr.Row() as config:
        file_name = gr.Textbox(lines=1, label="File Name", interactive=True, scale=3, value="")
        save = gr.Button(value="Save", scale=1)
        load = gr.Button(value="Load", scale=1)
    for i in range(20):
        with gr.Row():
            toggle = gr.Checkbox(label="", scale=1)
            order = gr.Number(label="Order", minimum=-1, precision=0, scale=1, show_label=False)
            # move_up = gr.Button(value="Move Up", scale=1)
            # move_down = gr.Button(value="Move Down", scale=1)
            role = gr.Dropdown(label="Role", choices=["System", "Assistant", "User"], scale=1, show_label=False)
            content = gr.Textbox(lines=1, label="Content", interactive=True, scale=10, value="", show_label=False)


# with gr.Blocks() as message_area:
#     with gr.Row():
#         with gr.Column(scale=1, variant="compact"):
#             order = gr.Number(label="Order", minimum=-1, precision=0, scale=1, show_label=False)
#             order2 = gr.Number(label="Order", minimum=-1, precision=0, scale=1, show_label=False)
#         with gr.Column(scale=1, variant="compact"):
#             role = gr.Dropdown(label="Role", choices=["System", "Assistant", "User"], scale=1, show_label=False)
#             role2 = gr.Dropdown(label="Role", choices=["System", "Assistant", "User"], scale=1, show_label=False)
#         with gr.Column(scale=10, variant="compact"):
#             content = gr.Textbox(lines=1, label="Content", interactive=True, scale=10, value="", show_label=False)
#             content2 = gr.Textbox(lines=1, label="Content", interactive=True, scale=10, value="", show_label=False)