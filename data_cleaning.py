import os
import pandas as pd

# -----------------------------
# Configuration
# -----------------------------
INPUT_DIR = "data/raw"
OUTPUT_DIR = "data/cleaned"

INPUT_FILE = "raw_sales_transactions.json"
OUTPUT_FILE = "cleaned_sales_transactions.json"

print("🔄 Starting data cleaning process...")

try:
    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    input_path = os.path.join(INPUT_DIR, INPUT_FILE)
    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)

    # Check if the input file exists
    if not os.path.exists(input_path):
        raise FileNotFoundError(
            f"Input file not found: {input_path}\n"
            "Please run data_generation.py first."
        )

    # Load the raw sales transactions
    df = pd.read_json(input_path)

    print(f"📦 Records loaded: {len(df)}")

    initial_rows = len(df)

    # ---------------------------------
    # Data Cleaning
    # ---------------------------------

    # Remove duplicate transactions
    df.drop_duplicates(subset="transaction_id", inplace=True)

    # Remove rows with missing values in essential columns
    df.dropna(
        subset=[
            "brand",
            "category",
            "unit_price",
            "discount_percentage",
            "quantity_sold",
            "sale_date"
        ],
        inplace=True
    )

    # Remove rows where brand or category is "Unknown"
    df = df[
        (df["brand"] != "Unknown") &
        (df["category"] != "Unknown")
    ]

    # Convert numeric columns
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df["discount_percentage"] = pd.to_numeric(
        df["discount_percentage"],
        errors="coerce"
    )

    # Remove rows with invalid numeric values
    df = df.dropna(subset=["unit_price", "discount_percentage"])

    # Standardize text
    df["brand"] = df["brand"].str.strip()
    df["category"] = df["category"].str.lower().str.strip()

    # Convert dates
    df["sale_date"] = pd.to_datetime(df["sale_date"], errors="coerce")

    # Remove invalid dates
    df = df.dropna(subset=["sale_date"])

    # Remove invalid prices or quantities
    df = df[
        (df["unit_price"] > 0) &
        (df["quantity_sold"] > 0)
    ]

    removed_rows = initial_rows - len(df)

    # ---------------------------------
    # Save cleaned dataset
    # ---------------------------------

    df.to_json(
        output_path,
        orient="records",
        indent=4,
        date_format="iso"
    )

    print("\n✅ Data cleaning completed successfully.")
    print(f"🗑️ Records removed: {removed_rows}")
    print(f"📊 Clean records remaining: {len(df)}")
    print(f"📂 Clean dataset saved to: {output_path}")
    print("🚀 Dataset is ready for the Data Transformation stage.")

except FileNotFoundError as e:
    print(f"❌ {e}")

except ValueError as e:
    print(f"❌ Data format error: {e}")

except Exception as e:
    print(f"❌ An unexpected error occurred: {e}")