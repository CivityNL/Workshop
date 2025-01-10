import argparse
import logging

from data_trial.data_trial import DataTrial

logging.basicConfig(filename='./data_trial.log', level=logging.INFO)
logger = logging.getLogger(__name__)


def do_something(ckan_url, ckan_api_token):
    data_trial: DataTrial = DataTrial(ckan_url, ckan_api_token, 'data-trial')
    data_trial.upload_csv_files()
    data_trial.upload_gpkg_files()
    data_trial.upload_xlsx_files()
    data_trial.upload_geojson_files()
    data_trial.upload_shape_zip_files()
    # data_trial.delete_packages('id:(data-trial)')
    # data_trial.delete_packages(None)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("ckan_url")
    parser.add_argument("ckan_api_token")

    args = parser.parse_args()

    do_something(args.ckan_url, args.ckan_api_token)
