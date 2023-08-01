import os,json
from loguru import logger

def save_session(file_name, system_message):
    logger.info(f"Saving '{file_name}.txt' SYSTEM message!")
    session_file_path = os.path.join("sessions", f"{file_name}.txt")

    try:
        with open(session_file_path, "w") as f:
            f.write(system_message)
    except IOError as e:
        print(f"Error: {e}")


def load_session(file_name, system_message, mode):
    logger.info(f"Loading '{file_name}.txt' SYSTEM message!")
    session_file_path = os.path.join("sessions", f"{file_name}.txt")

    try:
        with open(session_file_path, "r") as f:
            text = f.read()
    except IOError as e:
        print(f"Error: {e}")

    if mode == "Overwrite":
        system_message = text
    elif mode == "Prepend":
        system_message = text + "/n/n" + system_message
    elif mode == "Append":
        system_message = system_message + "/n/n" + text

    return system_message

def save_current_system_message(system_message):
    logger.info("Saving CURRENT SYSTEM message!")
    session_file_path = os.path.join("sessions", "current_system_message.txt")

    try:
        with open(session_file_path, "w") as f:
            f.write(system_message)
    except IOError as e:
        print(f"Error: {e}")


def load_current_system_message():
    logger.info("Loading CURRENT SYSTEM message!")
    session_file_path = os.path.join("sessions", "current_system_message.txt")

    try:
        with open(session_file_path, "r") as f:
            system_message = f.read()
    except IOError as e:
        print(f"Error: {e}")

    return system_message

def save_current_example_history(example_history):
    logger.info("Saving CURRENT EXAMPLE HISTORY!")
    session_file_path = os.path.join("sessions", "current_example_history.json")

    try:
        with open(session_file_path, "w") as f:
            f.write(example_history)
    except IOError as e:
        print(f"Error: {e}")

def load_current_example_history():
    logger.info("Loading CURRENT EXAMPLE HISTORY!")
    session_file_path = os.path.join("sessions", "current_example_history.json")

    try:
        with open(session_file_path, "r") as f:
            example_history = f.read()
    except FileNotFoundError:
        example_history = []
        print(f"Error: File '{session_file_path}' not found")
    except IOError as e:
        print(f"Error: {e}")

    return example_history

def save_current_chat_history(team_name, history):
    logger.info("Saving CHAT HISTORY!")

    # Check if the "sessions" directory exists
    if not os.path.exists("sessions"):
        os.makedirs("sessions")
        
    chat_history_file_path = os.path.join("sessions", "current_chat_history.json")
    team_history_file_path = os.path.join("sessions", f"{team_name}.json")

    try:
        with open(chat_history_file_path, "w") as f:
            f.write(json.dumps(history, indent=4))
        with open(team_history_file_path, "w") as f:
            f.write(json.dumps(history, indent=4))
    except IOError as e:
        print(f"Error: {e}")
    
    # Invert the history
    history = [[item[1], item[0]] for item in history]

    return history

def load_current_chat_history(team_name=""):
    logger.info("Loading CHAT HISTORY!")

    # Check if the "sessions" directory exists
    if not os.path.exists("sessions"):
        os.makedirs("sessions")

    if team_name == "":
        chat_history_file_path = os.path.join("sessions", "current_chat_history.json")
    else:
        chat_history_file_path = os.path.join("sessions", f"{team_name}.json")

    try:
        with open(chat_history_file_path, "r") as f:
            history = json.load(f)
    except FileNotFoundError:
        history = []
        print(f"Error: File '{chat_history_file_path}' not found")
    except IOError as e:
        history = []
        print(f"Error: {e}")

    return history

# def load_current_chat_history_inverted():
#     logger.info("Loading CHAT HISTORY!")

#     # Check if the "sessions" directory exists
#     if not os.path.exists("sessions"):
#         os.makedirs("sessions")

#     chat_history_file_path = os.path.join("sessions", "current_chat_history.json")

#     try:
#         with open(chat_history_file_path, "r") as f:
#             history = json.load(f)
#     except FileNotFoundError:
#         history = []
#         print(f"Error: File '{chat_history_file_path}' not found")
#     except IOError as e:
#         history = []
#         print(f"Error: {e}")

#     # Invert the history
#     history = [[item[1], item[0]] for item in history]

#     return history

def save_game_state(team_name, chatbot, day_box, items_box, friends_box):
    logger.info("Saving GAME STATE!")

    game_state = {
        "team_name": team_name,
        "day_box": day_box,
        "items_box": items_box,
        "friends_box": friends_box,
        "chatbot": chatbot,
    }

    # Check if the "sessions" directory exists
    if not os.path.exists("sessions"):
        os.makedirs("sessions")

    current_state_file_path = os.path.join("sessions", "current_state.json")
    team_state_file_path = os.path.join("sessions", f"{team_name}_state.json")

    try:
        with open(current_state_file_path, "w") as f:
            f.write(json.dumps(game_state, indent=4))
        with open(team_state_file_path, "w") as f:
            f.write(json.dumps(game_state, indent=4))
    except IOError as e:
        print(f"Error: {e}")

    return game_state

def load_game_state(team_name=""):
    logger.info("Loading GAME STATE!")

    # Check if the "sessions" directory exists
    if not os.path.exists("sessions"):
        os.makedirs("sessions")

    if team_name == "":
        game_state_file_path = os.path.join("sessions", "current_state.json")
    else:
        game_state_file_path = os.path.join("sessions", f"{team_name}_state.json")

    try:
        with open(game_state_file_path, "r") as f:
            game_state = json.load(f)
    except FileNotFoundError:
        game_state = {}
        print(f"Error: File '{game_state_file_path}' not found")
    except IOError as e:
        game_state = {}
        print(f"Error: {e}")

    return game_state