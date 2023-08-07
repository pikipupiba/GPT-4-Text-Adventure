# TODO:
#-1. !!!REFACTOR CODE!!!
# 0. AWS BABY!!!
# [done] 1. state to save raw chat history
# 2. sliders for character stats
# 2a. OR JUST FOR TEMPERATURE (limited range to maintain AI sanity)
# 3. emojis to indicate emotions
# 4. auto send next day message
# 6. define end of game
# 8. try to make the story more interesting
#    - add more characters with more agency
#    - special events/plot twists (on friday)
#       - timeout, thunderstorm (inside that day), get sick, field trip
# [almost] 9. fix dice rolls
# 10. add session functionality
# 11. Dropdown to select team name from saved sessions
# 12. Countdown timer bar + allow everyone to answer + average actions :) :) :)
# 12a. ABOVE IDEA IS AN ABSOLUTE GAME CHANGER
# 12b. Sometimes the timer will be short and it will single someone out to respond quickly

import gradio as gr
from PythonClasses.Game.Game import Game

use_models = [
    "gpt-4-0613",
    "gpt-3.5-turbo-0613",
    "gpt-3.5-turbo-16k-0613"
]

# Game instance
game = Game()

global render_dict

# PLAYER TAB
with gr.Blocks() as player:
    # STORY AREA
    with gr.Row(variant="compact") as story_area:
        # CHAT AREA
        with gr.Column(scale=10, variant="compact") as chat_area:
            # CHATBOT
            with gr.Row() as history_area:
                display_history = gr.Chatbot(height=600)
            # COMBAT AREA
            with gr.Row() as combat_area:
                combat_box = gr.Textbox(label="Combat", interactive=False)
            # USER INPUT
            with gr.Group():
                with gr.Row() as user_area:
                    # MODEL
                    model_select = gr.Dropdown(
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
                        restart = gr.Button(value="Restart", size="sm")
        # TEAM/STATS AREA
        with gr.Column(scale=1, variant="compact") as stats_area:
            # GAME NAME
            with gr.Group():
                with gr.Row():
                    game_name = gr.Textbox(lines=1, label="Game Name", interactive=True)
                    save_game = gr.Button(value="Save", size="sm")
                    load_game = gr.Button(value="Load", size="sm")
                    delete_game = gr.Button(value="Delete", size="sm")
            # STATS
            with gr.Group():
                day_box = gr.Textbox(lines=1, label="Game Time", interactive=False)
                item_box = gr.Textbox(lines=5, label="Items", interactive=False)
                relationship_box = gr.Textbox(lines=10, label="Friend Stats", interactive=False)

    # DEBUG AREA
    with gr.Column(variant="compact") as debug_area:
        # with gr.Row():
        #     token_jsons = []
        #     for model_name,tracker in TokenTracker.trackers.items():
        #         token_jsons.append(gr.JSON(label=f"{model_name} Token Tracker", interactive=False))
        execution_json = gr.JSON(label="Execution Info")
        game_state_json = gr.JSON(label="Game State")


    #--------------------------------------------------------------
    #                      PLAYER TAB FUNCTIONS
    #--------------------------------------------------------------
    # Array to update the interface from the game state. Contains all changeable interface elements.
    render_dict = [
        game_name,
        load_game,
        save_game,
        delete_game,

        display_history,
        combat_box,

        day_box,
        item_box,
        relationship_box,

        model_select,
        player_message,
        submit,
        retry,
        undo,
        restart,

        execution_json,
        game_state_json,
    ]
    #--------------------------------------------------------------
    # SUBMIT FUNCTIONS
    #--------------------------------------------------------------
    submit_array = [
        # Click "Do it!" button
        submit.click(
            # Add the player message to the history
            fn=game.submit, 
            inputs=[player_message],
            outputs=render_dict,
            queue=False
        ),
        # Press enter key
        player_message.submit(
            # Add the player message to the history
            fn=game.submit, 
            inputs=[player_message],
            outputs=render_dict,
            queue=False
        ),
        # Click "Retry" button
        retry.click(
            # Remove the last assistant message from the history
            fn=game.retry,
            inputs=[],
            outputs=render_dict,
            queue=False
        ),
        # Restart the game
            restart.click(
            fn=game.restart,
            inputs=[],
            outputs=render_dict,
        ),
    ]
    
    # What happens after the player submits a message
    for submit_item in submit_array:
        # Generate the assistant message
        submit_item.then(
            fn=game.stream_prediction,
            inputs=[],
            outputs=render_dict,
            queue=True
        )
    
    #--------------------------------------------------------------
    # AUXILIARY FUNCTIONS
    #--------------------------------------------------------------
    # Undo the last user and assistant message
    undo.click(
        fn=game.undo,
        inputs=[],
        outputs=render_dict,
        queue=False
    )

    # Delete the game
    delete_game.click(
        fn=game.delete_game,
        inputs=[],
        outputs=render_dict,
        queue=False
    )

    model_select.change(
        fn=game.change_model,
        inputs=[model_select],
        outputs=[],
        queue=False
    )

    # Update team name on change
    game_name.change(
        fn=game.change_name,
        inputs=[game_name],
        outputs=[],
        queue=False
    )

    # Load the game on enter
    game_name.submit(
        fn=game.load_game,
        inputs=[],
        outputs=render_dict,
        queue=False
    )

    # Load the game on button click
    load_game.click(
        fn=game.load_game,
        inputs=[],
        outputs=render_dict,
        queue=False
    )

    # Save the game on button click
    save_game.click(
        fn=game.save_game,
        inputs=[],
        outputs=[],
        queue=False
    )

    