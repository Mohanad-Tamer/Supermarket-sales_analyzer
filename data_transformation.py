import os
import pandas as pd

# -----------------------------
# Configuration
# -----------------------------
INPUT_DIR = "data/cleaned"
OUTPUT_DIR = "data/processed"

INPUT_FILE = "cleaned_sales_transactions.json"
OUTPUT_FILE = "processed_sales_transactions.json"

print("🔄 Starting data transformation process...")

try:
    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    input_path = os.path.join(INPUT_DIR, INPUT_FILE)
    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)

    # Check if input file exists
    if not os.path.exists(input_path):
        raise FileNotFoundError(
            f"Input file not found: {input_path}\n"
            "Please run data_cleaning.py first."
        )

    # Load cleaned dataset
    df = pd.read_json(input_path)

    print(f"📦 Records loaded: {len(df)}")

    # -----------------------------
    # Validate required columns
    # -----------------------------
    required_columns = [
        "transaction_id",
        "unit_price",
        "discount_percentage",
        "quantity_sold",
        "sale_date"
    ]

    missing_columns = [
        col for col in required_columns if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {', '.join(missing_columns)}"
        )

    # -----------------------------
    # Convert data types
    # -----------------------------
    df["sale_date"] = pd.to_datetime(df["sale_date"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df["discount_percentage"] = pd.to_numeric(
        df["discount_percentage"],
        errors="coerce"
    )
    df["quantity_sold"] = pd.to_numeric(
        df["quantity_sold"],
        errors="coerce"
    )

    # Remove rows with invalid values
    df.dropna(
        subset=[
            "sale_date",
            "unit_price",
            "discount_percentage",
            "quantity_sold"
        ],
        inplace=True
    )

    print(f"✅ Valid records after validation: {len(df)}")

    # -----------------------------
    # Data Transformation
    # -----------------------------

    print("⚡ Calculating business metrics...")

    # Discount amount
    df["discount_amount"] = (
        df["unit_price"] *
        (df["discount_percentage"] / 100)
    ).round(2)

    # Price after discount
    df["price_after_discount"] = (
        df["unit_price"] -
        df["discount_amount"]
    ).round(2)

    # Total before discount
    df["total_price_before_discount"] = (
        df["unit_price"] *
        df["quantity_sold"]
    ).round(2)

    # Total revenue
    df["total_net_revenue"] = (
        df["price_after_discount"] *
        df["quantity_sold"]
    ).round(2)

    # -----------------------------
    # Date Dimensions
    # -----------------------------

    df["sale_year"] = df["sale_date"].dt.year
    df["sale_month"] = df["sale_date"].dt.month
    df["sale_day"] = df["sale_date"].dt.day
    df["sale_hour"] = df["sale_date"].dt.hour
    df["day_of_week"] = df["sale_date"].dt.day_name()

    # -----------------------------
    # Save transformed dataset
    # -----------------------------

    df.to_json(
        output_path,
        orient="records",
        indent=4,
        date_format="iso"
    )

    print("\n✅ Data transformation completed successfully.")
    print(f"📊 Final dataset: {len(df)} records × {len(df.columns)} columns")
    print(f"📂 Processed dataset saved to: {output_path}")
    print("🚀 Dataset is ready for database loading.")

except FileNotFoundError as e:
    print(f"❌ {e}")

except ValueError as e:
    print(f"❌ {e}")

except Exception as e:
    print(f"❌ Unexpected error: {e}")