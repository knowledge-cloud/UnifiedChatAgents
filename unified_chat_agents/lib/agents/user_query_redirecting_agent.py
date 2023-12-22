from typing import List
from lib.prompt import BasePrompt
from lib.agents import BaseRedirectingAgent
from constants.prompts import UQRAPrompt
from lib.chat import ChatRole, ChatMessage


class UserQueryRedirectingAgent(BaseRedirectingAgent):
    """
    All the user messages will be redirected to UQRA.
    The agent can respond or redirect to another agent.
    """

    role: ChatRole = ChatRole.UQRA

    prompt: BasePrompt = UQRAPrompt()

    def __init__(self) -> None:
        """Initialize the UserQueryRedirectingAgent with a prompt and a model."""
        super().__init__(prompt=self.prompt)

    def predict(
        self,
        messages: List[ChatMessage]
    ) -> ChatMessage:
        """Get the redirecting agent."""
        print(f"Messages: {messages}")
        response = self.chat_completions(messages, {"type": "text"})

        # Implement Custom Logic here

        # change this
        return {"from_": self.role, "to": ChatRole.USER, "content": response}
