import os
import awsgi
from flask import (Flask, jsonify, request)
from utils.log_utils import (logger, LogUtils)
from lib.chat import ChatRole, ChatRoom
from models.vector_db.weaviate.weaviate_dao import WeaviateDAO
from utils.log_utils import (logger, LogUtils)
from aws_utils.secrets_manager import SecretsManager
import json

secrets = SecretsManager.get_secret("UCA")
os.environ["OPENAI_API_KEY"] = secrets["OPENAI_KEY"]
os.environ["WEAVIATE_KEY"] = secrets["WEAVIATE_KEY"]
os.environ["WEAVIATE_URL"] = "https://unified-chat-agents-el9cpwl9.weaviate.network"

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = "Hello"
    chat_messages = [{"from_": ChatRole.USER,
                      "to": ChatRole.UQRA, "content": user_message}]
    chat_room = ChatRoom("test_session_id_1", chat_messages)
    try:
        chat_room.chat()
        res = chat_room._get_last_message()
        logger.info(f"Response: {res}")
        return res["content"]
    except Exception as e:
        logger.error(f"Error: {e}")


@app.route('/docs', methods=['POST'])
def ingest_api_docs():
    logger.info(f"Request: {request}")
    data = json.loads(request.data)
    weaviate_dao = WeaviateDAO()
    saved_ids = weaviate_dao.insert_list(doc_info_list=data.get('data'), schema=data.get('class'))
    return jsonify({'message': 'Success', 'ids': saved_ids})

@app.route('/<class_name>/docs', methods=['GET'])
def fetch_all_docs(class_name: str):
    logger.info(f"Fetching all docs for class: {class_name}")
    weaviate_dao = WeaviateDAO()
    docs = weaviate_dao.fetch_all(schema=class_name)
    return jsonify({'message': 'Success', 'docs': docs})

@app.route('/<class_name>', methods=['DELETE'])
def delete_class(class_name: str):
    logger.info(f"Deleting class: {class_name}")
    weaviate_dao = WeaviateDAO()
    weaviate_dao.delete_collection(schema=class_name)
    return jsonify({'message': 'Success'})


def handler(event, context):
    logger.info(f"Event: {LogUtils.stringify(event)}")
    return awsgi.response(app, event, context)
