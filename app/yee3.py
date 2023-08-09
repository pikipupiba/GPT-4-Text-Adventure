import json

def complete_json(data):

    try:
        json.loads(data)
        return data, True
    except:
        pass

    # FSM states
    START, OBJECT, KEY, AFTER_KEY, VALUE, ARRAY, STRING, NUMBER, BOOL = range(9)
    state = START

    stack = []  # To keep track of opened structures
    output = []

    for char in data:
        if state == START:
            if char == '{':
                state = OBJECT
                stack.append(OBJECT)
                output.append('{')
            elif char == '[':
                state = ARRAY
                stack.append(ARRAY)
                output.append('[')
            
        elif state == OBJECT:
            if char == '"':
                state = KEY
                stack.append(KEY)
                output.append('"')
            elif char == '}':
                stack.pop()
                while stack and stack[-1] in [KEY, VALUE]:
                    stack.pop()
                state = stack[-1]
                state = stack[-1]
                output.append('}')
            elif char == ',':
                output.append(',')
                state = OBJECT

        elif state == KEY:
            if char == '"':
                state = AFTER_KEY
            
            output[-1] += char

        elif state == AFTER_KEY:
            if char == ':':
                state = VALUE
                stack.append(VALUE)
                output.append(':')

        elif state == VALUE:
            if char == '"':
                state = STRING
                stack.append(STRING)
                output.append('"')
            elif char == '{':
                state = OBJECT
                stack.append(OBJECT)
                output.append('{')
            elif char == '[':
                state = ARRAY
                stack.append(ARRAY)
                output.append('[')
            elif char == ',':
                output.append(',')
                if stack[-2] == OBJECT:
                    state = OBJECT
                elif stack[-1] == ARRAY:
                    state = ARRAY
            elif char == '}':
                stack.pop()
                state = stack[-1]
                output.append('}')
            elif char == ']':
                stack.pop()
                state = stack[-1]
                output.append(']')
            elif char.isdigit() or char in ['-', '+']:
                state = NUMBER
                stack.append(NUMBER)
                output.append(char)
            elif char.lower() == 't':
                state = BOOL
                stack.append(BOOL)
                output.append("true")
            elif char.lower() == 'f':
                state = BOOL
                stack.append(BOOL)
                output.append("false")
        elif state == BOOL:
            if char == ',':
                stack.pop()
                while stack and stack[-1] in [KEY, VALUE]:
                    stack.pop()
                state = stack[-1]
                output.append(',')
            elif char == '}':
                stack.pop()
                while stack and stack[-1] in [KEY, VALUE]:
                    stack.pop()
                state = stack[-1]
                output.append('}')
            elif char == ']':
                stack.pop()
                while stack and stack[-1] in [KEY, VALUE]:
                    stack.pop()
                state = stack[-1]
                output.append(']')

        elif state == ARRAY:
            if char == '"':
                state = STRING
                stack.append(STRING)
                output.append('"')
            elif char == '{':
                state = OBJECT
                stack.append(OBJECT)
                output.append('{')
            elif char == '[':
                state = ARRAY
                stack.append(ARRAY)
                output.append('[')
            elif char == ',':
                output.append(',')
                state = ARRAY
            elif char == ']':
                stack.pop()
                while stack and stack[-1] in [KEY, VALUE]:
                    stack.pop()
                state = stack[-1]
                output.append(']')

        elif state == STRING:
            if char == '"' and output[-1] != '\\':
                stack.pop()
                
                while stack and stack[-1] in [KEY, VALUE]:
                    stack.pop()
                state = stack[-1]
            
            output[-1] += char
        
        elif state == NUMBER:
            if not char.isdigit() and char not in ['.', 'e', 'E', '+', '-']:

                if char == ',':
                    output.append(',')

                stack.pop()
                while stack and stack[-1] in [KEY, VALUE]:
                    stack.pop()
                state = stack[-1]
            else:
            
                output[-1] += char

        # output.append(char)

    # Clean up the end of the output
    # while output and output[-1] in [',', ':', '{', '[', '"', ' ']:
    #     output.pop()

    while output[-1] in [',', ' ']:
        output.pop()

    while stack and stack[-1] in [KEY, AFTER_KEY, VALUE]:
        stack.pop()
        if output[-1] not in ['}', ']']:
            output.pop()

    while output[-1] in [',', ' ']:
        output.pop()

    # Close any open objects or arrays
    while stack:
        context = stack.pop()
        if context == OBJECT:
            output.append('}')
        elif context == ARRAY:
            output.append(']')
        elif context == STRING:
            output[-1] += '"'

    print(''.join(output))
    return json.loads(''.join(output)), False


