import pytest
from PythonClasses.Game.ChatMessage import RoleType, DisplayType, ChatMessage
from PythonClasses.Game.History import TurnState, History, HistoryFilter

def test_chat_message_initialization():
    cm = ChatMessage(RoleType.USER, {DisplayType.DISPLAY: "Hello"})
    assert cm.role == RoleType.USER
    assert cm.display == "Hello"
    assert cm.context is None
    assert cm.summary is None

def test_chat_message_setters_and_getters():
    cm = ChatMessage(RoleType.USER, {DisplayType.DISPLAY: "Hello"})
    
    # Using display property
    cm.display = "Updated Message"
    assert cm.display == "Updated Message"
    
    # Using __getitem__ and __setitem__
    cm[DisplayType.SUMMARY] = "Summary Message"
    assert cm[DisplayType.SUMMARY] == "Summary Message"
    
    # Using integer index
    cm[1] = "Display using index"
    assert cm.display == "Display using index"
    
    with pytest.raises(KeyError):
        _ = cm[4]

def test_chat_message_special_methods():
    cm = ChatMessage(RoleType.USER, {DisplayType.DISPLAY: "Hello", DisplayType.SUMMARY: "Summary"})
    assert cm[DisplayType.DISPLAY] == "Hello"
    assert cm[DisplayType.CONTEXT] is None

    # Test repr and str
    assert "<ChatMessage" in repr(cm)
    assert "Message from" in str(cm)

def test_history_methods():
    history = History()
    cm1 = ChatMessage(RoleType.USER, {DisplayType.DISPLAY: "Hello"})
    cm2 = ChatMessage(RoleType.ASSISTANT, {DisplayType.DISPLAY: "Hi"})
    cm3 = ChatMessage(RoleType.SYSTEM, {DisplayType.DISPLAY: "Info"})
    
    history.append(cm1)
    history.append(cm2)
    history.append(cm3)
    
    assert len(history) == 3
    assert history[1].display == "Hi"
    
    last_message, idx = history.get_last_message_of_type(RoleType.USER)
    assert last_message.display == "Hello"
    assert idx == 0

    assert history.last_system_message.display == "Info"
    assert history.last_role == RoleType.SYSTEM
    assert history.turn_state == TurnState.AWAITING_ACTION

    history.pop()
    assert len(history) == 2

    history2 = History([ChatMessage(RoleType.USER, {DisplayType.DISPLAY: "New Message"})])
    combined_history = history + history2
    assert len(combined_history) == 3

def test_history_filter_methods():
    history = HistoryFilter()
    cm1 = ChatMessage(RoleType.USER, {DisplayType.DISPLAY: "Hello"})
    cm2 = ChatMessage(RoleType.ASSISTANT, {DisplayType.DISPLAY: "Hi", DisplayType.CONTEXT: "Greeting context"})
    cm3 = ChatMessage(RoleType.USER, {DisplayType.DISPLAY: "Info", DisplayType.CONTEXT: "Info context"})
    
    history.append(cm1)
    history.append(cm2)
    history.append(cm3)
    
    paired_display = history.display_history()
    assert len(paired_display) == 2
    assert paired_display[1][1] == None
    assert paired_display[0][1] == "Hi"

    context_history = history.context_history()
    assert len(context_history) == 2

    assert context_history[0]['content'] == "Greeting context"
    
    api_context = history.api_call_context()
    assert len(api_context) == 2
    assert api_context[-1]['content'] == "Info context"

@pytest.fixture
def chat_history():
    # A pytest fixture to create and return a sample chat history
    messages = [
        ChatMessage(RoleType.USER, {DisplayType.DISPLAY: "Hello 1"}),
        ChatMessage(RoleType.ASSISTANT, {DisplayType.DISPLAY: "Hi 1", DisplayType.CONTEXT: "Context 1"}),
        ChatMessage(RoleType.USER, {DisplayType.DISPLAY: "Hello 2"}),
        ChatMessage(RoleType.ASSISTANT, {DisplayType.DISPLAY: "Hi 2", DisplayType.CONTEXT: "Context 2"}),
    ]
    return History(messages)

def test_history_methods_with_fixture(chat_history):
    assert len(chat_history) == 4
    assert chat_history[2].display == "Hello 2"
