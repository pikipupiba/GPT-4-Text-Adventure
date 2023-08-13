import re
from enum import Enum, auto
from typing import List, Union, Optional, Tuple, Dict
from loguru import logger

from PythonClasses.Helpers.helpers import generate_dice_string, get_nth_or_value


class RoleType(Enum):
    SYSTEM = auto()
    USER = auto()
    ASSISTANT = auto()
    ANY = auto()

class DisplayType(Enum):
    DISPLAY = auto()
    CONTEXT = auto()
    SUMMARY = auto()
    ANY = auto()

    def __repr__(self):
        return f"DisplayType.{self.name}"

class TurnState(Enum):
    AWAITING_USER = auto()
    AWAITING_ASSISTANT = auto()
    AWAITING_ACTION = auto()  # This could represent some other state, just an example

class ChatMessage:
    def __init__(self, role: RoleType, content: Dict[DisplayType, str]):
        self.role = role
        self.content = content

    @property
    def display(self) -> Optional[str]:
        return self.content.get(DisplayType.DISPLAY)

    @display.setter
    def display(self, value: str) -> None:
        self.content[DisplayType.DISPLAY] = value

    @property
    def context(self) -> Optional[str]:
        return self.content.get(DisplayType.CONTEXT)

    @context.setter
    def context(self, value: str) -> None:
        self.content[DisplayType.CONTEXT] = value

    @property
    def summary(self) -> Optional[str]:
        return self.content.get(DisplayType.SUMMARY)

    @summary.setter
    def summary(self, value: str) -> None:
        self.content[DisplayType.SUMMARY] = value
        
    def __getitem__(self, key: Union[int, DisplayType]) -> Optional[str]:
        if isinstance(key, int):
            try:
                key = list(DisplayType)[key]  # Convert index to corresponding DisplayType
            except IndexError:
                raise KeyError(f"Invalid index: {key}")
        return self.content.get(key)
    
    def __setitem__(self, key: Union[int, DisplayType], value: str) -> None:
        if isinstance(key, int):
            try:
                key = list(DisplayType)[key]
            except IndexError:
                raise KeyError(f"Invalid index: {key}")
        self.content[key] = value


    def __contains__(self, key: DisplayType) -> bool:
        return key in self.content
    
    def __delitem__(self, key: DisplayType) -> None:
        del self.content[key]
    
    def __repr__(self):
        return f"<ChatMessage from {self.role} contains {[dt for dt, content in self.content.items()]}>"
    
    def __str__(self):
        return f"Message from {self.role}: {self.content}"
    

class History:
    def __init__(self, messages: Optional[List[ChatMessage]] = None):
        self.messages = messages if messages is not None else []
    def __getitem__(self, index):
        return self.messages[index]
    def __setitem__(self, index, value):
        self.messages[index] = value
    def append(self, message: ChatMessage):
        self.messages.append(message)
    def pop(self):
        return self.messages.pop()
    def truncate(self, length: int):
        self.messages = self.messages[-length:]
    def clear(self):
        self.messages.clear()
    def __len__(self):
        return len(self.messages)
    def __iter__(self):
        return iter(self.messages)
    def __repr__(self):
        return f"<History with {len(self)} messages>"
    
    def __add__(self, other: Union[ChatMessage, 'History']) -> 'History':
        if isinstance(other, ChatMessage):
            return History(self.messages + [other])
        elif isinstance(other, History):
            return History(self.messages + other.messages)
        else:
            raise ValueError("You can only add a ChatMessage or another History to History.")
    
    def __iadd__(self, other: Union[ChatMessage, 'History']) -> 'History':
        if isinstance(other, ChatMessage):
            self.append(other)
        elif isinstance(other, History):
            self.messages.extend(other.messages)
        else:
            raise ValueError("You can only add a ChatMessage or another History to History.")
        return self

    def get_messages(self, roles: Union[RoleType, List[RoleType]], display_types: Union[DisplayType, List[DisplayType]], start_index: Optional[int] = None, end_index: Optional[int] = None) -> Dict[DisplayType, List[Dict]]:
        # Ensure the roles and display_types are in a list format
        if not isinstance(roles, list):
            roles = [roles]
        if not isinstance(display_types, list):
            display_types = [display_types]

        # Filter messages using list comprehension
        filtered_messages = [msg for msg in self.messages[start_index:end_index] if msg.role in roles and any(key in msg.content for key in display_types)]

        results = {dtype: [] for dtype in display_types}
        for msg in filtered_messages:
            for dtype in display_types:
                content_for_dtype = msg.content.get(dtype)
                if content_for_dtype:
                    message_dict = {
                        'role': msg.role,
                        'content': content_for_dtype
                    }
                    results[dtype].append(message_dict)

        # Filter out DisplayType keys with empty lists
        results = {dtype: val for dtype, val in results.items() if val}

        return results


    @property
    def last_system_message(self) -> Optional[ChatMessage]:
        for message in reversed(self.messages):
            if message.role == RoleType.SYSTEM:
                return message
        return None

    def get_last_message_of_type(self, role: RoleType) -> Optional[Tuple[ChatMessage, int]]:
        for index, message in reversed(list(enumerate(self.messages))):
            if message.role == role:
                return message, index
        return None
    
    @property
    def last_role(self) -> Optional[RoleType]:
        if self.messages:
            return self.messages[-1].role
        return None
    
    @property
    def turn_state(self) -> TurnState:
        if not self.messages:
            return TurnState.AWAITING_USER
        
        last_role = self.messages[-1].role

        if last_role == RoleType.USER:
            return TurnState.AWAITING_ASSISTANT
        elif last_role == RoleType.ASSISTANT:
            return TurnState.AWAITING_USER  # Assuming the next message would be from the user
        else:
            # For system or other message types, you can add more logic here
            # I've added a default state, but you can adjust based on your needs
            return TurnState.AWAITING_ACTION