array = [
    ['{"Stats_Schema": {"day": "Monday", "time": 55, "items":[{"name": "yee", "desc": "asd', 'obj', {}],
    # ['{"na', 'obj->key->"na"', {}],
    # ['{"name"', 'obj->key->"name"', {}],
    # ['{"name":', 'obj->key->"name"', {}],
    # ['{"name": ', 'obj->key->"name"', {}],
    # ['{"name":"', 'obj->key->"name"', {}],
    # ['{"name": "', 'obj->key->"name"->value->string->""', {"name": ""}],
    # ['{"name": "Joh', 'obj->key->"name"->value->string->"Joh"', {"name": "Joh"}],
    # ['{"name": "John"', 'obj', {"name": "John"}],
    # ['{"name": "John",', 'obj', {"name": "John"}],
    # ['{"name": "John" ,', 'obj', {"name": "John"}],
    # ['{"name": "John", "', 'obj', {"name": "John"}],
    # ['{"name": "John","ag', 'obj->key->"ag"', {"name": "John"}],
    # ['{"name": "John", "age"', 'obj->key->"age"', {"name": "John"}],
    # ['{"name": "John", "age":', 'obj->key->"age"', {"name": "John"}],
    # ['{"name": "John", "age": 3', 'obj->key->"age"->value->3', {"name": "John", "age": 3}],
    # ['{"name": "John", "age": 30,', 'obj->key->"age"->value->30', {"name": "John", "age": 30}],
    # ['{"name": "John", "age": 30, "is_student": false, "skills": [', 'obj->key->"skills"->value->array', {"name": "John", "age": 30, "is_student": False, "skills": []}],
    # ['{"name": "John", "age": 30, "is_student": false, "skills": ["', 'obj->key->"skills"->value->array->string->""', {"name": "John", "age": 30, "is_student": False, "skills": [""]}],
    # ['{"name": "John", "age": 30, "is_student": false, "skills": ["Py', 'obj->key->"skills"->value->array->string->"Py"', {"name": "John", "age": 30, "is_student": False, "skills": ["Py"]}],
    # ['{"name": "John", "age": 30, "is_student": false, "skills": ["Python"', 'obj->key->"skills"->value->array', {"name": "John", "age": 30, "is_student": False, "skills": ["Python"]}],
    # ['{"name": "John", "age": 30, "is_student": false, "skills": ["Python",', 'obj->key->"skills"->value->array', {"name": "John", "age": 30, "is_student": False, "skills": ["Python"]}],
    # ['{"name": "John", "age": 30, "is_student": false, "skills": ["Python", ', 'obj->key->"skills"->value->array', {"name": "John", "age": 30, "is_student": False, "skills": ["Python"]}],
    # ['{"name": "John", "age": 30, "is_student": false, "skills": ["Python", "', 'obj->key->"skills"->value->array->string->""', {"name": "John", "age": 30, "is_student": False, "skills": ["Python", ""]}],
]

json_yee = {
  "Stats_Schema": {
    "day": "Monday",
    "time": 60,
    "items": [
      {
        "name": "Sketchbook and Pencils",
        "description": "A neat collection of drawing pencils and a sketchbook"
      },
      {
        "name": "Beep",
        "description": "Boppopoop"
      }
    ],
    "relationships": [
      {
        "name": "Friend",
        "count": 1,
        "description": "A friend of mine"
      },
      {
        "name": "Enemy",
        "count": 10,
        "description": "An enemy of mine"
      }
    ]
  }
}

string_json = json.dumps(json_yee, separators=(',', ':'))

# Running the completion function on the examples

# completed_jsons_fsm = [complete_json(example[0]) for example in array]
# completed_jsons_fsm

for i in range(199,len(string_json)):
    print(i)
    completed_jsons_fsm = complete_json(string_json[0:i])