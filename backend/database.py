from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

# existing collections
students_collection = db["students"]
videos_collection = db["videos"]
evaluations_collection = db["evaluations"]
tasks_collection = db["tasks"]

# 🔥 NEW SAAS COLLECTIONS
users_collection = db["users"]
submissions_collection = db["submissions"]