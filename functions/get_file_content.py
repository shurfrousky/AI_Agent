import os
from .config import MAX_CHARS

def get_file_content(working_directory, file_path):
    full_path = os.path.join(working_directory, file_path)
    abs_full = os.path.abspath(full_path)
    abs_working = os.path.abspath(working_directory)
    is_file = os.path.isfile(abs_full)

    if not abs_full.startswith(abs_working):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not is_file:
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(abs_full, "r") as f:
            file_content = f.read()
            if len(file_content) > MAX_CHARS:
                too_long_msg = f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                return file_content[0:MAX_CHARS] + too_long_msg
            return file_content
        
    except Exception as e:
        return f'Error: File "{file_path}" can not be opened or read. {e}'
