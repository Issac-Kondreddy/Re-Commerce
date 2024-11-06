# api_gateway/main.py
from fastapi import FastAPI, Request
import httpx
import os

app = FastAPI()

USER_SERVICE_URL = os.getenv("USER_SERVICE_URL", "http://user_service:8000")
PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://product_service:8000")
ORDER_SERVICE_URL = os.getenv("ORDER_SERVICE_URL", "http://order_service:8000")

async def forward_request(service_url, path, method="GET", **kwargs):
    async with httpx.AsyncClient() as client:
        response = await client.request(method, f"{service_url}/{path}", **kwargs)
        return response

@app.get("/api/users/{path:path}")
async def user_service_proxy(path: str, request: Request):
    response = await forward_request(USER_SERVICE_URL, path, method=request.method, params=request.query_params, json=await request.json())
    return response.json()

@app.get("/api/products/{path:path}")
async def product_service_proxy(path: str, request: Request):
    response = await forward_request(PRODUCT_SERVICE_URL, path, method=request.method, params=request.query_params, json=await request.json())
    return response.json()

@app.get("/api/orders/{path:path}")
async def order_service_proxy(path: str, request: Request):
    response = await forward_request(ORDER_SERVICE_URL, path, method=request.method, params=request.query_params, json=await request.json())
    return response.json()
