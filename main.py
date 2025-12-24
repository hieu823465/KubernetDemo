"""
Simple FastAPI application for Kubernetes deployment testing.
"""
from fastapi import FastAPI
from pydantic import BaseModel
import os
import socket
from datetime import datetime

app = FastAPI(
    title="K8s Demo API",
    description="A simple FastAPI app for testing Kubernetes deployments",
    version="1.0.0"
)


class HealthResponse(BaseModel):
    status: str
    timestamp: str
    hostname: str
    version: str


class MessageResponse(BaseModel):
    message: str
    pod_name: str
    namespace: str


@app.get("/", response_model=MessageResponse)
async def root():
    """Root endpoint - returns basic info about the running pod."""
    return MessageResponse(
        message="Hello from FastAPI on Kubernetes! 🚀",
        pod_name=os.getenv("POD_NAME", socket.gethostname()),
        namespace=os.getenv("POD_NAMESPACE", "default")
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for Kubernetes liveness probe."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        hostname=socket.gethostname(),
        version="1.0.0"
    )


@app.get("/ready", response_model=HealthResponse)
async def readiness_check():
    """Readiness check endpoint for Kubernetes readiness probe."""
    return HealthResponse(
        status="ready",
        timestamp=datetime.utcnow().isoformat(),
        hostname=socket.gethostname(),
        version="1.0.0"
    )


@app.get("/info")
async def info():
    """Returns environment information - useful for debugging K8s deployments."""
    return {
        "hostname": socket.gethostname(),
        "pod_name": os.getenv("POD_NAME", "unknown"),
        "pod_namespace": os.getenv("POD_NAMESPACE", "unknown"),
        "pod_ip": os.getenv("POD_IP", "unknown"),
        "node_name": os.getenv("NODE_NAME", "unknown"),
        "environment": os.getenv("ENVIRONMENT", "development"),
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/echo/{message}")
async def echo(message: str):
    """Echo back the message provided in the path."""
    return {
        "message": message,
        "processed_at": datetime.utcnow().isoformat(),
        "pod_name": os.getenv("POD_NAME", "unknown")
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
