import os
import json

def save_session(file_name, engine, scenario, npc, environment, rules):
    saved_args = locals()

    print(saved_args)

    session_file = os.path.join("sessions", f"{file_name}.json")

    try:
        if os.path.exists(session_file):
            with open(session_file, "r") as f:
                session = json.load(f)
        else:
            session = {}
        
        for key, value in saved_args.items():
            session[key] = value
        
        with open(session_file, "w") as f:
            json.dump(session, f)
    except IOError as e:
        print(f"Error: {e}")

def load_session(file_name):
    session_file = os.path.join("sessions", f"{file_name}.json")

    try:
        if os.path.exists(session_file):
            with open(session_file, "r") as f:
                session = json.load(f)
        else:
            session = {}

        session_array = [value for key, value in session.items()]
        return session_array
    except IOError as e:
        print(f"Error: {e}")