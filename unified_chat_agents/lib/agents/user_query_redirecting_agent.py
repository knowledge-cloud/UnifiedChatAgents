import json
from typing import List
from lib.prompt import BasePrompt
from lib.agents import BaseRedirectingAgent, BaseAgentException
from constants.prompts import UQRAPrompt
from lib.chat import ChatRole, ChatMessage
from utils.log_utils import logger


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
        response = self.chat_completions(
            messages, {"type": "json_object"}, seed=1139909034989)
        formatted_response = json.loads(response)
        logger.info(f"Response: {formatted_response}")
        if formatted_response.get("user_response"):
            return ChatMessage(**{"from_": self.role, "to": ChatRole.USER, "content": formatted_response.get("user_response")})
        elif formatted_response.get("redirect_to"):
            logger.info(
                f"Redirecting to: {formatted_response.get('redirect_to')}")
            logger.info(
                f"Redirecting to: {ChatRole(formatted_response.get('redirect_to'))}")
            return ChatMessage(**{"from_": ChatRole.USER, "to": ChatRole(formatted_response.get("redirect_to"))})
        else:
            BaseAgentException("Invalid response from the agent.")
