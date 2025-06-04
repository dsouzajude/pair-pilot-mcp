"""
Interactive MCP Server

Core MCP server setup, tool definitions, and rich output for enhanced user experience.
This server allows AI agents to interact with a human user via CLI for feedback.
"""

import os
from typing import List, TypedDict

from mcp.server.fastmcp import FastMCP
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from .cli_handler import ask_free_form, ask_multiple_choice, ask_yes_no


class YesNoAnswerReturnType(TypedDict):
    answer: bool
    comments: str


class MultipleChoiceAnswerReturnType(TypedDict):
    selection: List[str]
    comments: str


# Initialize Rich Console for enhanced output
console = Console()

# Initialize FastMCP Server
mcp = FastMCP(
    name="interactive_cli_server",
    version="0.1.0",
    description="MCP server for interactive CLI-based user feedback with an enhanced UI.",
)


@mcp.tool(
    name="request_free_form_input",
    description="Asks the user a free-form question and returns their textual response.",
)
async def request_free_form_input_tool(question: str) -> str:
    """
    Tool for requesting free-form text input from the user.

    Args:
        question: The question to ask the user

    Returns:
        The user's text response
    """
    console.print(
        Panel(
            Text(question, style="italic white"),
            title="[bold blue]🤖 Agent Asks (Free-form)[/bold blue]",
            border_style="green",
            expand=False,
        )
    )
    return await ask_free_form("Your answer: ")


@mcp.tool(
    name="request_yes_no_input",
    description="Asks the user a yes/no question and returns their answer along with any optional comments. The response is a dictionary: {'answer': bool, 'comments': str}.",
)
async def request_yes_no_input_tool(question: str) -> YesNoAnswerReturnType:
    """
    Tool for requesting yes/no confirmation from the user, with optional comments.

    Args:
        question: The yes/no question to ask the user

    Returns:
        A dictionary containing the boolean answer and any textual comments.
        Example: {"answer": True, "comments": "This looks good."}
    """
    console.print(
        Panel(
            Text(question, style="italic white"),
            title="[bold blue]🤖 Agent Asks (Yes/No)[/bold blue]",
            border_style="yellow",
            expand=False,
        )
    )
    answer = await ask_yes_no(f"{question} (yes/no):")
    comments = await ask_free_form(
        "Additional comments (optional, press Enter to skip): "
    )
    return {"answer": answer, "comments": comments or ""}


@mcp.tool(
    name="request_multiple_choice_input",
    description="Presents the user with a list of options, returns their selected choices and any optional comments. The response is a dictionary: {'selection': List[str], 'comments': str}.",
)
async def request_multiple_choice_input_tool(
    question: str, options: List[str]
) -> MultipleChoiceAnswerReturnType:
    """
    Tool for requesting multiple choice selection from the user, with optional comments.

    Args:
        question: The question to ask the user
        options: List of choices to present

    Returns:
        A dictionary containing the selected choices (list of strings) and any textual comments.
        Example: {"selection": ["Option A"], "comments": "Option A is preferred because..."}
        Returns {"selection": [], "comments": "ERROR_NO_OPTIONS"} if no options are provided.
    """
    if not options:
        error_message = (
            "Error: No options provided by the agent for the multiple-choice question."
        )
        console.print(
            Panel(
                error_message,
                title="[bold red]Server Error[/bold red]",
                border_style="red",
            )
        )
        return {"selection": [], "comments": "ERROR_NO_OPTIONS"}

    console.print(
        Panel(
            Text(question, style="italic white"),
            title="[bold blue]🤖 Agent Asks (Multiple Choice)[/bold blue]",
            border_style="magenta",
            expand=False,
        )
    )
    selection = await ask_multiple_choice("Select an option:", options)
    comments = await ask_free_form(
        "Additional comments (optional, press Enter to skip): "
    )
    return {"selection": selection, "comments": comments or ""}


if __name__ == "__main__":

    host = os.environ.get(
        "HOST", "0.0.0.0"
    )  # Listen on all interfaces, crucial for Docker
    port = int(os.environ.get("PORT", 8100))  # Default port, can be configured

    console.print(
        f"🚀 Starting Interactive MCP Server ([bold cyan]{mcp.name}[/bold cyan])...",
        style="green",
    )
    console.print(
        f"   Listening on [link=http://{host}:{port}/sse]http://{host}:{port}/sse[/link]"
    )
    console.print(
        "   [italic]Waiting for agent connections. Press Ctrl+C to stop.[/italic]"
    )

    mcp.settings.host = host
    mcp.settings.port = port
    mcp.run(transport="sse")
