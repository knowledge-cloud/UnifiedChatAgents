from typing import List, Union
from lib.prompt import Message, BasePrompt
from lib.agents import BaseRedirectingAgent, RedirectingAgentRole
from constants.prompts import RAGAPrompt


class RetrievalAugmentedGenerationAgent(BaseRedirectingAgent):
    """
    The agent can respond or redirect to another agent.
    """

    role: RedirectingAgentRole = RedirectingAgentRole.RAGA

    prompt: BasePrompt = RAGAPrompt()

    def __init__(self) -> None:
        """Initialize the RetrievalAugmentedGenerationAgent with a prompt and a model."""
        super().__init__(prompt=self.prompt)

    def get_redirecting_agent(
        self,
        messages: List[Message]
    ) -> Union[RedirectingAgentRole, None]:
        """Get the redirecting agent."""
        response = self.chat_completions(messages, {"type": "json"})

        # Implement Custom Logic here

        return RedirectingAgentRole.ReqSA  # change this