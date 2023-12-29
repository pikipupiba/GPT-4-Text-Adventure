import re
from typing import List
from loguru import logger

from PythonClasses.Helpers.helpers import generate_dice_string


class UserMessage:
    # The `UserMessage` class is a Python class that provides a method called `build`. This method
    # takes a user message as input and performs several operations on it.

    def build(user_message: str):
        logger.debug(f"Building user message: {user_message}")

        # Remove leading and trailing whitespace
        user_message = user_message.strip()

        # Remove double spaces
        user_message = re.sub(r"\s+", " ", user_message)

        dice_roll_string = generate_dice_string()

        complete_user_message = f"{user_message}\n{dice_roll_string}"

        return complete_user_message
