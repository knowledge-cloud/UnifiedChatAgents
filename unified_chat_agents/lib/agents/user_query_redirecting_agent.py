from typing import List, Union
from lib.prompt import Message, BasePrompt
from lib.agents import BaseRedirectingAgent, RedirectingAgentRole
from constants.prompts import UQRAPrompt


class UserQueryRedirectingAgent(BaseRedirectingAgent):
    """
    All the user messages will be redirected to UQRA.
    The agent can respond or redirect to another agent.
    """

    role: RedirectingAgentRole = RedirectingAgentRole.UQRA

    prompt: BasePrompt = UQRAPrompt()

    def __init__(self) -> None:
        """Initialize the UserQueryRedirectingAgent with a prompt and a model."""
        super().__init__(prompt=self.prompt)

    def get_redirecting_agent(
        self,
        messages: List[Message]
    ) -> Union[RedirectingAgentRole, None]:
        """Get the redirecting agent."""
        response = self.chat_completions(messages, {"type": "json"})

        # Implement Custom Logic here

        return RedirectingAgentRole.RAGA  # change this