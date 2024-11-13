import base64
import hashlib
import json
import logging
import urllib.parse
import requests

from arcgis_for_server_harvester.src.domain.package import Package
from arcgis_for_server_harvester.src.domain.package_list import PackageList

logger = logging.getLogger(__name__)

class Ckan:

    def __init__(self, ckan_url: str, ckan_api_token: str, ckan_organization_id: str) -> None:
        super().__init__()
        self.__ckan_url: str = ckan_url
        self.__action_api_path: str = '/api/3/action/'
        self.__headers = {'Authorization': ckan_api_token}
        self.__ckan_organization_id: str = ckan_organization_id

    @staticmethod
    def hash(s: str) -> str:
        result = str(int.from_bytes(hashlib.sha1(s.encode('utf-8')).digest(), 'big'))
        return result

    @staticmethod
    def encode(s: str) -> str:
        result = str(base64.b64encode(s.replace('https://', '').encode('utf-8')), 'utf-8')
        return result

    @staticmethod
    def decode(b: bytes) -> str:
        result = str(base64.b64decode(b.decode('utf-8')), 'utf-8')
        result = 'https://' + result
        return result

    def create_package(self, package: Package) -> None:
        package_create_url: str = self.__ckan_url + self.__action_api_path + 'package_create'
        json_response: json = self.post_something(package_create_url, package.to_dict(self.__ckan_organization_id))
        if json_response['success']:
            logger.info(f'Successfully created package [{package.get_package_id()}]')
        else:
            logger.info(f'Error creating package [{package.get_package_id()}]: [{json_response["error"]}]')

    def get_packages_for_source(self, arcgis_for_server_url: str) -> PackageList:
        """
        Get packages for a specific ArcGIS for Server since CKAN may also contain packages for other ArcGIS for
        Servers. To keep track of the ArcGIS for Server a package belongs to, the URL is stored in the source field of
        the package
        """
        package_search_url: str = self.__ckan_url + self.__action_api_path + f'package_search?fl=id&rows=500&start=0&q=source:({Ckan.hash(arcgis_for_server_url)})'

        package_list = self.get_packages_for_query(package_search_url)

        return package_list

    def get_packages_for_organization(self, organization_id: str) -> PackageList:
        """
        Get packages for a specific organization
        """
        package_search_url: str = self.__ckan_url + self.__action_api_path + f'package_search?fl=id&rows=500&start=0&q=owner_org:({organization_id})'

        package_list = self.get_packages_for_query(package_search_url)

        return package_list

    def get_packages_for_query(self, package_search_url):
        package_list: PackageList = PackageList()
        json_response: json = self.get_something(package_search_url)
        if json_response['success']:
            logger.info(f'Successfully read packages for search [{package_search_url}]')
            results_json_array = json_response['result']['results']
            for result in results_json_array:
                package_id: str = result['id']
                package_list.add_package(Package(package_id))
        else:
            logger.info(f'Error reading packages for search [{package_search_url}]')
        return package_list

    def update_package(self, package):
        package_update_url: str = self.__ckan_url + self.__action_api_path + 'package_update'
        json_response: json = self.post_something(package_update_url, package.to_dict(self.__ckan_organization_id))
        if json_response['success']:
            logger.info(f'Successfully updated package [{package.get_package_id()}]')
        else:
            logger.info(f'Error updating package [{package.get_package_id()}]')

    def delete_packages(self, package_list: PackageList) -> None:
        for package in package_list:
            self.delete_package(package)

    def delete_package(self, package):
        package_delete_url: str = self.__ckan_url + self.__action_api_path + 'package_delete'
        payload = {'id': package.get_package_id()}
        json_response = self.post_something(package_delete_url, payload)
        if json_response['success']:
            logger.info(f"Existing package [{package.get_package_id()}] successfully deleted")
        else:
            logger.info(f'Error deleting package [{package.get_package_id()}]')

    def get_something(self, url: str) -> json:
        logger.info(f'Getting something from CKAN {url}')
        response = requests.request("GET", url, headers=self.__headers)
        data = response.text
        return json.loads(data)

    def post_something(self, url: str, data) -> json:
        logger.info(f'Posting data to CKAN {url}')
        response = requests.request("POST", url, headers=self.__headers, data=data)
        response_data = response.text
        return json.loads(response_data)
