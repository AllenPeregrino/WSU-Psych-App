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
single_record_csv = os.path.join(save_survey_path, "redcap_data_2.csv")

print(f"Using REDCap CSV: {single_record_csv}")

# -----------------------------
# Validate CSV exists
# -----------------------------
if not os.path.exists(single_record_csv):
    print(f"CSV file not found at {single_record_csv}")
    sys.exit(1)

# Optional sanity check (recommended)
df = pd.read_csv(single_record_csv)
print(f"CSV loaded. Rows: {len(df)}")

if len(df) != 1:
    print("⚠️ Warning: CSV contains more than one record")

# -----------------------------
# Generate report
# -----------------------------
try:
    create_report(single_record_csv)
    print("Test report successfully generated from redcap_data_2.csv")
except Exception as e:
    print(f"Error generating report: {e}")
    sys.exit(1)
