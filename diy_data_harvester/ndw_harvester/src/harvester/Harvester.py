import gzip
from os import path
import urllib.request
import xml.etree.ElementTree as ET

from domain.Situation import Situation

class Harvester:
    def __init__(self, url, file):
        self.url = url
        self.file = file
    
    def harvest_situations(self):
        self.download_data()
        result = self.parse_data()
        return result

    def download_data(self):
        with urllib.request.urlopen(self.url) as response:
            with gzip.GzipFile(fileobj=response) as uncompressed:
                file_content = uncompressed.read()

        with open(self.file, 'wb') as f:
            f.write(file_content)

    def parse_data(self):
        result = []

        root = ET.parse(self.file).getroot()

        situation_nodes = root.findall('{http://schemas.xmlsoap.org/soap/envelope/}Body/{http://datex2.eu/schema/2/2_0}d2LogicalModel/{http://datex2.eu/schema/2/2_0}payloadPublication/{http://datex2.eu/schema/2/2_0}situation')

        for situation_node in situation_nodes:
            result.append(self.process_situation(situation_node))

        return result            

    def process_situation(self, situation_node):
        severity = situation_node.find('{http://datex2.eu/schema/2/2_0}overallSeverity').text

        situtation_record = situation_node.find('{http://datex2.eu/schema/2/2_0}situationRecord')

        start_time = None
        end_time = None
        validity_time_specification_node = situtation_record.find('{http://datex2.eu/schema/2/2_0}validity/{http://datex2.eu/schema/2/2_0}validityTimeSpecification')
        if validity_time_specification_node is not None:
            start_time = self.get_node_text(validity_time_specification_node, '{http://datex2.eu/schema/2/2_0}overallStartTime')
            end_time = self.get_node_text(validity_time_specification_node, '{http://datex2.eu/schema/2/2_0}overallEndTime')

        causes = ''
        cause_description_values_node = situtation_record.find('{http://datex2.eu/schema/2/2_0}cause/{http://datex2.eu/schema/2/2_0}causeDescription/{http://datex2.eu/schema/2/2_0}values')
        if cause_description_values_node is not None:
            value_nodes = cause_description_values_node.findall('{http://datex2.eu/schema/2/2_0}value')
            for i in range(0, len(value_nodes)):
                causes += value_nodes[i].text
                if i < len(value_nodes) - 1:
                    causes += ';'

        lon = 0.0
        lat = 0.0
        location_for_display_node = situtation_record.find('{http://datex2.eu/schema/2/2_0}groupOfLocations/{http://datex2.eu/schema/2/2_0}locationForDisplay')
        if location_for_display_node is not None:
            lon = float(location_for_display_node.find('{http://datex2.eu/schema/2/2_0}longitude').text)
            lat = float(location_for_display_node.find('{http://datex2.eu/schema/2/2_0}latitude').text)

        situation = Situation(
            situation_node.get('id'),
            situation_node.get('version'),
            severity,
            start_time,
            end_time,
            causes,
            lon,
            lat
        )

        return situation


    def get_node_text(self, node, path):
        result = None

        child_node = node.find(path)
        if child_node is not None:
            result = child_node.text

        return result
