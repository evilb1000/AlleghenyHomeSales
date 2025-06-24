import pandas as pd
import os

# === Paths ===
input_path = "/Volumes/G-DRIVE ArmorATD/Python Projects/HomeSales/Data/09_final_cleaned_sales.csv"
output_path = "/Volumes/G-DRIVE ArmorATD/Python Projects/HomeSales/Data/data_insights/baselines/annual_sales_by_muni.csv"

# === Load data ===
df = pd.read_csv(input_path, parse_dates=["SALEDATE"], low_memory=False)

# === Clean & prepare ===
df["MUNIDESC"] = df["MUNIDESC"].astype(str).str.strip().str.upper()
df["SALE_YEAR"] = df["SALEDATE"].dt.year

# === Group by MUNI + Year ===
annual_counts = (
    df.groupby(["MUNIDESC", "SALE_YEAR"])
    .size()
    .reset_index(name="annual_sale_count")
    .sort_values(["MUNIDESC", "SALE_YEAR"])
)

# === Export ===
os.makedirs(os.path.dirname(output_path), exist_ok=True)
annual_counts.to_csv(output_path, index=False)

# === Bridgeville Check ===
bridgeville = annual_counts[annual_counts["MUNIDESC"] == "BRIDGEVILLE"]
print("📆 Bridgeville Annual Sales Count:")
print(bridgeville)

# === Total sanity check ===
total_sales = annual_counts["annual_sale_count"].sum()
print(f"\n🧮 Total sales captured across all municipalities: {total_sales:,}")

print(f"\n✅ Saved annual sales by muni to: {output_path}")
