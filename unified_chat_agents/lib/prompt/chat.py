from abc import ABC
from typing import List

from constants.prompts.user_message import UserMessagePrompt

from lib.chat import ChatMessage, ChatRole


class ChatPromptTemplate(ABC):
    """A prompt template for chat models."""

    def __init__(self, messages: List[ChatMessage]):
        """Initialize the ChatPromptTemplate with a list of messages."""
        self.messages = messages

    def get_format_messages(self, role: ChatRole) -> List[ChatMessage]:
        """
        Format the messages based on the role.
        """
        formatted_messages = []
        prompt = UserMessagePrompt()
        for message in self.messages:
            formatted_role = "assistant" if message.from_ == role else "user"
            formatted_message = prompt.get_prompt(
                role=formatted_role, content=message.content)

            formatted_messages.append(
                {"role": formatted_role, "content": formatted_message})
        return formatted_messages
