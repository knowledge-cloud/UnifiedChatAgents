from typing import Dict, List
from lib.chat import ChatMessage, ChatRole
from lib.agents import BaseRedirectingAgent, UserQueryRedirectingAgent, RetrievalAugmentedGenerationAgent, RequestSynthesizerAgent, ResponseSynthesizerAgent
from lib.prompt import ChatPromptTemplate
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
            messages = ChatPromptTemplate(
                self.messages).get_format_messages(last_message.to)
            response = self.AGENTS[last_message.to].predict(messages, **kwargs)
            logger.debug(f"ChatRoom::chat::response: {response}")
            logger.info(
                f"=======[{response.from_} -> {response.to}]===>>>>: {response.content if response.content else 'Redirection'}")
            if response.from_ == ChatRole.USER:
                self.last_message.to = response.to
            else:
                self.add_message(response)
            if response.to == ChatRole.USER:
                break
