import awsgi
from flask import (Flask, jsonify)
from lib.prompt import BasePrompt
from utils.log_utils import (logger, LogUtils)
from models.client.client_dao import clientDAOInstance


app = Flask(__name__)


@app.route('/chat', methods=['POST'])
def chat():
    res = BasePrompt("""
        Hi {name}, 
        {message}
        Thanks,
        {sender}
    """)
    print(res.input_variables)
    response = res.get_prompt(
        name="John", message="Hello World!", sender="Jane")
    return response


def handler(event, context):
    logger.info(f"Event: {LogUtils.stringify(data=event)}")
    return awsgi.response(app, event, context)
