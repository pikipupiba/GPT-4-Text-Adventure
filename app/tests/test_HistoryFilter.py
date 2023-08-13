from PythonClasses.Game.ChatMessage import Role, DisplayType, ChatMessage
from PythonClasses.Game.History import TurnState, History, HistoryFilter

import pytest

def create_sample_messages():
    return [
        ChatMessage(Role.USER, {DisplayType.DISPLAY: "User 1", DisplayType.CONTEXT: "Context User 1"}),
        ChatMessage(Role.ASSISTANT, {DisplayType.DISPLAY: "Assistant 1", DisplayType.CONTEXT: "Context Assistant 1", DisplayType.SUMMARY: "Summary Assistant 1"}),
        ChatMessage(Role.USER, {DisplayType.DISPLAY: "User 2", DisplayType.CONTEXT: "Context User 2", DisplayType.SUMMARY: "Summary User 2"}),
        ChatMessage(Role.SYSTEM, {DisplayType.DISPLAY: "System 1", DisplayType.CONTEXT: "Context System 1"})
    ]

@pytest.fixture
def sample_history():
    messages = create_sample_messages()
    return HistoryFilter(messages)

def test_history_filter_initialization(sample_history):
    assert len(sample_history) == 4

def test_history_filter_context_distance(sample_history):
    hf = HistoryFilter([], context_distance=5)
    assert hf._context_distance == 5

def test_history_filter_display_history_full(sample_history):
    display_history = sample_history.display_history()
    assert len(display_history) == 2
    assert display_history[0] == ("User 1", "Assistant 1")
    assert display_history[1] == ("User 2", None)

def test_history_filter_display_history_limit(sample_history):
    display_history = sample_history.display_history(display_distance=2)
    assert len(display_history) == 2
    assert display_history[1] == ("User 2", None)

def test_history_filter_context_history_full(sample_history):
    context_history = sample_history.context_history()
    assert len(context_history) == 3
    assert context_history[0]["content"] == "Context User 1"
    assert context_history[1]["content"] == "Context Assistant 1"
    assert context_history[2]["content"] == "Context User 2"

def test_history_filter_context_history_limit_context(sample_history):
    context_history = sample_history.context_history(context_distance=1)
    assert len(context_history) == 1
    assert context_history[0]["content"] == "Context User 2"

def test_history_filter_context_history_limit_summary(sample_history):
    context_history = sample_history.context_history(summary_distance=1)
    assert len(context_history) == 3

def test_history_filter_api_call_context(sample_history):
    api_call_context = sample_history.api_call_context()
    assert len(api_call_context) == 4
    assert api_call_context[-1] == "Context System 1"

def test_history_filter_with_no_messages():
    hf = HistoryFilter()
    assert len(hf.display_history()) == 0
    assert len(hf.context_history()) == 0
    assert len(hf.api_call_context()) == 0

def test_history_filter_only_summary_used_in_context():
    msg = ChatMessage(Role.USER, {DisplayType.SUMMARY: "Summary User"})
    hf = HistoryFilter([msg])
    context = hf.context_history()
    assert context[0]["content"] == "Summary User"

def test_history_filter_both_context_and_summary():
    msg1 = ChatMessage(Role.USER, {DisplayType.CONTEXT: "Context User"})
    msg2 = ChatMessage(Role.USER, {DisplayType.SUMMARY: "Summary User"})
    hf = HistoryFilter([msg1, msg2])
    context = hf.context_history()
    assert context[0]["content"] == "Context User"
    assert context[1]["content"] == "Summary User"

def test_history_filter_context_history_role_ordering(sample_history):
    context_history = sample_history.context_history()
    assert context_history[0]["role"] == "user"
    assert context_history[1]["role"] == "assistant"

def test_history_filter_display_history_multiple_assistant_msgs():
    messages = [
        ChatMessage(Role.USER, {DisplayType.DISPLAY: "User 1"}),
        ChatMessage(Role.ASSISTANT, {DisplayType.DISPLAY: "Assistant 1"}),
        ChatMessage(Role.ASSISTANT, {DisplayType.DISPLAY: "Assistant 2"})
    ]
    hf = HistoryFilter(messages)
    display_history = hf.display_history()
    assert len(display_history) == 2
    assert display_history[1] == (None, "Assistant 2")

def test_history_filter_context_history_with_only_context():
    messages = [
        ChatMessage(Role.USER, {DisplayType.CONTEXT: "Context User 1"}),
        ChatMessage(Role.ASSISTANT, {DisplayType.CONTEXT: "Context Assistant 1"})
    ]
    hf = HistoryFilter(messages)
    context_history = hf.context_history()
    assert len(context_history) == 2
    assert context_history[0]["content"] == "Context User 1"

def test_history_filter_last_system_message_context(sample_history):
    assert sample_history.last_system_message[DisplayType.CONTEXT] == "Context System 1"

def test_history_filter_summary_priority_over_context():
    msg = ChatMessage(Role.USER, {DisplayType.CONTEXT: "Context User", DisplayType.SUMMARY: "Summary User"})
    hf = HistoryFilter([msg], summary_distance=0)
    context = hf.context_history()
    assert context[0]["content"] == "Summary User"

def test_history_filter_empty_message():
    msg = ChatMessage(Role.USER, {})
    hf = HistoryFilter([msg])
    assert len(hf.context_history()) == 0

def test_history_filter_add_and_pop(sample_history):
    hf = HistoryFilter()
    msg = ChatMessage(Role.USER, {DisplayType.DISPLAY: "Hi"})
    hf.append(msg)
    assert len(hf) == 1
    popped_msg = hf.pop()
    assert popped_msg == msg
    assert len(hf) == 0

def test_history_filter_display_without_messages():
    hf = HistoryFilter()
    assert len(hf.display_history()) == 0
