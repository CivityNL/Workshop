import re

import requests
import json
import logging

from ckan.ckan import Ckan
from domain.package import Package
from domain.package_list import PackageList
from domain.resource import Resource

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
            URL of the ArcGISForServer instance, without the ? and format specifiers at
            the end. Example: https://sampleserver6.arcgisonline.com/arcgis/rest/services

    Methods
    -------
    """

    def __init__(self, url: str) -> None:
        super().__init__()
        self.__url: str = url

    def get_packages(self) -> PackageList:
        """Get a list of packages provided by this ArcGIS for Server instance. This determines what the actual
        packages will look like in CKAN. """
        result: PackageList = PackageList()

        result.add_all_packages(self._get_packages_from_folder(self.__url))

        return result

    def _get_packages_from_folder(self, url: str):
        """Create packages from a folder in the ArcGIS for Server instance."""
        result: PackageList = PackageList()

        response_json = self._get_json(url + '?f=pjson')

        """Process services JSON node"""
        if 'services' in response_json:
            services_json_array = response_json['services']
            for service in services_json_array:
                service_name: str = service['name']
                service_type: str = service['type']
                if (service_type == 'FeatureServer') or (service_type == 'MapServer'):
                    # ... or GPServer or SceneServer if you want to process those as well/instead
                    service_url: str = self.__url + '/' + service_name + '/' + service_type

                    service_response_json = self._get_json(service_url + '?f=pjson')

                    """Create a package from the information from ArcGIS for Server. We don't know the package ID, 
                    which has been assigned by CKAN. We can control the package name however. So we will use that to 
                    look up the package ID if needed. """
                    package: Package = Package(None, Ckan.hash(service_url))

                    package.add_name_value('access_rights', 'http://publications.europa.eu/resource/authority/access-right/PUBLIC')
                    package.add_name_value('authority', 'http://standaarden.overheid.nl/owms/terms/Leeuwarden_(gemeente)')
                    package.add_name_value('contact_point_email', 'servicedesk@civity.nl')
                    package.add_name_value('contact_point_name', 'Servicedesk')
                    package.add_name_value('dataplatform_link_enabled', 'False')
                    package.add_name_value('donl_link_enabled', 'False')
                    package.add_name_value('geonetwork_link_enabled', 'False')
                    package.add_name_value('geoserver_link_enabled', 'False')
                    package.add_name_value('isopen', 'false')
                    package.add_name_value('language', 'http://publications.europa.eu/resource/authority/language/ENG')
                    package.add_name_value('license_id', 'notspecified')
                    package.add_name_value('metadata_language', 'http://publications.europa.eu/resource/authority/language/ENG')
                    package.add_name_value('notes', self._get_notes(service_response_json))  # Can be markdown
                    package.add_name_value('privacy_sensitive', 'onbekend')
                    package.add_name_value('private','false')
                    package.add_name_value('publisher', 'http://standaarden.overheid.nl/owms/terms/Leeuwarden_(gemeente)')
                    package.add_name_value('source', Ckan.hash(self.__url))  # Used to look-up packages in subsequent harvester runs
                    package.add_name_value('tag_string', 'Just testing, Another tag')  # Comma separated list of tags
                    package.add_name_value('theme', 'http://standaarden.overheid.nl/owms/terms/Bestuur')
                    package.add_name_value('title', service_name.replace('/', ', '))
                    package.add_name_value('type', 'dataset')
                    package.add_name_value('update_frequency', 'voortdurend geactualiseerd')
                    package.add_name_value('vermelding_type', 'geo_dataset')

                    viewer_url: str = 'https://www.arcgis.com/apps/mapviewer/index.html?url=' + service_url + '&source=sd'
                    resource: Resource = Resource(Ckan.hash(viewer_url), f'Resource for {service_url}', 'ArcGIS.com MapViewer', 'MapViewer', viewer_url)
                    package.add_resource(resource)

                    # Example image from MapServer: https://geoproxy.s-hertogenbosch.nl/ags_extern/rest/services/Externvrij/Gezondheidsvoorzieningen/MapServer/export?dpi=96&transparent=true&format=png32&layers=show%3A1%2C2&bbox=582548.0071622641%2C6742839.362952325%2C610772.3798565273%2C6753253.908056165&bboxSR=102100&imageSR=102100&size=1477%2C545&f=image

                    result.add_package(package)

        """Process folders JSON node"""
        if 'folders' in response_json:
            folders_json_array = response_json.get('folders')
            for folder in folders_json_array:
                result.add_all_packages(self._get_packages_from_folder(url + '/' + folder))

        return result

    def _get_notes(self, service_response_json: json) -> str:
        """Get notes base on service description, description and layers. The notes field in a package can contain
         markdown allowing you to apply formatting. HTML tags though will be stripped for security reasons. """
        result: str = ''

        if 'service_description' in service_response_json:
            if len(service_response_json['serviceDescription']) > 0:
                result += f'### Service description\r\n{service_response_json["serviceDescription"]}\r\n'

        if 'description' in service_response_json:
            if len(service_response_json['description']) > 0:
                result += f'### Description\r\n{service_response_json["description"]}\r\n'

        result += '### Layers'
        if 'layers' in service_response_json:
            for layer in service_response_json['layers']:
                result += f'\r\n* Name: {layer["name"]}, id: {layer["id"]}'

        return result

    def _get_json(self, url: str):
        payload = {}
        headers = {}

        logger.info(f'Getting JSON from {url} for ArcGIS for Server {self.__url}')

        response = requests.request('GET', url, headers=headers, data=payload)
        response_string: str = response.text
        response_json = json.loads(response_string)

        return response_json
