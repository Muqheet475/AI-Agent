import os
import sys
from dotenv import load_dotenv
from functions.call_function import available_functions, call_function
from openai import OpenAI
import argparse
from prompts import system_prompt
import json
def main():

    #API Key
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key==None:
        raise Exception("No API_Key Found")

    #Prompt
    parser = argparse.ArgumentParser(description="Chatbot_Prompt")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    #Command-Line Arguments
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()


    #Model API Call
    client= OpenAI(base_url="https://openrouter.ai/api/v1",api_key=api_key,)
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]
    for _ in range(20):
        if _ == 19:
            print("Error: Exceded context limit")
            sys.exit(1)


        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            temperature=0,
            tools=available_functions,
        )

        message=response.choices[0].message
        messages.append(message)

        #Model Response
        if message.tool_calls == None:
             print(message.content)
             break

        #Tool Call
        for tool_call in message.tool_calls:
            if tool_call.type != "function":
                        continue
            result_message=call_function(tool_call,args.verbose)
            if not result_message['content']:
                raise Exception("Error: No resposne")
            if args.verbose:
                print(f"-> {result_message['content']}")

            messages.append(result_message)



        #Token Usage
        if args.verbose:
            if response.usage != None:
                print("\nUser prompt:",args.user_prompt)
                print("Prompt tokens:",response.usage.prompt_tokens)
                print("Response tokens:",response.usage.completion_tokens)
            else:
                raise RuntimeError("Failed to intilize connection with model")



if __name__ == "__main__":
    main()
