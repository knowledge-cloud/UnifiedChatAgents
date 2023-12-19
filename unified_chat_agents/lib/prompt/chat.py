from abc import ABC
from typing import List

from pydantic import BaseModel
from lib.prompt.base import BasePrompt
from constants.prompts.user_message import UserMessagePrompt


class Message(BaseModel):
    """A class to represent a message in a chat."""
    role: str
    """The role of the user."""

    message: str
    """The message."""


class ChatPromptTemplate(ABC):
    """A prompt template for chat models."""

    def __init__(self, messages: List[Message]):
        """Initialize the ChatPromptTemplate with a list of messages."""
        self.messages = messages

    @classmethod
    def from_messages(cls, messages):
        """Create a ChatPromptTemplate from a list of messages."""
        return cls(messages)

    def get_format_messages(self, role) -> List[Message]:
        """
        Format the messages based on the role.
        """
        formatted_messages = []
        prompt = UserMessagePrompt()
        for message in self.messages:
            formatted_role = "assistant" if message.role.lower() == role.lower() else "user"
            formatted_message = prompt.get_prompt(role=formatted_role, message=message.message)
            formatted_messages.append(Message(role=formatted_role, message=formatted_message))
        return formatted_messages