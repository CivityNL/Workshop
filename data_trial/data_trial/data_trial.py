import logging
import glob
import os

from data_trial.ckan.ckan import CKAN

logger = logging.getLogger(__name__)


class DataTrial:

    def __init__(self, ckan_url:str, ckan_api_token: str, ckan_package_id: str):
        super().__init__()
        self.__ckan = CKAN(ckan_url, ckan_api_token)
        self.__package_id = ckan_package_id
        self.__package_id = ckan_package_id

    def upload_csv_files(self):
        logger.info('Uploading CSV files...')
        if self.__ckan.package_exists(self.__package_id):
            logger.info(f'Package {self.__package_id} exists. Continue...')
            csv_files = self.list_files('./data/', '.csv')
            for resource_id in csv_files:
                csv_file_name = csv_files[resource_id]
                logger.info(f'Uploading CSV file [{csv_file_name}]...')
                self.upload_csv_file(
                    resource_id,
                    csv_file_name,
                    self.get_title(csv_file_name),
                    self.get_description(csv_file_name)
                )
        else:
            logger.info(f'Package {self.__package_id} does not exist. Cannot continue.')

    def upload_csv_file(self, resource_id: str, file_name: str, title: str, description: str):
        self.__ckan.delete_resource_if_exists(resource_id)

        payload = {
            'package_id': self.__package_id,
            'id': resource_id,
            'description': description,
            'format': 'CSV',
            'layer_extent': '[482.06, 306602.42, 284182.97, 637049.52]',
            'layer_srid': 28992,
            'name': title
        }

        self.__ckan.create_resource(file_name, payload)

    def upload_xlsx_files(self):
        logger.info('Uploading XLSX files...')
        if self.__ckan.package_exists(self.__package_id):
            logger.info(f'Package {self.__package_id} exists. Continue...')
            xlsx_files = self.list_files('./data/', '.xlsx')
            for resource_id in xlsx_files:
                xlsx_file_name = xlsx_files[resource_id]
                logger.info(f'Uploading CSV file [{xlsx_file_name}]...')
                self.upload_xlsx_file(
                    resource_id,
                    xlsx_file_name,
                    self.get_title(xlsx_file_name),
                    self.get_description(xlsx_file_name)
                )
        else:
            logger.info(f'Package {self.__package_id} does not exist. Cannot continue.')

    def upload_xlsx_file(self, resource_id: str, file_name: str, title: str, description: str):
        self.__ckan.delete_resource_if_exists(resource_id)

        payload = {
            'package_id': self.__package_id,
            'id': resource_id,
            'description': description,
            'format': 'XLSX',
            'layer_extent': '[482.06, 306602.42, 284182.97, 637049.52]',
            'layer_srid': 28992,
            'name': title
        }

        self.__ckan.create_resource(file_name, payload)

    def upload_shape_zip_files(self):
        logger.info('Uploading shape/zip files...')
        if self.__ckan.package_exists(self.__package_id):
            logger.info(f'Package {self.__package_id} exists. Continue...')
            shape_zip_files = self.list_files('./data/', '.zip')
            for resource_id in shape_zip_files:
                shape_zip_file_name = shape_zip_files[resource_id]
                logger.info(f'Uploading shape/zip file [{shape_zip_file_name}]...')
                self.upload_shape_zip_file(
                    resource_id,
                    shape_zip_file_name,
                    self.get_title(shape_zip_file_name),
                    self.get_description(shape_zip_file_name)
                )
        else:
            logger.info(f'Package {self.__package_id} does not exist. Cannot continue.')

    def upload_shape_zip_file(self, resource_id: str, file_name: str, title: str, description: str):
        self.__ckan.delete_resource_if_exists(resource_id)

        payload = {
            'package_id': self.__package_id,
            'id': resource_id,
            'description': description,
            'format': 'SHAPE/ZIP',
            'name': title
        }

        self.__ckan.create_resource(file_name, payload)

    def upload_gpkg_files(self):
        logger.info('Uploading GeoPackage files...')
        if self.__ckan.package_exists(self.__package_id):
            logger.info(f'Package {self.__package_id} exists. Continue...')
            gpkg_files = self.list_files('./data/', '.gpkg')
            for resource_id in gpkg_files:
                gpkg_file_name = gpkg_files[resource_id]
                logger.info(f'Uploading GeoPackage file [{gpkg_file_name}]...')
                self.upload_gpkg_file(
                    resource_id,
                    gpkg_file_name,
                    self.get_title(gpkg_file_name),
                    self.get_description(gpkg_file_name)
                )
        else:
            logger.info(f'Package {self.__package_id} does not exist. Cannot continue.')

    def upload_gpkg_file(self, resource_id: str, file_name: str, title: str, description: str):
        self.__ckan.delete_resource_if_exists(resource_id)

        payload = {
            'package_id': self.__package_id,
            'id': resource_id,
            'description': description,
            'format': 'GPKG',
            'name': title
        }

        self.__ckan.create_resource(file_name, payload)

    def upload_geojson_files(self):
        logger.info('Uploading GeoJSON files...')
        if self.__ckan.package_exists(self.__package_id):
            logger.info(f'Package {self.__package_id} exists. Continue...')

            json_files = self.list_files('./data/', '.json')
            self.do_upload_geojson_files(json_files)

            geojson_files = self.list_files('./data/', '.geojson')
            self.do_upload_geojson_files(geojson_files)
        else:
            logger.info(f'Package {self.__package_id} does not exist. Cannot continue.')

    def do_upload_geojson_files(self, json_files):
        for resource_id in json_files:
            json_file_name = json_files[resource_id]
            logger.info(f'Uploading GeoJSON file [{json_file_name}]...')
            self.upload_geojson_file(
                resource_id,
                json_file_name,
                self.get_title(json_file_name),
                self.get_description(json_file_name)
            )

    def upload_geojson_file(self, resource_id: str, file_name: str, title: str, description: str):
        self.__ckan.delete_resource_if_exists(resource_id)

        payload = {
            'package_id': self.__package_id,
            'id': resource_id,
            'description': description,
            'format': 'GEOJSON',
            'name': title
        }

        self.__ckan.create_resource(file_name, payload)

    def delete_packages(self, query: str | None):
        self.__ckan.delete_packages(query)

    def list_files(self, path: str, extension: str):
        result = {}

        for root, dirs_list, files_list in os.walk(path):
            for file_name in files_list:
                if os.path.splitext(file_name)[-1] == extension:
                    file_name_path = os.path.join(root, file_name)
                    result[file_name.replace('-', '_').replace('.', '_')] = file_name_path

        return result

    def get_title(self, data_file_name) -> str:
        return self.get_text_from_file(data_file_name, 'title')

    def get_description(self, data_file_name) -> str:
        return self.get_text_from_file(data_file_name, 'description')

    def get_text_from_file(self, data_file_name, extension):
        result: str = 'undefined'
        title_file_name = data_file_name + '.' + extension
        if os.path.isfile(title_file_name):
            file = open(title_file_name, 'r', encoding='utf-8')
            result = file.read()
        return result
