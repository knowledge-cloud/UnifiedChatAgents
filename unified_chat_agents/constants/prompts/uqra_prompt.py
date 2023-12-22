from lib.prompt.base import BasePrompt


class UQRAPrompt(BasePrompt):
    """UQRA Prompt."""

    def __init__(self):
        """Initialize the User Query Redirecting Agent Prompt with a specific format."""
        super().__init__("""
                         Your are Intelligent Assistant. Try to help the user with their query
                         """)
        # raise NotImplementedError
