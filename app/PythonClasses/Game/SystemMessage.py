import re
from typing import List
from loguru import logger

from PythonClasses.Schemas import schema_strings

class SystemMessage:
# The `SystemMessage` class is providing a method called `inject_schemas` that is used to inject
# schema strings into a given system message. It does this by searching for schema placeholders
# in the system message and replacing them with the corresponding schema string. The schema
# placeholders are identified using a specific pattern (`/*\schema_name*/\`) and are replaced
# using the `re.sub` function. If a schema string is not found for a particular schema name, the
# original placeholder is retained in the system message. The method returns the complete system
# message with the injected schemas.

    
    def inject_schemas(system_message: str):
    # The `inject_schemas` method is used to inject schema strings into a given system message. It
    # searches for schema placeholders in the system message and replaces them with the
    # corresponding schema string. The schema placeholders are identified using a specific pattern
    # (`/*\schema_name*/\`) and are replaced using the `re.sub` function. If a schema string is
    # not found for a particular schema name, the original placeholder is retained in the system
    # message. The method returns the complete system message with the injected schemas.

        logger.debug("Injecting schemas into system message")

        # Function to replace matched pattern with schema string
        num_found_schemas = 0
        def replacer(match):
            nonlocal num_found_schemas
            num_found_schemas += 1
            schema_name = match.group(1)  # Extract the schema_name from the matched pattern
            return schema_strings.get(schema_name, match.group(0))  # Return variable value or original if not found
        
        # /*\schema_name*/\  # Pattern to match schema placeholders
        schema_matcher = re.compile(r'\/\*\\(.*?)\/\*\\')  # Compile regex pattern to match schema placeholders

        # Replace schema placeholders with schema strings in system message
        complete_system_message = re.sub(schema_matcher, replacer, system_message)

        logger.info(f"Successfully injected *{num_found_schemas}* schemas")

        return complete_system_message