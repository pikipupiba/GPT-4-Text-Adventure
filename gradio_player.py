# TODO:
# 1. populate stats section from response
# 2. sliders to control HOW risky, loud, etc. the action is
# 3. populate tokens section from response
# 4. dropdown to select model

import gradio as gr
from gradio_gm import *
from GPTBot import *
from session import *

gm_bot = GPTBot("GM")
# player_bot = GPTBot("Player")

# slider = gr.Slider(minimum=0, maximum=100, step=1, value=50, label="Slider")

# PLAYER TAB
player_tab = gr.Blocks()
with player_tab:
    # STORY AREA
    story_area = gr.Row(variant="compact")
    with story_area:
        # CHAT
        chat_area = gr.Column(scale=10, variant="compact")
        with chat_area:
            # HISTORY
            with gr.Row() as history_area:
                # gr.ChatInterface(fn=gm_bot.predict, additional_inputs=[slider]).queue()
                # chat = gr.ChatInterface(fn=gm_bot.predict, chatbot=chatbot)
                chatbot = gr.Chatbot(value=load_current_chat_history)
            # USER INPUT
            with gr.Column() as message_area:
                with gr.Row():
                    player_message = gr.Textbox(lines=1, label="Player Message", interactive=True)
                    # submit = gr.Button(label="Submit", scale=1)
                with gr.Row():
                    retry = gr.Button(value="Retry")
                    undo = gr.Button(value="Undo")
                    clear = gr.ClearButton([chatbot, player_message])
        # STATS
        stats_area = gr.Column(scale=1, variant="compact")
        with stats_area:
            day_box = gr.Textbox(lines=1, label="Game Time", interactive=False)
            items_box = gr.Textbox(lines=5, label="Items", interactive=False)
            friends_box = gr.Textbox(lines=10, label="Friend Stats", interactive=False)

    # DEBUG AREA
    with gr.Column(variant="compact") as debug_area:
        with gr.Row():
            last_tokens = gr.Textbox(lines=1, label="Last Token", interactive=False)
            total_tokens = gr.Textbox(lines=1, label="Total Tokens", interactive=False)
            tokens_per_minute = gr.Textbox(lines=1, label="TPM", interactive=False)
        with gr.Row():
            tokens_json = gr.JSON(label="Tokens", interactive=False)
    
    # CHAT FUNCTIONS
    player_message.submit(
        fn=lambda msg,history: ["", history + [[msg, None]]], 
        inputs=[player_message, chatbot],
        outputs=[player_message, chatbot],
        queue=False
        ).then(
            fn=gm_bot.predict,
            inputs=[chatbot],
            outputs=[chatbot],
            queue=True
            ).then(
                fn=save_current_chat_history,
                inputs=[chatbot],
                outputs=[],
                queue=False
                ).then(
                    fn=gm_bot.get_tokens,
                    inputs=None,
                    outputs=[tokens_json],
                )
    
    retry.click(
        fn=lambda history: history[:-1] + [[history[-1][0], None]],
        inputs=[chatbot],
        outputs=[chatbot],
        queue=False
        ).then(
            fn=gm_bot.predict,
            inputs=[chatbot],
            outputs=[chatbot],
            queue=True
            ).then(
                fn=save_current_chat_history,
                inputs=[chatbot],
                outputs=[],
                queue=False
                ).then(
                    fn=gm_bot.get_tokens,
                    inputs=None,
                    outputs=[tokens_json],
                )
    
    undo.click(
        fn=lambda history: history[:-1],
        inputs=[chatbot],
        outputs=[chatbot],
        queue=False
        )
    # submit.click(fn=submit_message, inputs=[input_box, gm_message, story_box, total_tokens, dice_box], outputs=[story_box, day_box, items_box, friends_box, last_tokens, total_tokens, tokens_per_minute])