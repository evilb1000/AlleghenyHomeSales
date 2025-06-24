import pandas as pd
import os

# === File paths ===
base_path = "/Volumes/G-DRIVE ArmorATD/Python Projects/HomeSales/Data"
input_path = os.path.join(base_path, "05_with_ppsf.csv")
output_path = os.path.join(base_path, "06_grouped_stats.csv")

# === Define time bands ===
time_bands = {
    "2012": (2012, 2012),
    "2013_2017": (2013, 2017),
    "2018_2019": (2018, 2019),
    "2020_2022": (2020, 2022),
    "2023_2025": (2023, 2025)
}

# === Load dataset ===
df = pd.read_csv(input_path, dtype=str, low_memory=False)
df["PRICE_PER_SF"] = pd.to_numeric(df["PRICE_PER_SF"], errors="coerce")
df["SF_BUCKET"] = df["SF_BUCKET"].astype("category")
df["MUNIDESC"] = df["MUNIDESC"].str.strip().str.upper()
df["SALEDATE"] = pd.to_datetime(df["SALEDATE"], errors="coerce")
df["SALE_YEAR"] = df["SALEDATE"].dt.year

# === Compile all grouped stats ===
all_grouped = []

for label, (start, end) in time_bands.items():
    band_df = df[(df["SALE_YEAR"] >= start) & (df["SALE_YEAR"] <= end)].copy()

    grouped = band_df.groupby(["MUNIDESC", "SF_BUCKET"], observed=True).agg(
        MEAN_PPSF=("PRICE_PER_SF", "mean"),
        MEDIAN_PPSF=("PRICE_PER_SF", "median"),
        STD_PPSF=("PRICE_PER_SF", "std"),
        SAMPLE_SIZE=("PRICE_PER_SF", "count")
    ).reset_index()

    grouped["TIME_BAND"] = label
    all_grouped.append(grouped)

# === Concatenate and export ===
final_df = pd.concat(all_grouped, ignore_index=True)
final_df.to_csv(output_path, index=False)

print(f"✅ All grouped stats saved to: {output_path}")
print(f"🔢 Total rows: {len(final_df):,}")
