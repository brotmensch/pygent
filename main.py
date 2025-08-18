import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
import argparse
from functions.get_files_info import get_files_info
from functions.get_files_info import schema_get_files_info 
load_dotenv()
api_key=os.environ.get("GEMINI_API_KEY")
client=genai.Client(api_key=api_key)
working_directory="."
system_prompt="""
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

def main():
    
    parser = argparse.ArgumentParser(description="A tool that generates AI responses with optional verbose output.")
    parser.add_argument("prompt", type=str, help="The user's prompt for the AI.")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output.")
    
    args=parser.parse_args()
    available_functions=types.Tool(
        function_declarations=[
            schema_get_files_info,
        ]

    )

    function_map = {
    "get_files_info": get_files_info,
}
    
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
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],system_instruction=system_prompt)
    )
    if  response.function_calls:
        for response_function_call_part in response.function_calls:
            print(f"Calling function: {response_function_call_part.name}({response_function_call_part.args})")

            function_name=response_function_call_part.name
            if function_name in function_map:
                function_args = response_function_call_part.args
                if function_name == "get_files_info":
                    directory = function_args.get('directory', '.')
                    result = function_map[function_name](working_directory=working_directory, directory=directory)
                    print(result)
            
    else:
        print(response.text)
        if is_verbose:
            print("User prompt: " +user_prompt)
            print("Prompt tokens: "+str(response.usage_metadata.prompt_token_count))
            print("Response tokens: "+str(response.usage_metadata.candidates_token_count))

    
    




if __name__ == "__main__":
    main()
