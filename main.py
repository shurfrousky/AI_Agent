import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def generate_response(client, messages, verbose, user_prompt):
    # ai output message
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages,
    )
    
    # token count
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

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