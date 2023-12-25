from typing import List
from lib.prompt import BasePrompt
from lib.agents import BaseRedirectingAgent
from constants.prompts import RAGAPrompt
from lib.chat import ChatRole, ChatMessage


class RetrievalAugmentedGenerationAgent(BaseRedirectingAgent):
    """
    The agent that gives performs RAG search and redirects to appropriate agent based on the search results.
    """

    role: ChatRole = ChatRole.RAGA

    prompt: BasePrompt = RAGAPrompt()

    def __init__(self) -> None:
        """Initialize the RetrievalAugmentedGenerationAgent with a prompt and a model."""
        super().__init__(prompt=self.prompt)

    def predict(
        self,
        messages: List[ChatMessage],
        **kwargs
    ) -> ChatMessage:
        """Get the redirecting agent."""
        response = self.chat_completions(messages, {"type": "json"})

        # Implement Custom Logic here

        return ChatRole.ReqSA  # change this
