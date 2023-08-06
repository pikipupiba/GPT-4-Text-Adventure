from typing import Dict, List, Union
from loguru import logger

from ...Schemas import schema_strings

class PartialSchema:
    def __init__(self, schema: Dict[str, str], partial_json_string: str = None):
        self.schema = schema
        self.partial_json_string = partial_json_string

class SchemaManager:
    def __init__(self):
        self.schemas = schema_strings
    
    def get_schema(self, schema_name):
        return self.schemas[schema_name]
    
    def identify_streaming_schema(self, partial_json_string:str = None):
        logger.debug("Identifying streaming schema")

        if partial_json_string is None:
            logger.warning("No text provided. Returning None.")
            return None
        
        # See how many schemas match the partial json string
        matches = [{key:value} for key,value in self.schemas.items() if key.startswith(partial_json_string)]

        # If there's only one match, set self.streaming_schema to that schema
        if len(matches) == 1:
            logger.trace(f"Successfully identified streaming schema: {matches[0]['key']}")
            self.streaming_schema = matches[0]
            return matches[0]
        else:
            return None

