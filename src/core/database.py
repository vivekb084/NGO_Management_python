import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "")
DB_NAME = os.getenv("DB_NAME", "")

class Database:
    client = None
    db = None

    @classmethod
    def connect(cls):
        """Establish a connection to MongoDB and return the database instance."""
        if cls.client is None:
            try:
                # Initialize client with a timeout
                cls.client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
                
                # Ping to verify connection
                cls.client.admin.command('ping')
                
                # Assign the database
                cls.db = cls.client[DB_NAME]
                print(f"✅ Successfully connected to MongoDB database: '{DB_NAME}'")
                
            except ConnectionFailure as e:
                print(f"❌ Database connection failed: {e}")
                raise e
        return cls.db

    @classmethod
    def close(cls):
        """Close the MongoDB connection gracefully."""
        if cls.client:
            cls.client.close()
            cls.client = None
            cls.db = None
            print("🔌 MongoDB connection closed.")