# Kubernetes Fundamentals

## Why Kubernetes

Kubernetes is useful when applications are split into multiple containerized services and need coordinated operation across machines.

Common goals:

- Schedule workloads across a cluster
- Recover from failed containers or nodes
- Scale replicas up and down
- Expose applications reliably on the network
- Manage rolling updates without stopping the whole system

Managed Kubernetes offerings are also available from major cloud providers.

## Core Architecture

### Cluster

- A Kubernetes cluster is the full environment that runs your workloads
- It includes worker nodes and control-plane components

### Nodes

- Nodes are worker machines in the cluster
- They run the container runtime and host Pods
- Pods may be rescheduled to different nodes when needed

### Pods

- A Pod is the basic deployable unit in Kubernetes
- A Pod usually contains one main application container
- Each Pod gets its own cluster IP
- Pods are ephemeral and should be treated as replaceable

## Main Workload Objects

### Deployment

- `Deployment` manages stateless application replicas
- It keeps the desired number of Pods running
- If a Pod fails, Kubernetes creates a replacement

Example manifest skeleton:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: nginx:latest
```

### StatefulSet

- `StatefulSet` is used for stateful workloads
- Pods get predictable names such as `pod-0`, `pod-1`, and `pod-2`
- Scaling and replacement preserve ordering and identity more carefully than Deployments

## Networking and Exposure

### Service

- A `Service` provides stable access to one or more Pods
- It routes traffic to Pods selected by labels
- This hides the fact that individual Pods may be recreated over time

### Ingress

- `Ingress` defines how external HTTP(S) traffic enters the cluster and is routed to Services
- It is useful when multiple applications share external access

## Scheduling

- Kubernetes can place Pods on different nodes based on scheduling rules
- `nodeSelector` is a simple way to constrain a Pod to nodes with specific labels

## kubectl Basics

`kubectl` is the main command-line tool for interacting with Kubernetes objects.

```bash
kubectl apply -f manifest.yaml
kubectl create -f manifest.yaml
kubectl get pods
kubectl get services
kubectl describe deployment <name>
kubectl scale deployment <name> --replicas=5
```

Notes:

- `apply` is commonly used to create or update resources from manifests
- `get` provides a quick overview of deployed objects
- `describe` shows more detailed state and event information
- `scale` changes the desired replica count for scalable workloads

## Storage Basics

Kubernetes storage often involves:

- `StorageClass` for provisioning behavior
- `PersistentVolume` (PV) for storage resources
- `PersistentVolumeClaim` (PVC) for workload requests

Useful commands:

```bash
kubectl get sc
kubectl get pv
kubectl get pvc
```
