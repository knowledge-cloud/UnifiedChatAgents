from typing import List, Dict, Any
from abc import ABC, abstractmethod
    
    
class VectorStorageBaseDAO(ABC):

    @abstractmethod
    def insert(self, api_doc: Dict[str, Any]) -> str:
        """Inserts a single document into the collection"""
        raise NotImplementedError("Not implemented")
    
    @abstractmethod
    def insert_list(self, api_docs: List[Dict[str, Any]]) -> List[str]:
        """Inserts a list of documents into the collection"""
        raise NotImplementedError("Not implemented")
    
    @abstractmethod
    def fetch_all(self) -> List[Dict[str, Any]]:
        """Fetches all documents from the collection"""
        raise NotImplementedError("Not implemented")

    @abstractmethod
    def query(self, query: str, top_k: int, schema: str) -> List[Dict[str, Any]]:
        """Queries the collection for the given query string and returns the top k results"""
        raise NotImplementedError("Not implemented")
    
    @abstractmethod
    def query(self, embedding: List[float], top_k: int, schema: str) -> List[Dict[str, Any]]:
        """Queries the collection for the given embedding and returns the top k results"""
        raise NotImplementedError("Not implemented")
    
    @abstractmethod
    def delete_collection(self) -> None:
        """Deletes the collection"""
        raise NotImplementedError("Not implemented")