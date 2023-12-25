from lib.prompt.base import BasePrompt


class ResSAPrompt(BasePrompt):
    """ResSA Prompt."""

    def __init__(self):
        """Initialize the Response Synthesizer Agent Prompt with a specific format."""
        super().__init__("""
Based on all the messages and the rules respond to user.

Rules:
1. Currency: All the currency should be in INR.
                         """)
