import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info

# list of available functions for LLM to use
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)

# ai output message
def generate_response(client, messages, verbose, user_prompt):
    model_name = 'gemini-2.0-flash-001'
    system_prompt = """
        You are a helpful AI coding agent.

        When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

        - List files and directories

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
            print(f"Calling function: {fc.name}({fc.args})")
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