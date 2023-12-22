import os
import awsgi
from flask import (Flask)
from utils.log_utils import (logger, LogUtils)
from lib.chat import ChatRole, ChatRoom

os.environ["OPENAI_API_KEY"] = "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"

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


def handler(event, context):
    logger.info(f"Event: {LogUtils.stringify(data=event)}")
    return awsgi.response(app, event, context)
