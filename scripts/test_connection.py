import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

uri = os.getenv("MONGO_URI")

print(uri)

client = MongoClient(uri)

print(client.list_database_names())