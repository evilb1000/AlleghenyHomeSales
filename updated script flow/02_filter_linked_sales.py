import pandas as pd
import os

# === File paths ===
base_path = "/Volumes/G-DRIVE ArmorATD/Python Projects/HomeSales/Data"
input_path = os.path.join(base_path, "01_linked.csv")
output_path = os.path.join(base_path, "02_linked_strict.csv")

# === Load linked sales dataset ===
df = pd.read_csv(input_path, dtype=str, low_memory=False)
df["FINISHEDLIVINGAREA"] = pd.to_numeric(df["FINISHEDLIVINGAREA"], errors="coerce")

# === Filter to only rows with parcel linkage ===
filtered = df[df["FINISHEDLIVINGAREA"].notna()].copy()

# === Save strictly linked dataset ===
filtered.to_csv(output_path, index=False)
print(f"✅ Strictly linked dataset saved to: {output_path}")

# === Sanity check ===
print("\n🧾 Preview of filtered linked sales:")
print(filtered[["SALEDATE", "PARID", "PRICE", "FINISHEDLIVINGAREA"]].head(10))
print(f"\n🔢 Total strictly linked rows: {len(filtered):,}")
