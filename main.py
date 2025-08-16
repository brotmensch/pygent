import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
import argparse
load_dotenv()
api_key=os.environ.get("GEMINI_API_KEY")
client=genai.Client(api_key=api_key)



def main():
    
    parser = argparse.ArgumentParser(description="A tool that generates AI responses with optional verbose output.")
    parser.add_argument("prompt", type=str, help="The user's prompt for the AI.")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output.")
    
    args=parser.parse_args()
    
    
    user_prompt=args.prompt
    is_verbose=args.verbose
    
    messages=[
        types.Content(role="user",parts=[types.Part(text=user_prompt)])
    ]


    if len(sys.argv)==1: 
        print("Mist")
        sys.exit(1)
    #response = client.models.generate_content(model="gemini-2.0-flash-001", contents=sys.argv[1])
    response=client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages
    )
   
    print(response.text)
    if is_verbose:
        print("User prompt: " +user_prompt)
        print("Prompt tokens: "+str(response.usage_metadata.prompt_token_count))
        print("Response tokens: "+str(response.usage_metadata.candidates_token_count))
    




if __name__ == "__main__":
    main()
