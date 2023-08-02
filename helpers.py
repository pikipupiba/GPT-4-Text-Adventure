import json,random

def generate_dice_string(num_dice:int):
    dice_string = "intRollArray:["

    for i in range(num_dice):
        dice_string += str(random.randint(1,20))
        if i != num_dice-1:
            dice_string += ","
        else:
            dice_string += "]"

    return dice_string

def extract_json_objects(text, decoder=json.JSONDecoder()):
    """Find JSON objects in text, and yield the decoded JSON data

    Does not attempt to look for JSON arrays, text, or other JSON types outside
    of a parent JSON object.

    """
    pos = 0
    while True:
        match = text.find('{', pos)
        if match == -1:
            break
        try:
            result, index = decoder.raw_decode(text[match:])
            yield result
            pos = match + index
        except ValueError:
            pos = match + 1