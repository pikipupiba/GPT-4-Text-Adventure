import pytest
from typing import List, Dict, Union, Optional, Tuple
from enum import Enum, auto
import tiktoken
from collections.abc import Iterable

from PythonClasses.LLM.OpenAI import OpenAIModel

# Here, we're going to create a suite of tests for the OpenAIModel enum using pytest

@pytest.fixture(scope="module")
def example_string():
    return "This is a test string for tokenization."

@pytest.fixture(scope="module")
def example_tuple_prompt():
    return ("prompt", ["Hello", "How are you?"])

@pytest.fixture(scope="module")
def example_tuple_completion():
    return ("completion", ["Good morning", "I'm well"])

@pytest.fixture(scope="module")
def example_dict():
    return {
        "prompt": ["Hello", "What's up?"],
        "completion": ["Good day", "I'm doing well"]
    }

# Begin Tests
def test_enum_model_names():
    model_names = ["GPT_3_5_TURBO", "GPT_3_5_TURBO_16k", "GPT_4", "GPT_4_32k"]
    for model_name in model_names:
        assert model_name in OpenAIModel._member_names_

def test_model_str_representation():
    for model in OpenAIModel:
        assert str(model) == model.name

def test_model_max_tokens():
    assert OpenAIModel.GPT_3_5_TURBO.max_tokens == 4096
    assert OpenAIModel.GPT_3_5_TURBO_16k.max_tokens == 16384
    assert OpenAIModel.GPT_4.max_tokens == 8192
    assert OpenAIModel.GPT_4_32k.max_tokens == 32768

def test_model_price_prompt():
    assert OpenAIModel.GPT_3_5_TURBO.price["prompt"] == 0.0000015
    assert OpenAIModel.GPT_4.price["prompt"] == 0.00003

def test_model_price_completion():
    assert OpenAIModel.GPT_3_5_TURBO.price["completion"] == 0.000002
    assert OpenAIModel.GPT_4.price["completion"] == 0.00006

def test_encode_string(example_string):
    for model in OpenAIModel:
        assert isinstance(model.encode(example_string), list)

def test_encode_none():
    for model in OpenAIModel:
        assert model.encode(None) is None

def test_cost_input_prompt(example_tuple_prompt):
    for model in OpenAIModel:
        cost = model.cost(example_tuple_prompt)
        assert isinstance(cost, float)
        assert cost == model.num_tokens(example_tuple_prompt) * model.price["prompt"]

def test_cost_input_completion(example_tuple_completion):
    for model in OpenAIModel:
        cost = model.cost(example_tuple_completion)
        assert isinstance(cost, float)
        assert cost == model.num_tokens(example_tuple_completion) * model.price["completion"]

def test_cost_input_dict(example_dict):
    for model in OpenAIModel:
        cost_dict = model.cost(example_dict)
        assert isinstance(cost_dict, dict)
        for key, value in cost_dict.items():
            if key != "total":
                assert isinstance(value, (int, float))
            else:
                assert cost_dict["total"] == sum([v for k, v in cost_dict.items() if k != "total"])

def test_total_cost_input_tuple_prompt(example_tuple_prompt):
    for model in OpenAIModel:
        total_cost = model.total_cost(example_tuple_prompt)
        assert isinstance(total_cost, float)
        assert total_cost == model.num_tokens(example_tuple_prompt) * model.price["prompt"]

def test_total_cost_input_tuple_completion(example_tuple_completion):
    for model in OpenAIModel:
        total_cost = model.total_cost(example_tuple_completion)
        assert isinstance(total_cost, float)
        assert total_cost == model.num_tokens(example_tuple_completion) * model.price["completion"]

def test_total_cost_input_list(example_tuple_prompt, example_tuple_completion):
    input_list = [example_tuple_prompt, example_tuple_completion]
    for model in OpenAIModel:
        total_cost = model.total_cost(input_list)
        assert isinstance(total_cost, float)
        assert total_cost == sum(model.num_tokens(input_tuple) * model.price[input_tuple[0]] for input_tuple in input_list)

def test_tpm_max_values():
    assert OpenAIModel.GPT_3_5_TURBO.tpm_max == 90000
    assert OpenAIModel.GPT_4_32k.tpm_max == 0