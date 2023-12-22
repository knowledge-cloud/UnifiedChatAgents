from typing import Dict, List
from lib.chat import ChatMessage, ChatRole
from lib.agents import BaseRedirectingAgent, UserQueryRedirectingAgent, RetrievalAugmentedGenerationAgent, RequestSynthesizerAgent, ResponseSynthesizerAgent
from lib.prompt import ChatPromptTemplate


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

    def _get_last_message(self) -> ChatMessage:
        """Get the last message in the ChatRoom."""
        return self.messages[-1]

    def chat(self) -> None:
        """Continue the chat session."""

        while True:
            print("Chat Session Started")
            last_message = self._get_last_message()
            print(f"Last Message: {last_message}")
            messages = ChatPromptTemplate(
                self.messages).get_format_messages(last_message["to"])
            print(f"======= Calling {last_message['to'].value} Agent  =======")
            response = self.AGENTS[last_message["to"]].predict(messages)
            print(f"Response from {last_message['to']} Agent: {response}")
            self.add_message(response)
            print("=====================================")
            if response["to"] == ChatRole.USER:
                break

        print("Chat Session Ended")
