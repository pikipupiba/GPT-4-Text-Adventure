def complete_json(data):
    # FSM states
    START, OBJECT, KEY, AFTER_KEY, VALUE, ARRAY, STRING, NUMBER, BOOL = range(9)

    def handle_value_transition(char):
        nonlocal state
        transitions = {
            '"': STRING,
            '{': OBJECT,
            '[': ARRAY,
        }
        state = transitions.get(char, VALUE)
        stack.append(state)
        output.append(char)

    def handle_termination(char):
        nonlocal state
        if char in [',', '}', ']']:
            output.append(char)
            state = pop_state()

    def pop_state():
        stack.pop()
        return stack[-1] if stack else START

    state = START
    stack = []
    output = []

    for char in data:
        if state in [START, VALUE, ARRAY]:
            if char in ['{', '[', '"']:
                handle_value_transition(char)
            elif char in [',', '}', ']']:
                handle_termination(char)

        elif state == OBJECT:
            if char == '"':
                state = KEY
                stack.append(KEY)
                output.append(char)
            else:
                handle_termination(char)

        elif state == KEY:
            if char == '"':
                state = AFTER_KEY
            output[-1] += char

        elif state == AFTER_KEY:
            if char == ':':
                state = VALUE
                output.append(char)

        elif state == STRING:
            if char == '"' and output[-1] != '\\':
                state = pop_state()
            output[-1] += char

        elif state == NUMBER:
            if not char.isdigit() and char not in ['.', 'e', 'E', '+', '-']:
                state = pop_state()
            else:
                output[-1] += char

        elif state == BOOL:
            if char in [',', '}', ']']:
                state = pop_state()
                output.append(char)

    # Cleanup
    while output and output[-1] in [',', ' ']:
        output.pop()
    
    while stack and stack[-1] in [KEY, AFTER_KEY, VALUE]:
        stack.pop()
        output.pop()

    while output and output[-1] in [',', ' ']:
        output.pop()

    # Close any open objects or arrays
    while stack:
        context = stack.pop()
        output.append('}' if context == OBJECT else (']' if context == ARRAY else '"'))

    # Cleanup
    while output and output[-1] in [',', ' ', ':', '{', '[', '"']:
        output.pop()

    print(''.join(output))
    return ''.join(output)




array = [
    ['{"', 'obj', {}],
    ['{"na', 'obj->key->"na"', {}],
    ['{"name"', 'obj->key->"name"', {}],
    ['{"name":', 'obj->key->"name"', {}],
    ['{"name": ', 'obj->key->"name"', {}],
    ['{"name":"', 'obj->key->"name"', {}],
    ['{"name": "', 'obj->key->"name"->value->string->""', {"name": ""}],
    ['{"name": "Joh', 'obj->key->"name"->value->string->"Joh"', {"name": "Joh"}],
    ['{"name": "John"', 'obj', {"name": "John"}],
    ['{"name": "John",', 'obj', {"name": "John"}],
    ['{"name": "John" ,', 'obj', {"name": "John"}],
    ['{"name": "John", "', 'obj', {"name": "John"}],
    ['{"name": "John","ag', 'obj->key->"ag"', {"name": "John"}],
    ['{"name": "John", "age"', 'obj->key->"age"', {"name": "John"}],
    ['{"name": "John", "age":', 'obj->key->"age"', {"name": "John"}],
    ['{"name": "John", "age": 3', 'obj->key->"age"->value->3', {"name": "John", "age": 3}],
    ['{"name": "John", "age": 30,', 'obj->key->"age"->value->30', {"name": "John", "age": 30}],
    ['{"name": "John", "age": 30, "is_student": false, "skills": [', 'obj->key->"skills"->value->array', {"name": "John", "age": 30, "is_student": False, "skills": []}],
    ['{"name": "John", "age": 30, "is_student": false, "skills": ["', 'obj->key->"skills"->value->array->string->""', {"name": "John", "age": 30, "is_student": False, "skills": [""]}],
    ['{"name": "John", "age": 30, "is_student": false, "skills": ["Py', 'obj->key->"skills"->value->array->string->"Py"', {"name": "John", "age": 30, "is_student": False, "skills": ["Py"]}],
    ['{"name": "John", "age": 30, "is_student": false, "skills": ["Python"', 'obj->key->"skills"->value->array', {"name": "John", "age": 30, "is_student": False, "skills": ["Python"]}],
    ['{"name": "John", "age": 30, "is_student": false, "skills": ["Python",', 'obj->key->"skills"->value->array', {"name": "John", "age": 30, "is_student": False, "skills": ["Python"]}],
    ['{"name": "John", "age": 30, "is_student": false, "skills": ["Python", ', 'obj->key->"skills"->value->array', {"name": "John", "age": 30, "is_student": False, "skills": ["Python"]}],
    ['{"name": "John", "age": 30, "is_student": false, "skills": ["Python", "', 'obj->key->"skills"->value->array->string->""', {"name": "John", "age": 30, "is_student": False, "skills": ["Python", ""]}],
]

# Running the completion function on the examples
completed_jsons_fsm = [complete_json(example[0]) for example in array]
completed_jsons_fsm
