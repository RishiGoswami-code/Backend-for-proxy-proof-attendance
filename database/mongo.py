from motor import MotorClient
from motor.motor_asyncio import AsyncIOMotorClient
import os

mongo_str = os.getenv("MONGO_URI")

client = AsyncIOMotorClient(mongo_str)


db = client["Proxy-Proof Attendance"]

student_collection = db["student"]
Teacher_collection = db["teacher"]
admin_collection = db["admin"]

