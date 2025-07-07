from openai import OpenAI
from src.executors.chat_executor import SYSTEM_PROMPT

client = OpenAI()

tools = [
    {
        "type": "function",
        "function": {
            "name": "search_transactions",
            "description": "Search for transactions based on various criteria. USE THIS TOOL ONLY IF THE USER ASKS TO VIEW/LIST TRANSACTIONS.",
            "parameters": {
                "type": "object",
                "properties": {
                    "tags": {
                        "type": "string",
                        "description": "Comma-separated tag IDs.",
                    },
                    "label": {"type": "string", "description": "Search by label."},
                    "startDate": {
                        "type": "string",
                        "description": "Start date (ISO format).",
                    },
                    "endDate": {
                        "type": "string",
                        "description": "End date (ISO format).",
                    },
                    "type": {
                        "type": "string",
                        "description": "Type of transaction to search (income or expense).",
                    },
                },
                "additionalProperties": False,
            },
            # "strict": True,  # Removed strict to allow optional parameters
        },
    },
]


def viewer(messages):
    messages = [{"role": m.role, "content": m.content} for m in messages]
    messages.insert(
        0,
        {
            "role": "system",
            "content": f"""
Call only the tools if they make sense. Do not call the tools if the question is not related to transactions or if tools cannot be used.
Return 'NONE' if the question is not related to transactions or if tools cannot be used.
            """,
        },
    )

    completion = client.chat.completions.create(
        model="gpt-4.1", messages=messages, tools=tools, parallel_tool_calls=False
    )

    if (
        completion.choices[0].message.tool_calls
        and len(completion.choices[0].message.tool_calls) > 0
    ):
        tool_call = completion.choices[0].message.tool_calls[0]
        return {
            "name": tool_call.function.name,
            "arguments": tool_call.function.arguments,
        }

    return "NONE"
