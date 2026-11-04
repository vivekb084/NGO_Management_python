from src.core.database import Database
import bcrypt

class UserService:
    def __init__(self):
        db = Database.connect()
        self.collection = db["users"]

    def hash_password(self, password: str) -> str:
        # 1. Encode password string to bytes and enforce 72-byte limit
        pwd_bytes = password.encode("utf-8")[:72]
        
        # 2. Generate a secure salt and hash the password
        hashed = bcrypt.hashpw(pwd_bytes, bcrypt.gensalt())
        
        # 3. Return as a decoded string to store safely in MongoDB
        return hashed.decode("utf-8")
    
    def create_user(self, user_data: dict):

        # Check if email already exists
        if self.collection.find_one({"email": user_data["email"]}):
            return None, "Email is already registered."

        # Hash the user's password
        user_data["password"] = self.hash_password(user_data["password"])
        # Insert user into MongoDB
        result = self.collection.insert_one(user_data)
        return str(result.inserted_id), None


    def authenticate_user(self, email: str, password: str):
        # 1. Find user by email
        user = self.collection.find_one({"email": email})
        if not user:
            return None, "Invalid email or password."
        
        # 2. Check password
        stored_hash = user["password"].encode("utf-8")
        plain_password = password.encode("utf-8")[:72]
        
        if not bcrypt.checkpw(plain_password, stored_hash):
            return None, "Invalid email or password."
        
        # 3. Return user details (excluding password)
        return {
            "user_id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"]
        }, None