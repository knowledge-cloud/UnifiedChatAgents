import awsgi
from flask import (Flask, request, jsonify)


app = Flask(__name__)


@app.route('/chat', methods=['POST'])
def chat():
    return jsonify({'message': 'Hello World!'})


def handler(event, context):
    return awsgi.response(app, event, context)