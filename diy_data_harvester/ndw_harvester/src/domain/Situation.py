import json
from shapely.geometry import Point
from shapely import wkt
from shapely import wkb

class Situation:
    def __init__(self, situation_id, version, severity, valid_from, valid_to, causes, lon, lat):
        self.situation_id = situation_id
        self.version = version
        self.severity = severity
        self.valid_from = valid_from
        self.valid_to = valid_to
        self.causes = causes

        # Create WKT (to insert in the geom field) and WKB (to insert in the the_geom_from_wkt field) 
        # representation of the lon/lat of the situation. The the_geom_from_wkt field has been created
        # by OGR when the table was created using the CKAN datastore_create API call. 
        point = Point(lon, lat)
        self.geom = wkt.dumps(point)
        self.the_geom_from_wkt = wkb.dumps(point, hex=True, srid=4326)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def to_string(self):
        return('Situation id [{}], version [{}], severity [{}] from [{}], to [{}], cause(s) [{}], location [{} {}]'.format(
            self.situation_id, 
            self.version, 
            self.severity, 
            self.valid_from, 
            self.valid_to, 
            self.causes, 
            self.lon, 
            self.lat)
        )
