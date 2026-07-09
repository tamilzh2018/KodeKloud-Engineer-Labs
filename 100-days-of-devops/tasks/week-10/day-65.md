# Day 65: Deploy Redis Deployment on Kubernetes

## Task Overview

Deploy a Redis in-memory caching system on Kubernetes to improve database performance. Configure Redis with resource limits, ConfigMap-based configuration, and persistent storage volumes.

**Technical Specifications:**
- ConfigMap name: `my-redis-config` with maxmemory `2mb`
- Deployment name: `redis-deployment`
- Container image: `redis:alpine`
- Container name: `redis-container`
- Replicas: `1`
- CPU request: `1 CPU`
- Container port: `6379` (Redis default)
- Volume mounts: Empty directory at `/redis-master-data`, ConfigMap at `/redis-master`

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Create the Redis deployment configuration file

```sh
vi k3s-deployment.yaml
```

Create a new YAML file named `k3s-deployment.yaml` using the vi text editor. This file will contain the complete Redis deployment configuration including the ConfigMap for Redis settings, the Deployment specification with resource limits and volume mounts, and all necessary Kubernetes object definitions. The configuration needs to include two main resources: a ConfigMap to store Redis configuration parameters and a Deployment to run the Redis container with the specified requirements.

**Reference YAML structure:**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: my-redis-config
data:
  redis-config: |
    maxmemory 2mb
    maxmemory-policy allkeys-lru
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis-container
        image: redis:alpine
        ports:
        - containerPort: 6379
        resources:
          requests:
            cpu: "1"
        volumeMounts:
        - name: data
          mountPath: /redis-master-data
        - name: redis-config
          mountPath: /redis-master
      volumes:
      - name: data
        emptyDir: {}
      - name: redis-config
        configMap:
          name: my-redis-config
```

The ConfigMap stores Redis configuration with a maxmemory limit of 2mb and an LRU (Least Recently Used) eviction policy. The Deployment specifies 1 replica running the redis:alpine image (a lightweight Alpine Linux-based Redis container), requests 1 CPU core for guaranteed performance, exposes port 6379 for Redis client connections, and mounts two volumes: an emptyDir volume for temporary data storage that gets deleted when the pod terminates, and a configMap volume to inject the Redis configuration file into the container.

**Step 2:** Deploy Redis to the Kubernetes cluster

```sh
kubectl apply -f k3s-deployment.yaml
```

Apply the YAML configuration file to create the ConfigMap and Deployment resources in Kubernetes. The `kubectl apply` command is idempotent, meaning it can be run multiple times safely - it will create resources if they don't exist or update them if they do. Kubernetes will process the YAML file, create the ConfigMap first (as it's needed by the Deployment), then create the Deployment which will trigger the creation of a ReplicaSet and ultimately a Pod running the Redis container. The scheduler will assign the pod to an available node, pull the redis:alpine image if not already present, and start the container.

**Step 3:** Verify the Redis deployment is running

```sh
kubectl get pods
```

Check the status of all pods to confirm the Redis pod is running successfully. Look for a pod named `redis-deployment-<random-hash>` with status `Running` and readiness `1/1`. If the pod status shows `ContainerCreating`, wait a few seconds for Kubernetes to pull the image and start the container. If you see `ImagePullBackOff` or `Error` status, use `kubectl describe pod <pod-name>` to investigate. A healthy Redis deployment should show the pod in Running state with 0 restarts, indicating the container started successfully and is stable.

**Step 4:** Verify ConfigMap was created

```sh
kubectl get configmap
kubectl describe configmap my-redis-config
```

Confirm the ConfigMap was created and contains the correct Redis configuration. The `kubectl get configmap` command lists all ConfigMaps in the namespace, and `kubectl describe configmap my-redis-config` shows the detailed configuration data including the maxmemory setting. You should see the `redis-config` key with the value `maxmemory 2mb` and `maxmemory-policy allkeys-lru`. ConfigMaps are a way to inject configuration into containers without rebuilding images, making it easy to modify Redis settings without changing the deployment.

**Step 5:** Verify the deployment configuration

```sh
kubectl describe deployment redis-deployment
```

Examine the detailed deployment configuration to ensure all specifications are correct. This command shows the deployment strategy, replica count, pod template specification, resource requests, volume mounts, and current status. Verify that the deployment shows 1/1 replicas available, the container image is `redis:alpine`, CPU requests are set to 1 CPU, and both volumes (data and redis-config) are properly configured. The events section at the bottom will show the deployment creation and any scaling activities.

**Step 6:** Test Redis functionality (optional)

```sh
kubectl exec -it <redis-pod-name> -- redis-cli
```

Optionally connect to the Redis container and test that Redis is functioning correctly. Once inside the redis-cli prompt, you can run commands like `PING` (should return PONG), `CONFIG GET maxmemory` (should show 2097152 bytes which equals 2mb), and `SET test "Hello Redis"` followed by `GET test` to verify data storage. Type `exit` to leave the redis-cli. This verification ensures Redis is not only running but also accepting connections and processing commands with the correct configuration.

---

## Key Concepts

**Redis as a Caching Layer:**
- **In-Memory Database**: Stores data in RAM for ultra-fast read/write operations
- **Key-Value Store**: Simple data structure with string keys and various value types
- **Cache Performance**: Reduces database load by caching frequently accessed data
- **Data Structures**: Supports strings, lists, sets, sorted sets, hashes, bitmaps, and streams

**ConfigMap Usage:**
- **Configuration Decoupling**: Separates configuration from application code
- **Environment-Specific Settings**: Different configs for dev, staging, production
- **Dynamic Updates**: ConfigMaps can be updated without rebuilding images
- **Volume Mounting**: Configuration files injected into containers as files or environment variables

**Resource Management:**
- **CPU Requests**: Guarantees minimum CPU allocation (1 CPU = 1000 millicores)
- **Memory Limits**: Prevents Redis from consuming unlimited memory
- **Resource Quotas**: Cluster-wide limits on resource consumption
- **Quality of Service**: Kubernetes assigns QoS classes based on requests/limits

**Volume Types:**
- **emptyDir**: Temporary storage that exists for the pod's lifetime, deleted when pod terminates
- **configMap**: Injects configuration data as files in the container
- **persistentVolumeClaim**: Durable storage that persists beyond pod lifecycle
- **hostPath**: Mounts a directory from the host node (not recommended for production)

**Production Considerations:**
- **Persistence**: Use PersistentVolumeClaims for production Redis to survive pod restarts
- **High Availability**: Deploy Redis Sentinel for automatic failover and monitoring
- **Clustering**: Redis Cluster for horizontal scaling across multiple nodes
- **Security**: Enable authentication with requirepass, use network policies to restrict access
- **Monitoring**: Track memory usage, hit/miss rates, command latency, and eviction statistics

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 64](day-64.md) | [Day 66 →](day-66.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
