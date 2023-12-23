from typing import Optional
from enum import Enum

from pydantic import BaseModel


class ChatRole(Enum):
    USER = "Customer"
    """
    The user role.
    """

    UQRA = "UQRA"
    """
    USER_QUERY_REDIRECTING_AGENT
    All the user messages will be redirected to UQRA.
    The agent can respond or redirect to another agent.
    """

    RAGA = "RAGA"
    """
    RETRIEVAL_AUGMENTED_GENERATION_AGENT
    Will query relevant documents from the knowledge base and augment the user query.
    The agent can respond directly to user or send the queried data to any specified agent.
    """

    ReqSA = "ReqSA"
    """
    REQUEST_SYNTHESIZER_AGENT
    Will synthesize the required API request from user messages.
    The agent can respond directly to user or send the synthesized request to any specified agent.
    """

    ResSA = "ResSA"
    """
    RESPONSE_SYNTHESIZER_AGENT
    Will synthesize the natural language response from the API response.
    The agent will respond directly to user.
    """


class ChatMessage(BaseModel):
    from_: ChatRole
    """
    Who sent the message.
    """

    to: ChatRole
    """
    To whom the message is sent.
    """

    content: str = ""
    """
    The actual message.
    """

    prompt: Optional[str] = None
    """
    The prompt used by the agent to generate the message.
    """
