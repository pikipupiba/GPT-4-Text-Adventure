import dirtyjson
from dirtyjson.compat import StringIO
from PythonClasses.Schemas import schema_strings

# io = StringIO('["streaming API"]')
# print(dirtyjson.load(io)[0])

import json_stream

# def some_iterator():
#     yield b'{"some":'
#     yield b' "JSON"}'

# data = json_stream.load(some_iterator())

import json

def complete_json(s: str) -> (str, bool):
    # Removing trailing whitespaces
    original = s.rstrip()
    s = original
    
    # Check if it's empty
    if not s:
        return '', True
    
    # If the last character is a comma or colon, remove it since it indicates 
    # an incomplete key-value pair or list item
    if s[-1] in [',', ':']:
        s = s[:-1].rstrip()
    
    # If the string has an unclosed quote, check if it's a floating key or a value
    if s[-1] == '"':
        # Count quotes to determine if it's a key or value
        num_quotes = s.count('"')
        
        if num_quotes % 2 == 0:  # Even number of quotes, so it's a value
            pass
        else:  # Odd number of quotes, so it's a floating key
            s = s[::-1]  # Reverse string to find the previous quote or delimiter
            idx = s.find('"', 1)
            s = s[idx+1:][::-1]  # Remove the floating key
    
    # If the string has an unclosed quote after the above operation, close it
    if s.count('"') % 2 != 0:  # Odd number of quotes
        s += '"'
    
    # Count open and closed curly braces to detect open objects
    open_objects = s.count('{') - s.count('}')
    for _ in range(open_objects):
        s += '}'
    
    # Count open and closed square brackets to detect open arrays
    open_arrays = s.count('[') - s.count(']')
    for _ in range(open_arrays):
        s += ']'
    
    # If there are any trailing commas, remove them to make it valid JSON
    while s[-1] == ',':
        s = s[:-1].rstrip()
    
    # Check if the last character is a comma followed by a closing brace or bracket and remove it
    if s[-2:] in [',}', ',]']:
        s = s[:-2] + s[-1]
    
    # Determine if the passed JSON was incomplete
    is_complete = s == original
    
    return s, is_complete

# # Test again for the specific cases
# results_no_spaces = [(test, *complete_json(test)) for test in test_cases_no_spaces]
# specific_cases = [results_no_spaces[i] for i in [2, 3, 5, 6]]
# specific_cases

# Test the function
# data = '{"key": "value", "list": [1, 2, {"obj": ""}]}'
# result, was_complete = parse_incomplete_json(data)
# result, was_complete

# Test
# data = '{"key": "value", "list": [1, 2, {"obj": '
# result = parse_incomplete_json(data)
# print(result)

def some_iterator():
    for char in schema_strings["Stats_Schema"]:
        yield char


streaming_json = ""
result = None
for char in some_iterator():
    streaming_json += char
    result, complete = complete_json(streaming_json)
    yee = json.loads(result)
    print(result)
