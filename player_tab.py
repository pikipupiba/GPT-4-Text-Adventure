# TODO:
# 1. populate stats section from response
# 2. sliders to control HOW risky, loud, etc. the action is

import gradio as gr
from gm_tab import *
from LLM import *
from TokenTracker import *
from session import *

# LLM MODELS
llm = LLM([
    "gpt-3.5-turbo-0613",
    "gpt-3.5-turbo-16k-0613",
    "gpt-4-0613",
    "gpt-4-32k-0613",
])

# PLAYER TAB
player_tab = gr.Blocks()
with player_tab:
    game_state = gr.State(value=load_game_state)
    # STORY AREA
    with gr.Row(variant="compact") as story_area:
        # CHAT
        with gr.Column(scale=10, variant="compact") as chat_area:
            # HISTORY
            with gr.Row() as history_area:
                chatbot = gr.Chatbot(value=load_current_chat_history, height=600)
            # USER INPUT
            with gr.Group():
                with gr.Row() as user_area:
                    model = gr.Dropdown(
                        choices=["gpt-3.5-turbo-0613", "gpt-3.5-turbo-16k-0613", "gpt-4-0613", "gpt-4-32k-0613"],
                        label="Model",
                        value="gpt-4-0613",
                        scale=1,
                        )
                    player_message = gr.Textbox(lines=1, label="Player Message", interactive=True, scale=20)
                    submit = gr.Button(value="Do it!", scale=1, size="sm")
                    # with gr.Column(scale=1, variant="compact"):
                    with gr.Group():
                        retry = gr.Button(value="Retry", size="sm")
                        undo = gr.Button(value="Undo", size="sm")
                        clear = gr.ClearButton([chatbot, player_message], size="sm")
            # AI INPUT
            # ai_chatbot = gr.Chatbot(value=load_current_chat_history_inverted, visible=False)
            # with gr.Group():
            #     with gr.Row() as ai_area:
            #         ai_model = gr.Dropdown(
            #             choices=["gpt-3.5-turbo-0613", "gpt-3.5-turbo-16k-0613", "gpt-4-0613", "gpt-4-32k-0613"],
            #             label="AI Model",
            #             value="gpt-3.5-turbo-0613",
            #             scale=1,
            #             )
            #         ai_message = gr.Textbox(lines=1, label="AI Player Message", interactive=False, scale=20)
            #         ai_submit = gr.Button(value="Do it!", scale=1, size="sm")
            #         # with gr.Column(scale=1, variant="compact"):
            #         with gr.Group():
            #             ai_retry = gr.Button(value="AI Retry", size="sm")
            #             ai_generate = gr.Button(value="Generate", size="sm")
        # STATS
        with gr.Column(scale=1, variant="compact") as stats_area:
            team_name = gr.Textbox(lines=1, label="Team Name", interactive=True)
            with gr.Group():
                day_box = gr.Textbox(lines=1, label="Game Time", interactive=False)
                items_box = gr.Textbox(lines=5, label="Items", interactive=False)
                friends_box = gr.Textbox(lines=10, label="Friend Stats", interactive=False)

    # DEBUG AREA
    with gr.Column(variant="compact") as debug_area:
        with gr.Row():
            token_jsons = []
            for model_name,tracker in TokenTracker.trackers.items():
                token_jsons.append(gr.JSON(label=f"{model_name} Tokens", interactive=False))
        game_state_json = gr.JSON(label="Game State")
    
    # PLAYER TAB FUNCTIONS
    team_name.submit(
        fn=load_game_state,
        inputs=[team_name],
        outputs=[game_state_json],
        queue=False
    )

    def render_game_state(state):
        print("RENDERING GAME STATE!!!")
        return (state["team_name"], state["chatbot"], state["day_box"], state["items_box"], state["friends_box"])

    game_state_json.change(
        fn=render_game_state,
        inputs=[game_state],
        outputs=[team_name, chatbot, day_box, items_box, friends_box],
        queue=False
        )

    submits = []
    submits.append(submit.click(
        fn=lambda msg,history: ["", history + [[msg, None]]], 
        inputs=[player_message, chatbot],
        outputs=[player_message, chatbot],
        queue=False
        ))
    
    # submits.append(ai_submit.click(
    #     fn=lambda msg,history: ["", history + [[msg, None]]], 
    #     inputs=[ai_message, chatbot],
    #     outputs=[ai_message, chatbot],
    #     queue=False
    #     ))

    submits.append(player_message.submit(
        fn=lambda msg,history: ["", history + [[msg, None]]], 
        inputs=[player_message, chatbot],
        outputs=[player_message, chatbot],
        queue=False
        ))
    
    submits.append(retry.click(
        fn=lambda history: history[:-1] + [[history[-1][0], None]],
        inputs=[chatbot],
        outputs=[chatbot],
        queue=False
        ))
    
    for item in submits:
        predict = item.then(
            fn=llm.predict,
            inputs=[model,system_message,example_history,chatbot],
            outputs=[chatbot],
            queue=True
            )
        
        parse_stats_please = predict.then(
            fn=parse_stats,
            inputs=[chatbot],
            outputs=[day_box, items_box, friends_box],
            queue=False
            )

        save_state = parse_stats_please.then(
            fn=save_game_state,
            inputs=[team_name, chatbot, day_box, items_box, friends_box],
            outputs=[game_state],
            queue=False
            ).then(
                fn=lambda x:x,
                inputs=[game_state],
                outputs=[game_state_json],
                queue=False
                )

        get_tokens = predict.then(
            fn=LLM.get_all_tokens,
            inputs=None,
            outputs=token_jsons,
            queue=False
            )
    
    undo.click(
        fn=lambda history: history[:-1],
        inputs=[chatbot],
        outputs=[chatbot],
        queue=False
        )
        
    # ai_generate.click(
    #     fn=llm.predict,
    #     inputs=[ai_model, system_message_2 ,ai_chatbot],
    #     outputs=[ai_chatbot],
    #     queue=True
    #     ).then(
    #         fn=lambda history: history[-1][1],
    #         inputs=[ai_chatbot],
    #         outputs=[ai_message],
    #         queue=False
    #         )
    
    # for token_json in token_jsons:
    #     token_json.change(
    #         fn=lambda x: print("Changin' here boss..."),
    #         inputs=[],
    #         outputs=[],
    #         queue=False
    #         )