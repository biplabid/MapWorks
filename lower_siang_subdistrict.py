import requests
import json
import time

sub_districts = [
    "Sibe", "Kora", "Kangku", "New Seren", "Koyu", "Gensi", "Nari", "Likabali"
]

OVERPASS_URL = "http://overpass-api.de/api/interpreter"

query_template = """
[out:json][timeout:25];
area["name"="Lower Siang"]["admin_level"="6"]->.searchArea;
(
  relation["name"="{circle}"]["boundary"="administrative"]["admin_level"="7"](area.searchArea);
);
out geom;
"""

boundaries = []
not_found = []

for circle in sub_districts:
    print(f"Querying: {circle}")
    query = query_template.format(circle=circle)
    response = requests.post(OVERPASS_URL, data={"data": query})
    if response.status_code == 200:
        data = response.json()
        found = False
        for element in data.get("elements", []):
            if element.get("type") == "relation" and "geometry" in element:
                boundaries.append({
                    "name": circle,
                    "geometry": element["geometry"]
                })
                found = True
                break
        if not found:
            print(f"❌ No geometry found for: {circle}")
            not_found.append(circle)
    else:
        print(f"❌ Error fetching {circle}: HTTP {response.status_code}")
        not_found.append(circle)
    time.sleep(2)

# Save only successfully retrieved boundaries
geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {"name": item["name"]},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[(pt["lon"], pt["lat"]) for pt in item["geometry"]]]
            }
        }
        for item in boundaries
    ]
}

with open("lower_siang_circles_fixed.geojson", "w", encoding="utf-8") as f:
    json.dump(geojson, f, ensure_ascii=False, indent=2)

print("\n✅ Done.")
if not_found:
    print("⚠️ The following circles could not be found:")
    print("\n".join(not_found))
else:
    print("✅ All circles were successfully extracted.")
