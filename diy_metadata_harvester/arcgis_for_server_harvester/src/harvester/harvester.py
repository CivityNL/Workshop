from arcgis_for_server.arcgis_for_server import ArcGISForServer
from ckan.ckan import Ckan
from domain.package import Package
from domain.package_list import PackageList

class Harvester:
    """
    Harvester class which connects to ArcGIS for Server and determines which packages and resources are available in
    ArcGIS for Server. It subsequently connects to CKAN to determine which packages are available in CKAN. It then
    creates three lists: (1) packages which exist in ArcGIS for Server, but not in CKAN. These must be created in CKAN.
    (2) packages which exist in both ArcGIS for Server and CKAN. These must be updated in CKAN. (3) packages which exist
    in CKAN but do not exist in ArcGIS for Server. These must be deleted from CKAN. As a final step, these changes are
    applied in CKAN.
    """

    def __init__(self, arcgis_for_server_url, ckan_url, ckan_api_token, ckan_organization_id: str) -> None:
        """Create a harvester instance"""
        super().__init__()
        self.__arcgis_for_server_url = arcgis_for_server_url
        self.__ckan_url = ckan_url
        self.__ckan_api_token = ckan_api_token
        self.__ckan_organization_id = ckan_organization_id

    def run(self):
        """Run the harvester"""

        """Source: ArcGIS for Server"""
        arcgis_for_server: ArcGISForServer = ArcGISForServer(self.__arcgis_for_server_url)

        """Target: CKAN"""
        ckan: Ckan = Ckan(self.__ckan_url, self.__ckan_api_token, self.__ckan_organization_id)

        packages_in_source: PackageList = arcgis_for_server.get_packages()
        packages_in_target: PackageList = ckan.get_packages_for_source(self.__arcgis_for_server_url)

        create_package_names = packages_in_source.get_keys() - packages_in_target.get_keys()
        update_package_names = packages_in_source.get_keys() & packages_in_target.get_keys()
        delete_package_names = packages_in_target.get_keys() - packages_in_source.get_keys()

        """Create new packages which no not exist in target yet"""
        for package_name in create_package_names:
            package_from_source: Package = packages_in_source.get_package_by_name(package_name)
            ckan.create_package(package_from_source)

        """Update packages which exist in both source and target. ArcGIS for Server (source) is not aware of the 
        package ID from CKAN (target), so the package ID must be transferred from target to source. """
        for package_name in update_package_names:
            package_from_source: Package = packages_in_source.get_package_by_name(package_name)
            package_from_target: Package = packages_in_target.get_package_by_name(package_name)
            package_from_source.set_package_id(package_from_target.get_package_id())
            ckan.update_package(package_from_source)

        """Delete packages which no longer exist in source"""
        for package_name in delete_package_names:
            package_from_target: Package = packages_in_target.get_package_by_name(package_name)
            ckan.delete_package(package_from_target)
