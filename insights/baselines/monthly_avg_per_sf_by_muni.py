import pandas as pd
import os

# === Paths ===
input_path = "/Volumes/G-DRIVE ArmorATD/Python Projects/HomeSales/Data/09_final_cleaned_sales.csv"
output_path = "/Volumes/G-DRIVE ArmorATD/Python Projects/HomeSales/Data/data_insights/baselines/monthly_avg_ppsf_by_muni.csv"

# === Load data ===
df = pd.read_csv(input_path, parse_dates=["SALEDATE"], low_memory=False)

# === Clean & prep ===
df["MUNIDESC"] = df["MUNIDESC"].astype(str).str.strip().str.upper()
df["SALE_YEAR"] = df["SALEDATE"].dt.year
df["SALE_MONTH"] = df["SALEDATE"].dt.month

# Filter out junk
df = df[df["FINISHEDLIVINGAREA"] > 0]
df = df[df["PRICE_PER_SF"] > 0]

# === Group and summarize ===
summary = (
    df.groupby(["MUNIDESC", "SALE_YEAR", "SALE_MONTH"])
    .agg(
        avg_ppsf=("PRICE_PER_SF", "mean"),
        median_ppsf=("PRICE_PER_SF", "median"),
        sale_count=("PRICE_PER_SF", "count")
    )
    .reset_index()
)

# === Build full grid for all MUNI × YEAR × MONTH combos ===
all_munis = df["MUNIDESC"].unique()
all_years = df["SALE_YEAR"].unique()
all_months = range(1, 13)

full_index = pd.MultiIndex.from_product(
    [all_munis, sorted(all_years), all_months],
    names=["MUNIDESC", "SALE_YEAR", "SALE_MONTH"]
).to_frame(index=False)

# === Merge and fill ===
full_summary = pd.merge(full_index, summary, how="left", on=["MUNIDESC", "SALE_YEAR", "SALE_MONTH"])
full_summary["sale_count"] = full_summary["sale_count"].fillna(0).astype(int)

# Sort for sanity
full_summary = full_summary.sort_values(["MUNIDESC", "SALE_YEAR", "SALE_MONTH"])

# === Export ===
os.makedirs(os.path.dirname(output_path), exist_ok=True)
full_summary.to_csv(output_path, index=False)

# === Bridgeville peek ===
bridgeville = full_summary[full_summary["MUNIDESC"] == "BRIDGEVILLE"]
print("📈 Bridgeville Monthly PPSF Summary (With Gaps):")
print(bridgeville)

print(f"\n✅ Saved full monthly PPSF summary to: {output_path}")
