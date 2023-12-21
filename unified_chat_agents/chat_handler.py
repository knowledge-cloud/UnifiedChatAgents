import os
import awsgi
from flask import (Flask)
from lib.prompt import BasePrompt
from utils.log_utils import (logger, LogUtils)
from lib.prompt import Message
from lib.agents import BaseAgent
from lib.openai import OpenAIModel

os.environ["OPENAI_API_KEY"] = "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"

app = Flask(__name__)


@app.route('/chat', methods=['POST'])
def chat():
    prompt = BasePrompt("""
    You are very intelligent.
    """)
    agent = BaseAgent(prompt, OpenAIModel.GPT_3_5)
    messages = [Message({"role": "user", "content": "Hello, how are you?"})]
    try:
        response = agent.chat_completions(messages, {"type": "text"})
        print("response", response)
        return response
    except Exception as e:
        print(e)


def handler(event, context):
    logger.info(f"Event: {LogUtils.stringify(data=event)}")
    return awsgi.response(app, event, context)
