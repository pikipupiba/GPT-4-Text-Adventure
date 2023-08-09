import ijson
from io import StringIO

# Given partial JSON
partial_json = '''{"Stats_Schema":{"day":"Monday","time":55,"items":[{"name":"Sketchbook and Pencils","description":"Packed with lots of blank pages and vibrant colored pen'''

# Since ijson expects a file-like object, we'll use StringIO to provide our string as a file-like stream
input_stream = StringIO(partial_json)

# Parsing the JSON content
parsed_items = []
for prefix, event, value in ijson.parse(input_stream):
    print(parsed_items)
    parsed_items.append((prefix, event, value))

print(parsed_items)