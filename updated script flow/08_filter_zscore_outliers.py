import pandas as pd
import os

# === File paths ===
base_path = "/Volumes/G-DRIVE ArmorATD/Python Projects/HomeSales/Data"
input_path = os.path.join(base_path, "07_with_zscores.csv")
output_path = os.path.join(base_path, "08_zfiltered_output.csv")

# === Load data ===
df = pd.read_csv(input_path, dtype=str, low_memory=False)

# === Clean columns ===
df["Z_SCORE"] = pd.to_numeric(df["Z_SCORE"], errors="coerce")
df["SALEDESC"] = df["SALEDESC"].str.strip().str.upper()
df["TIME_BAND"] = df["TIME_BAND"].str.strip()

# === Initialize Z_PASS column ===
df["Z_PASS"] = False

# === VALID SALE always passes ===
df.loc[df["SALEDESC"] == "VALID SALE", "Z_PASS"] = True

# === SALE NOT ANALYZED passes only if Z between -2 and 2, PER TIME BAND ===
banded = df[df["SALEDESC"] == "SALE NOT ANALYZED"].copy()

for band in df["TIME_BAND"].dropna().unique():
    band_mask = (df["TIME_BAND"] == band) & (df["SALEDESC"] == "SALE NOT ANALYZED")
    df.loc[band_mask & (df["Z_SCORE"] > -2) & (df["Z_SCORE"] < 2), "Z_PASS"] = True

# === Save output ===
df.to_csv(output_path, index=False)
print(f"✅ Z-filtered dataset saved to: {output_path}")

# === Count breakdown ===
total_rows = len(df)
valid_sales = (df["SALEDESC"] == "VALID SALE").sum()
not_analyzed_total = (df["SALEDESC"] == "SALE NOT ANALYZED").sum()
not_analyzed_kept = ((df["SALEDESC"] == "SALE NOT ANALYZED") & (df["Z_PASS"])).sum()
not_analyzed_cut = not_analyzed_total - not_analyzed_kept
total_passed = df["Z_PASS"].sum()

print("\n📊 Z-Score Filtering Summary:")
print(f"🔢 Total rows processed:           {total_rows:,}")
print(f"✅ VALID SALE (auto-passed):       {valid_sales:,}")
print(f"📉 SALE NOT ANALYZED (total):      {not_analyzed_total:,}")
print(f"    └── Kept (Z_PASS=True):        {not_analyzed_kept:,}")
print(f"    └── Dropped (Z too extreme):   {not_analyzed_cut:,}")
print(f"\n🎯 Final dataset size:             {total_passed:,}")
