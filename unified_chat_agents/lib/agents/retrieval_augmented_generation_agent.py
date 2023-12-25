from typing import List
from lib.prompt import BasePrompt
from lib.agents import BaseRedirectingAgent
from constants.prompts import RAGAPrompt
from lib.chat import ChatRole, ChatMessage
from lib.agents.user_intent_capture_agent import UserIntentCaptureAgent
from utils.log_utils import logger
from models.vector_db.faiss.faiss_dao import FaissDAO
from lib.prompt import ChatPromptTemplate
import json


class RetrievalAugmentedGenerationAgent(BaseRedirectingAgent):
    """
    The agent that gives performs RAG search and redirects to appropriate agent based on the search results.
    """

    role: ChatRole = ChatRole.RAGA

    prompt: BasePrompt = RAGAPrompt()

    def __init__(self) -> None:
        """Initialize the RetrievalAugmentedGenerationAgent with a prompt and a model."""
        super().__init__(prompt=self.prompt)
        self._uica = UserIntentCaptureAgent()
        self._vectordb_dao = FaissDAO.load_from_local(index_name="ApiDocs")

    def predict(
        self,
        messages: List[ChatMessage],
        **kwargs
    ) -> ChatMessage:
        """Get the redirecting agent."""

        formatted_messages = ChatPromptTemplate(messages).get_format_messages(ChatRole.UICA)
        uica_response = self._uica.predict(formatted_messages)
        logger.info("=====================================")
        logger.info(f"{ChatRole.UICA} -> {ChatRole.RAGA}: {uica_response.content}")
        logger.info("-------------------------------------")
        
        query_response = self._vectordb_dao.query(uica_response.content, 2)
        logger.debug(f"API Docs fetched for query: {query_response}")

        api_details = [{"id": doc["id"], "api_description": doc["text"]} for doc in query_response]
        intent_messages = ChatPromptTemplate([uica_response]).get_format_messages(ChatRole.RAGA)
        api_doc = json.loads(self.chat_completions(intent_messages, {"type": "json_object"}, api_details=api_details))

        if not api_doc.get("doc_id"):
            return ChatMessage(**{"from_": self.role, "to": ChatRole.USER, "content": "Sorry, I could not find any relevant API docs."})
        else:
            raga_response = self._vectordb_dao.fetch_by_id(api_doc["doc_id"])
            return ChatMessage(**{"from_": self.role, "to": ChatRole.ReqSA, "kwargs": {"api_docs": raga_response}})
