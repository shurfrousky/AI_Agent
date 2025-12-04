from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.run_python_file import run_python_file
from functions.write_file import write_file
from google.genai import types

# lets LLM call on a function
def call_function(function_call_part, verbose=False):
    function_map = {                      # for accessing functions for LLM
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }
    function_name = function_call_part.name
    args = dict(function_call_part.args)
    args["working_directory"] = "./calculator"
    chosen_function = function_map.get(function_name)

    # error handling for no function name
    if not chosen_function:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_name,
                        response={"error": f"Unknown function: {function_name}"},
                    )
                ],
            )

    if verbose:
        print(f"Calling function: {function_name}({args})")  
    else:
        print(f" - Calling function: {function_name}")

    result = chosen_function(**args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": result},
            )
        ],
    )