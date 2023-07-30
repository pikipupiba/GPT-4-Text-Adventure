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

prev_history = []
def save_current_chat_history(history):
    # global prev_history
    # if history == prev_history:
    #     return
    # prev_history = history
    logger.info("Saving CHAT HISTORY!")

    # Check if the "sessions" directory exists
    if not os.path.exists("sessions"):
        os.makedirs("sessions")
        
    chat_history_file_path = os.path.join("sessions", "current_chat_history.json")

    try:
        with open(chat_history_file_path, "w") as f:
            f.write(json.dumps(history, indent=4))
    except IOError as e:
        print(f"Error: {e}")

def load_current_chat_history():
    logger.info("Loading CHAT HISTORY!")

    # Check if the "sessions" directory exists
    if not os.path.exists("sessions"):
        os.makedirs("sessions")

    chat_history_file_path = os.path.join("sessions", "current_chat_history.json")

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