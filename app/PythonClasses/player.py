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
#       - timeout, thunderstorm (insideWelcome that day), get sick, field trip
# [almost] 9. fix dice rolls
# 10. add session functionality
# 11. Dropdown to select team name from saved sessions
# 12. Countdown timer bar + allow everyone to answer + average actions :) :) :)
# 12a. ABOVE IDEA IS AN ABSOLUTE GAME CHANGER
# 12b. Sometimes the timer will be short and it will single someone out to respond quickly
import os
import gradio as gr
from PythonClasses.Game.FileManager import FileManager

from PythonClasses.Game.Game import Game

use_models = [
    "gpt-4-0613",
    "gpt-4-32k-0613",
    "gpt-3.5-turbo-0613",
    "gpt-3.5-turbo-16k-0613"
]

intro = [
    [
        None,
        '''
Welcome to 'AI Adventure Academy'!
(an interactive storytelling game)

You, as a team, must step into the shoes of the main character…

Main Character: a fifth grader on your first day at a new school
Birthday: Saturday
Invitations handed out: ZERO

…And I, as the game master, will describe the scenarios and characters you meet, while you shape the narrative with your actions. Your goal? Navigate recess, make decisions, and forge friendships, all before your birthday on Saturday. If you don’t make any friends your birthday party will be sad and lonely. Nobody wants that. Much like the first day of school, your only limit is your imagination.

The game evolves dynamically based on your choices and actions. If you decide to act against your apparent goal, that's allowed, provided it doesn't conflict with the story's established setting.

Every 'day' in the game lasts for an hour, and actions consume time. Make sure to keep an eye on your stats on the right side of the screen. This will tell you what day it is, how much time you have left, the items you haven’t used, and any relationships you have formed with your peers. At the end of each day, a new day will start and and I will introduce new scenarios at recess.

Finally, if you are confused or don’t know what to do, ask me questions! I can describe what is going on around you and perhaps you will be inspired to go make some friends.

With all that out of the way, let’s get started! What is your name?
        '''
        ]
    ]

# PLAYER TAB
with gr.Blocks(title="AI Adventure Academy", theme=gr.themes.Soft()) as combined:
    gr.HTML("<h1 style='text-align: center;'>AI Adventure Academy</h1>")
    # with gr.Tab("Player") as player_tab:
        # STORY AREA
    with gr.Row(variant="compact").style(equal_height=True) as story_area:
        # CHAT AREA
        with gr.Column(scale=7, variant="compact") as chat_area:
            # CHATBOT
            chatbot = gr.Chatbot(
                value=intro,
                height=600,
            )

            # USER MESSAGE AREA
            with gr.Row(variant="compact") as user_message_area:
                user_message = gr.Textbox(
                    value="",
                    placeholder="What will you do?",
                    lines=1,
                    label="Next Action",
                    interactive=True,
                    scale=20,
                    visible=False,
                )

                submit = gr.Button(
                    value="Do it!",
                    scale=1,
                    size="sm",
                    visible=False,
                )


                game_name = gr.Textbox(
                    value="",
                    placeholder="Bobby Hill",
                    lines=1,
                    label="Enter Character Name",
                    interactive=True,
                    scale=20,
                    visible=True,
                )

                start_game = gr.Button(
                    value="Begin Adventure!",
                    scale=1,
                    size="sm",
                    visible=True,
                )

            with gr.Row(variant="compact"):

                audio_speed = gr.Slider(
                    minimum=100,
                    maximum=200,
                    step=1,
                    value=150,
                    label="Audio Speed",
                    scale=7,
                    visible=True,
                )

                audio_box = gr.Audio(
                    value=os.path.join(FileManager.DATA_FOLDER, "Intro.mp3"),
                    label="Audio",
                    type="numpy",
                    scale=3,
                    visible=True,
                    interactive=True,
                    autoplay=True,
                )

                audio_volume = gr.Slider(
                    minimum=0,
                    maximum=100,
                    step=1,
                    value=75,
                    label="Audio Volume",
                    scale=1,
                    visible=False,
                )
                
        with gr.Column(
                scale=3,
                variant="compact",
                visible=False,
            ) as stats_area:

            day_box = gr.Textbox(lines=2, label="Today", interactive=False)
            item_box = gr.Textbox(lines=7, label="Items", interactive=False)
            relationship_box = gr.Textbox(lines=20, label="Relationships", interactive=False)


