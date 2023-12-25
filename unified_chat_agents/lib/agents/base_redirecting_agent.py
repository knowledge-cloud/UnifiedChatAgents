from abc import abstractmethod
from typing import List
from lib.agents import BaseAgent
from lib.prompt import BasePrompt
from lib.openai import OpenAIModel
from lib.chat import ChatRole, ChatMessage


class BaseRedirectingAgent(BaseAgent):
    """A class to represent a base redirecting agent."""

    role: ChatRole

    def __init__(
        self,
        prompt: BasePrompt,
        model: OpenAIModel = OpenAIModel.GPT_3_5
    ) -> None:
        """Initialize the BaseRedirectingAgent with a prompt and a model."""
        super().__init__(prompt=prompt, model=model)

    @abstractmethod
    def predict(self, messages: List[ChatMessage], **kwargs) -> ChatMessage:
        """
        Redirect or respond to the messages.
        """
        pass
