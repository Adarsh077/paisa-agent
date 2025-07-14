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
                        "description": "Comma-separated tag IDs. Use 'None' to get transactions without any tags",
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


def viewer(primary_message: str, chat_history: list = [], agent_response: str = ""):
    messages = []
    messages.append(
        {
            "role": "system",
            "content": f"""
Call only the tools if user is specifically asking to view list of transactions in latest message. Do not call the tools if the question is not related to transactions or if it is calculation based.
Return 'NONE' if the question is not related to transactions or if tools cannot be used.

ALWAYS Return 'NONE' for calculation based questions or if the question is not related to transactions.
- How much did I spend on groceries?: "NONE"
- How much did I earn last month?: "NONE"
- What were my total expenses last month?: "NONE"
- What is my current account balance?: "NONE"
            """,
        },
    )
    messages.extend([{"role": m.role, "content": m.content} for m in chat_history])
    messages.append({"role": "user", "content": primary_message})
    messages.append({"role": "assistant", "content": agent_response})

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
