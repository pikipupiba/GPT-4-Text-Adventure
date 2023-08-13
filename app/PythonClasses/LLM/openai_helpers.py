from typing import List

from loguru import logger

def build_openai_history(history: List[List[str]] = None):
    logger.trace("Building history OpenAI format")

    if history == None:
        logger.warning("No history provided. Returning None.")
        return None

    openai_history = []

    # Convert history to OpenAI format
    for user, assistant in history:
        if user != None:
            openai_history.append({"role": "user", "content": user})
        if assistant != None:
            openai_history.append(
                {"role": "assistant", "content": assistant}
            )

    logger.trace(
        f"Successfully built history OpenAI format | Found {len(openai_history)} chat message pairs"
    )

    return openai_history

def build_openai_system_message(system_message: str = None):
    logger.debug("Building system message OpenAI format")

    if system_message == None:
        logger.warning("No system message provided. Returning None.")
        return None

    openai_system_message = {"role": "system", "content": system_message}

    logger.trace("Successfully built system message OpenAI format")

    return openai_system_message