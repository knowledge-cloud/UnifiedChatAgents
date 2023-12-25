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


app = Flask(__name__)


@app.route('/chat', methods=['POST'])
def chat():
    api_doc = """
{
    "description": "Get the wallet of customer",
    "method": "GET",
    "path": "/customer/{customer_id}/wallet",
    "path_parameters": {
        "customer_id": {
            "description": "The customer ID",
            "type": "int"
        }
    },
}
"""
    user_message = "Hello"
    chat_messages = [
        ChatMessage(**{
            "from_": ChatRole.USER,
            "to": ChatRole.UQRA,
            "content": user_message
        }),
        ChatMessage(**{
            "from_": ChatRole.UQRA,
            "to": ChatRole.USER,
            "content": "Hello! How can I assist you today?"
        }),
        ChatMessage(**{
            "from_": ChatRole.USER,
            "to": ChatRole.ReqSA,
            "content": "I want to know the wallet balance of a customer?"
        }),
        ChatMessage(**{
                    "from_": ChatRole.ReqSA,
                    "to": ChatRole.USER,
                    "content": "Can you please provide the customer ID for whom you want to know the wallet balance?"
                    }),
        ChatMessage(**{
                    "from_": ChatRole.USER,
                    "to": ChatRole.UQRA,
                    "content": "1234"
                    }),
    ]
    chat_room = ChatRoom("test_session_id_1", chat_messages)
    try:
        start_time = datetime.now()
        chat_room.chat(api_docs=api_doc)
        logger.info(f"Time taken: {datetime.now() - start_time}")
        logger.info(f"Response: {chat_room.last_message}")
        return chat_room.last_message.model_dump_json()
    except Exception as e:
        logger.error(f"Error: {e.message}")


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
