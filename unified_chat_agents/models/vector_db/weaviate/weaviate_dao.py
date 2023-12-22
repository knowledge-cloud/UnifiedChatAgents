from models.vector_db import VectorStorageBaseDAO
import weaviate
from weaviate.auth import AuthApiKey
from typing import Any, Dict, List
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
        super().__init__()
        api_key = os.environ.get('WEAVIATE_KEY')
        url = os.environ.get('WEAVIATE_URL')
        self._client = weaviate.connect_to_wcs(url, AuthApiKey(api_key))
        self._embedding_generator = OpenAIEmbeddingGenerator()

    def insert(
        self,
        doc_info: Dict[str, Any],
        collection: str,
        id: str = None,
        text_key: str = "text",
    ) -> str:
        if not self._client.collections.exists(collection):
            self._client.collections.create(collection)

        properties = {}
        properties["text"] = doc_info[text_key]
        vector = self._embedding_generator.generate_embedding(
            text=properties["text"])
        logger.info(
            f"Inserting doc with id: {id}, class_name: {collection}, metadata: {properties}")

        docs = self._client.collections.get(collection)
        id = docs.data.insert(
            properties=properties,
            vector=vector
        )
        logger.info(f"Ingested doc with id: {id}")
        return id

    def insert_list(
        self,
        doc_info_list: List[Dict[str, Any]],
        collection: str,
        ids: List[str] = None,
        text_key: str = "text",
    ) -> List[str]:
        if not id is None or len(doc_info_list) != len(id):
            raise ValueError(
                "id must be None or have the same length as doc_info_list")
        for doc_info in doc_info_list:
            if not text_key in doc_info:
                raise ValueError(f"doc_info must contain key: {text_key}")

        # TODO: Batch insert
        ids = []
        for doc_info in doc_info_list:
            id = self.insert(doc_info=doc_info,
                             collection=collection, id=id, text_key=text_key)
            ids.append(id)
        return ids

    def fetch_all(self, schema: str) -> List[Dict[str, Any]]:
        raise NotImplementedError("Not implemented")

    def query(
        self,
        query: str,
        collection: str,
        top_k: int = None,
    ) -> List[Dict[str, Any]]:
        if top_k is None:
            top_k = self._top_k

        docs = self._client.collections.get(collection)
        query_results = docs.query.near_text(
            query=query,
            limit=top_k
        )
        return [object for object in query_results.objects]

    def query_by_vector(
        self,
        embedding: List[float],
        collection: str,
        top_k: int = None,
    ) -> List[Dict[str, Any]]:
        if top_k is None:
            top_k = self._top_k

        docs = self._client.collections.get(collection)
        query_results = docs.query.near_vector(
            near_vector=embedding,
            limit=top_k
        )
        return [object for object in query_results.objects]

    def delete_collection(self, collection: str) -> None:
        if self._client.collections.exists(collection):
            self._client.collections.delete(collection)