class HistoryFilter(History):
    def __init__(self, messages: Optional[List[ChatMessage]] = None, **kwargs):
        super().__init__(messages)
        self._context_distance = kwargs.get("context_distance")
        self._summary_distance = kwargs.get("summary_distance")
        self._display_distance = kwargs.get("display_distance")

    def _filter_messages_by_role_and_type(self, roles: List[RoleType], display_types: List[DisplayType], distance: Optional[int] = None) -> List[ChatMessage]:
        """Filter messages based on roles, display types, and distance."""
        messages = [msg for msg in self.messages if msg.role in roles and any(key in msg.content for key in display_types)]
        return messages[-distance:] if distance is not None else messages

    def display_history(self, display_distance: Optional[int] = None) -> List[List[Optional[str]]]:
        """Return paired user and assistant display messages."""
        display_distance = display_distance if display_distance is not None else self._display_distance
        messages = self._filter_messages_by_role_and_type([RoleType.USER, RoleType.ASSISTANT], [DisplayType.DISPLAY], display_distance)
        
        user_messages, assistant_messages = [], []
        for message in messages:
            content = message.content.get(DisplayType.DISPLAY)
            if message.role == RoleType.USER:
                user_messages.append(content)
                assistant_messages.append(None)
            else:
                if assistant_messages and assistant_messages[-1] is None:
                    assistant_messages[-1] = content
                else:
                    user_messages.append(None)
                    assistant_messages.append(content)

        return list(zip(user_messages, assistant_messages))

    def context_history(self, context_distance: Optional[int] = None, summary_distance: Optional[int] = None) -> List[Dict[str, str]]:
        """Return context or summary of recent messages."""
        context_distance = context_distance if context_distance is not None else self._context_distance
        summary_distance = summary_distance if summary_distance is not None else self._summary_distance

        messages = self._filter_messages_by_role_and_type([RoleType.USER, RoleType.ASSISTANT], [DisplayType.CONTEXT, DisplayType.SUMMARY], context_distance)
        context = []
        for idx, msg in enumerate(messages[::-1]):  # Single reversal here
            if summary_distance is None or idx < summary_distance:
                content = msg.content.get(DisplayType.CONTEXT) or msg.content.get(DisplayType.SUMMARY)
            else:
                content = msg.content.get(DisplayType.SUMMARY) or msg.content.get(DisplayType.CONTEXT)

            context.append({"role": msg.role.name.lower(), "content": content})

        return context

    def api_call_context(self) -> List[str]:
        """Return context for API calls."""
        recent_messages = self.context_history()
        if hasattr(self, 'last_system_message') and self.last_system_message:
            recent_messages.append(self.last_system_message.content.get(DisplayType.CONTEXT))
        return recent_messages


class UserMessage:
# The `UserMessage` class is a Python class that provides a method called `build`. This method
# takes a user message as input and performs several operations on it.

    def __init__(self, user_message = None):

        self.user_message = user_message

    
    def build(user_message: str):

        logger.debug(f"Building user message: {user_message}")

        # Remove leading and trailing whitespace
        user_message = user_message.strip()

        # Remove double spaces
        user_message = re.sub(r'\s+', ' ', user_message)

        dice_roll_string = generate_dice_string()

        complete_user_message = f"{user_message}\n{dice_roll_string}"

        return complete_user_message


import re,json
from typing import List
from loguru import logger

from PythonClasses.Schemas import schema_strings

