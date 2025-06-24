import pandas as pd
import os

# === File paths ===
input_path = "/Volumes/G-DRIVE ArmorATD/Python Projects/HomeSales/Data/09_final_cleaned_sales.csv"
output_path = "/Volumes/G-DRIVE ArmorATD/Python Projects/HomeSales/Data/data_insights/baselines/monthly_ppsf_by_usedesc_and_muni.csv"

# === Load data ===
df = pd.read_csv(input_path, parse_dates=["SALEDATE"], low_memory=False)

# === Prep ===
df["MUNIDESC"] = df["MUNIDESC"].str.strip().str.upper()
df["USEDESC"] = df["USEDESC"].str.strip().str.upper()
df["SALE_YEAR"] = df["SALEDATE"].dt.year
df["SALE_MONTH"] = df["SALEDATE"].dt.month

# Filter to valid PPSF data
df = df[df["PRICE_PER_SF"] > 0]

# === Group and summarize ===
summary = (
    df.groupby(["USEDESC", "MUNIDESC", "SALE_YEAR", "SALE_MONTH"])
    .agg(
        avg_ppsf=("PRICE_PER_SF", "mean"),
        median_ppsf=("PRICE_PER_SF", "median"),
        sale_count=("PRICE_PER_SF", "count")
    )
    .reset_index()
    .sort_values(["USEDESC", "MUNIDESC", "SALE_YEAR", "SALE_MONTH"])
)

# === Export ===
os.makedirs(os.path.dirname(output_path), exist_ok=True)
summary.to_csv(output_path, index=False)

# === Confirm sample ===
print("📊 Sample of Monthly PPSF by Unit Type and Muni:")
print(summary.head(10))
print(f"\n✅ Saved to: {output_path}")
