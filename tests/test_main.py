"""
Tests for the FastAPI Kubernetes Demo application.
"""
import pytest
from httpx import AsyncClient, ASGITransport
from main import app


@pytest.fixture
def anyio_backend():
    return 'asyncio'


@pytest.mark.anyio
async def test_root_endpoint():
    """Test the root endpoint returns correct structure."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "pod_name" in data
    assert "namespace" in data
    assert "Kubernetes" in data["message"]


@pytest.mark.anyio
async def test_health_endpoint():
    """Test the health check endpoint."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "hostname" in data
    assert "version" in data


@pytest.mark.anyio
async def test_readiness_endpoint():
    """Test the readiness check endpoint."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/ready")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"


@pytest.mark.anyio
async def test_info_endpoint():
    """Test the info endpoint returns environment information."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/info")
    
    assert response.status_code == 200
    data = response.json()
    assert "hostname" in data
    assert "pod_name" in data
    assert "pod_namespace" in data
    assert "environment" in data
    assert "timestamp" in data


@pytest.mark.anyio
async def test_openapi_docs():
    """Test that OpenAPI docs are available."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/openapi.json")
    
    assert response.status_code == 200
    data = response.json()
    assert "info" in data
    assert data["info"]["title"] == "K8s Demo API"
