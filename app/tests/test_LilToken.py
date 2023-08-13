import time
from datetime import datetime
import pytest
from PythonClasses.LLM.LilToken import LilToken
from PythonClasses.LLM.OpenAI import OpenAIModel
from PythonClasses.Game.ChatMessage import RoleType, DisplayType, ChatMessage
from PythonClasses.Game.History import TurnState, History, HistoryFilter

# Mocking the OpenAIModel for testing purposes
class MockModel:
    model_name = "mock_model"
    
    price = {
        "prompt": 0.5,
        "completion": 2
    }

    @staticmethod
    def num_tokens(input_data):
        # Mocking the number of tokens for simplicity
        return input_data

    @staticmethod
    def cost(input=None, cost_type=None):
        if input is None:
            return 0

        # Mocking the cost based on input type
        if isinstance(input, (ChatMessage, History, HistoryFilter)):
            return MockModel.num_tokens(input) * MockModel.price.get(cost_type, 0.05)

        if isinstance(input, dict):
            cost_dict = {key: MockModel.cost(value, cost_type) for key, value in input.items()}
            total = sum(cost_dict.values())
            cost_dict["total"] = total
            return cost_dict

        if isinstance(input, (str, list, tuple)) and (input[0] == "prompt" or input[0] == "completion"):
            return MockModel.num_tokens(input[1]) * MockModel.price.get(input[0], 0.05)

        if isinstance(input, (list, tuple)):
            return sum(MockModel.cost(message) for message in input)

        return 0

# Test initialization
def test_initialization():
    token = LilToken(MockModel)
    assert token.model == MockModel
    assert token.start is not None
    assert token.end is None

# Test elapsed_time property
def test_elapsed_time():
    token = LilToken(MockModel)
    assert token.elapsed_time is not None

# Test tokens property
def test_tokens():
    token = LilToken(MockModel, system=10, history=20, completion=30)
    assert token.tokens == [10, 20, 30]

# ... (similar tests for other properties)

# Test stop method
def test_stop():
    token = LilToken(MockModel)
    token.stop()
    assert token.end is not None

# Test addition operation
def test_addition():
    token1 = LilToken(MockModel, system=10, history=20, completion=30)
    token2 = LilToken(MockModel, system=5, history=15, completion=25)
    result = token1 + token2
    assert result.system == 15
    assert result.history == 35
    assert result.completion == 55

# Test addition with different models (should raise an error)
def test_addition_different_models():
    class AnotherMockModel:
        name = "another_mock_model"
    
    token1 = LilToken(MockModel, system=10, history=20, completion=30)
    token2 = LilToken(AnotherMockModel, system=5, history=15, completion=25)
    with pytest.raises(Exception):
        result = token1 + token2

# Assuming the necessary imports are already present
# from PythonClasses.LLM.LilToken import LilToken
# from PythonClasses.LLM.OpenAI import OpenAIModel  # Mock this if needed
# import pytest

# 1. Test default initialization values
def test_default_values():
    token = LilToken(MockModel)
    assert token.system is 0
    assert token.history is 0
    assert token.completion is 0

# 2-4. Test individual token initializations
def test_system_initialization():
    token = LilToken(MockModel, system=10)
    assert token.system == 10

def test_history_initialization():
    token = LilToken(MockModel, history=20)
    assert token.history == 20

def test_completion_initialization():
    token = LilToken(MockModel, completion=30)
    assert token.completion == 30

# 5. Test token dictionary property
def test_token_dict():
    token = LilToken(MockModel, system=10, history=20, completion=30)
    assert token.token_dict == {"system": 10, "history": 20, "completion": 30}

# 6-7. Test prompt and completion token properties
def test_prompt_tokens():
    token = LilToken(MockModel, system=10, history=20)
    assert token.prompt_tokens == 30

def test_completion_tokens():
    token = LilToken(MockModel, completion=30)
    assert token.completion == 30

# 8. Test total tokens property
def test_total_tokens():
    token = LilToken(MockModel, system=10, history=20, completion=30)
    assert token.total_tokens == 60

# 9-10. Test elapsed time before and after stop
def test_elapsed_time_before_stop():
    token = LilToken(MockModel)
    assert token.elapsed_time is not None

