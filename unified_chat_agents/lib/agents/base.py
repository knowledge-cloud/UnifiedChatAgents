from abc import ABC
from typing import List

from openai import OpenAI
from openai.types.chat.completion_create_params import ResponseFormat

from lib.prompt import BasePrompt
from lib.openai import OpenAIModel
from lib.chat import ChatMessage


class BaseAgent(ABC):
    prompt: BasePrompt
    """The prompt for the agent."""

    model: OpenAIModel
    """The model for the agent."""

    client: OpenAI

    def __init__(
        self,
        prompt: BasePrompt,
        model: OpenAIModel,
        # Can pass OPENAI_API_KEY as keyword argument or as environment variable
        **kwargs
    ) -> None:
        """Initialize the Agent with a prompt and a model."""
        self.prompt = prompt
        self.model = model
        self.client = OpenAI(api_key=kwargs.get("OPENAI_API_KEY"))

    def chat_completions(
        self,
        messages: List[ChatMessage],
        response_format: ResponseFormat = {"type": "text"},
        **kwargs
    ) -> str:
        """
        Get the chat completions for the provided messages.
        The output format can be `json_object` or `string`.
        """

        system_prompt = self.prompt.get_prompt(**kwargs)
        system_message: ChatMessage = {
            "role": "system", "content": system_prompt}
        messages = [system_message] + messages

        print(messages)

        response = self.client.chat.completions.create(
            model=self.model.value,
            response_format=response_format,
            messages=[system_message] + messages
        )

        return response.choices[0].message.content
