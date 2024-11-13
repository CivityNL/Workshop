from arcgis_for_server_harvester.src.arcgis_for_server.arcgis_for_server import ArcGISForServer
from arcgis_for_server_harvester.src.ckan.ckan import Ckan
from arcgis_for_server_harvester.src.domain.package import Package
from arcgis_for_server_harvester.src.domain.package_list import PackageList


class Harvester:
    def __init__(self, arcgis_for_server_url, ckan_url, ckan_api_token, ckan_organization_id: str) -> None:
        super().__init__()
        self.__arcgis_for_server_url = arcgis_for_server_url
        self.__ckan_url = ckan_url
        self.__ckan_api_token = ckan_api_token
        self.__ckan_organization_id = ckan_organization_id

    def run(self):
        """Source: ArcGIS for Server"""
        arcgis_for_server: ArcGISForServer = ArcGISForServer(self.__arcgis_for_server_url)

        """Target: CKAN"""
        ckan: Ckan = Ckan(self.__ckan_url, self.__ckan_api_token, self.__ckan_organization_id)

        packages_in_source: PackageList = arcgis_for_server.get_packages()
        packages_in_target: PackageList = ckan.get_packages_for_source(self.__arcgis_for_server_url)

        create_package_ids = packages_in_source.get_keys() - packages_in_target.get_keys()
        update_package_ids = packages_in_source.get_keys() & packages_in_target.get_keys()
        delete_package_ids = packages_in_target.get_keys() - packages_in_source.get_keys()

        """Create new packages which no not exist in target yet"""
        for package_id in create_package_ids:
            package: Package = packages_in_source.get_package_by_id(package_id)
            ckan.create_package(package)

        """Update packages which exist in both source and target"""
        for package_id in update_package_ids:
            package: Package = packages_in_source.get_package_by_id(package_id)
            ckan.update_package(package)

        """Delete packages which no longer exist in source"""
        for package_id in delete_package_ids:
            package: Package = packages_in_target.get_package_by_id(package_id)
            ckan.delete_package(package)
