from enum import Enum
from lib.openai.openai_chat_message import OpenAIChatMessage, OpenaiChatRole

class OpenAIModel(Enum):
    GPT_4 = "gpt-4-1106-preview"
    GPT_3_5 = "gpt-3.5-turbo-1106"
