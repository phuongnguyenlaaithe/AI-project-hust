import osmium
import geojson

class OSMHandler(osmium.SimpleHandler):
    def __init__(self, geojson_file):
        super(OSMHandler, self).__init__()
        self.geojson_file = geojson_file
        self.features = []

    def extract_address_tags(self, tags):
        housenumber = tags.get("addr:housenumber", "")
        street = tags.get("addr:street", "")
        return housenumber, street

    def decode_utf8(self, text):
        try:
            return text.encode('utf-8').decode('utf-8')
        except UnicodeDecodeError:
            return text

    def node(self, n):
        # Handle OSM nodes
        if n.location.valid():
            housenumber, street = self.extract_address_tags(n.tags)
            # Decode UTF-8 encoded characters in street name
            street = self.decode_utf8(street)
            properties = {
                "osm_id": n.id,
                "addr:housenumber": housenumber,
                "addr:street": street,
            }
            # Only add the feature if at least one of the address tags is non-empty
            if housenumber or street:
                point = {
                    "type": "Feature",
                    "properties": properties,
                    "geometry": {
                        "type": "Point",
                        "coordinates": [n.location.lon, n.location.lat],
                    },
                }
                self.features.append(point)

if __name__ == "__main__":
    input_osm_file = "data/map.osm"
    output_geojson_file = "data/map.geojson"

    handler = OSMHandler(output_geojson_file)
    handler.apply_file(input_osm_file)

    # Create GeoJSON feature collection
    feature_collection = geojson.FeatureCollection(handler.features)

    # Save GeoJSON to a file
    with open(output_geojson_file, "w", encoding="utf-8") as f:
        geojson.dump(feature_collection, f, ensure_ascii=False, indent=2)
