import requests
import json
import time

# List of 8 sub-districts (circles) in Lower Siang
sub_districts = [
    "Sibe", "Kora", "Kangku", "New Seren", "Koyu", "Gensi", "Nari", "Likabali"
]

# Overpass API endpoint
OVERPASS_URL = "http://overpass-api.de/api/interpreter"

# Query template to extract administrative boundaries
query_template = """
[out:json][timeout:25];
area["name"="Lower Siang"]["admin_level"="6"]->.searchArea;
(
  relation["name"="{circle}"]["boundary"="administrative"]["admin_level"="7"](area.searchArea);
);
out geom;
"""

# Function to query and extract geometry
def get_circle_boundary(circle_name):
    query = query_template.format(circle=circle_name)
    response = requests.post(OVERPASS_URL, data={"data": query})
    if response.status_code == 200:
        data = response.json()
        for element in data.get("elements", []):
            if element["type"] == "relation" and "geometry" in element:
                return {
                    "name": circle_name,
                    "geometry": element["geometry"]
                }
    return None

# Loop through sub-districts and collect boundaries
boundaries = []
not_found = []

for circle in sub_districts:
    print(f"Querying: {circle}")
    result = get_circle_boundary(circle)
    if result:
        boundaries.append(result)
    else:
        print(f"❌ No geometry found for: {circle}")
        not_found.append(circle)
    time.sleep(2)  # Be nice to the OSM server

# Save to GeoJSON-style format
geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {"name": item["name"]},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[(point["lon"], point["lat"]) for point in item["geometry"]]]
            }
        }
        for item in boundaries if item and "geometry" in item
    ]
}

# Write to file
with open("lower_siang_circles_fixed.geojson", "w", encoding="utf-8") as f:
    json.dump(geojson, f, ensure_ascii=False, indent=2)

print("\n✅ Done.")
if not_found:
    print("⚠️ The following circles could not be found:")
    print("\n".join(not_found))
else:
    print("✅ All circles were successfully extracted.")
