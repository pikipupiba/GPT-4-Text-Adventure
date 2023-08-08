import re
from typing import List
from loguru import logger

from PythonClasses.Schemas import schema_strings

class SystemMessage:
    
    def inject_schemas():

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
        complete_system_message = re.sub(schema_matcher, replacer, self.system_message)

        logger.info(f"Successfully injected *{num_found_schemas}* schemas")

        return complete_system_message