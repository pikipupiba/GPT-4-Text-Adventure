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

import gradio as gr

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
with gr.Blocks() as player_tab:
    # STORY AREA
    with gr.Row(variant="compact").style(equal_height=True) as story_area:
        # CHAT AREA
        with gr.Column(scale=10, variant="compact") as chat_area:
            # CHATBOT
            chatbot = gr.Chatbot(
                value=intro, 
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

                audio_box = gr.Audio(
                    # value="/path/to/intro.mp3",
                    label="Audio",
                    type="numpy",
                    scale=1,
                    visible=True,
                    interactive=False,
                    autoplay=True,
                )
                
        with gr.Column(
                scale=1,
                variant="compact",
                visible=False,
            ) as stats_area:

            day_box = gr.Textbox(lines=1, label="Today", interactive=False)
            item_box = gr.Textbox(lines=5, label="Items", interactive=False)
            relationship_box = gr.Textbox(lines=10, label="Relationships", interactive=False)