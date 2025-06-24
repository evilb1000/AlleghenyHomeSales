import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
plt.switch_backend('tkagg')

# === Load data ===
file_path = "/Volumes/G-DRIVE ArmorATD/Python Projects/HomeSales/Data/09_final_cleaned_sales.csv"
df = pd.read_csv(file_path, low_memory=False)

# === Normalize columns ===
df["MUNIDESC"] = df["MUNIDESC"].astype(str).str.strip()
df["SALEDATE"] = pd.to_datetime(df["SALEDATE"], errors="coerce")
df = df[df["SALEDATE"].notna()]

# === Monthly grouping ===
df["MONTH"] = df["SALEDATE"].dt.to_period("M").dt.to_timestamp()

# ✅ Filter for 2025 only
df = df[df["MONTH"].dt.year == 2025]

# === Clean price column ===
df["PRICE_PER_SF"] = pd.to_numeric(df["PRICE_PER_SF"], errors="coerce")

# === Aggregate ===
grouped = df.groupby(["MUNIDESC", "MONTH"]).agg(
    SALE_COUNT=("PRICE_PER_SF", "count"),
    AVG_PPSF=("PRICE_PER_SF", "mean")
).reset_index()

# === Top metros ===
top_metros = grouped.groupby("MUNIDESC")["SALE_COUNT"].sum().nlargest(5).index.tolist()
df_top = grouped[grouped["MUNIDESC"].isin(top_metros)].copy()

# === Pivot tables ===
sales_pivot = df_top.pivot(index="MONTH", columns="MUNIDESC", values="SALE_COUNT").sort_index()
ppsf_pivot = df_top.pivot(index="MONTH", columns="MUNIDESC", values="AVG_PPSF").reindex(sales_pivot.index)

# === Plot ===
fig, ax1 = plt.subplots(figsize=(14, 7))
bar_width = 0.08
x_base = list(range(len(sales_pivot.index)))
num_metros = len(sales_pivot.columns)

# === Plot grouped bars ===
for i, metro in enumerate(sales_pivot.columns):
    offset = (i - num_metros / 2) * bar_width + bar_width / 2
    bar_positions = [x + offset for x in x_base]
    ax1.bar(bar_positions, sales_pivot[metro], width=bar_width, alpha=0.7, label=metro)

# === X-axis: only 2025 month labels, one per cluster center ===
month_labels = sales_pivot.index.strftime("%b %Y")
ax1.set_xticks(x_base)
ax1.set_xticklabels(month_labels, rotation=45)
ax1.set_xlabel("Month", fontsize=12)
ax1.set_ylabel("Sale Count", fontsize=12)
ax1.grid(axis="y", linestyle="--", alpha=0.5)

# === PPSF overlay ===
ax2 = ax1.twinx()
for metro in ppsf_pivot.columns:
    ax2.plot(x_base, ppsf_pivot[metro], marker="o", label=metro)

ax2.set_ylabel("Avg PPSF ($)", fontsize=12)

# === Style both Y-axes ===
ax1.tick_params(axis='y', labelsize=10, labelcolor='black')
ax2.tick_params(axis='y', labelsize=10, labelcolor='black')

for label in ax1.get_yticklabels():
    label.set_fontweight('bold')

for label in ax2.get_yticklabels():
    label.set_fontweight('bold')

ax2.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"${x:,.0f}"))

# === Shared legend ===
lines, labels = ax2.get_legend_handles_labels()
fig.legend(lines, labels, loc="lower right", bbox_to_anchor=(0.75, 0.01), fontsize=9, ncol=len(labels))

# === Title + layout ===
fig.suptitle("Top 5 Metros (2025): Monthly Sale Count vs. Price per SF", fontsize=16, fontweight="bold")
plt.tight_layout()

# === Maximize window (Mac) ===
figManager = plt.get_current_fig_manager()
figManager.resize(1600, 900)

plt.show()
