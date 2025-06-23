# Deployment Management for Email Assistant

This document provides instructions on how to manage the `email-assistant` deployment on your `k3s` cluster.

## 1. Check Deployment Status

To check the current status of your `email-assistant` deployment, use the following command:

```bash
kubectl get deployment email-assistant
```

To check the status of the pods associated with the deployment:

```bash
kubectl get pods -l app=email-assistant
```

To check the status of the service:

```bash
kubectl get services -l app=email-assistant
```

## 2. Turn Off the Deployment

To turn off (delete) the `email-assistant` deployment and its associated service, use the following commands:

```bash
kubectl delete deployment email-assistant
kubectl delete service email-assistant-service
```

## 3. Restart the Deployment

To restart the `email-assistant` deployment, you can first delete it and then re-apply the deployment and service configurations.

**Step 1: Turn off the deployment**

```bash
kubectl delete deployment email-assistant
kubectl delete service email-assistant-service
```

**Step 2: Re-apply the deployment and service**

```bash
kubectl apply -f email-assistant-deployment.yaml
kubectl apply -f email-assistant-service.yaml
```

## 4. Turn On the Deployment

To turn on (create) the `email-assistant` deployment and its associated service, use the following commands:

```bash
kubectl apply -f email-assistant-deployment.yaml
kubectl apply -f email-assistant-service.yaml
```

## 5. Access the Streamlit Application

Once the deployment is running, you can access the Streamlit application. First, get the internal IP of your `k3s` node:

```bash
kubectl get nodes -o wide
```

Look for the `INTERNAL-IP` of your node (e.g., `139.84.201.110`). The Streamlit application is exposed on `NodePort` `30000`.

You can access the application by navigating to `http://<YOUR_NODE_INTERNAL_IP>:30000` in your web browser. For example, if your node's internal IP is `139.84.201.110`, you would go to `http://139.84.201.110:30000`.