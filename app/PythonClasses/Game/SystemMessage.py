import re
# from typing import List
from loguru import logger

from PythonClasses.Schemas import schema_strings

class SystemMessage:
    """The `SystemMessage` class has a static method called `inject_schemas` which takes a system
message as input. It injects schema strings into the system message by replacing matched
patterns with the corresponding schema string. The method uses regular expressions to find
patterns in the system message and then replaces them with the schema string from the
`schema_strings` dictionary. The method also keeps track of the number of schemas found and
logs the number of schemas injected. Finally, it returns the complete system message with the
injected schemas."""

    @staticmethod
    def inject_schemas(system_message: str):
        """
        The function inject_schemas takes a system_message string as input, searches for patterns
        matching /*\\schema_name/*\\ in the string, replaces them with the corresponding schema 
        string from the schema_strings dictionary, and returns the modified system_message string.
        
        :param system_message: The `system_message` parameter is a string that represents a system
        message. This function is designed to inject schema strings into the system message by 
        replacing matched patterns with the corresponding schema string
        :type system_message: str
        :return: the complete system message after injecting the schemas.
        """
        logger.debug("Injecting schemas into system message")
        # Function to replace matched pattern with schema string
        num_found_schemas = 0
        def replacer(match):
            nonlocal num_found_schemas
            num_found_schemas += 1
            schema_name = match.group(1)
            return schema_strings.get(schema_name, match.group(0))
        schema_matcher = re.compile(r'\/\*\\(.*?)\/\*\\')
        complete_system_message = re.sub(schema_matcher, replacer, system_message)
        logger.info(f"Successfully injected *{num_found_schemas}* schemas")
        return complete_system_message
