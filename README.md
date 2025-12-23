# FastAPI Kubernetes Demo

A simple FastAPI application for testing Kubernetes deployments.

## Features

- 🚀 **FastAPI** with automatic OpenAPI documentation
- 🏥 **Health & Readiness endpoints** for K8s probes
- 🐳 **Docker** containerized with security best practices
- ☸️ **Kubernetes manifests** included

## Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | Root endpoint with pod info |
| `GET /health` | Liveness probe endpoint |
| `GET /ready` | Readiness probe endpoint |
| `GET /info` | Detailed environment info |
| `GET /docs` | Swagger UI documentation |

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
# or
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Visit http://localhost:8000/docs for API documentation.

## Docker

```bash
# Build the image
docker build -t fastapi-demo:latest .

# Run the container
docker run -p 8000:8000 fastapi-demo:latest
```

## Kubernetes Deployment

```bash
# Build and load image (for local K8s like minikube/kind)
docker build -t fastapi-demo:latest .

# For minikube
eval $(minikube docker-env)
docker build -t fastapi-demo:latest .

# For kind
kind load docker-image fastapi-demo:latest

# Apply Kubernetes manifests
kubectl apply -f k8s/

# Check deployment status
kubectl get pods -l app=fastapi-demo
kubectl get svc fastapi-demo-service

# Access the service (NodePort)
# minikube: minikube service fastapi-demo-nodeport
# kind: kubectl port-forward svc/fastapi-demo-service 8000:80

# View logs
kubectl logs -l app=fastapi-demo -f
```

## Testing Load Balancing

With 3 replicas, you can test K8s load balancing:

```bash
# Run multiple requests and observe different pod names
for i in {1..10}; do curl -s http://localhost:8000/ | jq .pod_name; done
```

## Project Structure

```
KubernetesDemo/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── Dockerfile          # Container definition
├── README.md           # This file
└── k8s/
    ├── deployment.yaml # K8s Deployment
    └── service.yaml    # K8s Service
```
