import pandas as pd
import os

# === File paths ===
base_path = "/Volumes/G-DRIVE ArmorATD/Python Projects/HomeSales/Data"
input_path = os.path.join(base_path, "03_filtered_sales.csv")
output_path = os.path.join(base_path, "04_sf_bucketed.csv")

# === Load dataset ===
df = pd.read_csv(input_path, dtype=str, low_memory=False)
df["FINISHEDLIVINGAREA"] = pd.to_numeric(df["FINISHEDLIVINGAREA"], errors="coerce")

# === Define SF Buckets ===
bins = [0, 1000, 1500, 2000, 2500, 3000, 10000]
labels = ["0–1000", "1001–1500", "1501–2000", "2001–2500", "2501–3000", "3001+"]

# === Apply Buckets ===
df["SF_BUCKET"] = pd.cut(df["FINISHEDLIVINGAREA"], bins=bins, labels=labels, right=True)

# === Save output ===
df.to_csv(output_path, index=False)
print(f"✅ SF-bucketed data saved to: {output_path}")

# === Sanity check ===
print("\n📦 SF_BUCKET distribution:")
print(df["SF_BUCKET"].value_counts(dropna=False).sort_index())
print(f"\n🔢 Total rows bucketed: {len(df):,}")
