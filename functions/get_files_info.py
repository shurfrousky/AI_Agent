import os
from google import genai
from google.genai import types

# tells LLM how to use function
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

# gets info of requested file
def get_files_info(working_directory, directory="."):
    full_path = os.path.join(working_directory, directory)
    abs_working = os.path.abspath(working_directory)
    abs_full = os.path.abspath(full_path)

    # error handling
    if not abs_full.startswith(abs_working):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'

    try:    
        contents = os.listdir(full_path)
    except Exception as e:
        return f'Error: {str(e)}'

    # create string of directory info
    lines = []
    for content in contents:
        item_path = os.path.join(full_path, content)

        try:
            size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
        except Exception as e:
            return f'Error: {str(e)}'
        
        lines.append(f"- {content}: file_size={size} bytes, is_dir={is_dir}")

    result = "\n".join(lines)

    return result