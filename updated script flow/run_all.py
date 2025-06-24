import subprocess
import os
import pandas as pd

# === Base paths ===
script_dir = "/Volumes/G-DRIVE ArmorATD/Python Projects/HomeSales/updated script flow"
data_dir = "/Volumes/G-DRIVE ArmorATD/Python Projects/HomeSales/Data"

# === Script order and corresponding output files ===
steps = [
    ("01_link_parcels_to_sales.py", "01_linked.csv"),
    ("02_filter_linked_sales.py", "02_linked_strict.csv"),
    ("03_filter_clean_sales.py", "03_filtered_sales.csv"),
    ("04_add_sf_bucket.py", "04_sf_bucketed.csv"),
    ("05_add_ppsf_column.py", "05_with_ppsf.csv"),
    ("06_group_stats.py", "06_grouped_stats.csv"),          # summary stats
    ("07_add_zscores.py", "07_with_zscores.csv"),
    ("08_filter_zscore_outliers.py", "08_zfiltered_output.csv"),
    ("09_finalize_dataset.py", "09_final_cleaned_sales.csv")
]

print("👑 Running full HomeSales pipeline...\n")

for script_name, output_file in steps:
    print(f"🚦 Running {script_name} ...")
    result = subprocess.run(["python3", os.path.join(script_dir, script_name)], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"❌ {script_name} FAILED.\n")
        print(result.stderr)
        break

    print(f"✅ {script_name} completed.")

    # === Count rows if file exists ===
    output_path = os.path.join(data_dir, output_file)
    if os.path.exists(output_path):
        try:
            df = pd.read_csv(output_path, low_memory=False)
            print(f"🔢 Rows in {output_file}: {len(df):,}\n")
        except Exception as e:
            print(f"⚠️ Could not read {output_file} for row count: {e}\n")
    else:
        print(f"⚠️ Output file {output_file} not found.\n")

print("🏁 All scripts completed.")
