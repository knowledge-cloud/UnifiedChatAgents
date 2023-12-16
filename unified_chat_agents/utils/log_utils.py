import json
import logging

class LogUtils:
    def __init__(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

    def stringifier(data: dict) -> str:
        return json.dumps(data,  separators=(', ', ': '))

LogUtilsInstance = LogUtils()
logger = LogUtilsInstance.logger
    
