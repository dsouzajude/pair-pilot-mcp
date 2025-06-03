"""
Unit tests for CLI handler functions.
Tests the questionary-based user interaction logic with mocked inputs.
"""

import pytest
from unittest.mock import AsyncMock, patch

from src.cli_handler import ask_free_form, ask_yes_no, ask_multiple_choice


class TestCliHandler:
    """Test CLI handler functions with mocked questionary."""

    @pytest.mark.asyncio
    @patch('src.cli_handler.questionary.text')
    async def test_ask_free_form_success(self, mock_text):
        """Test successful free-form text input."""
        mock_text.return_value.ask_async = AsyncMock(return_value="test response")
        
        result = await ask_free_form("Test question:")
        
        assert result == "test response"
        mock_text.assert_called_once_with("Test question:")

    @pytest.mark.asyncio
    @patch('src.cli_handler.questionary.text')
    async def test_ask_free_form_cancelled(self, mock_text):
        """Test free-form input when user cancels (Ctrl+C)."""
        mock_text.return_value.ask_async = AsyncMock(return_value=None)
        
        result = await ask_free_form("Test question:")
        
        assert result == ""

    @pytest.mark.asyncio
    @patch('src.cli_handler.questionary.confirm')
    async def test_ask_yes_no_true(self, mock_confirm):
        """Test yes/no confirmation returning True."""
        mock_confirm.return_value.ask_async = AsyncMock(return_value=True)
        
        result = await ask_yes_no("Proceed?")
        
        assert result is True
        mock_confirm.assert_called_once_with("Proceed?", default=True)

    @pytest.mark.asyncio
    @patch('src.cli_handler.questionary.confirm')
    async def test_ask_yes_no_false(self, mock_confirm):
        """Test yes/no confirmation returning False."""
        mock_confirm.return_value.ask_async = AsyncMock(return_value=False)
        
        result = await ask_yes_no("Proceed?")
        
        assert result is False

    @pytest.mark.asyncio
    @patch('src.cli_handler.questionary.confirm')
    async def test_ask_yes_no_cancelled(self, mock_confirm):
        """Test yes/no confirmation when user cancels."""
        mock_confirm.return_value.ask_async = AsyncMock(return_value=None)
        
        result = await ask_yes_no("Proceed?")
        
        assert result is False

    @pytest.mark.asyncio
    @patch('src.cli_handler.questionary.checkbox')
    async def test_ask_multiple_choice_success(self, mock_select):
        """Test successful multiple choice selection."""
        options = ["Option A", "Option B", "Option C"]
        mock_select.return_value.ask_async = AsyncMock(return_value=["Option B"])
        
        result = await ask_multiple_choice("Choose:", options)
        
        assert result == ["Option B"]
        mock_select.assert_called_once_with("Choose:", choices=options)

    @pytest.mark.asyncio
    @patch('src.cli_handler.questionary.checkbox')
    async def test_ask_multiple_choice_cancelled(self, mock_select):
        """Test multiple choice when user cancels."""
        options = ["Option A", "Option B"]
        mock_select.return_value.ask_async = AsyncMock(return_value=[])
        
        result = await ask_multiple_choice("Choose:", options)
        
        assert result == []

    @pytest.mark.asyncio
    async def test_ask_multiple_choice_no_options(self):
        """Test multiple choice with empty options list."""
        result = await ask_multiple_choice("Choose:", [])
        
        assert result == "ERROR_NO_OPTIONS" 