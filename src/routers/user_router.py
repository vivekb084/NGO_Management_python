from fastapi import APIRouter, HTTPException, status
from src.models.user_model import UserCreate, UserLogin
from src.services.user_service import UserService

# Create a router instance with a common prefix and tag for Swagger docs
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate):
    user_service = UserService()
    
    # Convert Pydantic model to dictionary
    user_data = user.model_dump()
    
    # Attempt to save user in MongoDB
    user_id, error = user_service.create_user(user_data)
    
    if error:
        raise HTTPException(status_code=400, detail=error)
        
    return {
        "message": "User registered successfully!",
        "user_id": user_id,
        "name": user.name,
        "email": user.email
        # Notice: 'password' is intentionally omitted here for security!
    }


@router.post("/login", status_code=status.HTTP_200_OK)
def login_user(credentials: UserLogin):
    user_service = UserService()
    
    # Authenticate credentials
    user_info, error = user_service.authenticate_user(credentials.email, credentials.password)
    
    if error:
        raise HTTPException(status_code=401, detail=error)
        
    return {
        "message": "Login successful!",
        "user": user_info
    }