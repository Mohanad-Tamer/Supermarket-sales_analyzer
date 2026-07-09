import os
import json
import requests

# -----------------------------
# Configuration
# -----------------------------
API_URL = "https://dummyjson.com/products?limit=200"
OUTPUT_DIR = "data/raw"
OUTPUT_FILE = "raw_products.json"

print("🔄 Starting data extraction from the DummyJSON API...")

try:
    # Create the output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Send GET request to the API
    response = requests.get(API_URL, timeout=10)

    # Raise an exception for HTTP errors (404, 500, etc.)
    response.raise_for_status()

    # Parse the JSON response
    json_data = response.json()

    # Extract the products list
    products_list = json_data.get("products", [])

    # Validate that data was returned
    if not products_list:
        print("⚠️ No product data was returned from the API.")
        exit()

    # Define the output path
    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)

    # Save the extracted data as a JSON file
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(products_list, file, indent=4, ensure_ascii=False)

    print("\n✅ Data extraction completed successfully.")
    print(f"📦 Total products extracted: {len(products_list)}")
    print(f"📂 Raw data saved to: {output_path}")
    print("🚀 The dataset is ready for the next ETL stage: Data Cleaning.")

except requests.exceptions.Timeout:
    print("❌ Request timed out. Please try again later.")

except requests.exceptions.ConnectionError:
    print("❌ Failed to connect to the API. Please check your internet connection.")

except requests.exceptions.HTTPError as http_err:
    print(f"❌ HTTP error occurred: {http_err}")

except json.JSONDecodeError:
    print("❌ Failed to parse the JSON response from the API.")

except Exception as e:
    print(f"❌ An unexpected error occurred: {e}")