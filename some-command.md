
# Install helm
winget install Helm.Helm
set env
"$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User"); helm lint ./chart"

# ========== HELM CHART WORKFLOW ==========

# 1. VALIDATE CHART
# Set PATH first (if helm not recognized)
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Lint the chart
helm lint ./chart

# 2. CLEAN UP OLD DEPLOYMENTS (if switching from raw YAML)
kubectl delete -f k8s/

# 3. INSTALL WITH HELM

# Default installation (3 replicas)
helm install fastapi-demo ./chart

# Development environment (1 replica, lower resources)
helm install fastapi-demo ./chart -f ./chart/values-dev.yaml

# Production environment (5 replicas, higher resources)
helm install fastapi-demo ./chart -f ./chart/values-prod.yaml

# Override specific values
helm install fastapi-demo ./chart --set replicaCount=2
helm install fastapi-demo ./chart --set ingress.enabled=true

# 4. MANAGE DEPLOYMENTS

# List all releases
helm list

# View release status
helm status fastapi-demo

# View deployment history
helm history fastapi-demo

# Upgrade after changes
helm upgrade fastapi-demo ./chart

# Upgrade with value overrides
helm upgrade fastapi-demo ./chart --set replicaCount=5

# Rollback to previous version
helm rollback fastapi-demo

# Rollback to specific revision
helm rollback fastapi-demo 1

# 5. DEBUG AND INSPECT

# Dry run (see what would be deployed)
helm install fastapi-demo ./chart --dry-run --debug

# View current values
helm get values fastapi-demo

# View all values (including defaults)
helm get values fastapi-demo --all

# View generated manifest
helm get manifest fastapi-demo

# 6. UNINSTALL
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


############ INGRESS ################

# Enable Ingress addon in Minikube
minikube addons enable ingress

# Apply Ingress configuration
kubectl apply -f k8s/ingress.yaml

# Check Ingress status
kubectl get ingress

# IMPORTANT: To access Ingress, run this in a NEW PowerShell terminal AS ADMINISTRATOR
# Keep this terminal running while you want to access the application
minikube tunnel

# After running minikube tunnel, access your application at:
# - http://127.0.0.1 (IP-based access)
# - http://fastapi-demo.local (hostname-based, requires hosts file entry)

# Optional: Add to hosts file for hostname access
# Edit C:\Windows\System32\drivers\etc\hosts (as Administrator)
# Add this line:
# 127.0.0.1 fastapi-demo.local

# Alternative: Access via Minikube IP directly (without tunnel)
minikube ip
# Then open browser to: http://<minikube-ip>

# View Ingress details
kubectl describe ingress fastapi-demo-ingress

# Delete Ingress
kubectl delete -f k8s/ingress.yaml


# If use Ingress then first must enable it
minikube addons enable ingress