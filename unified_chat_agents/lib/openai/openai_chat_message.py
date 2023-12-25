from pydantic import BaseModel
from enum import Enum

class OpenaiChatRole(Enum):
    SYSTEM = "system"
    """
    The system role (OpenAI).
    """

    USER = "user"
    """
    The user role.
    """

    ASSISTANT = "assistant"
    """
    The assistant role.
    """


class OpenAIChatMessage(BaseModel):
    """
    A message in a Openai chat conversation.
    """

    role: str
    """
    Who sent the message.
    """

    content: str = ""
    """
    The content of the message.
    """

    def __str__(self) -> str:
        return f"{self.role} : {self.content}"