schemas = {
    "day": {
        "use": "When time passes in a measurable way. Always use after an action.",
        "description": "Use this format to describe the day of the week and the amount of time remaining. Each day begins with 60 minutes.",
        "variables": {
            "day": "Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday",
            "time": "time remaining in the day in minutes, must include the integer number even if it's 0: int between 0 and 60",
            "quip": "short quip about the amount of time remaining: <5 words",
        },
        "format": "..DAY..{day} with {time} minutes left. {quip}..DAY.."
    },
    "item": {
        "use": "When an item is used, gained, or changes status.",
        "description": "Use this format to describe an item and its condition. Items can be used or gained.",
        "variables": {
            "name": "name of the item - <5 words",
            "status": "the current condition, status, or amount remaining of the item: <10 words",
        "format": "..ITEM..{name} ({status})..ITEM.."
    },
    "relationship": {
        "use": "When the number or attitude of NPCs of a certain type changes or they react to something you do.",
        "description": "Use this format to describe my relationships with NPCs. Relationships can be gained, lost and change.",
        "variables": {
            "level": "Creative relationship levels. This is a spectrum: Arch Nemesis, Enemy, Rival, Neutral, Ally, Friend, Best Friend, Family, Lover, Soulmate, Spouse, etc.",
            "change": "change to the number of NPCs in this level, includes the sign: +/- int",
            "count": "number of NPCs of this type after change, should remain self consistent: int",
            "rationale": "rationale for the change in the number of NPCs of this type: <20 words",
            "info": "current relevant information about NPCs of this type such as names, sentiment, and/or reasoning: <20 words",
        },
        "format": "..RELATIONSHIP..{type} | {change} | {count}\n---> {rationale}\n---> {info}..RELATIONSHIP.."
    },
    "action": {
        "use": "When an action is taken.",
        "description": "Use this format to describe an action taken by a character. Actions can succeed or fail.",
        "variables": {
            "name": "name of character: <5 words",
            "action": "attempted action: <20 words",
            "difficulty": "level of difficulty, be creative: 1 word",
            "dcRationale": "rationale for the DC: <20 words",
            "dc": "DC for the action. Harder actions have higher DCs: int between 1 and 20",
            "modifierRationale": "rationale for roll modifier to allow for positive or negative externalities. Using the right item for a situation or being creative should give a bonus. Using the wrong item for a situation or being distracted or weak should give a penalty: <20 words",
            "modifier": "+/- to the roll based on rationale, show the +/- sign: int between -10 and +10",
            "numRolls": "number of dice rolls so far this turn. Starts at 0 every turn and increments by 1 for each roll: int",
            "roll": "the user will send dice rolls with each turn called rolls[]. use rolls[numRolls] for this value: int",
            "result": "roll + modifier: int",
            "success": "SUCCESS if {result} >= {dc}, else FAILURE. Add an adjective if the difference is great: string",
            "elapsedTime": "realistic and precise estimate of how long the action took: int",
        },
        "format": "---> {name} is trying to {action}.\n---> Difficulty: {difficulty} - {dcRationale} ({dc})\n---> {'Bonus' or 'Penalty'}: {modifierRationale} ({modifier})\n\n..HIDE..---> Result: {rolls[numRolls]} {modifier sign: + or -} {modifier} {<, >, or =} {dc}  |  {adjective} {SUCCESS or FAILURE}\n---> Elapsed Time: {elapsedTime} minutes..HIDE..",
        }
    }
}

class SystemMessage:
# The `SystemMessage` class is providing a method called `inject_schemas` that is used to inject
# schema strings into a given system message. It does this by searching for schema placeholders
# in the system message and replacing them with the corresponding schema string. The schema
# placeholders are identified using a specific pattern (`/*\schema_name*/\`) and are replaced
# using the `re.sub` function. If a schema string is not found for a particular schema name, the
# original placeholder is retained in the system message. The method returns the complete system
# message with the injected schemas.

    
    def inject_schemas(system_message: str):
    # The `inject_schemas` method is used to inject schema strings into a given system message. It
    # searches for schema placeholders in the system message and replaces them with the
    # corresponding schema string. The schema placeholders are identified using a specific pattern
    # (`/*\schema_name*/\`) and are replaced using the `re.sub` function. If a schema string is
    # not found for a particular schema name, the original placeholder is retained in the system
    # message. The method returns the complete system message with the injected schemas.

        logger.debug("Injecting schemas into system message")

        # # Function to replace matched pattern with schema string
        # num_found_schemas = 0
        # def replacer(match):
        #     nonlocal num_found_schemas
        #     num_found_schemas += 1
        #     schema_name = match.group(1)  # Extract the schema_name from the matched pattern
        #     return schema_strings.get(schema_name, match.group(0))  # Return variable value or original if not found
        
        # # /*\schema_name*/\  # Pattern to match schema placeholders
        # schema_matcher = re.compile(r'\/\*\\(.*?)\/\*\\')  # Compile regex pattern to match schema placeholders

        # # Replace schema placeholders with schema strings in system message
        # complete_system_message = re.sub(schema_matcher, replacer, system_message)

        complete_system_message = f"{system_message}\n\n{json.dumps(schemas, separators=(',', ':'))}"

        # logger.info(f"Successfully injected *{num_found_schemas}* schemas")

        return complete_system_message