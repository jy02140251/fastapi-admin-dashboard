"""
Authentication API Tests.

Tests for user registration, login, and profile endpoints
using pytest-asyncio and httpx for async HTTP testing.
"""

import pytest
from httpx import AsyncClient, ASGITransport

from main import app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client():
    """Create an async test client."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.anyio
async def test_health_check(client: AsyncClient):
    """Test the health check endpoint returns 200."""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


@pytest.mark.anyio
async def test_register_user(client: AsyncClient):
    """Test user registration with valid data."""
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "SecureP@ss123",
        "full_name": "Test User",
    }
    response = await client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "password" not in data


@pytest.mark.anyio
async def test_login_success(client: AsyncClient):
    """Test login with valid credentials returns tokens."""
    # Register first
    await client.post("/api/v1/auth/register", json={
        "username": "logintest",
        "email": "login@example.com",
        "password": "TestP@ss456",
    })

    # Login
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "logintest", "password": "TestP@ss456"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.anyio
async def test_login_invalid_credentials(client: AsyncClient):
    """Test login with invalid credentials returns 401."""
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "nonexistent", "password": "wrongpass"},
    )
    assert response.status_code == 401


@pytest.mark.anyio
async def test_get_profile_unauthorized(client: AsyncClient):
    """Test accessing profile without token returns 401."""
    response = await client.get("/api/v1/auth/me")
    assert response.status_code == 401