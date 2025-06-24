import pandas as pd
import os
import itertools

# === Paths ===
input_path = "/Volumes/G-DRIVE ArmorATD/Python Projects/HomeSales/Data/09_final_cleaned_sales.csv"
output_path = "/Volumes/G-DRIVE ArmorATD/Python Projects/HomeSales/Data/data_insights/baselines/monthly_sales_by_muni.csv"

# === Load data ===
df = pd.read_csv(input_path, parse_dates=["SALEDATE"], low_memory=False)

# === Clean & prepare ===
df["MUNIDESC"] = df["MUNIDESC"].astype(str).str.strip().str.upper()
df["SALE_YEAR"] = df["SALEDATE"].dt.year
df["SALE_MONTH"] = df["SALEDATE"].dt.month

# === Actual monthly counts ===
counts = (
    df.groupby(["MUNIDESC", "SALE_YEAR", "SALE_MONTH"])
    .size()
    .reset_index(name="sale_count")
)

# === Create full combo grid ===
all_munis = df["MUNIDESC"].unique()
all_years = df["SALE_YEAR"].dropna().astype(int).unique()
all_months = range(1, 13)

full_index = pd.MultiIndex.from_product(
    [all_munis, sorted(all_years), all_months],
    names=["MUNIDESC", "SALE_YEAR", "SALE_MONTH"]
).to_frame(index=False)

# === Merge + Fill Missing ===
merged = pd.merge(full_index, counts, how="left", on=["MUNIDESC", "SALE_YEAR", "SALE_MONTH"])
merged["sale_count"] = merged["sale_count"].fillna(0).astype(int)

# === Sort & Export ===
merged = merged.sort_values(["MUNIDESC", "SALE_YEAR", "SALE_MONTH"])
os.makedirs(os.path.dirname(output_path), exist_ok=True)
merged.to_csv(output_path, index=False)

# === Bridgeville Check ===
bridgeville = merged[merged["MUNIDESC"] == "BRIDGEVILLE"]
print("📊 Bridgeville Monthly Sales Count (With Zeros):")
print(bridgeville)

print(f"\n✅ Saved complete monthly sales grid to: {output_path}")
