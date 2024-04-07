# read_data_router.py
from fastapi import APIRouter

read_data_router = APIRouter()

@read_data_router.get("/")
async def read_data():
    return {"message": "Read data route"}