# with gr.Tab(" "):
    with gr.Box(visible=False) as config_tab:
        with gr.Group():
            with gr.Row():
                # SELECT MODEL
                select_model = gr.Radio(
                    choices=use_models,
                    label="Select Model",
                    value=use_models[0],
                    scale=1,
                )
                with gr.Column():
                    system_select = gr.Radio(
                        choices=["full", "short", "none"],
                        label="System Select",
                        value="full",
                    )
                    schema_select = gr.Radio(
                        choices=["full", "short", "none"],
                        label="Schema Select",
                        value="full",
                    )
                retry = gr.Button(value="Retry", size="sm")
                undo = gr.Button(value="Undo", size="sm")
                clear = gr.Button(value="Clear", size="sm")
                restart = gr.Button(value="Restart", size="sm")
                render = gr.Button(value="Render", size="sm")

        # GAME NAME
        with gr.Group():
            with gr.Row():
                history_name = gr.Textbox(
                    value="BAH",
                    lines=1,
                    label="History Name",
                    interactive=True,
                    scale=1,
                )
                
                save_game = gr.Button(value="Save", size="sm")
                delete_game = gr.Button(value="Delete", size="sm")
                load_game = gr.Button(value="Load", size="sm")
                
                select_history_name = gr.Dropdown(
                    choices=FileManager.get_file_names(FileManager.HISTORY_FOLDER),
                    show_label=True,
                    label="Select History",
                    scale=1,
                )

        # DEBUG AREA
        with gr.Column(variant="compact") as debug_area:
            # with gr.Row():
            #     token_jsons = []
            #     for model_name,tracker in TokenTracker.trackers.items():
            #         token_jsons.append(gr.JSON(label=f"{model_name} Token Tracker", interactive=False))
            with gr.Row() as total_token_jsons:
                gpt_4_json = gr.JSON(label="gpt 4", interactive=False)
                gpt_4_32_json = gr.JSON(label="gpt 4 32k", interactive=False)
                gpt_3_5_turbo_json = gr.JSON(label="gpt 3.5 turbo", interactive=False)
                gpt_3_5_turbo_16_json = gr.JSON(label="gpt 3.5 turbo 16k", interactive=False)
            with gr.Row() as game_average_token_jsons:
                game_average_gpt_4_json = gr.JSON(label="game average gpt 4", interactive=False)
                game_average_gpt_4_32_json = gr.JSON(label="game average gpt 4 32k", interactive=False)
                game_average_gpt_3_5_turbo_json = gr.JSON(label="game average gpt 3.5 turbo", interactive=False)
                game_average_gpt_3_5_turbo_16_json = gr.JSON(label="game average gpt 3.5 turbo 16k", interactive=False)
            with gr.Row() as game_token_jsons:
                game_gpt_4_json = gr.JSON(label="last turn gpt 4", interactive=False)
                game_gpt_4_32_json = gr.JSON(label="last turn gpt 4 32k", interactive=False)
                game_gpt_3_5_turbo_json = gr.JSON(label="last turn gpt 3.5 turbo", interactive=False)
                game_gpt_3_5_turbo_16_json = gr.JSON(label="last turn gpt 3.5 turbo 16k", interactive=False)
            with gr.Row():
                final_game_stats = gr.JSON(label="Final Game Stats", interactive=False, scale=10)
                compile_game_stats = gr.Button(value="Compile Game Stats", size="sm", scale=1)
            turn_json = gr.JSON(label="Game State")


# with gr.Tab(" "):
    with gr.Box(visible=False) as gm_tab:

        with gr.Group():
            # SAVE/LOAD SESSION
            with gr.Row():
                system_message_name = gr.Textbox(
                    value="NEW",
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
                    value="BEST_system_message",
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
                            value=FileManager.load_system_message("NEW"),
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