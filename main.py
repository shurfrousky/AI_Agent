import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file
from call_function import call_function

# list of available functions for LLM to use
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
         schema_run_python_file,
         schema_write_file
     ]
)

# ai output message
def generate_response(client, messages, verbose, user_prompt):
    tool_responses = []
    model_name = 'gemini-2.0-flash-001'
    system_prompt = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

        - List files and directories
        - Read file contents
        - Execute Python files with optional arguments
        - Write or overwrite files

        All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
        """
    response = client.models.generate_content(
        model=model_name, contents=messages, 
        config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt),
    )
    
    # token count
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    if response.function_calls:
        for fc in response.function_calls:
            function_call_result = call_function(fc, verbose=verbose)
            parts = function_call_result.parts

            if not parts or not getattr(parts[0], "function_response", None):
                raise RuntimeError("Function call result missing function_response")
            
            func_response = parts[0].function_response.response
            if func_response is None:
                raise RuntimeError("Function call result missing report data")
            
            tool_responses.append(parts[0])
            if verbose:
                print(f"-> {func_response}")
                
        if verbose:
            print(response.text)
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")
    else:
        if verbose:
            print(response.text)
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")
        else:
            print(response.text)

def main():
    # getting API key
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")
    
    client = genai.Client(api_key=api_key)
    args = sys.argv[1:]
    verbose = False

    print("\nHello from ai-agent!\n")

    # checking error's
    if not args:
        print("No prompts were provided.")
        print("Try typing your prompt after the file name.")
        print('Example: main.py "Your message here". \n ')
        sys.exit(1)

    # checking for --verbose command
    if "--verbose" in args:
        verbose = True
        args.remove("--verbose")

    # grabbing input
    user_prompt = " ".join(args)
    messages = [
                types.Content(role="user", parts=[types.Part(text=user_prompt)]),
            ]
    
    generate_response(client, messages, verbose, user_prompt)


if __name__ == "__main__":
    main()