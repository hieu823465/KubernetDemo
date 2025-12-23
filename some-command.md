
# Install helm
winget install Helm.Helm
set env
"$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User"); helm lint ./chart"

# Some useful helm sytax:
# First, delete the existing raw YAML deployment
kubectl delete -f k8s/

# Install with default values (3 replicas)
helm install fastapi-demo ./chart

# Install for development (1 replica)
helm install fastapi-demo ./chart -f ./chart/values-dev.yaml

# Install for production (5 replicas)
helm install fastapi-demo ./chart -f ./chart/values-prod.yaml

# Override values inline
helm install fastapi-demo ./chart --set replicaCount=2

# Upgrade after changes
helm upgrade fastapi-demo ./chart

# Rollback to previous version
helm rollback fastapi-demo

# Uninstall
helm uninstall fastapi-demo



############ MINI KUBE ################

C:\minikube\minikube.exe start
C:\minikube\minikube.exe stop


# Copy image from docker desktop to minikube
C:\minikube\minikube.exe image load fastapi-demo:latest

# Build Docker image
docker build -t fastapi-demo:latest .

# Apply K8s manifests
kubectl apply -f k8s/

# Check pods
kubectl get pods -l app=fastapi-demo

# See all resources in your namespace
kubectl get all

# Point your shell to minikube's Docker daemon
& C:\minikube\minikube.exe -p minikube docker-env --shell powershell | Invoke-Expression

# get pods
kubectl get pods -l app=fastapi-demo

# Get service
kubectl get svc

# port forward
kubectl port-forward svc/fastapi-demo-service 8080:80