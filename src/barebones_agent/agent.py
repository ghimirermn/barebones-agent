import os
import json
from dotenv import load_dotenv
from groq import Groq
from barebones_agent.prompt import SYSTEM_PROMPT
from barebones_agent.tools import execute_tool

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "read the contents of a file at the given path.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path to read"}
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_directory",
            "description": "list files and subdirectories at the given path.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Directory path to list"}
                },
                "required": ["path"],
            },
        },
    },
]

def agent_loop():
    print("barebones agent (type 'quit' to exit)")
    print("-" * 40)
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    while True:
        user_input = input("\n You: ").strip()
        if user_input.lower() in ("quit", "exit"):
            break
        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})

        while True:    
            response = client.chat.completions.create(
                model=MODEL, messages=messages, tools=TOOLS, tool_choice="auto"
            )
            msg = response.choices[0].message
            messages.append(msg)

            if not msg.tool_calls:
                print(f"\nAgent: {msg.content}")
                break
            if msg.content:
                print(f"\n  (thought) {msg.content}")
            
            for tc in msg.tool_calls:
                name = tc.function.name
                args = json.loads(tc.function.arguments)
                print(f"  (action) {name}({args})")
                result = execute_tool(name, args)
                print(f"  (observation) {result[:200]}{'...' if len(result) > 200 else ''}")
                messages.append(
                    {"role": "tool", "tool_call_id": tc.id, "content": result}
                )

if __name__ == "__main__":
    agent_loop()
