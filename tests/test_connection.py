import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "")
DB_NAME = os.getenv("DB_NAME", "")

def check_database_exists():
    try:
        # 1. Connect to MongoDB
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
        
        # 2. Test connection with ping
        client.admin.command('ping')
        print("✅ Successfully connected to MongoDB server!")
        
        # 3. Get a list of all existing database names on the server
        existing_databases = client.list_database_names()
        
        # 4. Check if our target database is in the list
        if DB_NAME in existing_databases:
            print(f"✅ Database '{DB_NAME}' exists on the server.")
        else:
            print(f"⚠️ Database '{DB_NAME}' does NOT exist yet.")
            print("   (Remember: MongoDB creates databases lazily. It will appear once you insert your first document!)")
            
    except ConnectionFailure as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    check_database_exists()