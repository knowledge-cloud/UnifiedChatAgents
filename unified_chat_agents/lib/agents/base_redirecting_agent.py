from abc import abstractmethod
from enum import Enum
from typing import List, Union
from lib.agents import BaseAgent
from lib.prompt import Message, BasePrompt
from lib.openai import OpenAIModel


class RedirectingAgentRole(Enum):
    UQRA = "USER_QUERY_REDIRECTING_AGENT"
    """
    All the user messages will be redirected to UQRA.
    The agent can respond or redirect to another agent.
    """

    RAGA = "RETRIEVAL_AUGMENTED_GENERATION_AGENT"
    """
    Will query relevant documents from the knowledge base and augment the user query.
    The agent can respond directly to user or send the queried data to any specified agent.
    """

    ReqSA = "REQUEST_SYNTHESIZER_AGENT"
    """
    Will synthesize the required API request from user messages.
    The agent can respond directly to user or send the synthesized request to any specified agent.
    """

    ResSA = "RESPONSE_SYNTHESIZER_AGENT"
    """
    Will synthesize the natural language response from the API response.
    The agent will respond directly to user.
    """


class BaseRedirectingAgent(BaseAgent):
    """A class to represent a base redirecting agent."""

    role: RedirectingAgentRole

    def __init__(
        self,
        prompt: BasePrompt,
        model: OpenAIModel = OpenAIModel.GPT_3_5
    ) -> None:
        """Initialize the BaseRedirectingAgent with a prompt and a model."""
        super().__init__(prompt=prompt, model=model)

    @abstractmethod
    def get_redirecting_agent(self, messages: List[Message]) -> Union[RedirectingAgentRole, None]:
        """
        Redirect or respond to the messages.
        """
        pass
