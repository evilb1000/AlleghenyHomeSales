import pandas as pd

# === File path ===
input_path = "/Volumes/G-DRIVE ArmorATD/Python Projects/HomeSales/Data/09_final_cleaned_sales.csv"

# === Load necessary columns ===
df = pd.read_csv(input_path, usecols=["MUNIDESC", "SALEDATE"], parse_dates=["SALEDATE"], low_memory=False)

# === Normalize ===
df["MUNIDESC"] = df["MUNIDESC"].str.strip().str.upper()
df["SALE_YEAR"] = df["SALEDATE"].dt.year

# === Filter to 2020–2025 inclusive ===
df_filtered = df[df["SALE_YEAR"].between(2020, 2025)]

# === Count total sales by MUNI ===
muni_counts = df_filtered["MUNIDESC"].value_counts().reset_index()
muni_counts.columns = ["MUNIDESC", "total_sales_2020_2025"]

# === Add average per year ===
muni_counts["avg_per_year"] = (muni_counts["total_sales_2020_2025"] / 6).round(2)

# === Show all rows ===
pd.set_option("display.max_rows", None)

print("🏙️ Total Sales by Municipality (2020–2025):")
print(muni_counts)
