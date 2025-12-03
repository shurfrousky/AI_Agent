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

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads and returns the contents of a text file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory.",
            ),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file with optional command-line-style arguments, constrained to the working directory." ,
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="Optional space-separated arguments to pass to the Python script.",
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites the contents of a text file, constrained to the working directory." ,
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text content to write into the file.",
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