def test_elapsed_time_after_stop():
    token = LilToken(MockModel)
    token.stop()
    assert token.elapsed_time is not None

# 11-13. Test TPM properties
def test_tpm_system():
    token = LilToken(MockModel, system=600)
    time.sleep(0.1)
    token.stop()
    assert token.tpm[0] == 600 / token.elapsed_time * 60

def test_tpm_history():
    token = LilToken(MockModel, history=600)
    time.sleep(0.1)
    token.stop()
    assert token.tpm[1] == 600 / token.elapsed_time * 60

def test_tpm_completion():
    token = LilToken(MockModel, completion=600)
    time.sleep(0.1)
    token.stop()
    assert token.tpm[2] == 600 / token.elapsed_time * 60

# 14. Test TPM total
def test_tpm_total():
    token = LilToken(MockModel, system=600, history=600, completion=600)
    time.sleep(0.1)
    token.stop()
    assert token.tpm_total == 1800 / token.elapsed_time * 60

# 15-17. Test cost properties (assuming MockModel's cost method returns sum of tokens)
def test_cost_system():
    token = LilToken(MockModel, system=10)
    assert token.cost[0] == 10 * 0.5

def test_cost_history():
    token = LilToken(MockModel, history=20)
    assert token.cost[1] == 20 * 0.5

def test_cost_completion():
    token = LilToken(MockModel, completion=30)
    assert token.cost[2] == 30 * 2

# 18-20. Test CPM properties
def test_cpm_system():
    token = LilToken(MockModel, system=600)
    time.sleep(0.1)
    token.stop()
    assert token.cpm[0] == 600*0.5 / token.elapsed_time * 60

def test_cpm_history():
    token = LilToken(MockModel, history=600)
    time.sleep(0.1)
    token.stop()
    assert token.cpm[1] == 600*0.5 / token.elapsed_time * 60

def test_cpm_completion():
    token = LilToken(MockModel, completion=600)
    time.sleep(0.1)
    token.stop()
    assert token.cpm[2] == 600*2 / token.elapsed_time * 60

# 21. Test CPM total
def test_cpm_total():
    token = LilToken(MockModel, system=600, history=600, completion=600)
    time.sleep(0.1)
    token.stop()
    assert token.cpm_total == 1800 / token.elapsed_time * 60

# 22-24. Test addition with None values
def test_addition_with_none_start():
    token1 = LilToken(MockModel, system=10, start=None)
    token2 = LilToken(MockModel, system=5)
    result = token1 + token2
    assert result.start == token2.start

def test_addition_with_none_end():
    token1 = LilToken(MockModel, system=10)
    token1.stop()
    token2 = LilToken(MockModel, system=5, end=None)
    result = token1 + token2
    assert result.end == token1.end

def test_addition_with_both_none_start():
    token1 = LilToken(MockModel, system=10, start=None)
    token2 = LilToken(MockModel, system=5, start=None)
    result = token1 + token2
    assert result.start is not None

# 25-27. Test addition with different models
def test_addition_same_models():
    token1 = LilToken(MockModel, system=10)
    token2 = LilToken(MockModel, system=5)
    result = token1 + token2
    assert result.system == 15

def test_addition_different_models():
    class AnotherMockModel:
        name = "another_mock_model"
    
    token1 = LilToken(MockModel, system=10)
    token2 = LilToken(AnotherMockModel, system=5)
    with pytest.raises(Exception):
        result = token1 + token2

# 28-30. Test elapsed time with different start and end times
def test_elapsed_time_with_start():
    from datetime import timedelta
    token = LilToken(MockModel, start=datetime.now() - timedelta(minutes=5))
    assert 300 <= token.elapsed_time <= 301

def test_elapsed_time_with_end():
    from datetime import timedelta
    token = LilToken(MockModel, end=datetime.now() + timedelta(minutes=5))
    assert 299 <= token.elapsed_time <= 301

def test_elapsed_time_with_start_and_end():
    from datetime import timedelta
    token = LilToken(MockModel, start=datetime.now() - timedelta(minutes=10), end=datetime.now() - timedelta(minutes=5))
    assert 300 <= token.elapsed_time <= 301
