class SchemaStream:
    def __init__(self):
        schema_delimiter = r'\.\.[A-Z]+\.\.'
        self.full_string = ""
        self.schema_name = ""
        self.item_index = None
        self.items_array = None
        self.relationships_array = []
        self.temp_string = ""


    def check(self, content: str):
        self.full_string += content

opening_match = re.search(schema_delimiter, Game._last_display(game_name)[1])
if opening_match:
    in_stream = True
    schema_name = opening_match.group(0)[2:-2]
    Game._last_display(game_name)[1] = Game._last_display(game_name)[1][:opening_match.start()]
    content = content.rstrip('.')

if schema_name not in Game._last_turn(game_name).stats:
    Game._last_turn(game_name).stats[schema_name] = ""

if schema_name == "DAY":
    Game._last_turn(game_name).stats["DAY"] += content
if schema_name == "ITEM":
    if item_index is None:
        if items_array is None:
            items_array = Game._last_turn(game_name).stats["ITEM"].split('\n')
            # Remove empty strings, if any, resulting from split
            items_array = [item for item in items_array if item]

        temp_string += content
        # See if exactly 1 item in items_array matches the content.
        # Check if the start of any item in the array matches the content
        matching_indices = [index for index, item in enumerate(items_array) if item.startswith(temp_string)]
        if len(matching_indices) == 0:
            # If no match, append the content to the end of the array
            item_index = len(items_array)
            items_array.append(temp_string)
        elif len(matching_indices) == 1 and len(temp_string) > 4:
            # If a match is found, replace the item at the first matching index
            item_index = matching_indices[0]
            items_array[item_index] = temp_string

    else:
        # If we already found the item index, just append the content to the item
        items_array[item_index] += content
        # Update the stats with the modified items_array
        Game._last_turn(game_name).stats["ITEM"] = '\n'.join(items_array)


elif schema_name == "RELATIONSHIP":
    if item_index is None:
        if items_array is None:
            items_array = Game._last_turn(game_name).stats["RELATIONSHIP"].split('\n')
            # Remove empty strings, if any, resulting from split
            items_array = [item for item in items_array if item]

        temp_string += content
        # See if exactly 1 item in items_array matches the content.
        # Check if the start of any item in the array matches the content
        matching_indices = [index for index, item in enumerate(items_array) if item.startswith(temp_string)]
        if len(matching_indices) == 0:
            # If no match, append the content to the end of the array
            item_index = len(items_array)
            items_array.append(temp_string)
        elif len(matching_indices) == 1 and len(temp_string) > 4:
            # If a match is found, replace the item at the first matching index
            item_index = matching_indices[0]
            items_array[item_index] = temp_string

# Look for closing tag in the accumulated data for the schema
closing_match = re.search(schema_delimiter, Game._last_turn(game_name).stats[schema_name])
if closing_match:
    items_array = None
    item_index = None
    temp_string = ""
    Game._last_turn(game_name).stats[schema_name] = Game._last_turn(game_name).stats[schema_name][:closing_match.start()]
    if Game._last_turn(game_name).stats[schema_name][-1] != "\n":
        Game._last_turn(game_name).stats[schema_name] += "\n"
    in_stream = False
    schema_name = ""