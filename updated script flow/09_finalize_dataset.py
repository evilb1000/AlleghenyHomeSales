import pandas as pd
import os

# === File paths ===
base_path = "/Volumes/G-DRIVE ArmorATD/Python Projects/HomeSales/Data"
input_path = os.path.join(base_path, "08_zfiltered_output.csv")
output_path = os.path.join(base_path, "09_final_cleaned_sales.csv")

# === Load dataset ===
df = pd.read_csv(input_path, dtype=str, low_memory=False)

# === Clean Z_PASS column ===
df["Z_PASS"] = df["Z_PASS"].astype(str).str.strip().str.upper()
df = df[df["Z_PASS"] == "TRUE"].copy()

# === Save final output ===
df.to_csv(output_path, index=False)
print(f"✅ Final cleaned dataset saved to: {output_path}")

# === Display final count ===
print(f"\n🎯 Final dataset size: {len(df):,} rows")
