import motor.motor_asyncio
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = "smart_code_reviewer"

class Database:
    client: motor.motor_asyncio.AsyncIOMotorClient = None
    db: motor.motor_asyncio.AsyncIOMotorDatabase = None

db = Database()

async def connect_to_mongo():
    try:
        db.client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
        # Send a ping to confirm a successful connection
        await db.client.admin.command('ping')
        db.db = db.client[DB_NAME]
        print(f"Successfully connected to MongoDB: {DB_NAME}")
    except Exception as e:
        print(f"Could not connect to MongoDB: {e}")
        raise e

async def close_mongo_connection():
    if db.client:
        db.client.close()
        print("MongoDB connection closed")

def get_db():
    return db.db
