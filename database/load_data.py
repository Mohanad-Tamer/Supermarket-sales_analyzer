import pandas as pd
from sqlalchemy import create_engine
import os


# ==========================
# Read cleaned JSON data
# ==========================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

json_file = os.path.join(
    BASE_DIR,
    "data",
    "cleaned",
    "cleaned_sales_transactions.json"
)

df = pd.read_json(json_file)

print("Data loaded into pandas:")
print(df.head())


# ==========================
# MySQL connection details
# ==========================

username = "root"
password = "supermarket123"   # Change this if your MySQL password is different
host = "localhost"
port = "3306"
database = "DATA_ENG_PROJ"


# ==========================
# Create connection
# ==========================

engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
)


# ==========================
# Test connection
# ==========================

try:
    with engine.connect() as connection:
        print("Connected to MySQL successfully!")

except Exception as e:
    print("Connection failed:")
    print(e)
    exit()


# ==========================
# Load data into MySQL
# ==========================

try:
    df.to_sql(
        name="sales_transactions",
        con=engine,
        if_exists="replace",
        index=False
    )

    print("Data inserted successfully!")

except Exception as e:
    print("Error while inserting data:")
    print(e)