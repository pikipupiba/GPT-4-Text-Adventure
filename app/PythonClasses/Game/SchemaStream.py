import json
from typing import Dict, List, Union
from loguru import logger

from PythonClasses.Helpers.string_helpers import *

from PythonClasses.Schemas import schema_strings

class PartialSchema:
    def __init__(self, schema_name: Dict[str, str], partial_json_string: str = None):

        logger.debug(f"Initializing PartialSchema with schema: {schema_name}")
        self.schema_name = schema_name
        self.schema_string = schema_strings[schema_name]
        self.schema = json.loads(self.schema_string)
        
        self.partial_json_string = partial_json_string

        self.data = {}
        self.current_position = 0
        self.current_key = None
        self.current_value_type = None
        self.current_value = None

        self.updated = False
        self.complete = False
    
    def key_complete(self):
        # Key is complete, add it to data
        self.data[self.current_key] = self.current_value
        self.current_key = None
        self.current_value_type = None
        self.current_value = None

        # Make sure we send the update. We have a complete key/value pair!
        self.updated = True

    def find_next_key(self):
        # Check if partial json string contains any remaining keys
        remaining_keys = set(self.schema.keys()) - set(self.data.keys())
        for key in remaining_keys:
            key_position = self.partial_json_string.find(f"\"{key}\":", self.current_position)
            if key_position != -1:
                self.current_key = key
                # move position to end of key
                self.current_position = key_position + len(key)
                # We found a key but definitely no value yet, return current data
                return None
        # No keys found, return current data
        return None
    
    def find_next_value_type(self):
        # Find next non-whitespace character
        value_position, char = next_non_whitespace(self.partial_json_string, self.current_position)
        
        if value_position is None:
            # Definitely no value
            return None
        
        self.current_position = value_position

        if char == "{":
            # Value is a dictionary. Recursion!?!?
            self.current_value_type = "dict"

        elif char == "[":
            # Value is a list
            self.current_value_type = "list"

        elif char == "\"":
            # Value is a string
            self.current_value_type = "string"

        elif char.lower() == "t":
            # Value is a true
            self.current_value_type = "boolean"
            self.current_value = True
            self.key_complete()

        elif char.lower() == "f":
            # Value is a false
            self.current_value_type = "boolean"
            self.current_value = False
            self.key_complete()
        
        elif char.isdigit() or char == "-":
            # Value is a number
            self.current_value_type = "number"

        return None
    
    def find_next_value(self):
        # Get partial value from partial json string
        self.current_value = self.partial_json_string[self.current_position:]

        if self.current_value_type == "string":
            # Is the string complete?
            next_quote_position = self.partial_json_string[self.current_position:].find("\"")
            if next_quote_position != -1:
                # String is complete, return it
                self.current_position = next_quote_position + 1
                self.key_complete()
                return None
            
        elif self.current_value_type == "number":
            # Is the number complete?
            next_non_number_position, next_non_number_char = next_non_number(self.partial_json_string, self.current_position)
            if next_non_number_position is not None:
                # Number is complete, return it
                self.current_value = int(self.partial_json_string[self.current_position:next_non_number_position])
                self.current_position = next_non_number_position
                self.key_complete()
                return None
            
        elif self.current_value_type == "boolean":
            # Should have handled this immediately
            logger.warning("Boolean value should have been handled immediately. Returning None.")
            return None
        
        elif self.current_value_type == "list":
            # Value is a list. Recursion!?!?
            pass

        elif self.current_value_type == "dict":
            # Value is a dictionary. Recursion!?!?
            pass
        
        # Stream the string value into the data
        self.data[self.current_key] = self.current_value
        self.updated = True
        
        return None

    def check(self, partial_json_string: str = None):
        logger.debug("Checking partial json string against schema")

        if partial_json_string is None:
            logger.warning("No partial json string provided. Returning None.")
            return None
        
        # Add chunk to partial json string
        self.partial_json_string += partial_json_string
        
        try:
            # Full send! See if we can get the full json
            self.full_data = json.loads(self.partial_json_string)
            logger.trace(f"{self.schema_name} complete!")
            self.complete = True
            return None
        except json.decoder.JSONDecodeError as e:
            # json string is incomplete, continue
            pass

        if self.current_key is None:
            # We aren't currently working on a key, so let's find one
            self.find_next_key()
            return None
        
        if self.current_value_type is None:
            # We don't know the value type, so let's find it
            self.find_next_value_type()
            return None

        # We know the value type, so let's get the value
        self.find_next_value()
        
        # If partial json string contains any values, return them
        return None
            



class SchemaStream:
    def __init__(self):
        self.schema_strings = schema_strings

        self.streaming_json = ""

        self.partial_schema = None

        self.schema_name = None

        self.complete = False

    
    def get_schema_string(self, schema_name):
        return self.schema_strings[schema_name]
    
    def get_schema(self, schema_name):
        return json.loads(self.schema_strings[schema_name])
    
    def check_json_string(self, streaming_json: str = None):
        logger.trace("Checking json string against schemas")

        if streaming_json is None:
            logger.warning("No streaming json provided. Returning None.")
            return None
        
        self.streaming_json = streaming_json
        
        if (not self.partial_schema) and (not self.identify_streaming_schema(self.streaming_json)):
            logger.debug("No streaming schema identified. Returning None.")
            return None
        
        # Check if json string contains any values
        self.partial_schema.check(self.streaming_json)

        if self.partial_schema.complete:
            # json is complete
            logger.debug(f"{self.partial_schema.schema_name} complete!")
            data = self.partial_schema.data
            self.streaming_json = ""
            self.partial_schema = None
            self.complete = True
            return data

        if self.partial_schema.updated:
            # json contains new data
            logger.trace(f"{self.partial_schema.schema_name} schema updated!")
            self.partial_schema.updated = False
            return self.partial_schema.data
        
        # Not done and no update to send
        return None

    
    def identify_streaming_schema(self):
        logger.debug("Identifying streaming schema")

        if self.streaming_json is None:
            logger.warning("No text provided. Returning False.")
            return False
        
        # See how many schemas match the partial json string
        schema_name_matches = [key for key,value in self.schema_strings.items() if key.startswith(self.streaming_json)]

        # If there's only one match, set self.streaming_schema to that schema
        if len(schema_name_matches) != 1:
            # No matches or multiple matches
            return False

        logger.trace(f"Successfully identified streaming schema: {schema_name_matches[0]}")
        self.schema_name = schema_name_matches[0]
        self.partial_schema = PartialSchema(self.schema_name, self.streaming_json)

        # Successfully identified streaming schema
        return True