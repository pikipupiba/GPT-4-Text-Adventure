from PythonClasses.Game.ChatMessage import Role, DisplayType, ChatMessage
from PythonClasses.Game.History import TurnState, History, HistoryFilter

import pytest

def test_init():
    msg = ChatMessage(Role.USER, {DisplayType.DISPLAY: "Hi"})
    assert msg.role == Role.USER
    assert msg.display == "Hi"

def test_display_property():
    msg = ChatMessage(Role.USER, {DisplayType.DISPLAY: "Hi"})
    msg.display = "Hello"
    assert msg.display == "Hello"

def test_context_property():
    msg = ChatMessage(Role.USER, {DisplayType.DISPLAY: "Hi", DisplayType.CONTEXT: "Greetings"})
    assert msg.context == "Greetings"
    msg.context = "Salutations"
    assert msg.context == "Salutations"

def test_summary_property():
    msg = ChatMessage(Role.USER, {DisplayType.DISPLAY: "Hi", DisplayType.SUMMARY: "Summary here"})
    assert msg.summary == "Summary here"
    msg.summary = "New Summary"
    assert msg.summary == "New Summary"

def test_getitem():
    msg = ChatMessage(Role.USER, {DisplayType.DISPLAY: "Hi"})
    assert msg[DisplayType.DISPLAY] == "Hi"
    assert msg[1] == "Hi"

def test_setitem():
    msg = ChatMessage(Role.USER, {DisplayType.DISPLAY: "Hi"})
    msg[DisplayType.DISPLAY] = "Hello"
    assert msg[DisplayType.DISPLAY] == "Hello"
    msg[1] = "Hey"
    assert msg[DisplayType.DISPLAY] == "Hey"

def test_contains():
    msg = ChatMessage(Role.USER, {DisplayType.DISPLAY: "Hi"})
    assert DisplayType.DISPLAY in msg

def test_delitem():
    msg = ChatMessage(Role.USER, {DisplayType.DISPLAY: "Hi", DisplayType.CONTEXT: "Greetings"})
    del msg[DisplayType.DISPLAY]
    assert msg[DisplayType.DISPLAY] is None

def test_repr():
    msg = ChatMessage(Role.USER, {DisplayType.DISPLAY: "Hi"})
    assert repr(msg) == "<ChatMessage from Role.USER contains [DisplayType.DISPLAY]>"

def test_str():
    msg = ChatMessage(Role.USER, {DisplayType.DISPLAY: "Hi"})
    assert str(msg) == "Message from Role.USER: {DisplayType.DISPLAY: 'Hi'}"
