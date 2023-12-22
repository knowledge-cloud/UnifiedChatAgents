from typing import List
from openai import OpenAI
from aws_utils.secrets_manager import SecretsManager
import os

    
class OpenAIEmbeddingGenerator():
    def __init__(self):
        self._client = OpenAI()
    
    def generate_embedding(self, text: str, model: str = "text-embedding-ada-002") -> List[float]:
        """Generates embedding for given text using OpenAI API"""
        return self._client.embeddings.create(input=text, model=model).data[0].embedding
    
