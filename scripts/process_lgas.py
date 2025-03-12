import json

# add ID field (LGA_CODE) to the LGAs geojson file

with open('../data/raw/georef-australia-local-government-area.geojson', "r", encoding="utf-8") as f:
    data = json.load(f)

for feature in data["features"]:
    feature["id"] = feature["properties"]['lga_code'][0]


with open('../data/processed/georef-australia-local-government-area-ids.geojson', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)


print(json.dumps(data["features"][0], indent=8))
