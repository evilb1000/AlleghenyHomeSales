import os
import requests
import pandas as pd
from time import sleep

# === CONFIG ===
output_folder = "/Volumes/G-DRIVE ArmorATD/Python Projects/HomeSales/Data"
os.makedirs(output_folder, exist_ok=True)
output_path = os.path.join(output_folder, "allegheny_parcel_data.csv")

# === API CONFIG ===
RESOURCE_ID = "9a1c60bd-f9f7-4aba-aeb7-af8c3aaa44e5"  # Assessment dataset
API_URL = "https://data.wprdc.org/api/3/action/datastore_search"
BATCH_SIZE = 10000

# === PULL DATA IN CHUNKS ===
all_records = []
offset = 0

print("Starting download of parcel data...")

while True:
    params = {
        "resource_id": RESOURCE_ID,
        "limit": BATCH_SIZE,
        "offset": offset
    }

    print(f"Fetching rows {offset} to {offset + BATCH_SIZE}...")
    response = requests.get(API_URL, params=params)
    response.raise_for_status()
    result = response.json()["result"]
    records = result["records"]

    if not records:
        break

    all_records.extend(records)
    offset += BATCH_SIZE

    # Be kind to the API
    sleep(0.5)

print(f"Total records fetched: {len(all_records)}")

# === SAVE TO CSV ===
df = pd.DataFrame.from_records(all_records)
df.to_csv(output_path, index=False)
print(f"Saved parcel data to {output_path}")
