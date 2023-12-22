from typing import List, Dict, Any
from abc import ABC, abstractmethod


class VectorStorageBaseDAO(ABC):
    """Base class for vector storage DAOs"""

    def __init__(self):
        self._top_k = 5

    @abstractmethod
    def insert(
        self,
        doc_info: Dict[str, Any],
        collection: str,
        id: str = None,
        text_key: str = "text",
    ) -> str:
        """Inserts a single document into the collection"""
        raise NotImplementedError("Not implemented")

    @abstractmethod
    def insert_list(
        self,
        doc_info_list: List[Dict[str, Any]],
        collection: str,
        ids: List[str] = None,
        text_key: str = "text",
    ) -> List[str]:
        """Inserts a list of documents into the collection"""
        raise NotImplementedError("Not implemented")

    @abstractmethod
    def fetch_all(self) -> List[Dict[str, Any]]:
        """Fetches all documents from the collection"""
        raise NotImplementedError("Not implemented")

    @abstractmethod
    def query(
        self,
        query: str,
        collection: str,
        top_k: int = None,
    ) -> List[Dict[str, Any]]:
        """Queries the collection for the given query string and returns the top k results"""
        raise NotImplementedError("Not implemented")

    @abstractmethod
    def query_by_vector(
        self,
        embedding: List[float],
        collection: str,
        top_k: int = None,
    ) -> List[Dict[str, Any]]:
        """Queries the collection for the given embedding and returns the top k results"""
        raise NotImplementedError("Not implemented")

    @abstractmethod
    def delete_collection(self, collection: str) -> None:
        """Deletes the collection"""
        raise NotImplementedError("Not implemented")
