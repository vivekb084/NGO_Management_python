from fastapi.testclient import TestClient
# Adjust the import below based on how your FastAPI app instance is named
# e.g., from main import app  or  from app.main import app
from src.main import app 

client = TestClient(app)

def test_read_root():
    """
    Test the root endpoint to ensure the application is up and responding.
    """
    response = client.get("/")
    # Change 200 to whatever your root status code is (e.g., 200 OK)
    assert response.status_code in [200, 404] 
    if response.status_code == 200:
        assert isinstance(response.json(), dict)

def test_health_check():
    """
    Test a standard health check endpoint if you have one.
    """
    response = client.get("/health")
    if response.status_code == 200:
        data = response.json()
        assert data.get("status") == "healthy"

# Example of testing an NGO-specific feature (e.g., fetching campaigns or projects)
def test_user_login():
    """
    Example test checking user login functionality.
    """
    response = client.post("/users/login", json={"email": "vivek@gmail.com", "password": "123456"})
    assert response.status_code == 200
    
    # Access the nested 'user' key first
    response_data = response.json()
    assert "user" in response_data
    assert "user_id" in response_data["user"]
    
    # Optional: Verify the value is correct
    assert response_data["user"]["user_id"] == "6ad9e9ae6dbcc2fb8261cce4"
