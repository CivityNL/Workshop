from arcgis_for_server_harvester.src.arcgis_for_server.arcgis_for_server import ArcGISForServer
from arcgis_for_server_harvester.src.domain.PackageList import PackageList


def do_something():
    arcgis_for_server: ArcGISForServer = ArcGISForServer('https://sampleserver6.arcgisonline.com/arcgis/rest/services')
    package_list: PackageList = arcgis_for_server.get_packages()
    for package in package_list:
        print(package.get_package_id())

if __name__ == '__main__':
    do_something()
