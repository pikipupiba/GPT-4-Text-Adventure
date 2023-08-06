import os

from loguru import logger

def load_file(file_path: str = None, log: str = None) -> str:
    """
    Load a file from a file path.

    Parameters:
    - file_path (str): The path to the file.

    Returns:
    - str: The contents of the file.
    """

    if file_path is None:
        logger.error(f"LOAD FILE: {log} | None | No file_path provided. Unable to load file.")
        return {"error": f"LOAD FILE: {log} | None | No file_path provided. Unable to load file."}
    
    log_string = f"LOAD FILE: {log} | {file_path}"
    logger.trace(log_string)

    try:
        with open(file_path, "r") as f:
            file = f.read()
        logger.trace(f"{log_string} | Successfully loaded file")
        return file
    except FileNotFoundError:
        logger.error(f"{log_string} | File not found")
        return {"error": f"{log_string} | File not found"}
    except IOError as e:
        logger.error(f"{log_string} | IOError: {e}")
        return {"error": f"{log_string} | IOError: {e}"}

def save_file(file_path: str = None, file_contents: str = None, log: str = None):
    """
    Save a file to a file path.

    Parameters:
    - file_path (str): The path to the file.
    - file_contents (str): The contents of the file.

    Returns:
    - dict: An error message if the file could not be saved, otherwise None.
    """
    if file_path is None:
        logger.error(f"SAVE FILE: {log} | None | No file_path provided. Unable to load file.")
        return {"error": f"SAVE FILE: {log} | None | No file_path provided. Unable to load file."}
    
    log_string = f"SAVE FILE: {log} | {file_path}"
    logger.trace(log_string)

    if file_contents is None:
        logger.warning(f"{log_string} | Saving empty file")
        file_contents = ""

    try:
        with open(file_path, "w") as f:
            f.write(file_contents)
        logger.trace(f"{log} | {file_path} | Successfully saved file")
        return None
    except IOError as e:
        logger.error(f"{log} | {file_path} | IOError: {e}")
        return {"error": f"{log} | IOError: {e}"}
    
def delete_file(file_path: str = None, log: str = None):
    """
    Delete a file from a file path.

    Parameters:
    - file_path (str): The path to the file.

    Returns:
    - dict: An error message if the file could not be deleted, otherwise None.
    """
    if file_path is None:
        logger.error(f"DELETE FILE: {log} | None | No file_path provided. Unable to delete file.")
        return {"error": f"DELETE FILE: {log} | None | No file_path provided. Unable to delete file."}
    
    log_string = f"DELETE FILE: {log} | {file_path}"
    logger.trace(log_string)

    try:
        os.remove(file_path)
        logger.trace(f"{log_string} | Successfully deleted file")
        return None
    except FileNotFoundError:
        logger.error(f"{log_string} | File not found")
        return {"error": f"{log_string} | File not found"}
    except IOError as e:
        logger.error(f"{log_string} | IOError: {e}")
        return {"error": f"{log_string} | IOError: {e}"}