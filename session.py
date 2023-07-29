import os
import json

def save_session(file_name, system_message):

    session_file_path = os.path.join("sessions", f"{file_name}.txt")

    try:
        with open(session_file_path, "w") as f:
            f.write(system_message)
    except IOError as e:
        print(f"Error: {e}")


def load_session(file_name, system_message, mode):
    
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