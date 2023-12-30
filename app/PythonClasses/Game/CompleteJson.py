import json

from loguru import logger


class CompleteJson:
    # The `CompleteJson` class is a Python class that provides a method called `complete_json`. This
    # method takes a string as input and attempts to complete any incomplete JSON structures in the
    # string. It uses a finite state machine (FSM) approach to parse the input string and identify
    # the incomplete JSON structures. It then adds the necessary closing brackets or quotes to
    # complete the structures.

    def complete_json(data):
        try:
            data_json = json.loads(data.strip())
            return data_json, True
        except:
            pass

        # FSM states
        START, OBJECT, KEY, AFTER_KEY, VALUE, ARRAY, STRING, NUMBER, BOOL = range(9)
        state = START

        stack = []  # To keep track of opened structures
        output = []

        for char in data:
            if state == START:
                if char == "{":
                    state = OBJECT
                    stack.append(OBJECT)
                    output.append("{")
                elif char == "[":
                    state = ARRAY
                    stack.append(ARRAY)
                    output.append("[")

            elif state == OBJECT:
                if char == '"':
                    state = KEY
                    stack.append(KEY)
                    output.append('"')
                elif char == "}":
                    stack.pop()
                    while stack and stack[-1] in [KEY, VALUE]:
                        stack.pop()
                    state = stack[-1]
                    output.append("}")
                elif char == ",":
                    output.append(",")
                    state = OBJECT

            elif state == KEY:
                if char == '"':
                    state = AFTER_KEY

                output[-1] += char

            elif state == AFTER_KEY:
                if char == ":":
                    state = VALUE
                    stack.append(VALUE)
                    output.append(":")

            elif state == VALUE:
                if char == '"':
                    state = STRING
                    stack.append(STRING)
                    output.append('"')
                elif char == "{":
                    state = OBJECT
                    stack.append(OBJECT)
                    output.append("{")
                elif char == "[":
                    state = ARRAY
                    stack.append(ARRAY)
                    output.append("[")
                elif char == ",":
                    output.append(",")
                    if stack[-2] == OBJECT:
                        state = OBJECT
                    elif stack[-1] == ARRAY:
                        state = ARRAY
                elif char == "}":
                    stack.pop()
                    state = stack[-1]
                    output.append("}")
                elif char == "]":
                    stack.pop()
                    state = stack[-1]
                    output.append("]")
                elif char.isdigit() or char in ["-", "+"]:
                    state = NUMBER
                    stack.append(NUMBER)
                    output.append(char)
                elif char.lower() == "t":
                    state = BOOL
                    stack.append(BOOL)
                    output.append("true")
                elif char.lower() == "f":
                    state = BOOL
                    stack.append(BOOL)
                    output.append("false")
            elif state == BOOL:
                if char == ",":
                    stack.pop()
                    while stack and stack[-1] in [KEY, VALUE]:
                        stack.pop()
                    state = stack[-1]
                    output.append(",")
                elif char == "}":
                    stack.pop()
                    while stack and stack[-1] in [KEY, VALUE]:
                        stack.pop()
                    state = stack[-1]
                    output.append("}")
                elif char == "]":
                    stack.pop()
                    while stack and stack[-1] in [KEY, VALUE]:
                        stack.pop()
                    state = stack[-1]
                    output.append("]")

            elif state == ARRAY:
                if char == '"':
                    state = STRING
                    stack.append(STRING)
                    output.append('"')
                elif char == "{":
                    state = OBJECT
                    stack.append(OBJECT)
                    output.append("{")
                elif char == "[":
                    state = ARRAY
                    stack.append(ARRAY)
                    output.append("[")
                elif char == ",":
                    output.append(",")
                    state = ARRAY
                elif char == "]":
                    stack.pop()
                    while stack and stack[-1] in [KEY, VALUE]:
                        stack.pop()
                    state = stack[-1]
                    output.append("]")

            elif state == STRING:
                if char == '"' and output[-1] != "\\":
                    stack.pop()

                    while stack and stack[-1] in [KEY, VALUE]:
                        stack.pop()
                    state = stack[-1]

                output[-1] += char

            elif state == NUMBER:
                if not char.isdigit() and char not in [".", "e", "E", "+", "-"]:
                    if char == ",":
                        output.append(",")

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

        while output[-1] in [",", " "]:
            output.pop()

        while stack and stack[-1] in [KEY, AFTER_KEY, VALUE]:
            stack.pop()
            if output[-1] not in ["}", "]"]:
                output.pop()

        while output[-1] in [",", " "]:
            output.pop()

        # Close any open objects or arrays
        while stack:
            context = stack.pop()
            if context == OBJECT:
                output.append("}")
            elif context == ARRAY:
                output.append("]")
            elif context == STRING:
                output[-1] += '"'

        # print(''.join(output))
        try:
            final_json = json.loads("".join(output))
            return final_json, False
        except:
            logger.error("Error loading json")
            logger.error(f"Input string: {data}")
            logger.error(f'Completed json: {"".join(output)}')
            return None, False
