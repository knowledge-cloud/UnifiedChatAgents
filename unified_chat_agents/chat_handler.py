import awsgi
from flask import (Flask, jsonify)
from utils.log_utils import (logger, LogUtils)


app = Flask(__name__)


@app.route('/chat', methods=['POST'])
def chat():
    return jsonify({'message': 'Hello World!'})


def handler(event, context):
    logger.info(f"Event: {LogUtils.stringifier(data=event)}")
    return awsgi.response(app, event, context)