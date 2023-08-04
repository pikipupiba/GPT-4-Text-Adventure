import os,json
from loguru import logger

def save_session(file_name, system_message):
    logger.info(f"Saving '{file_name}.txt' SYSTEM message!")
    session_file_path = os.path.join("sessions", "system_messages", f"{file_name}.txt")

    try:
        with open(session_file_path, "w") as f:
            f.write(system_message)
    except IOError as e:
        print(f"Error: {e}")

def load_session(file_name, system_message, mode):
    logger.info(f"Loading '{file_name}.txt' SYSTEM message!")
    session_file_path = os.path.join("sessions", "system_messages", f"{file_name}.txt")

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
    logger.debug("Saving CURRENT SYSTEM message!")
    session_file_path = os.path.join("sessions", "current" "system_message.txt")

    try:
        with open(session_file_path, "w") as f:
            f.write(system_message)
    except IOError as e:
        print(f"Error: {e}")

def load_current_system_message():
    logger.debug("Loading CURRENT SYSTEM message!")
    session_file_path = os.path.join("sessions", "current" "system_message.txt")

    try:
        with open(session_file_path, "r") as f:
            system_message = f.read()
    except FileNotFoundError:
        print(f"Error: File '{session_file_path}' not found. Creating.")
        system_message = ""
        save_current_system_message(system_message)
    except IOError as e:
        system_message = ""
        print(f"Error: {e}")

    return system_message

def save_current_example_history(example_history):
    logger.debug("Saving CURRENT EXAMPLE HISTORY!")
    session_file_path = os.path.join("sessions", "current", "example_history.json")

    try:
        with open(session_file_path, "w") as f:
            f.write(example_history)
    except IOError as e:
        print(f"Error: {e}")

def load_current_example_history():
    logger.debug("Loading CURRENT EXAMPLE HISTORY!")
    session_file_path = os.path.join("sessions", "current", "example_history.json")

    try:
        with open(session_file_path, "r") as f:
            example_history = f.read()
    except FileNotFoundError:
        print(f"Error: File '{session_file_path}' not found")
        example_history = []
        save_current_example_history(example_history)
    except IOError as e:
        print(f"Error: {e}")
        example_history = []

    return example_history

def save_current_chat_history(history):
    logger.debug("Saving CHAT HISTORY!")

    # Check if the "sessions" directory exists
    if not os.path.exists("sessions"):
        os.makedirs("sessions")
        
    chat_history_file_path = os.path.join("sessions", "current", "current_chat_history.json")

    try:
        with open(chat_history_file_path, "w") as f:
            f.write(json.dumps(history, indent=4))
    except IOError as e:
        print(f"Error: {e}")
    
    # Invert the history
    history = [[item[1], item[0]] for item in history]

    return history

def load_current_chat_history(team_name=""):
    logger.debug("Loading CHAT HISTORY!")

    # Check if the "sessions" directory exists
    if not os.path.exists("sessions"):
        os.makedirs("sessions")

    chat_history_file_path = os.path.join("sessions", "current", "chat_history.json")

    try:
        with open(chat_history_file_path, "r") as f:
            history = json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{chat_history_file_path}' not found. Creating.")
        history = []
        save_current_chat_history(history)
    except IOError as e:
        history = []
        print(f"Error: {e}")

    return history