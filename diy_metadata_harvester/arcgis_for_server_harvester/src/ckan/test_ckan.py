from unittest import TestCase

from arcgis_for_server_harvester.src.ckan.ckan import Ckan


class TestCkan(TestCase):

    def test_encode(self):
        input_string: str = 'https://sampleserver6.arcgisonline.com/arcgis/rest/services/Earthquakes_Since1970/MapServer'

        encoded: str = Ckan.encode(input_string)

        print(encoded)

        decoded: str = Ckan.decode(encoded.encode())

        print(decoded)

        if decoded != input_string:
            self.fail()
