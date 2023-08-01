# TODO:
#-1. !!!REFACTOR CODE!!!
# 0. AWS BABY!!!
# 1. state to save raw chat history
# 2. sliders for character stats
# 3. emojis to indicate emotions
# 4. auto send next day message
# 6. define end of game
# 7. make an unlocked system message
# 8. try to make the story more interesting
#    - add more characters with more agency
#    - special events/plot twists (on friday)
#       - timeout, thunderstorm (inside that day), get sick, field trip
# 9. fix dice rolls
# 10. add session functionality

import gradio as gr
from gm_tab import *
from Game import *
from TokenTracker import *
from session import *

use_models = [
    "gpt-4-0613",
    "gpt-3.5-turbo-0613",
    "gpt-3.5-turbo-16k-0613"
]

# LLM MODELS
llm = Game(use_models)

# PLAYER TAB
with gr.Blocks() as player_tab:
    game_state = gr.State(value=load_game_state)
    # STORY AREA
    with gr.Row(variant="compact") as story_area:
        # CHAT AREA
        with gr.Column(scale=10, variant="compact") as chat_area:
            # CHATBOT
            with gr.Row() as history_area:
                chatbot = gr.Chatbot(value=load_current_chat_history, height=600)
            # USER INPUT
            with gr.Group():
                with gr.Row() as user_area:
                    # MODEL
                    model = gr.Dropdown(
                        choices=use_models,
                        label="Model",
                        value=use_models[0],
                        scale=1,
                        )
                    # MESSAGE
                    player_message = gr.Textbox(lines=1, label="Player Message", interactive=True, scale=20)
                    # BUTTONS
                    submit = gr.Button(value="Do it!", scale=1, size="sm")
                    with gr.Group():
                        retry = gr.Button(value="Retry", size="sm")
                        undo = gr.Button(value="Undo", size="sm")
                        clear = gr.Button(value="Clear", size="sm")
        # TEAM/STATS AREA
        with gr.Column(scale=1, variant="compact") as stats_area:
            # TEAM NAME
            with gr.Group():
                with gr.Row():
                    team_name = gr.Textbox(lines=1, label="Team Name", interactive=True)
                    load_team_state = gr.Button(value="Load", size="sm")
            # STATS
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


    #--------------------------------------------------------------
    #                      PLAYER TAB FUNCTIONS
    #--------------------------------------------------------------
    
    #--------------------------------------------------------------
    # SUBMIT FUNCTIONS
    #--------------------------------------------------------------
    submits = [
        # Click "Do it!" button
        submit.click(
            # Add the player message to the history
            fn=lambda msg,history: ["", history + [[msg, None]]], 
            inputs=[player_message, chatbot],
            outputs=[player_message, chatbot],
            queue=False
        ),
        # Press enter key
        player_message.submit(
            # Add the player message to the history
            fn=lambda msg,history: ["", history + [[msg, None]]], 
            inputs=[player_message, chatbot],
            outputs=[player_message, chatbot],
            queue=False
        ),
        # Click "Retry" button
        retry.click(
            # Remove the last assistant message from the history
            fn=lambda history: history[:-1] + [[history[-1][0], None]],
            inputs=[chatbot],
            outputs=[chatbot],
            queue=False
        )
    ]
    
    # What happens after the player submits a message
    for item in submits:
        # Generate the assistant message
        predict = item.then(
            fn=llm.predict,
            inputs=[model,system_message,example_history,chatbot],
            outputs=[chatbot],
            queue=True
        )
        
        # Display stats that were parsed from the assistant message
        parse_stats_please = predict.then(
            fn=parse_stats,
            inputs=[chatbot],
            outputs=[day_box, items_box, friends_box],
            queue=False
        )

        # Save the game state after populating the stats boxes
        save_state = parse_stats_please.then(
            fn=save_game_state,
            inputs=[team_name, chatbot, day_box, items_box, friends_box],
            outputs=[game_state],
            queue=False
        ).then(
            # Update the game state json box from the game state
            fn=lambda x:x,
            inputs=[game_state],
            outputs=[game_state_json],
            queue=False
            )

        # Update the token trackers
        get_tokens = predict.then(
            fn=LLM.get_all_tokens,
            inputs=None,
            outputs=token_jsons,
            queue=False
        )
    
    #--------------------------------------------------------------
    # AUXILIARY FUNCTIONS
    #--------------------------------------------------------------
    # Clear all story boxes
    clear.click(
        fn=lambda:["","","","","",""],
        inputs=[],
        outputs=[player_message, chatbot, team_name, day_box, items_box, friends_box],
    ),

    # Load the game state from the team name on enter
    team_name.submit(
        fn=load_game_state,
        inputs=[team_name],
        outputs=[game_state_json],
        queue=False
    )
    # Load the game state from the team name on button click
    load_team_state.click(
        fn=load_game_state,
        inputs=[team_name],
        outputs=[game_state_json],
        queue=False
    )

    # Break game state apart for rendering
    def render_game_state(state):
        return (state["team_name"], state["chatbot"], state["day_box"], state["items_box"], state["friends_box"])
    # Update all story boxes when the game state json changes
    game_state_json.change(
        fn=render_game_state,
        inputs=[game_state],
        outputs=[team_name, chatbot, day_box, items_box, friends_box],
        queue=False
    )

    # Undo the last user and assistant message
    undo.click(
        fn=lambda history: history[:-1],
        inputs=[chatbot],
        outputs=[chatbot],
        queue=False
    )