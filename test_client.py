import asyncio

import os

from mcp import ClientSession
from mcp.client.sse import sse_client

SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8100/sse")


async def test_free_form_input(session: ClientSession):
    print("\n--- Testing: request_free_form_input ---")
    question = "What is your favorite programming language?"
    print(f"Client: Asking free-form question: '{question}'")
    try:
        response = await session.call_tool(
            "request_free_form_input", {"question": question}
        )
        print(f"Server Response: {response.content}")
    except Exception as e:
        print(f"Error calling request_free_form_input: {e}")


async def test_yes_no_input(session: ClientSession):
    print("\n--- Testing: request_yes_no_input ---")
    question = "Do you enjoy using MCP?"
    print(f"Client: Asking yes/no question: '{question}'")
    try:
        response = await session.call_tool(
            "request_yes_no_input", {"question": question}
        )
        # The response content will be a string "true" or "false" from the MCP server
        # if the tool returns a boolean that gets JSON serialized.
        # Or it might be an actual boolean if the transport/SDK handles it.
        # Let's assume it's serialized as a string by default from FastMCP or needs parsing.
        # Based on current PairPilot server, it returns a direct bool which should be fine.
        print(f"Server Response: {response.content}")
    except Exception as e:
        print(f"Error calling request_yes_no_input: {e}")


async def test_multiple_choice_input(session: ClientSession):
    print("\n--- Testing: request_multiple_choice_input ---")
    question = "Which topic do you want to discuss?"
    options = ["Technology", "Science", "Art"]
    print(
        f"Client: Asking multiple-choice question: '{question}' with options: {options}"
    )
    try:
        response = await session.call_tool(
            "request_multiple_choice_input", {"question": question, "options": options}
        )
        print(f"Server Response: {response.content}")
    except Exception as e:
        print(f"Error calling request_multiple_choice_input: {e}")


async def main():
    print(f"Attempting to connect to MCP server at {SERVER_URL}...")
    try:
        streams = sse_client(SERVER_URL)
        async with streams as stream_context:
            session = ClientSession(*stream_context)
            async with session as session_context:
                await session_context.initialize()
                print("Session initialized. Available tools from server:")
                tools_response = await session.list_tools()
                if tools_response and tools_response.tools:
                    print([tool.name for tool in tools_response.tools])
                else:
                    print("No tools reported by the server or error in listing tools.")
                    return

                await test_free_form_input(session)
                await test_yes_no_input(session)
                await test_multiple_choice_input(session)

    except ConnectionRefusedError:
        print(f"Connection refused. Ensure the MCP server is running at {SERVER_URL}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        print("\n--- Test client finished ---")


if __name__ == "__main__":
    asyncio.run(main())
