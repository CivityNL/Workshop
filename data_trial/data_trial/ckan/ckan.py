import json
import logging
from pathlib import Path
from time import sleep

import requests

logger = logging.getLogger(__name__)


class CKAN:

    def __init__(self, ckan_url: str, ckan_api_token: str) -> None:
        super().__init__()
        self.__ckan_url = ckan_url
        self.__action_api_path = '/api/3/action/'
        self.__headers = {'Authorization': ckan_api_token}

    def package_exists(self, package_id: str) -> bool:
        url: str = self.__ckan_url + self.__action_api_path + 'package_show?id=' + package_id
        package_show_json = self.get_something(url)
        return package_show_json['success']

    def delete_resource_if_exists(self, resource_id):
        resource_show_url = self.__ckan_url + self.__action_api_path + 'resource_show?id=' + resource_id
        resource_show_json = self.get_something(resource_show_url)
        if resource_show_json['success']:
            self.delete_resource(resource_id)
        else:
            logger.info(f'Resource [{resource_id}] does not exist, no need to delete it from CKAN [{self.__ckan_url}].')

    def delete_resource(self, resource_id: str) -> bool:
        resource_delete_url: str = self.__ckan_url + self.__action_api_path + 'resource_delete'
        payload = {'id': resource_id}
        resource_delete_json = self.post_data(resource_delete_url, payload)
        if resource_delete_json["success"]:
            logger.info(f"Existing resource [{resource_id}] successfully deleted. Giving CKAN [{self.__ckan_url}] some rest...")
            sleep(10)

    def create_resource(self, file_name, payload):
        resource_create_url: str = self.__ckan_url + self.__action_api_path + 'resource_create'
        resource_file: Path = Path(file_name)
        if resource_file.is_file():
            files = {'upload': open(file_name, 'rb')}
            self.post_data_and_files(resource_create_url, payload, files)

    def get_something(self, url: str) -> json:
        logger.info(f'Getting something from CKAN {url}')
        response = requests.request("GET", url, headers=self.__headers)
        data = response.text
        return json.loads(data)

    def post_data_and_files(self, url: str, data: json, files) -> json:
        logger.info(f'Posting data and files to CKAN {url}')
        response = requests.request("POST", url, headers=self.__headers, data=data, files=files)
        response_data = response.text
        return json.loads(response_data)

    def post_data(self, url: str, data: json) -> json:
        logger.info(f'Posting data to CKAN {url}')
        response = requests.request("POST", url, headers=self.__headers, data=data)
        response_data = response.text
        return json.loads(response_data)
