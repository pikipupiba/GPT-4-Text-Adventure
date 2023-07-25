import gradio as gr
from gm import *
from openai_helpers import *

with gr.Blocks() as player_area:
    with gr.Row(variant="compact") as yee:
        with gr.Column(scale=10, variant="compact") as story_area:
            story_box = gr.Textbox(lines=12, label="Story", interactive=True, value="Please choose 5 items.")
            with gr.Row():
                input_box = gr.Textbox(lines=1, label="Input", interactive=True, scale=10, value="pen, pencil, marker, chalk, cell phone")
                submit = gr.Button(value="Submit", scale=1)
        with gr.Column(scale=1, variant="compact") as stats_area:
            day_box = gr.Textbox(lines=1, label="Game Time", interactive=False)
            items_box = gr.Textbox(lines=5, label="Items", interactive=False)
            friends_box = gr.Textbox(lines=10, label="Friend Stats", interactive=False)

    submit.click(fn=submit_message, inputs=[input_box, gm_message, story_box], outputs=[story_box, day_box, items_box, friends_box])