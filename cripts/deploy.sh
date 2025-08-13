## 4. scripts/deploy.sh - Deployment Script
#!/bin/bash
"""
Production Deployment Script
Deploys the Patent Research Agent to production environment
"""

set -e

# Configuration
APP_NAME="patent-research-agent"
DOCKER_REGISTRY="your-registry.com"
VERSION=$(git rev-parse --short HEAD)
ENVIRONMENT=${1:-production}

echo "🚀 Deploying $APP_NAME to $ENVIRONMENT"
echo "Version: $VERSION"

# Build Docker image
echo "🐳 Building Docker image..."
docker build -t $DOCKER_REGISTRY/$APP_NAME:$VERSION .
docker tag $DOCKER_REGISTRY/$APP_NAME:$VERSION $DOCKER_REGISTRY/$APP_NAME:latest

# Push to registry
echo "📤 Pushing to registry..."
docker push $DOCKER_REGISTRY/$APP_NAME:$VERSION
docker push $DOCKER_REGISTRY/$APP_NAME:latest

# Deploy to Kubernetes
echo "☸️ Deploying to Kubernetes..."
kubectl set image deployment/$APP_NAME app=$DOCKER_REGISTRY/$APP_NAME:$VERSION
kubectl rollout status deployment/$APP_NAME

# Run health check
echo "🏥 Running health check..."
kubectl get pods -l app=$APP_NAME

echo "✅ Deployment complete!"
