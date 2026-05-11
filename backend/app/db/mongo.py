from pymongo import MongoClient
from app.config import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI)

db = client[DB_NAME]

users_collection = db["users"]
exams_collection = db["exams"]
students_collection = db["students"]
schemes_collection = db["schemes"]
submissions_collection = db["submissions"]
evaluations_collection = db["evaluations"]