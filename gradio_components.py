import gradio as gr

from openai import *

with gr.Blocks() as player_area:
    chatbot = gr.ChatInterface(submit_message)
    msg = gr.Textbox()
    clear = gr.ClearButton([msg, chatbot])

with gr.Blocks() as game_master_area:
    system_message = gr.Textbox(lines=40, label="System Message", interactive=True)

game_area = gr.TabbedInterface([game_master_area, player_area], ["Game Master", "Player"])