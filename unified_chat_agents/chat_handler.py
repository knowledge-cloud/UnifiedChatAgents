import os
import json
import awsgi
from datetime import datetime
from flask import (Flask, jsonify, request)

from lib.chat import ChatRole, ChatRoom, ChatMessage
from models.vector_db.faiss.faiss_dao import FaissDAO
from utils.log_utils import (logger, LogUtils)
from aws_utils.secrets_manager import SecretsManager
from aws_utils.s3_utils import S3Utils

secrets = SecretsManager.get_secret("UCA")
os.environ["OPENAI_API_KEY"] = secrets["OPENAI_KEY"]
os.environ["WEAVIATE_KEY"] = secrets["WEAVIATE_KEY"]
os.environ["WEAVIATE_URL"] = "https://unified-chat-agents-el9cpwl9.weaviate.network"
os.environ["VECTOR_DB_BUCKET"] = "uca-vector-store"

S3Utils.download_to_directory(bucket_name=os.environ.get("VECTOR_DB_BUCKET"), directory="/tmp/faiss")


app = Flask(__name__)


@app.route('/chat', methods=['POST'])
def chat():
    data = json.loads(request.data)
    chat_messages = [ ChatMessage(**message) for message in data.get("messages")]
    chat_room = ChatRoom("test_session_id_1", chat_messages)
    start_time = datetime.now()
    chat_room.chat()
    logger.info(f"Time taken: {datetime.now() - start_time}")
    logger.info(f"Response: {chat_room.last_message}")

    response = {
        "message": "Success",
        "chat_messages": [json.loads(chat_message.model_dump_json()) for chat_message in chat_room.messages],
        "last_message": json.loads(chat_room.last_message.model_dump_json())
    }
    return response


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
    logger.info(f"Deleting collection: {collection}")
    faiss_dao = FaissDAO.load_from_local(index_name=collection)
    faiss_dao.delete_collection()
    return jsonify({'message': 'Success'})


@app.errorhandler(Exception)
def handle_exception(e):
    logger.error(f"Error: {e}")
    return {
        "message": "Error",
        "last_message": {
            "from_": ChatRole.UQRA.value,
            "to": ChatRole.USER.value,
            "content": "Something went wrong. Please try again later.",
            "kwargs": {}
        }
    }


def handler(event, context):
    logger.info(f"Event: {LogUtils.stringify(event)}")
    return awsgi.response(app, event, context)
