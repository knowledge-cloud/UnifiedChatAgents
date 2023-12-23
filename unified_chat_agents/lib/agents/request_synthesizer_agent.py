from typing import List
from lib.prompt import BasePrompt
from lib.agents import BaseRedirectingAgent
from lib.chat import ChatRole, ChatMessage
from constants.prompts import ReqSAPrompt


class RequestSynthesizerAgent(BaseRedirectingAgent):
    """
    The agent can respond or redirect to another agent.
    """

    role: ChatRole = ChatRole.ReqSA

    prompt: BasePrompt = ReqSAPrompt()

    def __init__(self) -> None:
        """Initialize the RequestSynthesizerAgent with a prompt and a model."""
        super().__init__(prompt=self.prompt)

    def predict(
        self,
        messages: List[ChatMessage]
    ) -> ChatMessage:
        """Get the redirecting agent."""
        response = self.chat_completions(messages, {"type": "json_object"})

        # Implement Custom Logic here

        return ChatMessage(**{"from_": self.role, "to": ChatRole.USER, "content": response})
