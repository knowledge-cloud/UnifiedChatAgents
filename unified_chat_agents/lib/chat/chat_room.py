from typing import Dict, List
from lib.chat import ChatMessage, ChatRole
from lib.agents import BaseRedirectingAgent, UserQueryRedirectingAgent, RetrievalAugmentedGenerationAgent, RequestSynthesizerAgent, ResponseSynthesizerAgent
from lib.prompt import ChatPromptTemplate
from datetime import datetime
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

    def chat(self) -> None:
        """Continue the chat session."""

        while True:
            logger.info("Chat Session Started")
            last_message = self.last_message
            logger.info(f"Last Message: {last_message}")
            messages = ChatPromptTemplate(
                self.messages).get_format_messages(last_message.to)
            logger.info(f"======= Calling {last_message.to} Agent  =======")
            start_time = datetime.now()
            response = self.AGENTS[last_message.to].predict(messages)
            if response.from_ == ChatRole.USER:
                logger.info("Chat Session Ended")
                self.last_message.to = response.to
            else:
                self.add_message(response)
            logger.info(
                f"================= {datetime.now() - start_time} ====================")
            for message in self.messages:
                logger.info(message)
            if response.to == ChatRole.USER:
                break

        logger.info("Chat Session Ended")
