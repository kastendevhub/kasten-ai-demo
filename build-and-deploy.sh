#!/bin/bash

# Build and Deploy Animal Chat Application

set -e

echo "🐾 Building Animal Chat Application..."

# Build Docker image
echo "📦 Building Docker image..."
docker buildx build --platform=linux/arm64,linux/amd64 --pull --push -t ghcr.io/kastendevhub/animal-chat:latest .

# Apply Kubernetes manifests
echo "🚀 Deploying to Kubernetes..."
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml

# Wait for deployment
echo "⏳ Waiting for deployment to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/animal-chat-app -n qdrant

# Get service info
echo "✅ Deployment complete!"
echo ""
echo "📋 Service Information:"
kubectl get pods,svc,ingress -n qdrant -l app=animal-chat-app

echo ""
echo "🌐 Access the application:"
echo "  - Port forward: kubectl port-forward -n qdrant svc/animal-chat-service 8080:80"
echo "  - Then visit: http://localhost:8080"
echo ""
echo "  - Or add to /etc/hosts: echo '127.0.0.1 animal-chat.local' >> /etc/hosts"
echo "  - And setup ingress controller to access via: http://animal-chat.local"
