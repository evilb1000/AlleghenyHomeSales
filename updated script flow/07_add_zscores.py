import pandas as pd
import os

# === File paths ===
base_path = "/Volumes/G-DRIVE ArmorATD/Python Projects/HomeSales/Data"
sales_path = os.path.join(base_path, "05_with_ppsf.csv")
stats_path = os.path.join(base_path, "06_grouped_stats.csv")
output_path = os.path.join(base_path, "07_with_zscores.csv")

# === Load datasets ===
sales = pd.read_csv(sales_path, dtype=str, low_memory=False)
stats = pd.read_csv(stats_path)

# === Prep sales columns ===
sales["PRICE_PER_SF"] = pd.to_numeric(sales["PRICE_PER_SF"], errors="coerce")
sales["SF_BUCKET"] = sales["SF_BUCKET"].astype("category")
sales["MUNIDESC"] = sales["MUNIDESC"].str.strip().str.upper()
sales["SALEDATE"] = pd.to_datetime(sales["SALEDATE"], errors="coerce")
sales["SALE_YEAR"] = sales["SALEDATE"].dt.year

# === Assign TIME_BAND to each sale ===
def assign_time_band(year):
    if pd.isna(year): return None
    if year == 2012: return "2012"
    elif 2013 <= year <= 2017: return "2013_2017"
    elif 2018 <= year <= 2019: return "2018_2019"
    elif 2020 <= year <= 2022: return "2020_2022"
    elif 2023 <= year <= 2025: return "2023_2025"
    else: return None

sales["TIME_BAND"] = sales["SALE_YEAR"].apply(assign_time_band)

# === Merge on all 3 keys: MUNIDESC, SF_BUCKET, TIME_BAND ===
stats["SF_BUCKET"] = stats["SF_BUCKET"].astype("category")
stats["MUNIDESC"] = stats["MUNIDESC"].str.strip().str.upper()
merged = sales.merge(stats, on=["MUNIDESC", "SF_BUCKET", "TIME_BAND"], how="left")

# === Calculate Z-Score ===
merged["Z_SCORE"] = (merged["PRICE_PER_SF"] - merged["MEAN_PPSF"]) / merged["STD_PPSF"]

# === Save output ===
merged.to_csv(output_path, index=False)
print(f"✅ Z-score calculations saved to: {output_path}")

# === Sanity check ===
print("\n📊 Sample Z-scores:")
print(merged[["PARID", "MUNIDESC", "SF_BUCKET", "TIME_BAND", "PRICE_PER_SF", "MEAN_PPSF", "STD_PPSF", "Z_SCORE"]].head(10))
print(f"\n🔢 Total properties with Z-scores calculated: {len(merged):,}")
