import pandas as pd

# === File path ===
input_path = "/Volumes/G-DRIVE ArmorATD/Python Projects/HomeSales/Data/09_final_cleaned_sales.csv"
output_path = "/Volumes/G-DRIVE ArmorATD/Python Projects/HomeSales/Data/data_insights/baselines/focused_insights/top_40_muni_price_growth.csv"

# === Load needed columns ===
df = pd.read_csv(
    input_path,
    usecols=["MUNIDESC", "SALEDATE", "PRICE_PER_SF"],
    parse_dates=["SALEDATE"],
    low_memory=False
)

# === Prep fields ===
df["MUNIDESC"] = df["MUNIDESC"].str.strip().str.upper()
df["SALE_YEAR"] = df["SALEDATE"].dt.year
df = df[(df["SALE_YEAR"] >= 2020) & (df["SALE_YEAR"] <= 2025)]
df = df[df["PRICE_PER_SF"] > 0]

# === Group: muni × year ===
grouped = (
    df.groupby(["MUNIDESC", "SALE_YEAR"])["PRICE_PER_SF"]
    .agg(avg_ppsf="mean", median_ppsf="median", sale_count="count")
    .reset_index()
)

# === Total 5-year sale counts per muni ===
total_sales = grouped.groupby("MUNIDESC")["sale_count"].sum().reset_index()
total_sales["avg_per_year"] = (total_sales["sale_count"] / 5).round(2)

# === Filter to top 40ish (avg ≥ 75/year) ===
top_munis = total_sales[total_sales["avg_per_year"] >= 75]["MUNIDESC"]

# === Focus grouped table on top munis only ===
filtered = grouped[grouped["MUNIDESC"].isin(top_munis)]

# === Pivot out 2020 and 2025 avg PPSF ===
pivot = filtered.pivot(index="MUNIDESC", columns="SALE_YEAR", values="avg_ppsf").reset_index()
pivot.columns.name = None

# Keep only munis with both 2020 and 2025 data
pivot = pivot.dropna(subset=[2020, 2025])

# === Calculate growth ===
pivot["growth_pct"] = ((pivot[2025] - pivot[2020]) / pivot[2020] * 100).round(2)
pivot = pivot.rename(columns={2020: "avg_ppsf_2020", 2025: "avg_ppsf_2025"})

# === Join back in sale totals ===
pivot = pivot.merge(total_sales[["MUNIDESC", "sale_count"]], on="MUNIDESC")

# === Sort by growth descending ===
pivot = pivot.sort_values("growth_pct", ascending=False).reset_index(drop=True)

# === Save to CSV ===
pivot.to_csv(output_path, index=False)

# === Output ===
pd.set_option("display.max_rows", None)
print("🚀 Top 40 Growth Markets (2020–2025):")
print(pivot[["MUNIDESC", "avg_ppsf_2020", "avg_ppsf_2025", "growth_pct", "sale_count"]])

# === Munhall Spotlight ===
print("\n🔍 Munhall PPSF Growth Breakdown:")
print(pivot[pivot["MUNIDESC"] == "MUNHALL"].T)
