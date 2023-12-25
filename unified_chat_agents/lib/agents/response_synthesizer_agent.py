from typing import List
from lib.prompt import BasePrompt
from lib.agents import BaseRedirectingAgent
from constants.prompts import ResSAPrompt
from lib.chat import ChatRole, ChatMessage
from lib.openai import OpenAIChatMessage


class ResponseSynthesizerAgent(BaseRedirectingAgent):
    """
    The agent can only respond can not redirect to another agent.
    """

    role: ChatRole = ChatRole.ResSA

    prompt: BasePrompt = ResSAPrompt()

    def __init__(self) -> None:
        """Initialize the ResponseSynthesizerAgent with a prompt and a model."""
        super().__init__(prompt=self.prompt)

    def predict(
        self,
        messages: List[OpenAIChatMessage],
        **kwargs
    ) -> ChatMessage:
        """Get the redirecting agent. If None, then the agent can only respond."""
        response = self.chat_completions(messages, {"type": "text"})

        return ChatMessage(
            **{
                "from_": self.role,
                "to": ChatRole.USER,
                "content": response,
            }
        )
