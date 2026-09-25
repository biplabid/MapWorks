import osmnx as ox
import json
import os

output_filename = "arunachal_district_boundary.geojson"

# List of districts in Arunachal Pradesh (you can expand this list if needed)
# This list is crucial as Overpass API queries are typically by name.
# It's recommended to verify these names against OpenStreetMap for accuracy.
arunachal_districts = [
    "Anjaw, Arunachal Pradesh, India",
    "Changlang, Arunachal Pradesh, India",
    "Dibang Valley, Arunachal Pradesh, India",
    "East Kameng, Arunachal Pradesh, India",
    "East Siang, Arunachal Pradesh, India",
    "Kra Daadi, Arunachal Pradesh, India",
    "Kurung Kumey, Arunachal Pradesh, India",
    "Lohit, Arunachal Pradesh, India",
    "Longding, Arunachal Pradesh, India",
    "Lower Dibang Valley, Arunachal Pradesh, India",
    "Lower Siang, Arunachal Pradesh, India",
    "Lower Subansiri, Arunachal Pradesh, India",
    "Namsai, Arunachal Pradesh, India",
    "Papum Pare, Arunachal Pradesh, India",
    "Shi Yomi, Arunachal Pradesh, India",  # New district
    "Siang, Arunachal Pradesh, India",
    "Tawang, Arunachal Pradesh, India",
    "Tirap, Arunachal Pradesh, India",
    "Upper Siang, Arunachal Pradesh, India",
    "Upper Subansiri, Arunachal Pradesh, India",
    "West Kameng, Arunachal Pradesh, India",
    "West Siang, Arunachal Pradesh, India",
    "Kamle, Arunachal Pradesh, India"  # New district
]

# Initialize a FeatureCollection to hold all district boundaries
all_districts_geojson = {
    "type": "FeatureCollection",
    "features": []
}

# Keep track of district names already added to avoid duplicates if running multiple times
added_district_names = set()

# If the output file already exists, load its content first
if os.path.exists(output_filename):
    with open(output_filename, "r") as f:
        try:
            existing_data = json.load(f)
            if existing_data and "type" in existing_data and existing_data["type"] == "FeatureCollection":
                all_districts_geojson["features"].extend(existing_data["features"])
                for feature in existing_data["features"]:
                    if "properties" in feature and "name" in feature["properties"]:
                        added_district_names.add(feature["properties"]["name"])
                print(f"Successfully loaded existing data from '{output_filename}'.")
            else:
                print(
                    f"Warning: Existing file '{output_filename}' is not a valid FeatureCollection. It will be overwritten.")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from '{output_filename}': {e}. The file will be overwritten.")
        except Exception as e:
            print(f"An unexpected error occurred while reading '{output_filename}': {e}. The file will be overwritten.")

# Fetch data for each district
for district_name_query in arunachal_districts:
    # Extract just the district name for checking against already added names
    district_simple_name = district_name_query.split(',')[0].strip()

    if district_simple_name in added_district_names:
        print(f"Skipping '{district_simple_name}' as it's already processed or exists in the file.")
        continue

    print(f"Fetching boundary for: {district_name_query}...")
    try:
        # Use ox.geocode_to_gdf to get the administrative boundary
        # By default, it uses the Nominatim API which then queries Overpass.
        gdf = ox.geocode_to_gdf(district_name_query)

        if not gdf.empty:
            # Convert the GeoDataFrame to GeoJSON features
            # Each row in the GeoDataFrame becomes a feature in the GeoJSON.
            geojson_features = json.loads(gdf.to_json())['features']

            # Add fetched features to our main list
            all_districts_geojson['features'].extend(geojson_features)
            added_district_names.add(district_simple_name)
            print(f"Successfully fetched boundary for {district_simple_name}.")
        else:
            print(f"No boundary found for: {district_name_query}. Check spelling or OSM coverage.")

    except Exception as e:
        print(f"An error occurred while fetching {district_name_query}: {e}")
        print("Please check your internet connection or the district name's validity on OpenStreetMap.")

# Save all collected data to a single GeoJSON file
try:
    with open(output_filename, "w") as f:
        json.dump(all_districts_geojson, f, indent=2)
    print(f"\nAll fetched district boundaries have been saved to '{output_filename}'.")
except Exception as e:
    print(f"Error writing to file '{output_filename}': {e}")