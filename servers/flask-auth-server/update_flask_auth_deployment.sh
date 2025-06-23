#!/bin/bash

# Define variables
IMAGE_NAME="flask-auth-server"
IMAGE_TAG="latest"
LOCAL_REGISTRY="localhost:5000"
DEPLOYMENT_FILE="flask-auth-deployment.yaml"
NAMESPACE="default" # Assuming default namespace, change if needed

# Full image name with registry and tag
FULL_IMAGE_NAME="${LOCAL_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"

echo "--- Building Docker image: ${FULL_IMAGE_NAME} ---"
docker build -t "${FULL_IMAGE_NAME}" .

if [ $? -ne 0 ]; then
    echo "Docker build failed. Exiting."
    exit 1
fi

echo "--- Pushing Docker image to local registry ---"
docker push "${FULL_IMAGE_NAME}"

if [ $? -ne 0 ]; then
    echo "Docker push failed. Exiting."
    exit 1
fi

echo "--- Updating Kubernetes deployment: ${DEPLOYMENT_FILE} ---"
# Use kubectl set image to update the deployment
kubectl set image deployment/${IMAGE_NAME} ${IMAGE_NAME}=${FULL_IMAGE_NAME} -n ${NAMESPACE}

if [ $? -ne 0 ]; then
    echo "Kubernetes deployment update failed. Exiting."
    exit 1
fi

echo "--- Deployment update successful! ---"
echo "You can verify the deployment status with: kubectl rollout status deployment/${IMAGE_NAME} -n ${NAMESPACE}"
echo "And check the pods with: kubectl get pods -l app=${IMAGE_NAME} -n ${NAMESPACE}"