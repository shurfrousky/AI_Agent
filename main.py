import os
import sys
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def main():
    print("\nHello from ai-agent!\n")

    if len(sys.argv) == 1:
        print("No prompts were provided.\nClosing app...")
        sys.exit(1)

    response = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=sys.argv
        )
    
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count

    print(response.text)
    print(f"Prompt tokens: {prompt_tokens}\nResponse tokens: {response_tokens}")

if __name__ == "__main__":
    main()
