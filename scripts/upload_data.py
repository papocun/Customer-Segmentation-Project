import os
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# Connect to MongoDB
client = MongoClient(os.getenv("MONGO_URI"))

# Create Database
db = client["customer_segmentation"]

# Create Collection
collection = db["customers"]

# Read your cleaned dataset
df = pd.read_csv("data/processed/marketing_cleaned.csv")   # <-- Change this path if needed

# Convert DataFrame to list of dictionaries
records = df.to_dict(orient="records")

# Optional: Clear old data if re-running
collection.delete_many({})

# Insert new data
collection.insert_many(records)

print(f"Uploaded {len(records)} records successfully!")