import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import sys
import os


#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from app.app import app, get_db
from app.app import Base


TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

Base.metadata.create_all(bind=engine)


@pytest.mark.asyncio
async def test_register_user():
    async with AsyncClient(base_url="http://user-service:8001") as client:
        response = await client.post("/api/v1/auth/register", json={
            "login": "testuser",
            "password": "testpassword",
            "email": "testuser@example.com"
        })
        assert response.status_code == 200
        assert response.json() == {"message": "User successfully registered"}

@pytest.mark.asyncio
async def test_register_existing_user():
    async with AsyncClient(base_url="http://user-service:8001") as client:
        response = await client.post("/api/v1/auth/register", json={
            "login": "testuser",
            "password": "testpassword",
            "email": "testuser@example.com"
        })
        assert response.status_code == 400
        assert response.json() == {"detail": "Login already registered"}


@pytest.mark.asyncio
async def test_login_user():
    async with AsyncClient(base_url="http://user-service:8001") as client:
        response = await client.post("/api/v1/auth/login", json={
            "login": "testuser",
            "password": "testpassword"
        })
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_user():
    async with AsyncClient(base_url="http://user-service:8001") as client:
        response = await client.post("/api/v1/auth/login", json={
            "login": "wronguser",
            "password": "wrongpassword"
        })
        assert response.status_code == 401
        assert response.json() == {"detail": "Incorrect login or password"}


@pytest.mark.asyncio
async def test_get_profile():
    async with AsyncClient(base_url="http://user-service:8001") as client:
        login_response = await client.post("/api/v1/auth/login", json={
            "login": "testuser",
            "password": "testpassword"
        })
        token = login_response.json()["access_token"]

        profile_response = await client.get("/api/v1/users/profile", headers={
            "Authorization": f"Bearer {token}"
        })

        assert profile_response.status_code == 200
        assert profile_response.json()["login"] == "testuser"
