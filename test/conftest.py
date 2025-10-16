import os
import pytest
from pymongo import MongoClient
from fastapi.testclient import TestClient

# ⚠️ Ajusta esta importación al lugar donde está tu app
from main import app

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
TEST_DB = os.environ.get("TEST_DB", "test_db")


@pytest.fixture(scope="session")
def mongo_client():
    client = MongoClient(MONGO_URI)
    yield client
    client.close()


@pytest.fixture(autouse=True)
def cleanup_db(mongo_client):
    """
    Antes y después de cada test limpiamos las colecciones.
    """
    db = mongo_client[TEST_DB]
    db.customers.delete_many({})
    db.cards.delete_many({})
    db.charges.delete_many({})
    yield
    db.customers.delete_many({})
    db.cards.delete_many({})
    db.charges.delete_many({})


@pytest.fixture
def client():
    """
    Cliente de pruebas para FastAPI.
    """
    with TestClient(app) as c:
        yield c
