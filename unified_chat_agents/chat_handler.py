import awsgi
from flask import (Flask, jsonify)
from utils.log_utils import (logger, LogUtils)
from models.client.client_dao import clientDAOInstance


app = Flask(__name__)


@app.route('/chat', methods=['POST'])
def chat():
    # res = clientDAOInstance.get_client("Test Org", "1")
    res = clientDAOInstance.save_client(
        "1", "Test Org", "test_client", "api.xyz.com")
    print(res)
    # print(res.id)
    # print(res.base_url)
    return jsonify({'message': 'Hello World!'})


def handler(event, context):
    logger.info(f"Event: {LogUtils.stringify(data=event)}")
    return awsgi.response(app, event, context)
