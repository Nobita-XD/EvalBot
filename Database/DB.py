import os
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient


DB = os.environ.get("DB")
mongo_client = MongoClient(DB)
db = mongo_client.abhi
