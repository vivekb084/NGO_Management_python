from fastapi import FastAPI , Request
from contextlib import asynccontextmanager
from src.core.database import Database
from src.routers import user_router  # Import the user router
from src.core.middleware import log_request_routing
import socket

# Manage database connection lifecycle
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to MongoDB
    print("🚀 Starting up and connecting to MongoDB...")
    Database.connect()
    yield
    # Shutdown: Close MongoDB connection
    print("🛑 Shutting down and closing MongoDB connection...")
    Database.close()

# Initialize FastAPI app
app = FastAPI(
    title="NGO_Managment",
    version="1.0.0",
    lifespan=lifespan
)

# Get the container's unique hostname/ID assigned by Docker
CONTAINER_ID = socket.gethostname()

# --- REGISTER ROUTERS --
app.include_router(user_router.router)
# As you build more features, just include them here:
# app.include_router(product_router.router)
# app.include_router(order_router.router)

# Register the middleware globally
app.middleware("http")(log_request_routing)

# Base route to check if server is running
@app.get("/")
def read_root():
    return {
        "message": "Hello from NGO Management API",
        "handled_by_container": CONTAINER_ID
    }