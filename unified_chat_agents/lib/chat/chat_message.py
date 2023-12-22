from typing import Dict, Optional, TypedDict
from enum import Enum


class ChatRole(Enum):
    USER = "USER"
    """
    The user role.
    """

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


class ChatMessage(TypedDict):
    from_: ChatRole
    """
    Who sent the message.
    """

    to: ChatRole
    """
    To whom the message is sent.
    """

    content: Dict[str, str]
    """
    The actual message.
    """

    prompt: Optional[str]
    """
    The prompt used by the agent to generate the message.
    """
