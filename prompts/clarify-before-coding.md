# Guide to Clarifying Before You Code
Whenever you encounter ambiguity, need a decision, or could benefit from the user's guidance before continuing, pause and **always** use the `pair-pilot` MCP server to ask for clarification or any question you might have. Always use one of the following tools:

- `request_free_form_input(question: str)` — for open-ended questions or feedback.
- `request_yes_no_input(question: str)` — for simple confirmations.
- `request_multiple_choice_input(question: str, options: list)` — when offering a defined set of paths.

After receiving a response, continue the task accordingly and **always check if the user would like to continue or end the session** using `request_yes_no_input`. Repeat this process until both you and the user agree that we're in alignment.
