import pandas as pd
import os

# === File paths ===
base_path = "/Volumes/G-DRIVE ArmorATD/Python Projects/HomeSales/Data"
sales_path = os.path.join(base_path, "allegheny_home_sales.csv")
parcel_path = os.path.join(base_path, "allegheny_parcel_data.csv")
output_path = os.path.join(base_path, "01_linked.csv")

# === Load sales data ===
sales = pd.read_csv(sales_path, dtype=str, low_memory=False)
sales["SALEDATE"] = pd.to_datetime(sales["SALEDATE"], errors="coerce")
sales["PRICE"] = pd.to_numeric(sales["PRICE"], errors="coerce")

# === Load parcel data (select columns only) ===
parcel_cols = [
    "PARID", "CLASS", "CLASSDESC", "LOTAREA", "USECODE", "USEDESC",
    "ROOF", "ROOFDESC", "BASEMENT", "BASEMENTDESC",
    "CONDITION", "CONDITIONDESC", "FINISHEDLIVINGAREA", "ASOFDATE"
]
parcel = pd.read_csv(parcel_path, usecols=parcel_cols, dtype=str, low_memory=False)

# === Merge sales and parcel data on PARID ===
merged = sales.merge(parcel, on="PARID", how="left")
merged["FINISHEDLIVINGAREA"] = pd.to_numeric(merged["FINISHEDLIVINGAREA"], errors="coerce")

# === Save merged dataset ===
merged.to_csv(output_path, index=False)
print(f"✅ Merged dataset saved to: {output_path}")

# === Quick sanity check ===
print("\n🧾 Preview of merged data:")
print(merged[["SALEDATE", "PARID", "PRICE", "FINISHEDLIVINGAREA"]].head(10))
print(f"\n🔢 Total rows in merged dataset: {len(merged):,}")
