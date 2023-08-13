from PythonClasses.Game.ChatMessage import TurnState, RoleType, DisplayType, ChatMessage, History, HistoryFilter

import pytest

def test_init():
    msg = ChatMessage(RoleType.USER, {DisplayType.DISPLAY: "Hi"})
    assert msg.role == RoleType.USER
    assert msg.display == "Hi"

def test_display_property():
    msg = ChatMessage(RoleType.USER, {DisplayType.DISPLAY: "Hi"})
    msg.display = "Hello"
    assert msg.display == "Hello"

def test_context_property():
    msg = ChatMessage(RoleType.USER, {DisplayType.DISPLAY: "Hi", DisplayType.CONTEXT: "Greetings"})
    assert msg.context == "Greetings"
    msg.context = "Salutations"
    assert msg.context == "Salutations"

def test_summary_property():
    msg = ChatMessage(RoleType.USER, {DisplayType.DISPLAY: "Hi", DisplayType.SUMMARY: "Summary here"})
    assert msg.summary == "Summary here"
    msg.summary = "New Summary"
    assert msg.summary == "New Summary"

def test_getitem():
    msg = ChatMessage(RoleType.USER, {DisplayType.DISPLAY: "Hi"})
    assert msg[DisplayType.DISPLAY] == "Hi"
    assert msg[0] == "Hi"

def test_setitem():
    msg = ChatMessage(RoleType.USER, {DisplayType.DISPLAY: "Hi"})
    msg[DisplayType.DISPLAY] = "Hello"
    assert msg[DisplayType.DISPLAY] == "Hello"
    msg[0] = "Hey"
    assert msg[DisplayType.DISPLAY] == "Hey"

def test_contains():
    msg = ChatMessage(RoleType.USER, {DisplayType.DISPLAY: "Hi"})
    assert DisplayType.DISPLAY in msg

def test_delitem():
    msg = ChatMessage(RoleType.USER, {DisplayType.DISPLAY: "Hi", DisplayType.CONTEXT: "Greetings"})
    del msg[DisplayType.DISPLAY]
    assert DisplayType.DISPLAY not in msg

def test_repr():
    msg = ChatMessage(RoleType.USER, {DisplayType.DISPLAY: "Hi"})
    assert repr(msg) == "<ChatMessage from RoleType.USER contains [DisplayType.DISPLAY]>"

def test_str():
    msg = ChatMessage(RoleType.USER, {DisplayType.DISPLAY: "Hi"})
    assert str(msg) == "Message from RoleType.USER: {DisplayType.DISPLAY: 'Hi'}"
