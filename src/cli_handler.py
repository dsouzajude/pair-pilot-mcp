"""
CLI Handler Module

This module contains asynchronous functions responsible for interacting with the user
via the CLI using the questionary library for a polished experience.
"""

from typing import List

import questionary


async def ask_free_form(prompt_message: str) -> str:
    """
    Asks the user a free-form question and returns their textual response.

    Args:
        prompt_message: The question/prompt to display to the user

    Returns:
        The user's text response, or empty string if cancelled
    """
    response = await questionary.text(prompt_message).ask_async()

    # If response is None (user cancelled, e.g., Ctrl+C), return empty string
    if response is None:
        return ""

    return response


async def ask_yes_no(prompt_message: str) -> bool:
    """
    Asks the user a yes/no question and returns a boolean.

    Args:
        prompt_message: The yes/no question to display to the user

    Returns:
        True for yes, False for no or if cancelled
    """
    confirmation = await questionary.confirm(prompt_message, default=True).ask_async()

    # If confirmation is None (user cancelled), return False as default
    if confirmation is None:
        return False

    return confirmation


async def ask_multiple_choice(prompt_message: str, options: List[str]) -> List[str]:
    """
    Presents the user with multiple choices and returns the selected options as a list of strings.

    Args:
        prompt_message: The question to display to the user
        options: List of choice options to present

    Returns:
        The selected choices as a list of strings, or empty list if cancelled or no options
    """
    # Handle empty options list
    if not options:
        return "ERROR_NO_OPTIONS"

    choice = await questionary.checkbox(prompt_message, choices=options).ask_async()

    # If choice is None (user cancelled), return empty string
    if choice is None:
        return []

    return choice
