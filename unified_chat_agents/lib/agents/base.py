from abc import ABC
from typing import List
import tiktoken

from openai import OpenAI
from openai.types.chat.completion_create_params import ResponseFormat

from lib.prompt import BasePrompt
from utils.log_utils import logger
from lib.openai import OpenAIModel, OpenAIChatMessage, OpenaiChatRole
# from utils.log_utils import logger


class BaseAgentException(Exception):
    """A base exception for the BaseAgent class."""
    pass


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
        self.encoding = tiktoken.encoding_for_model(model.value)

    def chat_completions(
        self,
        messages: List[OpenAIChatMessage],
        response_format: ResponseFormat = {"type": "text"},
        **kwargs
    ) -> str:
        """
        Get the chat completions for the provided messages.
        The output format can be `json_object` or `string`.
        """

        system_prompt = self.prompt.get_prompt(**kwargs)
        system_message: OpenAIChatMessage = OpenAIChatMessage(**{
            "role": OpenaiChatRole.SYSTEM.value, "content": system_prompt
        })
        messages = [system_message] + messages

        for message in messages:
            logger.debug(f"********************{message.role}*****************")
            logger.debug(
                f"BaseAgent::chat_completions::messages: {message.content}")
            logger.debug(f"Length: {len(message.content)}")

        response = self.client.chat.completions.create(
            model=self.model.value,
            response_format=response_format,
            messages=messages,
            seed=kwargs.get("seed"),
        )

        logger.info(f"OpenAI::Usage:: {response.usage.model_dump_json()}")
        logger.debug(f"OpenAI::Choices:: {response.choices[0].message.content}")

        return response.choices[0].message.content

    def calculate_token(self, string):
        """Returns the number of tokens in a text string."""
        num_tokens = len(self.encoding.encode(string))
        return num_tokens
