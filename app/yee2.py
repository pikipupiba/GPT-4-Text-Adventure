examples = [
    '{"',
    '{"na',
    '{"name"',
    '{"name":',
    '{"name": ',
    '{"name":"',
    '{"name": "',
    '{"name": "Joh',
    '{"name": "John"',
    '{"name": "John",',
    '{"name": "John" ,',
    '{"name": "John", "',
    '{"name": "John","ag',
    '{"name": "John", "age"',
    '{"name": "John", "age":',
    '{"name": "John", "age": 3',
    '{"name": "John", "age": 30,',
    '{"name": "John", "age": 30, "is_student": false, "skills": [',
    '{"name": "John", "age": 30, "is_student": false, "skills": ["',
    '{"name": "John", "age": 30, "is_student": false, "skills": ["Py',
    '{"name": "John", "age": 30, "is_student": false, "skills": ["Python"',
    '{"name": "John", "age": 30, "is_student": false, "skills": ["Python",',
    '{"name": "John", "age": 30, "is_student": false, "skills": ["Python", ',
    '{"name": "John", "age": 30, "is_student": false, "skills": ["Python", "',
]

def complete_json(data):
    stack = []
    output = []
    last_key_start = None
    awaiting_value = False
    
    for i, char in enumerate(data):
        if char == '"' and (i == 0 or data[i-1] != '\\'):
            if stack and stack[-1] == "string":
                stack.pop()
                if stack and stack[-1] == "key":
                    stack.pop()
                    awaiting_value = True
                elif stack and stack[-1] == "value":
                    stack.pop()
                    awaiting_value = False
            else:
                stack.append("string")
                if stack and stack[-1] == "object" and "key" not in stack and "value" not in stack:
                    stack.append("key")
                    last_key_start = len(output)
        elif char == ':' and "string" not in stack:
            if not awaiting_value:
                continue
            awaiting_value = False
            stack.append("value")
        elif char == ',' and "string" not in stack:
            if stack and stack[-1] == "value":
                stack.pop()
        elif char == '{' and "string" not in stack:
            stack.append("object")
            awaiting_value = False
        elif char == '}' and "string" not in stack and stack and stack[-1] == "object":
            stack.pop()
            if stack and stack[-1] == "key":
                stack.pop()
                output = output[:last_key_start]
            if stack and stack[-1] == "value":
                stack.pop()
            awaiting_value = False
        elif char == '[' and "string" not in stack:
            stack.append("array")
            awaiting_value = False
        elif char == ']' and "string" not in stack and stack and stack[-1] == "array":
            stack.pop()
        output.append(char)

    # Remove any incomplete keys or values
    if stack and stack[-1] == "key":
        output = output[:last_key_start]
    elif stack and stack[-1] == "value" and awaiting_value:
        if output[-1] == ':':
            output.pop()

    # Close any open objects or arrays
    while stack:
        context = stack.pop()
        if context == "object":
            output.append('}')
        elif context == "array":
            output.append(']')

    return ''.join(output)

# Running the completion function on the examples
completed_jsons = [complete_json(example) for example in examples]
completed_jsons