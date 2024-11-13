import base64

import cryptocode
import requests
import json
import logging

from arcgis_for_server_harvester.src.ckan.ckan import Ckan
from arcgis_for_server_harvester.src.domain.package import Package
from arcgis_for_server_harvester.src.domain.package_list import PackageList

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
        super().__init__()
        self.__url: str = url
        self.__key = 'aitidfob'

    """Get a list of package with just their ID's provided by this ArcGIS for Server instance"""
    def get_packages(self) -> PackageList:
        result: PackageList = PackageList()

        response_json = self.get_json(self.__url + '?f=pjson')

        """Process services JSON node"""
        services_json_array = response_json['services']
        for service in services_json_array:
            service_name = service['name']
            service_type = service['type']
            if service_type == 'MapServer':  # ... or FeatureServer or GPServer if you want to process those as well/instead
                service_url: str = self.__url + '/' + service_name + '/' + service_type

                service_response_json = self.get_json(service_url + '?f=pjson')

                """Create a package from the information from ArcGIS for Server"""
                package: Package = Package(Ckan.hash(service_url))

                package.add_name_value('access_rights', 'http://publications.europa.eu/resource/authority/access-right/PUBLIC')
                package.add_name_value('authority', 'http://standaarden.overheid.nl/owms/terms/Leeuwarden_(gemeente)')
                package.add_name_value('contact_point_email', 'servicedesk@civity.nl')
                package.add_name_value('contact_point_name', 'Servicedesk')
                package.add_name_value('dataplatform_link_enabled', 'False')
                package.add_name_value('geonetwork_link_enabled', 'False')
                package.add_name_value('geoserver_link_enabled', 'False')
                package.add_name_value('isopen', 'false')
                package.add_name_value('language', 'http://publications.europa.eu/resource/authority/language/ENG')
                package.add_name_value('license_id', 'notspecified')
                package.add_name_value('metadata_language', 'http://publications.europa.eu/resource/authority/language/ENG')
                package.add_name_value('name', Ckan.hash(service_url))  # Used as URL as well, must be unique
                package.add_name_value('notes', f'**Service description** {service_response_json["serviceDescription"]} **Description** {service_response_json["description"]}')  # Can be markdown
                package.add_name_value('privacy_sensitive', 'onbekend')
                package.add_name_value('private','false')
                package.add_name_value('publisher', 'http://standaarden.overheid.nl/owms/terms/Leeuwarden_(gemeente)')
                package.add_name_value('source', Ckan.hash(self.__url))
                package.add_name_value('tag_string', 'Just testing')  # Comma separated list of tags
                package.add_name_value('theme', 'http://standaarden.overheid.nl/owms/terms/Bestuur')
                package.add_name_value('title', service_response_json['mapName'])
                package.add_name_value('type', 'dataset')
                package.add_name_value('update_frequency', 'voortdurend geactualiseerd')
                package.add_name_value('vermelding_type', 'geo_dataset')

                result.add_package(package)

        """Process folders JSON node. Create new ArcGISForServer instances"""
        # folders_json_array = response_json.get('folders')
        # for folder in folders_json_array:
        #     folder_arcgis_for_server: ArcGISForServer = ArcGISForServer(self.__url + '/' + folder)

        return result

    def get_json(self, url: str):
        payload = {}
        headers = {}

        response = requests.request('GET', url, headers=headers, data=payload)
        response_string: str = response.text
        response_json = json.loads(response_string)

        return response_json

    """Somehow come up with a unique identifier which can be used in URL's. Semantic key, ugly. 
    Alternative: double bookkeeping. Also not a good idea"""
    def encode_package_id(self, package_id: str) -> str:
        return cryptocode.encrypt(package_id, self.__key)

    def decode_package_id(self, encoded_package_id: str) -> str:
        return cryptocode.decrypt(encoded_package_id, self.__key)

