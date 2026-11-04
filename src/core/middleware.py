import socket
from fastapi import Request

CONTAINER_ID = socket.gethostname()

async def log_request_routing(request: Request, call_next):
    proxy_used = request.headers.get("x-proxy-used", "FALSE")
    upstream_target = request.headers.get("x-upstream-server", "Direct / Unknown")
    
    print(f"📥 [REQUEST ARRIVED]")
    print(f"   -> Handled by Container ID: {CONTAINER_ID}")
    print(f"   -> Reverse Proxy (Nginx) Used?: {proxy_used}")
    print(f"   -> Path: {request.url.path}")
    print(f"   -> Nginx Upstream Route: {upstream_target}")
    
    response = await call_next(request)
    return response