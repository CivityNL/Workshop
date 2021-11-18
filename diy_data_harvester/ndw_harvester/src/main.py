from ckan.Ckan import Ckan
from domain.Situation import Situation
from harvester.Harvester import Harvester


def process_data():
    print("Begin harvesting...")

    # Include for example a timestamp in the file name if you want to keep it for future reference.
    # It is beginning to look a bit like a generic opendata.ndw.nu harvester
    harvester = Harvester('https://opendata.ndw.nu/gebeurtenisinfo.xml.gz', '/data/gebeurtenisinfo.xml') 
    situations = harvester.harvest_situations()

    ckan = Ckan('https://tst-ckan-dataplatform-nl.dataplatform.nl', '48b1a4bc-2e39-4e64-b95b-4b6d3eb69ecc')
    ckan.upsert_situations('gebeurtenisinformatie', situations)

    # TODO Delete situations which are no longer of interest
    # ckan.delete_situations(...))

    print("Harvesting finished. Processed " + str(len(situations)) + " situations.")

    return situations


def main():
    process_data()


if __name__ == "__main__":
    main()