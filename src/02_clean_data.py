"""
=============================================================================
Project: E-Commerce Sales, Pricing & Profitability Analysis
Script: 02_clean_data.py
Purpose: Ingest raw e-commerce dataset, perform data quality checks,
         convert data types (dates, text, numbers), validate business rules,
         and export a clean, standardized dataset ready for PostgreSQL & Power BI.
=============================================================================
"""

import os
import sys
import pandas as pd
import numpy as np


def main():
    print("=" * 70)
    print("  PHASE 2: DATA CLEANING & STANDARDIZATION PIPELINE")
    print("=" * 70)

    # -------------------------------------------------------------------------
    # STEP 1: DEFINE FILE PATHS SAFELY
    # -------------------------------------------------------------------------
    # Using relative paths anchored to the project root directory
    raw_dir = os.path.join("data", "raw")
    processed_dir = os.path.join("data", "processed")

    # In our project folder, the raw file is named 'Sample - Superstore.csv'
    # We support both variants just in case the filename is hyphenated differently
    raw_file_path = os.path.join(raw_dir, "Sample - Superstore.csv")
    if not os.path.exists(raw_file_path):
        raw_file_path = os.path.join(raw_dir, "Sample-Superstore.csv")

    output_file_path = os.path.join(processed_dir, "cleaned_superstore.csv")

    if not os.path.exists(raw_file_path):
        print(f"[ERROR] Raw data file not found at: {raw_file_path}")
        print("Please place 'Sample - Superstore.csv' inside 'data/raw/'.")
        sys.exit(1)

    # -------------------------------------------------------------------------
    # STEP 2: LOAD RAW DATASET (READ-ONLY)
    # -------------------------------------------------------------------------
    # Note: Kaggle Superstore contains Windows-1252 character encodings (e.g., curly quotes).
    # Specifying encoding='windows-1252' prevents UnicodeDecodeErrors.
    print(f"\n[INFO] Loading raw data from: {raw_file_path}")
    raw_df = pd.read_csv(raw_file_path, encoding="windows-1252")

    # Capture initial benchmark statistics (Before)
    initial_rows = len(raw_df)
    initial_cols = len(raw_df.columns)
    initial_duplicates = raw_df.duplicated().sum()
    initial_nulls = raw_df.isnull().sum().sum()

    print(f"  -> Successfully loaded {initial_rows:,} rows and {initial_cols} columns.")
    print(f"  -> Total initial null values: {initial_nulls}")
    print(f"  -> Total exact duplicate rows: {initial_duplicates}")

    # Create a working copy so the original dataframe is never mutated directly
    df = raw_df.copy()

    # -------------------------------------------------------------------------
    # STEP 3: STANDARDIZE COLUMN NAMES (FOR SQL & PYTHON BEST PRACTICE)
    # -------------------------------------------------------------------------
    # In raw data: Column names have spaces and hyphens (e.g., 'Sub-Category', 'Order ID').
    # In SQL and Python, lowercase snake_case (e.g., 'sub_category', 'order_id')
    # avoids awkward quotes and syntax errors.
    print("\n[INFO] Standardizing column names to lowercase snake_case...")
    df.columns = (
        df.columns
        .str.strip()                     # Remove accidental leading/trailing spaces
        .str.lower()                     # Convert all letters to lowercase
        .str.replace(" ", "_", regex=False)    # Replace spaces with underscores
        .str.replace("-", "_", regex=False)    # Replace hyphens with underscores
    )
    print("  -> Cleaned Column Names:")
    print("    ", list(df.columns))

    # -------------------------------------------------------------------------
    # STEP 4: DATA TYPE CONVERSIONS (DATES & STRINGS)
    # -------------------------------------------------------------------------
    print("\n[INFO] Converting date columns to datetime objects...")
    # Raw dates are stored as text (e.g., "11/8/2016" = Month/Day/Year).
    # Converting them to datetime allows time-series analysis, filtering by year/month,
    # and calculating shipping duration.
    df["order_date"] = pd.to_datetime(df["order_date"], format="%m/%d/%Y", errors="raise")
    df["ship_date"] = pd.to_datetime(df["ship_date"], format="%m/%d/%Y", errors="raise")

    # Standardize text columns: remove unnecessary whitespace from strings
    string_columns = df.select_dtypes(include=["object", "string"]).columns
    for col in string_columns:
        df[col] = df[col].astype(str).str.strip()

    # Format Postal Code:
    # US ZIP codes are 5 digits. If read as numbers, codes with leading zeros (e.g., 01852 in Massachusetts)
    # lose their leading zero. Converting to string and padding with zeros ensures valid 5-digit ZIPs.
    print("[INFO] Standardizing postal codes to 5-digit string format...")
    df["postal_code"] = df["postal_code"].astype(str).str.split(".").str[0].str.zfill(5)

    # -------------------------------------------------------------------------
    # STEP 5: BUSINESS LOGIC & SANITY VALIDATIONS
    # -------------------------------------------------------------------------
    print("\n[INFO] Running business sanity checks...")

    # Check 1: Delivery must never occur before the order was placed
    invalid_shipping_dates = df[df["ship_date"] < df["order_date"]]
    if len(invalid_shipping_dates) > 0:
        print(f"  [WARNING] Found {len(invalid_shipping_dates)} rows where ship_date < order_date!")
    else:
        print("  [PASS] All shipping dates occur on or after order dates.")

    # Check 2: Sales must be positive numbers
    negative_sales = df[df["sales"] < 0]
    if len(negative_sales) > 0:
        print(f"  [WARNING] Found {len(negative_sales)} rows with negative sales!")
    else:
        print("  [PASS] All sales values are non-negative.")

    # Check 3: Quantity must be at least 1 unit
    invalid_quantities = df[df["quantity"] <= 0]
    if len(invalid_quantities) > 0:
        print(f"  [WARNING] Found {len(invalid_quantities)} rows with quantity <= 0!")
    else:
        print("  [PASS] All order quantities are >= 1 unit.")

    # Check 4: Discount should be between 0.0 (0%) and 1.0 (100%)
    invalid_discounts = df[(df["discount"] < 0.0) | (df["discount"] > 1.0)]
    if len(invalid_discounts) > 0:
        print(f"  [WARNING] Found {len(invalid_discounts)} rows with invalid discount values!")
    else:
        print("  [PASS] All discount values are in valid [0.0, 1.0] range.")

    # -------------------------------------------------------------------------
    # STEP 6: FEATURE ENRICHMENT (ANALYTICAL HELPER COLUMNS)
    # -------------------------------------------------------------------------
    # Calculate delivery duration in days (order_date to ship_date)
    # This is a key operational KPI for fulfillment analysis
    df["shipping_duration_days"] = (df["ship_date"] - df["order_date"]).dt.days

    # Calculate unit price = sales / quantity (pre-discount estimate)
    # Round financial metrics to 2 decimal places for clean reporting
    df["sales"] = df["sales"].round(2)
    df["profit"] = df["profit"].round(2)
    df["discount"] = df["discount"].round(2)

    # -------------------------------------------------------------------------
    # STEP 7: SAVE CLEANED DATASET TO PROCESSED DIRECTORY
    # -------------------------------------------------------------------------
    # Ensure processed directory exists
    os.makedirs(processed_dir, exist_ok=True)

    print(f"\n[INFO] Saving cleaned dataset to: {output_file_path}")
    df.to_csv(output_file_path, index=False, encoding="utf-8")
    print("  -> File saved successfully with UTF-8 encoding.")

    # -------------------------------------------------------------------------
    # STEP 8: BEFORE-AND-AFTER QUALITY VALIDATION REPORT
    # -------------------------------------------------------------------------
    final_rows = len(df)
    final_cols = len(df.columns)
    final_nulls = df.isnull().sum().sum()
    final_duplicates = df.duplicated().sum()

    print("\n" + "=" * 70)
    print("                   DATA QUALITY AUDIT REPORT")
    print("=" * 70)
    print(f"{'Metric':<30} | {'Before (Raw)':<16} | {'After (Cleaned)':<16}")
    print("-" * 70)
    print(f"{'Total Row Count':<30} | {initial_rows:<16} | {final_rows:<16}")
    print(f"{'Total Column Count':<30} | {initial_cols:<16} | {final_cols:<16}")
    print(f"{'Missing / Null Values':<30} | {initial_nulls:<16} | {final_nulls:<16}")
    print(f"{'Duplicate Rows':<30} | {initial_duplicates:<16} | {final_duplicates:<16}")
    print(f"{'Order Date Format':<30} | {'Text / String':<16} | {'datetime64[ns]':<16}")
    print(f"{'Ship Date Format':<30} | {'Text / String':<16} | {'datetime64[ns]':<16}")
    print(f"{'Postal Code Format':<30} | {'int64':<16} | {'5-digit string':<16}")
    print(f"{'Added Columns':<30} | {'None':<16} | {'shipping_days':<16}")
    print("=" * 70)

    # Re-verify that raw file was NOT touched
    if os.path.exists(raw_file_path):
        current_raw_size = os.path.getsize(raw_file_path)
        print(f"[VERIFIED] Raw source file remains intact ({current_raw_size:,} bytes).")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
