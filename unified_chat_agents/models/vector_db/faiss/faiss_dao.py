from models.vector_db import VectorStorageBaseDAO
from typing import Any, Dict, List, Optional, Sized
from lib.openai.embedding_generator import OpenAIEmbeddingGenerator
import uuid
from aws_utils.s3_utils import S3Utils
import os
from pathlib import Path
from utils.log_utils import logger
import numpy as np
import pickle
import faiss


class FaissDAO(VectorStorageBaseDAO):
    def __init__(
        self, 
        index: Any, 
        index_name: str,
        db_dir_path: str,
        docstore: Dict[str, Any],
        index_to_docstore_id: Dict[int, str],
        embedding_generator: OpenAIEmbeddingGenerator = None,
        ):
        super().__init__()
        if not index_name:
            raise ValueError("index_name must be specified")

        self._vector_db_bucket = os.environ.get("VECTOR_DB_BUCKET")
        self._index = index
        self._index_name = index_name
        self._db_dir_path = db_dir_path
        self._docstore = docstore
        self._index_to_docstore_id = index_to_docstore_id
        self._embedding_generator = embedding_generator if embedding_generator else OpenAIEmbeddingGenerator()

    def _len_check_if_sized(self, x: Any, y: Any, x_name: str, y_name: str) -> None:
        if isinstance(x, Sized) and isinstance(y, Sized) and len(x) != len(y):
            raise ValueError(
                f"{x_name} and {y_name} expected to be equal length but "
                f"len({x_name})={len(x)} and len({y_name})={len(y)}"
            )
        return
    
    def _persist_to_local(self) -> None:
        logger.info(f"Persisting Faiss index to: {self._db_dir_path}")

        path = Path(self._db_dir_path)
        path.mkdir(exist_ok=True, parents=True)

        # save index separately since it is not picklable
        faiss.write_index(
            self._index, str(path / "{index_name}.faiss".format(index_name=self._index_name))
        )
        # save docstore, index_to_docstore_id
        with open(path / "{index_name}.pkl".format(index_name=self._index_name), "wb") as f:
            pickle.dump((self._docstore, self._index_to_docstore_id), f)
        
        S3Utils.upload_diretory(bucket_name=self._vector_db_bucket, directory=self._db_dir_path)
        return


    def _create_faiss_files(db_dir_path: str, index_name: str) -> None:
        path = Path(db_dir_path)
        path.mkdir(exist_ok=True, parents=True)

        index = faiss.IndexFlatL2(1536)

        faiss_file_path = str(path / f"{index_name}.faiss")
        if not os.path.exists(faiss_file_path):
            logger.info(f"Creating Faiss file: {faiss_file_path}")
            faiss.write_index(index, faiss_file_path)

        pkl_file_path = path / f"{index_name}.pkl"
        if not os.path.exists(pkl_file_path):
            logger.info(f"Creating pkl file: {pkl_file_path}")
            with open(pkl_file_path, "wb") as f:
                pickle.dump(({}, {}), f)
 

    def _add(
        self, 
        doc_info: Dict[str, Any], 
        vector: List[float],
        id: str = None,
        ) -> str:
        """Add a single document to the index and docstore."""
        if id is None:
            id = str(uuid.uuid4())
        
        # add vector to index
        self._index.add(np.array([vector], dtype=np.float32))

        # update docstore and index_to_docstore_id
        self._docstore.add({id: doc_info})
        self._index_to_docstore_id.update({len(self._index_to_docstore_id) + 1: id})
        self._persist_to_local(db_dir_path="./faiss")
        return id
    

    def _add_list(
        self, 
        doc_info_list: List[Dict[str, Any]], 
        vectors: List[List[float]], 
        ids: List[str] = None,
        ) -> List[str]:
        """Add a list of documents to the index and docstore."""
        self._len_check_if_sized(doc_info_list, vectors, "doc_info_list", "vectors")
        self._len_check_if_sized(doc_info_list, ids, "doc_info_list", "ids") if ids else None
        
        if ids is None:
            ids = [str(uuid.uuid4()) for _ in range(len(doc_info_list))]
        
        # add vectors to index
        self._index.add(np.array(vectors, dtype=np.float32))

        # update docstore and index_to_docstore_id
        self._docstore.update({id: doc_info for id, doc_info in zip(ids, doc_info_list)})
        starting_len = len(self._index_to_docstore_id)
        self._index_to_docstore_id.update({starting_len + j: id_ for j, id_ in enumerate(ids)})
        self._persist_to_local()
        return ids
    

    def _query_by_vector(
        self, 
        vector: List[float], 
        top_k: int,
        ) -> List[Dict[str, Any]]:
        if top_k is None:
            raise ValueError("top_k must be specified")

        vector_array = np.array([vector], dtype=np.float32)
        _, indices = self._index.search(vector_array, top_k)
        logger.info(f"indices: {indices}")

        logger.info(f"docstore: {self._docstore}")
        results = []
        for j, i in enumerate(indices[0]):
            if i < 0:
                continue #Add warning that index strength is less top_k

            docstore_id = self._index_to_docstore_id[i]
            results.append((self._docstore[docstore_id]))
        return results

    
    def insert(
        self, 
        doc_info: Dict[str, Any], 
        id: str = None, 
        text_key: str = "text",
        ) -> str:
        if not text_key in doc_info:
            raise ValueError(f"doc_info must contain key: {text_key}")

        vector = self._embedding_generator.generate_embedding(text=doc_info[text_key])
        return self._add(doc_info=doc_info, vector=vector, id=id)
    
    def insert_list(
        self, 
        doc_info_list: List[Dict[str, Any]],
        ids: List[str] = None, 
        text_key: str = "text",
        ) -> List[str]:
        if any(text_key not in doc_info for doc_info in doc_info_list):
            raise ValueError(f"doc_info must contain key: {text_key}")
        
        vectors = [self._embedding_generator.generate_embedding(text=doc_info[text_key]) for doc_info in doc_info_list]
        return self._add_list(doc_info_list=doc_info_list, vectors=vectors, ids=ids)


    def fetch_all(self) -> List[Dict[str, Any]]:
        results = []
        logger.info(f"docstore: {self._docstore}")
        for _, value in self._docstore.items():
            results.append(value)
        return results

    def query(
        self, 
        query: str, 
        top_k: int = None, 
        ) -> List[Dict[str, Any]]:
        if top_k is None:
            top_k = self._top_k

        vector = self._embedding_generator.generate_embedding(text=query)
        return self.query_by_vector(embedding=vector, top_k=top_k)


    def query_by_vector(
        self, 
        embedding: List[float],  
        top_k: int = None, 
        ) -> List[Dict[str, Any]]:
        if top_k is None:
            top_k = self._top_k
        return self._query_by_vector(vector=embedding, top_k=top_k)
    
    
    def delete_collection(self) -> None:
        if os.path.exists(self._db_dir_path):
            os.remove(self._db_dir_path)
        else:
            logger.warn(f"The file does not exist: {self._db_dir_path}")


    @classmethod
    def load_from_local(
        cls, 
        db_dir_path: str = "/tmp/faiss", 
        index_name: str = None
        ):
        if not index_name or index_name == "":
            raise ValueError("index_name must be specified")

        cls._create_faiss_files(db_dir_path=db_dir_path, index_name=index_name)
        path = Path(db_dir_path)
        index = faiss.read_index(str(path / "{index_name}.faiss".format(index_name=index_name)))

        with open(path / "{index_name}.pkl".format(index_name=index_name), "rb") as f:
            docstore, index_to_docstore_id = pickle.load(f)
        return cls(
            index=index, 
            index_name=index_name, 
            db_dir_path=db_dir_path, 
            docstore=docstore, 
            index_to_docstore_id=index_to_docstore_id
            )
