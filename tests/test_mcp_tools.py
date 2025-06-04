"""
Unit tests for MCP tool functions.
Tests the FastMCP tool functions end-to-end with mocked CLI handlers.
"""

from unittest.mock import patch

import pytest

from src.main import (
    request_free_form_input_tool,
    request_multiple_choice_input_tool,
    request_yes_no_input_tool,
)


class TestMcpTools:
    """Test MCP tool functions with mocked CLI handlers."""

    @pytest.mark.asyncio
    @patch("src.main.console.print")
    @patch("src.main.ask_free_form")
    async def test_request_free_form_input_tool(self, mock_ask_free_form, mock_print):
        """Test free-form input tool end-to-end."""
        mock_ask_free_form.return_value = "user response"

        result = await request_free_form_input_tool("What's your name?")

        assert result == "user response"
        mock_ask_free_form.assert_called_once_with("Your answer: ")
        mock_print.assert_called_once()  # Verify rich panel was displayed

    @pytest.mark.asyncio
    @patch("src.main.console.print")
    @patch("src.main.ask_free_form")
    @patch("src.main.ask_yes_no")
    async def test_request_yes_no_input_tool_true_with_comments(
        self, mock_ask_yes_no, mock_ask_free_form, mock_print
    ):
        """Test yes/no input tool returning True with comments."""
        mock_ask_yes_no.return_value = True
        mock_ask_free_form.return_value = "User provided comments."

        result = await request_yes_no_input_tool("Continue with operation?")

        expected_result = {"answer": True, "comments": "User provided comments."}
        assert result == expected_result
        mock_ask_yes_no.assert_called_once_with("Continue with operation? (yes/no):")
        mock_ask_free_form.assert_called_once_with(
            "Additional comments (optional, press Enter to skip): "
        )
        assert mock_print.call_count == 1  # Original panel print

    @pytest.mark.asyncio
    @patch("src.main.console.print")
    @patch("src.main.ask_free_form")
    @patch("src.main.ask_yes_no")
    async def test_request_yes_no_input_tool_true_no_comments(
        self, mock_ask_yes_no, mock_ask_free_form, mock_print
    ):
        """Test yes/no input tool returning True without comments."""
        mock_ask_yes_no.return_value = True
        mock_ask_free_form.return_value = ""  # User presses Enter

        result = await request_yes_no_input_tool("Continue with operation?")

        expected_result = {"answer": True, "comments": ""}
        assert result == expected_result
        mock_ask_yes_no.assert_called_once_with("Continue with operation? (yes/no):")
        mock_ask_free_form.assert_called_once_with(
            "Additional comments (optional, press Enter to skip): "
        )
        assert mock_print.call_count == 1

    @pytest.mark.asyncio
    @patch("src.main.console.print")
    @patch("src.main.ask_free_form")
    @patch("src.main.ask_yes_no")
    async def test_request_yes_no_input_tool_false_with_comments(
        self, mock_ask_yes_no, mock_ask_free_form, mock_print
    ):
        """Test yes/no input tool returning False with comments."""
        mock_ask_yes_no.return_value = False
        mock_ask_free_form.return_value = "Important feedback."

        result = await request_yes_no_input_tool("Delete file?")

        expected_result = {"answer": False, "comments": "Important feedback."}
        assert result == expected_result
        mock_ask_yes_no.assert_called_once_with("Delete file? (yes/no):")
        mock_ask_free_form.assert_called_once_with(
            "Additional comments (optional, press Enter to skip): "
        )
        assert mock_print.call_count == 1

    @pytest.mark.asyncio
    @patch("src.main.console.print")
    @patch("src.main.ask_free_form")
    @patch("src.main.ask_yes_no")
    async def test_request_yes_no_input_tool_false_no_comments(
        self, mock_ask_yes_no, mock_ask_free_form, mock_print
    ):
        """Test yes/no input tool returning False without comments."""
        mock_ask_yes_no.return_value = False
        mock_ask_free_form.return_value = ""

        result = await request_yes_no_input_tool("Delete file?")

        expected_result = {"answer": False, "comments": ""}
        assert result == expected_result
        mock_ask_yes_no.assert_called_once_with("Delete file? (yes/no):")
        mock_ask_free_form.assert_called_once_with(
            "Additional comments (optional, press Enter to skip): "
        )
        assert mock_print.call_count == 1  # mock_print is called once for the panel

    @pytest.mark.asyncio
    @patch("src.main.console.print")
    @patch("src.main.ask_free_form")
    @patch("src.main.ask_multiple_choice")
    async def test_request_multiple_choice_input_tool_success_with_comments(
        self, mock_ask_multiple_choice, mock_ask_free_form, mock_print
    ):
        """Test multiple choice input tool with valid options and comments."""
        options = ["Option 1", "Option 2", "Option 3"]
        mock_ask_multiple_choice.return_value = ["Option 2"]
        mock_ask_free_form.return_value = "User chose Option 2."

        result = await request_multiple_choice_input_tool("Choose approach:", options)

        expected_result = {
            "selection": ["Option 2"],
            "comments": "User chose Option 2.",
        }
        assert result == expected_result
        mock_ask_multiple_choice.assert_called_once_with("Select an option:", options)
        mock_ask_free_form.assert_called_once_with(
            "Additional comments (optional, press Enter to skip): "
        )
        assert mock_print.call_count == 1

    @pytest.mark.asyncio
    @patch("src.main.console.print")
    @patch("src.main.ask_free_form")
    @patch("src.main.ask_multiple_choice")
    async def test_request_multiple_choice_input_tool_success_no_comments(
        self, mock_ask_multiple_choice, mock_ask_free_form, mock_print
    ):
        """Test multiple choice input tool with valid options and no comments."""
        options = ["Option 1", "Option 2", "Option 3"]
        mock_ask_multiple_choice.return_value = ["Option 1"]
        mock_ask_free_form.return_value = ""

        result = await request_multiple_choice_input_tool("Choose approach:", options)

        expected_result = {"selection": ["Option 1"], "comments": ""}
        assert result == expected_result
        mock_ask_multiple_choice.assert_called_once_with("Select an option:", options)
        mock_ask_free_form.assert_called_once_with(
            "Additional comments (optional, press Enter to skip): "
        )
        assert mock_print.call_count == 1

    @pytest.mark.asyncio
    @patch("src.main.console.print")
    async def test_request_multiple_choice_input_tool_no_options(self, mock_print):
        """Test multiple choice input tool with empty options list."""
        result = await request_multiple_choice_input_tool("Choose approach:", [])

        expected_result = {"selection": [], "comments": "ERROR_NO_OPTIONS"}
        assert result == expected_result
        # Should print error panel
        assert mock_print.call_count == 1
