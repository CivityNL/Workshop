import argparse
import logging

# from ckan.ckan import Ckan
# from domain.package_list import PackageList
from harvester.harvester import Harvester

logging.basicConfig(filename='./arcgis_for_server_metadata_harvester.log', level=logging.INFO)

def do_something(arcgis_for_server_url: str, ckan_url: str, ckan_api_token: str, ckan_organization_id: str):
    # ckan: Ckan = Ckan(ckan_url, ckan_api_token, ckan_organization_id)
    # packages: PackageList = ckan.get_packages_for_organization(ckan_organization_id)
    # ckan.delete_packages(packages)

    harvester: Harvester = Harvester(arcgis_for_server_url, ckan_url, ckan_api_token, ckan_organization_id)
    harvester.run()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('arcgis_for_server_url')
    parser.add_argument('ckan_url')
    parser.add_argument('ckan_api_token')
    parser.add_argument('ckan_organization_id')

    args = parser.parse_args()

    do_something(args.arcgis_for_server_url, args.ckan_url, args.ckan_api_token, args.ckan_organization_id)
