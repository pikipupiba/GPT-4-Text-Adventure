# TODO:
# 1. populate stats section from response
# 2. sliders to control HOW risky, loud, etc. the action is
# 3. populate tokens section from response
# 4. dropdown to select model

import gradio as gr
from gm_tab import *
from LLM import *
from TokenTracker import *
from session import *

# LLM MODELS
llms = {
    "gpt-3.5-turbo-0613": LLM("gpt-3.5-turbo-0613"),
    "gpt-3.5-turbo-16k-0613": LLM("gpt-3.5-turbo-16k-0613"),
    "gpt-4-0613": LLM("gpt-4-0613"),
    "gpt-4-32k-0613": LLM("gpt-4-32k-0613"),
}

# PLAYER TAB
player_tab = gr.Blocks()
with player_tab:
    # STORY AREA
    with gr.Row(variant="compact") as story_area:
        # CHAT
        with gr.Column(scale=10, variant="compact") as chat_area:
            # HISTORY
            with gr.Row() as history_area:
                chatbot = gr.Chatbot(value=load_current_chat_history)
            # USER INPUT
            # with gr.Column() as message_area:
            with gr.Row() as message_area:
                model = gr.Dropdown(
                    choices=["gpt-3.5-turbo-0613", "gpt-3.5-turbo-16k-0613", "gpt-4-0613", "gpt-4-32k-0613"],
                    label="Model",
                    default="gpt-3.5-turbo-0613",
                    scale=1,
                    )
                player_message = gr.Textbox(lines=1, label="Player Message", interactive=True, scale=20)
                submit = gr.Button(value="Do it!", scale=1, size="sm")
                # with gr.Column(scale=1, variant="compact"):
                with gr.Group(scale=1):
                    retry = gr.Button(value="Retry", size="sm")
                    undo = gr.Button(value="Undo", size="sm")
                    clear = gr.ClearButton([chatbot, player_message], size="sm")
        # STATS
        stats_area = gr.Column(scale=1, variant="compact")
        with stats_area:
            day_box = gr.Textbox(lines=1, label="Game Time", interactive=False)
            items_box = gr.Textbox(lines=5, label="Items", interactive=False)
            friends_box = gr.Textbox(lines=10, label="Friend Stats", interactive=False)

    # DEBUG AREA
    with gr.Column(variant="compact") as debug_area:
        with gr.Row():
            token_jsons = {}
            for model,tracker in TokenTracker.trackers.items():
                token_jsons[model] = gr.JSON(label=f"{model} Tokens", interactive=False)
    
    # PLAYER TAB FUNCTIONS
    submit.click(
        fn=lambda msg,history: ["", history + [[msg, None]]], 
        inputs=[player_message, chatbot],
        outputs=[player_message, chatbot],
        queue=False
        ).then(
            fn=llm.predict,
            inputs=[model, system_message,chatbot],
            outputs=[chatbot],
            queue=True
            ).then(
                fn=save_current_chat_history,
                inputs=[chatbot],
                outputs=[],
                queue=False
                ).then(
                    fn=LLM.get_all_tokens,
                    inputs=None,
                    outputs=token_jsons,
                )
    
    player_message.submit(
        fn=lambda msg,history: ["", history + [[msg, None]]], 
        inputs=[player_message, chatbot],
        outputs=[player_message, chatbot],
        queue=False
        ).then(
            fn=llm.predict,
            inputs=[system_message,chatbot],
            outputs=[chatbot],
            queue=True
            ).then(
                fn=save_current_chat_history,
                inputs=[chatbot],
                outputs=[],
                queue=False
                ).then(
                    fn=LLM.get_all_tokens,
                    inputs=None,
                    outputs=token_jsons,
                )
    
    retry.click(
        fn=lambda history: history[:-1] + [[history[-1][0], None]],
        inputs=[chatbot],
        outputs=[chatbot],
        queue=False
        ).then(
            fn=llm.predict,
            inputs=[system_message,chatbot],
            outputs=[chatbot],
            queue=True
            ).then(
                fn=save_current_chat_history,
                inputs=[chatbot],
                outputs=[],
                queue=False
                ).then(
                    fn=LLM.get_all_tokens,
                    inputs=None,
                    outputs=token_jsons,
                )
    
    undo.click(
        fn=lambda history: history[:-1],
        inputs=[chatbot],
        outputs=[chatbot],
        queue=False
        )
    # submit.click(fn=submit_message, inputs=[input_box, gm_message, story_box, total_tokens, dice_box], outputs=[story_box, day_box, items_box, friends_box, last_tokens, total_tokens, tokens_per_minute])