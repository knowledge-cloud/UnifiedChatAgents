from lib.prompt.base import BasePrompt


class UserMessagePrompt(BasePrompt):
    """A class to format user messages."""

    def __init__(self):
        """Initialize the UserMessagePrompt with a specific format."""
        super().__init__(
            """
Role:
{role}
====================
Message:
{message}
""")
