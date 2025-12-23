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