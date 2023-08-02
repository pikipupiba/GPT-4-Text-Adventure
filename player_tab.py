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
# 11. Dropdown to select team name from saved sessions

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

# Game instance
game = Game(models=use_models)

# PLAYER TAB
with gr.Blocks() as player_tab:
    # STORY AREA
    with gr.Row(variant="compact") as story_area:
        # CHAT AREA
        with gr.Column(scale=10, variant="compact") as chat_area:
            # CHATBOT
            with gr.Row() as history_area:
                chatbot = gr.Chatbot(height=600)
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
                    load_team_state = gr.Button(value="Load Team State", size="sm")
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
                token_jsons.append(gr.JSON(label=f"{model_name} Token Tracker", interactive=False))
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
            fn=game.retry,
            inputs=[game_state_json],
            outputs=[game_state_json, chatbot],
            queue=False
        )
    ]
    
    # What happens after the player submits a message
    for item in submits:
        # Generate the assistant message
        predict = item.then(
            fn=game.predict,
            inputs=[model,system_message,example_history,chatbot],
            outputs=[chatbot],
            queue=True
        )
        
        # Display stats that were parsed from the assistant message
        render_stats = predict.then(
            fn=game.render_stats,
            inputs=[],
            outputs=[day_box, items_box, friends_box],
            queue=False
        )

        # Save the game state after populating the stats boxes
        save_state = render_stats.then(
            fn=game.save_game_state,
            inputs=[team_name],
            outputs=[game_state_json],
            queue=False
        )

        # Update the token trackers
        get_tokens = save_state.then(
            fn=game.get_all_tokens,
            inputs=[],
            outputs=token_jsons,
            queue=False
        )
    
    #--------------------------------------------------------------
    # AUXILIARY FUNCTIONS
    #--------------------------------------------------------------
    # Clear all story boxes
    clear.click(
        fn=game.clear,
        inputs=[game_state_json],
        outputs=[game_state_json],
    ),

    # Load the game state from the team name on enter
    team_name.submit(
        fn=game.load_game_state,
        inputs=[team_name],
        outputs=[game_state_json],
        queue=False
    )
    # Load the game state from the team name on button click
    load_team_state.click(
        fn=game.load_game_state,
        inputs=[team_name],
        outputs=[game_state_json],
        queue=False
    )

    # Update all story boxes when the game state json changes
    game_state_json.change(
        fn=game.render_game_state,
        inputs=[],
        outputs=[team_name, chatbot, player_message, day_box, items_box, friends_box],
        queue=False
    )

    # Undo the last user and assistant message
    undo.click(
        fn=game.undo,
        inputs=[game_state_json],
        outputs=[game_state_json],
        queue=False
    )