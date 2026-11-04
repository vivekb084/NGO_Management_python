import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "")
DB_NAME = os.getenv("DB_NAME", "")

def list_database_collections():
    try:
        # Connect to MongoDB
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
        
        # Ping to ensure connection is valid
        client.admin.command('ping')
        
        # Access the database
        db = client[DB_NAME]
        
        # List all collection names in the database
        collections = db.list_collection_names()
        
        print(f"✅ Connected to Database: '{DB_NAME}'")
        print(f"📊 Found {len(collections)} collection(s) (tables):")
        
        if collections:
            for name in collections:
                print(f"   - {name}")
        else:
            print("   (No collections found yet. Insert some data to create them!)")
            
    except ConnectionFailure as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    list_database_collections()