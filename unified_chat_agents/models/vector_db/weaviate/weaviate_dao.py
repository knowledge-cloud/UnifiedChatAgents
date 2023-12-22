from models.vector_db import VectorStorageBaseDAO
from aws_utils.secrets_manager import SecretsManager
import weaviate
from weaviate.auth import AuthApiKey
from typing import Any, Dict, List, cast
from lib.openai.embedding_generator import OpenAIEmbeddingGenerator
import os
from utils.log_utils import (logger)


API_DOC_SCHEMA: List[Dict] = [
    {
        "dataType": ["string"],
        "description": "Text property",
        "name": "text",
    },
]

class WeaviateDAO(VectorStorageBaseDAO):
    def __init__(self):
        api_key = os.environ.get('WEAVIATE_KEY')
        url = os.environ.get('WEAVIATE_URL')
        self._client = weaviate.connect_to_wcs(url, AuthApiKey(api_key))
        self._embedding_generator = OpenAIEmbeddingGenerator()
    
    def insert(
        self, 
        doc_info: Dict[str, Any], 
        schema: str,
        id: str = None, 
        text_key: str = "text",
    ) -> str:
        if not self._client.collections.exists(schema):
            self._client.collections.create(schema)

        properties = {}
        properties["text"] = doc_info[text_key]
        vector = self._embedding_generator.generate_embedding(text=properties["text"])
        logger.info(f"Inserting doc with id: {id}, class_name: {schema}, metadata: {properties}")

        api_docs = self._client.collections.get(schema)
        id = api_docs.data.insert(
            properties=properties,
            vector=vector
        )
        logger.info(f"Ingested doc with id: {id}")
        return id
    
    def insert_list(
        self, 
        doc_info_list: List[Dict[str, Any]],
        schema: str,
    ) -> List[str]:
        #TODO: Batch insert
        ids = []
        for doc_info in doc_info_list:
            id = self.insert(doc_info=doc_info, schema=schema)
            ids.append(id)
        return ids

    def fetch_all(self, schema: str) -> List[Dict[str, Any]]:
        raise NotImplementedError("Not implemented")

    
    def query(self, query: str, top_k: int, schema: str) -> List[Dict[str, Any]]:
        api_docs = self._client.collections.get(schema)
        results = api_docs.query.near_text(
            query=query,
            limit=top_k
        )
        return results
    
    def query(self, embedding: List[float],  top_k: int, schema: str) -> List[Dict[str, Any]]:
        api_docs = self._client.collections.get(schema)
        results = api_docs.query.near_vector(
            near_vector=embedding,
            limit=top_k
        )
        return results
    
    def delete_collection(self, schema: str) -> None:
        if self._client.collections.exists(schema):
            self._client.collections.delete(schema)