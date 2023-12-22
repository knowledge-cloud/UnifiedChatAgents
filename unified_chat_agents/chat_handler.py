import os
import awsgi
from flask import (Flask, jsonify, request)
from utils.log_utils import (logger, LogUtils)
from models.vector_db.faiss.faiss_dao import FaissDAO
from utils.log_utils import (logger, LogUtils)
from aws_utils.secrets_manager import SecretsManager
from aws_utils.s3_utils import S3Utils
import json
from flask import (Flask, jsonify, request)
from lib.chat import ChatRole, ChatRoom, ChatMessage
from models.vector_db.weaviate.weaviate_dao import WeaviateDAO

secrets = SecretsManager.get_secret("UCA")
os.environ["OPENAI_API_KEY"] = secrets["OPENAI_KEY"]
os.environ["WEAVIATE_KEY"] = secrets["WEAVIATE_KEY"]
os.environ["WEAVIATE_URL"] = "https://unified-chat-agents-el9cpwl9.weaviate.network"
os.environ["VECTOR_DB_BUCKET"] = "uca-vector-store"


app = Flask(__name__)


@app.route('/chat', methods=['POST'])
def chat():
    user_message = "Hello"
    chat_messages = [ChatMessage(**{"from_": ChatRole.USER,
                                    "to": ChatRole.UQRA, "content": user_message})]
    chat_room = ChatRoom("test_session_id_1", chat_messages)
    try:
        chat_room.chat()
        res = chat_room.get_last_message()
        logger.info(f"Response: {res}")
        return res.model_dump_json()
    except Exception as e:
        logger.error(f"Error: {e}")


@app.route('/docs', methods=['POST'])
def ingest_api_docs():
    logger.info(f"Request: {request}")
    data = json.loads(request.data)
    faiss_dao = FaissDAO.load_from_local(index_name=data.get("collection"))
    saved_ids = faiss_dao.insert_list(doc_info_list=data.get('data'))
    return jsonify({'message': 'Success', 'ids': saved_ids})


@app.route('/<collection>/docs', methods=['GET'])
def fetch_all_docs(collection: str):
    logger.info(f"Fetching all docs form : {collection}")
    faiss_dao = FaissDAO.load_from_local(index_name=collection)
    docs = faiss_dao.fetch_all()
    return jsonify({'message': 'Success', 'docs': docs})


@app.route('/<collection>', methods=['DELETE'])
def delete_class(collection: str):
    logger.info(f"Deleting collectionq: {collection}")
    faiss_dao = FaissDAO.load_from_local(index_name=collection)
    faiss_dao.delete_collection(collection=collection)
    return jsonify({'message': 'Success'})


def handler(event, context):
    logger.info(f"Event: {LogUtils.stringify(event)}")
    S3Utils.download_to_directory(bucket_name=os.environ.get(
        "VECTOR_DB_BUCKET"), directory="/tmp/faiss")
    return awsgi.response(app, event, context)
