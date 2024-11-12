import base64

from cryptography.fernet import Fernet
import requests
import json
import logging

from arcgis_for_server_harvester.src.domain.Package import Package
from arcgis_for_server_harvester.src.domain.PackageList import PackageList

logger = logging.getLogger(__name__)


class ArcGISForServerException(Exception):
    """
    Exception class for exceptions raised in ArcGISForServer's.

    Attributes
    ----------


    Methods
    -------
    """

    def __init__(self, *args):
        super().__init__(*args)


class ArcGISForServer:
    """
    ArcGISForServer wrapper.

    Attributes
    ----------
        __url
            URL of the ArcGISForServer instance, without the ? and format specifiers   at the end. Example:
            https://sampleserver6.arcgisonline.com/arcgis/rest/services

    Methods
    -------
    """

    def __init__(self, url: str) -> None:
        self.__url: str = url
        self.__key = base64.urlsafe_b64encode('snetmychovcifmehoghrowib'.encode())

    """Get a list of package ID's provided by this ArcGIS for Server instance"""
    def get_packages(self) -> PackageList:
        result: PackageList = PackageList()

        payload = {}
        headers = {}

        response = requests.request('GET', self.__url + '?f=pjson', headers=headers, data=payload)
        response_string: str = response.text
        response_json = json.loads(response_string)

        """Process services JSON node"""
        services_json_array = response_json['services']
        for service in services_json_array:
            service_name = service['name']
            service_type = service['type']
            if service_type == 'MapServer':  # ... or FeatureServer or GPServer if you want to process those as well/instead
                service_url: str = self.__url + '/' + service_name + '/' + service_type

                package_id = self.encode_package_id(service_url)

                package: Package = Package(package_id)

                result.add_package(package)



        """Process folders JSON node. Create new ArcGISForServer instances"""
        # folders_json_array = response_json.get('folders')
        # for folder in folders_json_array:
        #     folder_arcgis_for_server: ArcGISForServer = ArcGISForServer(self.__url + '/' + folder)

        return result

    def get_package(self, package_id: str) -> Package:
        result: Package = Package(package_id)
        url: str = self.decode_package_id(package_id)

    """Somehow turn this mapName into a unique identifier"""
    def encode_package_id(self, package_id: str) -> str:
        return package_id.replace('https://', '').replace('/', '-')

    def decode_package_id(self, encoded_package_id: str) -> str:
        return 'https://' + encoded_package_id.replace('-', '/')