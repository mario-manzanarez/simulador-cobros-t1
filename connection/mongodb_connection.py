from fastapi import FastAPI
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb://localhost:27017"

@asynccontextmanager
async def lifespan(app: FastAPI):
    client = AsyncIOMotorClient(MONGO_URI)
    app.mongodb_client = client
    app.mongodb = client.test_db
    print("✅ MongoDB conectado")
    yield
    client.close()
    print("🛑 MongoDB cerrado")


