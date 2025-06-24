import os
import requests
import pandas as pd
from time import sleep

# === CONFIGURATION ===
output_folder = "/Volumes/G-DRIVE ArmorATD/Python Projects/HomeSales/Data"
os.makedirs(output_folder, exist_ok=True)
output_path = os.path.join(output_folder, "allegheny_home_sales.csv")

# === CKAN PAGINATION CONFIG ===
CKAN_ENDPOINT = "https://data.wprdc.org/api/3/action/datastore_search"
RESOURCE_ID = "5bbe6c55-bce6-4edb-9d04-68edeb6bf7b1"
BATCH_SIZE = 10000  # Max limit CKAN allows per request

all_records = []
offset = 0

print("Starting download...")

while True:
    params = {
        "resource_id": RESOURCE_ID,
        "limit": BATCH_SIZE,
        "offset": offset
    }

    print(f"Fetching records {offset} to {offset + BATCH_SIZE}...")
    response = requests.get(CKAN_ENDPOINT, params=params)
    response.raise_for_status()
    result = response.json()["result"]
    records = result["records"]

    if not records:
        break

    all_records.extend(records)
    offset += BATCH_SIZE

    # Safety delay to be kind to the server
    sleep(0.5)

print(f"Total records fetched: {len(all_records)}")
df = pd.DataFrame.from_records(all_records)
df.to_csv(output_path, index=False)
print(f"Saved all data to: {output_path}")
