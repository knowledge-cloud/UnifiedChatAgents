from typing import Dict, List, Union
from lib.chat import ChatMessage, ChatRole
from lib.agents import BaseRedirectingAgent, UserQueryRedirectingAgent, RetrievalAugmentedGenerationAgent, RequestSynthesizerAgent, ResponseSynthesizerAgent
from lib.prompt import ChatPromptTemplate
from lib.openai import OpenAIChatMessage
from utils.log_utils import logger


class ChatRoom:
    messages: List[ChatMessage]
    session_id: str

    def __init__(self, session_id: str, messages: List[ChatMessage]) -> None:
        """Initialize the ChatRoom with a session_id and messages."""
        self.session_id = session_id
        self.messages = messages
        self.AGENTS: Dict[ChatRole, BaseRedirectingAgent] = {
            ChatRole.UQRA: UserQueryRedirectingAgent(),
            ChatRole.RAGA: RetrievalAugmentedGenerationAgent(),
            ChatRole.ReqSA: RequestSynthesizerAgent(),
            ChatRole.ResSA: ResponseSynthesizerAgent()
        }

    def add_message(self, message: ChatMessage) -> None:
        """Add a message to the ChatRoom."""
        self.messages.append(message)

    @property
    def last_message(self) -> ChatMessage:
        """Get the last message in the ChatRoom."""
        return self.messages[-1]

    @last_message.setter
    def last_message(self, message: ChatMessage) -> None:
        """Set the last message in the ChatRoom."""
        self.messages[-1] = message

    def chat(self, **kwargs) -> None:
        """Continue the chat session."""
        for message in self.messages:
            logger.info(
                f"=======[{message.from_} -> {message.to}]===>>>>: {message.content}")

        while True:
            last_message = self.last_message
            messages = self._format_messages(self.messages, last_message.to)
            kwargs = last_message.kwargs if last_message.kwargs else kwargs
            response = self.AGENTS[last_message.to].predict(messages, **kwargs)
            logger.debug(f"ChatRoom::chat::response: {response}")
            logger.info(
                f"{response.from_} -> {response.to}: {response.content if response.content else f'Redirection with kwargs: {response.kwargs}'}")
            logger.info("-------------------------------------")
            if response.from_ == ChatRole.USER:
                self.last_message.to = response.to
            else:
                self.add_message(response)
            if response.to == ChatRole.USER:
                break

        logger.info("Chat Session Ended")


    def _format_messages(
        self, 
        messages: List[ChatMessage], 
        role: ChatRole
        ) -> Union[List[ChatMessage], List[OpenAIChatMessage]]:
        """Format the messages to the format expected by the model."""
        if role != ChatRole.RAGA:
            return ChatPromptTemplate(self.messages).get_format_messages(role)
        return messages
