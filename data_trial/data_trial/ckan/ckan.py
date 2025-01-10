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

    def delete_packages(self, query: str | None) -> None:
        package_search_url = self.__ckan_url + self.__action_api_path + f'package_search?fl=id&fl=notes&fl=title&rows=1000&start=0'
        if query is not None:
            package_search_url += f'&q={query}'

        package_search_response = self.get_something(package_search_url)

        if package_search_response['success']:
            logger.info(f'Successfully read packages for search [{package_search_url}]')
            results_json_array = package_search_response['result']['results']
            for result in results_json_array:
                package_id: str = result['id']
                self.delete_package_if_exists(package_id)

    def delete_package_if_exists(self, package_id):
        package_show_url = self.__ckan_url + self.__action_api_path + 'package_show?id=' + package_id
        package_show_json = self.get_something(package_show_url)
        if package_show_json['success']:
            self.delete_package(package_id)
        else:
            logger.info(f'Package [{package_id}] does not exist, no need to delete it from CKAN [{self.__ckan_url}].')

    def delete_package(self, package_id: str) -> bool:
        package_delete_url: str = self.__ckan_url + self.__action_api_path + 'dataset_purge'
        payload = {'id': package_id}
        return self.delete_something(package_delete_url, payload)

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
        return self.delete_something(resource_delete_url, payload)

    def create_resource(self, file_name, payload):
        resource_create_url: str = self.__ckan_url + self.__action_api_path + 'resource_create'
        resource_file: Path = Path(file_name)
        if resource_file.is_file():
            files = {'upload': open(file_name, 'rb')}
            self.post_data_and_files(resource_create_url, payload, files)

    def get_something(self, url: str) -> json:
        response = requests.request("GET", url, headers=self.__headers)
        data = response.text
        return json.loads(data)

    def delete_something(self, url: str, data: json) -> bool:
        logger.info(f'Deleting something from CKAN {url}')
        delete_json = self.post_data(url, data)
        if delete_json["success"]:
            logger.info(f"Existing thing [{data}] successfully deleted. Giving CKAN [{self.__ckan_url}] some rest...")
            sleep(10)
            return True
        else:
            logger.info(f"Existing thing [{data}] not deleted.")
            return False

    def post_data_and_files(self, url: str, data: json, files) -> json:
        logger.info(f'Posting data and files to CKAN {url}')
        response = requests.request("POST", url, headers=self.__headers, data=data, files=files)
        response_data = response.text
        return json.loads(response_data)

    def post_data(self, url: str, data: json) -> json:
        logger.info(f'Posting data to CKAN {url}')
        response = requests.request("POST", url, headers=self.__headers, data=data)
        return json.loads(response.text)
