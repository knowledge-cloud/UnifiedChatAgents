from abc import ABC
from typing import List

from constants.prompts.user_message import UserMessagePrompt

from lib.chat import ChatMessage, ChatRole
from lib.openai import OpenAIChatMessage, OpenaiChatRole


class ChatPromptTemplate(ABC):
    """A prompt template for chat models."""

    def __init__(self, messages: List[ChatMessage]):
        """Initialize the ChatPromptTemplate with a list of messages."""
        if not isinstance(messages, list) or not all(isinstance(message, ChatMessage) for message in messages):
            raise ValueError("ChatPromptTemplate expects a list of ChatMessage.")
        self.messages = messages

    def get_format_messages(self, role: ChatRole) -> List[OpenAIChatMessage]:
        """
        Format the messages based on the role.
        """
        formatted_messages = []
        prompt = UserMessagePrompt()
        for message in self.messages:
            formatted_role = OpenaiChatRole.ASSISTANT if message.from_ == role else OpenaiChatRole.USER
            formatted_message = prompt.get_prompt(
                role=message.from_.value, content=message.content)

            formatted_messages.append(
                OpenAIChatMessage(**{"role": formatted_role.value, "content": formatted_message}))
        return formatted_messages
