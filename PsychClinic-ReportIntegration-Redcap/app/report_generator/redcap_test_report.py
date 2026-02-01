#!/usr/bin/env python3
import os
import sys
import pandas as pd

# -----------------------------
# Fix Python path so 'app' can be imported from anywhere
# -----------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

print(f"Project root added to sys.path: {PROJECT_ROOT}")

try:
    from app.report_generator.Report_Generator_Sorting import create_report
    print("Successfully imported create_report!")
except ModuleNotFoundError as e:
    print("Error importing create_report:", e)
    sys.exit(1)

# -----------------------------
# Settings
# -----------------------------
save_survey_path = os.path.join(PROJECT_ROOT, "app", "report_generator")
full_csv_path = os.path.join(save_survey_path, "redcap_data.csv")
record_id_to_test = 2

print(f"Full REDCap CSV path: {full_csv_path}")

# -----------------------------
# Load CSV
# -----------------------------
if not os.path.exists(full_csv_path):
    print(f"CSV file not found at {full_csv_path}")
    sys.exit(1)

df = pd.read_csv(full_csv_path)
print(f"CSV loaded. Total records: {len(df)}")

# -----------------------------
# Filter for specific record
# -----------------------------
record_df = df[df['record_id'] == record_id_to_test]

if record_df.empty:
    print(f"No data found for record_id {record_id_to_test}")
    sys.exit(1)

record_csv_path = os.path.join(save_survey_path, f"record_{record_id_to_test}.csv")
record_df.to_csv(record_csv_path, index=False)
print(f"Filtered CSV saved at: {record_csv_path}")

# -----------------------------
# Generate report
# -----------------------------
try:
    create_report(record_csv_path)
    print(f"Test report successfully generated for record_id {record_id_to_test}")
except Exception as e:
    print(f"Error generating report: {e}")
    sys.exit(1)
