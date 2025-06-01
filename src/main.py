"""
Interactive MCP Server

Core MCP server setup, tool definitions, and rich output for enhanced user experience.
This server allows AI agents to interact with a human user via CLI for feedback.
"""

import os
from typing import List

from mcp.server.fastmcp import FastMCP
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from .cli_handler import ask_free_form, ask_multiple_choice, ask_yes_no

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
    description="Asks the user a yes/no question and returns True for yes, False for no.",
)
async def request_yes_no_input_tool(question: str) -> bool:
    """
    Tool for requesting yes/no confirmation from the user.

    Args:
        question: The yes/no question to ask the user

    Returns:
        True for yes, False for no
    """
    console.print(
        Panel(
            Text(question, style="italic white"),
            title="[bold blue]🤖 Agent Asks (Yes/No)[/bold blue]",
            border_style="yellow",
            expand=False,
        )
    )
    # questionary.confirm already includes the (y/N) prompt
    return await ask_yes_no(f"{question} (yes/no):")


@mcp.tool(
    name="request_multiple_choice_input",
    description="Presents the user with a list of options and returns their selected choice as a string.",
)
async def request_multiple_choice_input_tool(question: str, options: List[str]) -> str:
    """
    Tool for requesting multiple choice selection from the user.

    Args:
        question: The question to ask the user
        options: List of choices to present

    Returns:
        The selected choice as a string
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
        # Return a specific error string or raise an MCP-compatible error
        return "ERROR_NO_OPTIONS"

    console.print(
        Panel(
            Text(question, style="italic white"),
            title="[bold blue]🤖 Agent Asks (Multiple Choice)[/bold blue]",
            border_style="magenta",
            expand=False,
        )
    )
    return await ask_multiple_choice("Select an option:", options)


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
