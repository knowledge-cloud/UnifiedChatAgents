from typing import List, Union
from lib.prompt import Message, BasePrompt
from lib.agents import BaseRedirectingAgent, RedirectingAgentRole
from constants.prompts import ResSAPrompt


class ResponseSynthesizerAgent(BaseRedirectingAgent):
    """
    The agent can only respond can not redirect to another agent.
    """

    role: RedirectingAgentRole = RedirectingAgentRole.ResSA

    prompt: BasePrompt = ResSAPrompt()

    def __init__(self) -> None:
        """Initialize the ResponseSynthesizerAgent with a prompt and a model."""
        super().__init__(prompt=self.prompt)

    def get_redirecting_agent(
        self,
        messages: List[Message]
    ) -> Union[RedirectingAgentRole, None]:
        """Get the redirecting agent. If None, then the agent can only respond."""
        response = self.chat_completions(messages, {"type": "json"})

        # Implement Custom Logic here

        return None  # change this