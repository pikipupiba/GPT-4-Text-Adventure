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

# PLAYER TAB
with gr.Blocks() as player_tab:
    # STORY AREA
    with gr.Row(variant="compact").style(equal_height=True) as story_area:
        # CHAT AREA
        with gr.Column(scale=10, variant="compact") as chat_area:
            # CHATBOT
            chatbot = gr.Chatbot(
                value="", 
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
                    placeholder="What is your team name?",
                    lines=1,
                    label="Enter Team Name",
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
                
        with gr.Column(
                scale=1,
                variant="compact",
                visible=False,
            ) as stats_area:

            day_box = gr.Textbox(lines=1, label="Today", interactive=False)
            item_box = gr.Textbox(lines=5, label="Items", interactive=False)
            relationship_box = gr.Textbox(lines=10, label="Relationships", interactive=False)