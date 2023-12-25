from httpx import Client
from utils.log_utils import logger


class ApiToolbox:
    def __init__(self, base_url):
        self.client = Client(base_url=base_url)

    def execute_request(self, request_info):
        method = request_info.get('method').upper()
        endpoint = request_info.get('url')
        url = endpoint
        data = request_info.get('data', {})
        headers = request_info.get('headers', {})

        if data:
            logger.debug(f"{method}: {url}:: {data}")
        else:
            logger.debug(f"{method}: {url}")

        match method:
            case 'GET':
                response = self._get(url, headers)
            case 'POST':
                response = self._post(url, data, headers)
            case 'PUT':
                response = self._put(url, data, headers)
            case 'DELETE':
                response = self._delete(url, headers)
            case _:
                raise ValueError(f"Invalid method: {method}")

        logger.debug(f"Response: {response}")
        return response

    def _get(self, url, headers):
        response = self.client.get(url, headers=headers)
        response_json = response.json()
        logger.debug(f"GET Response: {response_json}")
        return response_json

    def _post(self, url, data, headers):
        response = self.client.post(url, json=data, headers=headers)
        response_json = response.json()
        logger.debug(f"POST Response: {response_json}")
        return response_json

    def _put(self, url, data, headers):
        response = self.client.put(url, json=data, headers=headers)
        response_json = response.json()
        logger.debug(f"PUT Response: {response_json}")
        return response_json

    def _delete(self, url, headers):
        response = self.client.delete(url, headers=headers)
        response_json = response.json()
        logger.debug(f"DELETE Response: {response_json}")
        return response_json
