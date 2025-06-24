import pandas as pd
import os

# === File paths ===
base_path = "/Volumes/G-DRIVE ArmorATD/Python Projects/HomeSales/Data"
input_path = os.path.join(base_path, "02_linked_strict.csv")
output_path = os.path.join(base_path, "03_filtered_sales.csv")

# === Load data ===
df = pd.read_csv(input_path, dtype=str, low_memory=False)

# === Normalize SALEDESC ===
df["SALEDESC"] = df["SALEDESC"].str.strip().str.upper()

# === Filter to valid and analyzable sales ===
keep_sales = ["VALID SALE", "SALE NOT ANALYZED"]
filtered = df[df["SALEDESC"].isin(keep_sales)].copy()

# === Normalize and filter by property class ===
filtered["CLASSDESC"] = filtered["CLASSDESC"].str.strip().str.upper()
filtered = filtered[filtered["CLASSDESC"] == "RESIDENTIAL"]

# === Normalize and filter by structure type ===
valid_usedesc = [
    "SINGLE FAMILY", "TWO FAMILY",
    "TOWNHOUSE", "ROWHOUSE", "CONDOMINIUM"]

filtered["USEDESC"] = filtered["USEDESC"].str.strip().str.upper()
filtered = filtered[filtered["USEDESC"].isin(valid_usedesc)]

# === Save cleaned output ===
filtered.to_csv(output_path, index=False)
print(f"✅ Filtered residential unit sales saved to: {output_path}")

# === Preview ===
print("\n🧾 Preview of filtered data:")
print(filtered[["SALEDATE", "PARID", "PRICE", "SALEDESC", "CLASSDESC", "USEDESC"]].head(10))
print(f"\n🔢 Total filtered rows: {len(filtered):,}")
