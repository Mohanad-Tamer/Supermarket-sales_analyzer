import os
import json
import random
from datetime import datetime, timedelta

# -----------------------------
# Configuration
# -----------------------------
INPUT_DIR = "data/raw"
INPUT_FILE = "raw_products.json"

OUTPUT_DIR = "data/raw"
OUTPUT_FILE = "raw_sales_transactions.json"

print("🔄 Loading raw product data...")

try:
    # Ensure the input file exists
    input_path = os.path.join(INPUT_DIR, INPUT_FILE)

    if not os.path.exists(input_path):
        raise FileNotFoundError(
            f"Input file not found: {input_path}\n"
            "Please run data_extraction.py first."
        )

    # Load products from the extracted JSON file
    with open(input_path, "r", encoding="utf-8") as file:
        products = json.load(file)

    print(f"✅ Loaded {len(products)} products.")
    print("🚀 Generating 10,000 sales transactions...")

    large_sales_data = []

    # Generate sales over the last year
    start_date = datetime.now() - timedelta(days=365)

    for i in range(1, 10001):

        product = random.choice(products)

        quantity = random.randint(1, 5)

        random_days = random.randint(0, 365)
        random_hours = random.randint(0, 23)
        random_minutes = random.randint(0, 59)

        sale_date = start_date + timedelta(
            days=random_days,
            hours=random_hours,
            minutes=random_minutes
        )

        transaction = {
            "transaction_id": f"TXN-{100000 + i}",
            "product_id": product["id"],
            "product_title": product["title"],
            "category": product["category"],
            "brand": product.get("brand", "Unknown"),
            "unit_price": product["price"],
            "discount_percentage": product["discountPercentage"],
            "quantity_sold": quantity,
            "sale_date": sale_date.strftime("%Y-%m-%d %H:%M:%S")
        }

        large_sales_data.append(transaction)

    # Create output directory if needed
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(large_sales_data, file, indent=4, ensure_ascii=False)

    print("\n✅ Sales data generation completed successfully.")
    print(f"📦 Transactions generated: {len(large_sales_data)}")
    print(f"📂 File saved to: {output_path}")
    print("🚀 The dataset is ready for the Data Cleaning stage.")

except FileNotFoundError as e:
    print(f"❌ {e}")

except json.JSONDecodeError:
    print("❌ Failed to read the product JSON file.")

except Exception as e:
    print(f"❌ An unexpected error occurred: {e}")