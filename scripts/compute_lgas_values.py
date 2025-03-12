import json
import pandas as pd
import random

# create a dataframe of values to plot the Choropleth map for the Australian LGAs
with open('../data/processed/georef-australia-local-government-area-ids.geojson', 'r', encoding='utf-8') as f:
    data = json.load(f)

lga_ids = []
values = []

for feature in data["features"]:
    lga_ids.append(feature["id"])
    values.append(random.uniform(0, 10))

df = pd.DataFrame({
    'lga': lga_ids,
    'value': values
})

if len(lga_ids) == len(set(lga_ids)):
    print("All LGA IDs are unique.")
else:
    print("There are duplicate LGA IDs.")

print(df)

df.to_csv('../data/processed/lgas_values.csv', index=False)