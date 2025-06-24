import pandas as pd
import os

# === File paths ===
base_path = "/Volumes/G-DRIVE ArmorATD/Python Projects/HomeSales/Data"
input_path = os.path.join(base_path, "04_sf_bucketed.csv")
output_path = os.path.join(base_path, "05_with_ppsf.csv")

# === Load dataset ===
df = pd.read_csv(input_path, dtype=str, low_memory=False)
df["PRICE"] = pd.to_numeric(df["PRICE"], errors="coerce")
df["FINISHEDLIVINGAREA"] = pd.to_numeric(df["FINISHEDLIVINGAREA"], errors="coerce")

# === Calculate Price Per SF ===
df["PRICE_PER_SF"] = df["PRICE"] / df["FINISHEDLIVINGAREA"]

# === Save output ===
df.to_csv(output_path, index=False)
print(f"✅ PPSF-added data saved to: {output_path}")

# === Sanity check ===
print("\n📐 PRICE_PER_SF sample:")
print(df[["PRICE", "FINISHEDLIVINGAREA", "PRICE_PER_SF"]].head(10))
print(f"\n🔢 Total rows with PPSF: {df['PRICE_PER_SF'].notna().sum():,}")
