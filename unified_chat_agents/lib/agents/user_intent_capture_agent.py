from typing import List
import json

from lib.agents.base import BaseAgent
from lib.chat.chat_message import ChatRole
from lib.prompt.base import BasePrompt
from constants.prompts.uica_prompt import UICAPrompt
from lib.chat.chat_message import ChatMessage
from utils.log_utils import logger
from lib.openai import OpenAIModel, OpenAIChatMessage


class UserIntentCaptureAgent(BaseAgent):
    """User Intent Capture Agent."""

    role: ChatRole = ChatRole.UICA

    prompt: BasePrompt = UICAPrompt()

    def __init__(self, model: OpenAIModel = OpenAIModel.GPT_3_5):
        """Initialize the User Intent Capture Agent."""
        super().__init__(prompt=self.prompt, model=model)

    def predict(self, messages: List[OpenAIChatMessage]) -> ChatMessage:
        """Predict the user intent."""
        # Implement Custom Logic here
        response = self.chat_completions(messages, {"type": "json_object"}, seed=1139909034989)
        formatted_response = json.loads(response)
        logger.info(f"UICA Response: {formatted_response}")
        return ChatMessage(**{"from_": self.role, "to": ChatRole.RAGA, "content": formatted_response.get("intent")}) #TODO: make intent field dynamic