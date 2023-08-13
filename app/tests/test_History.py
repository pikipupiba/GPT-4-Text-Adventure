import pytest
from PythonClasses.Game.ChatMessage import RoleType, DisplayType, ChatMessage
from PythonClasses.Game.History import TurnState, History, HistoryFilter

def test_init():
    history = History()
    assert len(history) == 0
    
    history_with_msgs = History([chat_msg1, chat_msg2])
    assert len(history_with_msgs) == 2

def test_get_item():
    history = History([chat_msg1, chat_msg2])
    assert history[0] == chat_msg1

def test_set_item():
    history = History([chat_msg1, chat_msg2])
    history[0] = chat_msg3
    assert history[0] == chat_msg3

def test_append():
    history = History()
    history.append(chat_msg1)
    assert chat_msg1 in history

def test_pop():
    history = History([chat_msg1])
    popped_msg = history.pop()
    assert popped_msg == chat_msg1

def test_truncate():
    history = History([chat_msg1, chat_msg2, chat_msg3])
    history.truncate(2)
    assert len(history) == 2

def test_clear():
    history = History([chat_msg1, chat_msg2])
    history.clear()
    assert len(history) == 0

def test_len():
    history = History([chat_msg1, chat_msg2])
    assert len(history) == 2

def test_iter():
    history = History([chat_msg1, chat_msg2])
    messages = list(history)
    assert messages == [chat_msg1, chat_msg2]

def test_add():
    history1 = History([chat_msg1])
    history2 = History([chat_msg2])
    combined = history1 + history2
    assert len(combined) == 2

def test_iadd():
    history = History([chat_msg1])
    history += chat_msg2
    assert len(history) == 2

def test_get_messages():
    history = History([chat_msg1, chat_msg2, chat_msg3])
    msgs = history.get_messages(RoleType.USER, DisplayType.DISPLAY)
    assert len(msgs[DisplayType.DISPLAY]) == 1
    assert msgs[DisplayType.DISPLAY][0]['role'] == RoleType.USER

def test_last_system_message():
    history = History([chat_msg1, chat_msg2, chat_msg3])
    assert history.last_system_message == chat_msg3

def test_get_last_message_of_type():
    history = History([chat_msg1, chat_msg2, chat_msg3])
    last_msg, index = history.get_last_message_of_type(RoleType.USER)
    assert last_msg == chat_msg1
    assert index == 0

def test_last_role():
    history = History([chat_msg1, chat_msg2])
    assert history.last_role == RoleType.ASSISTANT

def test_turn_state():
    history = History([chat_msg1, chat_msg2])
    assert history.turn_state == TurnState.AWAITING_USER

# Setup
chat_msg1 = ChatMessage(RoleType.USER, {DisplayType.DISPLAY: "Hi"})
chat_msg2 = ChatMessage(RoleType.ASSISTANT, {DisplayType.DISPLAY: "Hello"})
chat_msg3 = ChatMessage(RoleType.SYSTEM, {DisplayType.DISPLAY: "Welcome"})
