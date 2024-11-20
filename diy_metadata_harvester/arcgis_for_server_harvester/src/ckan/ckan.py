import base64
import hashlib
import json
import logging
import uuid

import requests

from domain.package import Package
from domain.package_list import PackageList
from domain.resource import Resource

logger = logging.getLogger(__name__)

class CkanException(Exception):
    """
    Exception class for exceptions raised in Ckan's.

    Attributes
    ----------


    Methods
    -------
    """

    def __init__(self, *args):
        super().__init__(*args)


class Ckan:
    """
    CKAN

    Attributes
    ----------
        __ckan_url
            URL of the CKAN instance, without the api/action part
        __headers
            Headers including the API token for the CKAN instance, from a user with sufficient privileges
        __ckan_organization_id
            ID of the organization to which the packages created will be assigned. If your harvester includes logic
            to assign packages to organizations, this organization ID will be used as the default organization for
            packages which cannot be assigned to an organization.

    Methods
    -------
    """

    def __init__(self, ckan_url: str, ckan_api_token: str, ckan_organization_id: str) -> None:
        super().__init__()
        self.__ckan_url: str = ckan_url
        self.__action_api_path: str = '/api/3/action/'
        self.__headers = {'Authorization': ckan_api_token}
        self.__ckan_organization_id: str = ckan_organization_id

    @staticmethod
    def hash(s: str) -> str:
        hex_string = hashlib.md5(s.encode("UTF-8")).hexdigest()
        result = str(uuid.UUID(hex=hex_string))
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
        """Create a package"""
        package_create_url: str = self.__ckan_url + self.__action_api_path + 'package_create'

        json_response: json = self._post_something(package_create_url, package.to_dict(self.__ckan_organization_id))

        if json_response['success']:
            logger.info(f'Successfully created package with name [{package.get_package_name()}]')
            package.set_package_id(json_response['result']['id'])
            self.create_resources(package)
        else:
            logger.info(f'Error creating package [{package.get_package_id()}]: [{json_response["error"]}]')

    def get_packages_for_source(self, arcgis_for_server_url: str) -> PackageList:
        """
        Get packages for a specific ArcGIS for Server since CKAN may also contain packages for other ArcGIS for
        Servers. To keep track of the ArcGIS for Server a package belongs to, the hashed version of the URL is stored
        in the "source" field of the package.
        """
        package_search_url: str = self.__ckan_url + self.__action_api_path + f'package_search?fl=id,name&rows=500&start=0&q=source:({Ckan.hash(arcgis_for_server_url)})'

        package_list = self._get_packages_for_query(package_search_url)

        return package_list

    def get_packages_for_organization(self, organization_id: str) -> PackageList:
        """
        Get packages for a specific organization
        """
        package_search_url: str = self.__ckan_url + self.__action_api_path + f'package_search?fl=id,name&rows=500&start=0&q=owner_org:({organization_id})'

        package_list = self._get_packages_for_query(package_search_url)

        return package_list

    def get_package_by_id(self, package_id: str) -> Package:
        """Get package by ID"""
        package: Package | None = None

        package_show_url: str = self.__ckan_url + self.__action_api_path + f'package_show?id=({package_id})'

        package = self._get_package_for_show(package_show_url)

        return package

    def get_package_by_name(self, package_name: str) -> Package:
        """
        Get package by Name
        """
        package: Package | None

        package_show_url: str = self.__ckan_url + self.__action_api_path + f'package_show?id=({package_name})'

        package = self._get_package_for_show(package_show_url)

        return package

    def update_package(self, package):
        """
        Update package.
        """
        package_update_url: str = self.__ckan_url + self.__action_api_path + 'package_update'

        json_response: json = self._post_something(package_update_url, package.to_dict(self.__ckan_organization_id))
        if json_response['success']:
            logger.info(f'Successfully updated package [{package.get_package_id()}]')
            self.create_resources(package)
        else:
            logger.info(f'Error updating package [{package.get_package_id()}]')

    def delete_packages(self, package_list: PackageList) -> None:
        """
        Delete packages in the list provided.
        """
        for package in package_list:
            self.delete_package(package)

    def delete_package(self, package):
        """
        Completely delete package. Instead of a package_delete, this method uses a dataset_purge to remove the
        entire package from the database instead of just marking it as "deleted". If a package is just marked as
        deleted, you might run into problems if a package with the same ID or name must be re-created later on.
        """
        package_delete_url: str = self.__ckan_url + self.__action_api_path + 'dataset_purge'

        payload = {'id': package.get_package_id()}

        json_response = self._post_something(package_delete_url, payload)
        if json_response['success']:
            logger.info(f'Existing package [{package.get_package_id()}] successfully deleted')
        else:
            logger.info(f'Error deleting package [{package.get_package_id()}]')

    def create_resources(self, package: Package) -> None:
        """Since we do a package create or update without resources, resources will always be non-existent after
        create or update. Use this method to create them. To know to which package a resource belongs, the package ID
        is included in the resource. Providing the resources directly in a resources array works from Postman, but not
        from the code in this project for a still unknown reason. Requires further investigation. """
        for i in range(package.num_resources()):
            resource: Resource = package.get_package_by_index(i)
            self.create_resource(package.get_package_id(), resource)

    def create_resource(self, package_id: str, resource: Resource) -> None:
        """Create a resource. Provide the ID of the package the resource belongs to. """
        resource_create_url: str = self.__ckan_url + self.__action_api_path + 'resource_create'
        json_response: json = self._post_something(resource_create_url, resource.to_dict(package_id))
        if json_response['success']:
            logger.info(f'Successfully created resource [{resource.get_resource_id()}]')
        else:
            logger.info(f'Error creating resource [{resource.get_resource_id()}]')

    def _get_package_for_show(self, package_show_url):
        package: Package | None = None

        json_response: json = self._get_something(package_show_url)

        if json_response['success']:
            logger.info(f'Successfully read package by ID or name from [{package_show_url}]')
            package_id: str = json_response['result']['id']
            package_name: str = json_response['result']['name']
            package = Package(package_id, package_name)
        else:
            logger.info(f'Error reading packages for search [{package_show_url}]')

        return package

    def _get_packages_for_query(self, package_search_url) -> PackageList:
        package_list: PackageList = PackageList()

        json_response: json = self._get_something(package_search_url)

        if json_response['success']:
            logger.info(f'Successfully read packages for search [{package_search_url}]')
            results_json_array = json_response['result']['results']
            for result in results_json_array:
                package_id: str = result['id']
                package_name: str = result['name']
                package_list.add_package(Package(package_id, package_name))
        else:
            logger.info(f'Error reading packages for search [{package_search_url}]')

        return package_list

    def _get_something(self, url: str) -> json:
        logger.info(f'Getting something from CKAN {url}')
        response = requests.request("GET", url, headers=self.__headers)
        data = response.text
        return json.loads(data)

    def _post_something(self, url: str, data) -> json:
        logger.info(f'Posting data to CKAN {url}')
        response = requests.request("POST", url, headers=self.__headers, data=data)
        response_data = response.text
        return json.loads(response_data)
