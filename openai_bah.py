def submit_message(message):
    # submit system message + story + stats + action to model
    return 0

def build_system_message(system_messages, stats, story, surprise):
    # build system message from GM input
    message = ""

    for message in system_messages:
        message += message + "\n"

    message += "stats:/n"

    for stat in stats:
        message += stat + "\n"

    message += "story:/n" + story + "\n"

    message += "surprise:/n" + surprise

    return message

def build_messages(player_message, system_messages, story, stats, surprise):
    # submit system message + story + stats + action to model

    system_message = build_system_message(system_messages, stats, story, surprise)

    system_message += 

    messages = [
        {"role": "system", "content": system_message},
        # {"role": "assistant", "content": story},
        {"role": "user", "content": player_message},
    ]

    return messages