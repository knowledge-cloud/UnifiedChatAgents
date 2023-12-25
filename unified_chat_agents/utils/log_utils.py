import json
import logging


class LogUtils:
    def __init__(self):
        self.logger = logging.getLogger("UCA")
        self.logger.setLevel(logging.INFO)
        # self.logger.setLevel(logging.DEBUG)

    def stringify(data: dict) -> str:
        return json.dumps(data,  separators=(', ', ': '))


logger = LogUtils().logger
