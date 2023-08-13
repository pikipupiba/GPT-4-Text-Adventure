from typing import Dict, List, Optional, Tuple, Union
from enum import Enum, auto
from PythonClasses.Game.ChatMessage import ChatMessage, Role

class TurnState(Enum):
    AWAITING_USER = auto()
    AWAITING_ASSISTANT = auto()
    AWAITING_ACTION = auto()  # This could represent some other state, just an example

class History:
    def __init__(self, messages: Optional[List[ChatMessage]] = None):
        self.messages = messages if messages is not None else []
        self.current_system_message = None
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
    
    @property
    def current_system_message_openai_format(self) -> dict:
        """Format the system message for display."""
        if self.current_system_message is None:
            return {}
        return {
            'role': "system",
            'content': self.current_system_message.content
        }
    
    def __add__(self, other: Union[ChatMessage, List[ChatMessage], 'History']) -> 'History':
        if isinstance(other, ChatMessage):
            return History(self.messages + [other])
        elif isinstance(other, list):
            return History(self.messages + other)
        elif isinstance(other, History):
            return History(self.messages + other.messages)
        else:
            raise ValueError("You can only add a ChatMessage or another History to History.")
    
    def __iadd__(self, other: Union[ChatMessage, List[ChatMessage], 'History']) -> 'History':
        if isinstance(other, ChatMessage):
            if other.role == Role.SYSTEM:
                # If the system message has changed, update it.
                if self.current_system_message is None or self.current_system_message.content[0] != other.content[0]:  # Assuming the first index (0) is for SYSTEM content
                    self.current_system_message = other
            self.append(other)
        elif isinstance(other, list):
            for message in other:
                if not isinstance(message, ChatMessage):
                    raise ValueError("The list should only contain ChatMessage objects.")
                self.append(message)
        elif isinstance(other, History):
            self.messages.extend(other.messages)
        else:
            raise ValueError("You can only add a ChatMessage, a list of ChatMessages, or another History to History.")
        return self

    def get_messages(self, roles: Union[Role, List[Role]], start_index: Optional[int] = None, end_index: Optional[int] = None) -> Dict[str, List[Dict]]:
        # Ensure the roles are in a list format
        if not isinstance(roles, list):
            roles = [roles]

        # Filter messages using list comprehension
        filtered_messages = [msg for msg in self.messages[start_index:end_index] if msg.role in roles]

        results = {
            'display': [],
            'context': [],
            'summary': []
        }
        for msg in filtered_messages:
            if msg.display:
                results['display'].append({
                    'role': msg.role,
                    'content': msg.display
                })
            if msg.context:
                results['context'].append({
                    'role': msg.role,
                    'content': msg.context
                })
            if msg.summary:
                results['summary'].append({
                    'role': msg.role,
                    'content': msg.summary
                })

        # Filter out keys with empty lists
        results = {key: val for key, val in results.items() if val}

        return results


    @property
    def last_system_message(self) -> Optional[ChatMessage]:
        return next((message for message in reversed(self.messages) if message.role == Role.SYSTEM), None)

    def get_last_message_of_type(self, role: Role) -> Optional[Tuple[ChatMessage, int]]:
        return next(((message, index) for index, message in reversed(list(enumerate(self.messages))) if message.role == role), None)
    
    @property
    def last_role(self) -> Optional[Role]:
        if self.messages:
            return self.messages[-1].role
        return None
    
    @property
    def turn_state(self) -> TurnState:
        if not self.messages:
            return TurnState.AWAITING_USER
        
        last_role = self.last_role

        if last_role == Role.USER:
            return TurnState.AWAITING_ASSISTANT
        elif last_role == Role.ASSISTANT:
            return TurnState.AWAITING_USER  # Assuming the next message would be from the user
        else:
            # For system or other message types, you can add more logic here
            # I've added a default state, but you can adjust based on your needs
            return TurnState.AWAITING_ACTION

class HistoryFilter(History):

    DEFAULT_CONTEXT_DISTANCE = 100
    DEFAULT_SUMMARY_DISTANCE = 100
    DEFAULT_DISPLAY_DISTANCE = 100

    def __init__(self, messages: Optional[List[ChatMessage]] = None, **kwargs):
        super().__init__(messages)
        self._context_distance = kwargs.get("context_distance", None)
        self._summary_distance = kwargs.get("summary_distance", None)
        self._display_distance = kwargs.get("display_distance", None)

    def _filter_messages_by_role_and_type(self, roles: List[Role], content_types: List[str], distance: Optional[int] = None) -> List[ChatMessage]:
        """Filter messages based on roles and content types."""
        messages = [msg for msg in self.messages if msg.role in roles and any(content_type in ['display', 'context', 'summary'] for content_type in content_types)]
        return messages[-distance:] if distance is not None else messages

    def display_history(self, display_distance: Optional[int] = None) -> List[List[Optional[str]]]:
        """Return paired user and assistant display messages."""
        display_distance = display_distance if display_distance is not None else self._display_distance
        messages = self._filter_messages_by_role_and_type([Role.USER, Role.ASSISTANT], ['display'], display_distance)
        
        user_messages, assistant_messages = [], []
        for message in messages:
            if message.role == Role.USER:
                user_messages.append(message.display)
                assistant_messages.append(None)
            else:
                if assistant_messages and assistant_messages[-1] is None:
                    assistant_messages[-1] = message.display
                else:
                    user_messages.append(None)
                    assistant_messages.append(message.display)

        return list(zip(user_messages, assistant_messages))

    def context_history(self, context_distance: Optional[int] = None, summary_distance: Optional[int] = None) -> List[Dict[str, str]]:
        """Return context or summary of recent messages."""
        
        # Default to class attributes if parameters are not provided
        context_distance = context_distance or self._context_distance
        summary_distance = summary_distance or self._summary_distance

        # Filter messages based on role and type
        messages = self._filter_messages_by_role_and_type([Role.USER, Role.ASSISTANT], ['context', 'summary'], context_distance)
        
        # Using list comprehension for faster processing
        context = [
            {
                "role": msg.role.name.lower(),
                "content": msg.context if (summary_distance is None or idx < summary_distance) and msg.context else msg.summary or msg.context
            }
            for idx, msg in enumerate(messages) if msg.context or msg.summary
        ]

        return context

    def api_call_context(self) -> List[str]:
        """Return context for API calls."""
        recent_messages = self.context_history()
        if hasattr(self, 'last_system_message') and self.last_system_message:
            recent_messages.append(self.last_system_message.context)
        return recent_messages