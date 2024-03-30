# query_router.py
from fastapi import APIRouter

query_router = APIRouter()

@query_router.get("/")
async def query():
    return {"message": "Query route"}

