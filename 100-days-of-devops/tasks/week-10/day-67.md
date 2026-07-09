# Day 67: Deploy Guest Book App on Kubernetes

## Task Overview

Deploy a complete multi-tier guestbook application on Kubernetes featuring a PHP frontend, Redis master for write operations, and Redis slaves for read operations. This architecture demonstrates service discovery, load distribution, and scalable application design.

**Technical Specifications:**

**Backend Tier:**
- Redis Master: deployment `redis-master`, 1 replica, image `redis`, container `master-redis-devops`
- Redis Slave: deployment `redis-slave`, 2 replicas, image `gcr.io/google_samples/gb-redisslave:v3`, container `slave-redis-devops`
- Resource requests: CPU 100m, Memory 100Mi per container
- Port: 6379 (Redis default)
- Environment: GET_HOSTS_FROM=dns for service discovery

**Frontend Tier:**
- Deployment: `frontend`, 3 replicas
- Image: `gcr.io/google-samples/gb-frontend@sha256:a908df8486ff66f2c4daa0d3d8a2fa09846a1fc8efd65649c0109695c7c5cbff`
- Container: `php-redis-devops`
- Resource requests: CPU 100m, Memory 100Mi
- Port: 80, NodePort: 30009

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Create Redis master deployment and service configuration

```sh
vi k3s-redis-master.yaml
```

Create the YAML configuration file for the Redis master deployment and service. The Redis master handles all write operations and serves as the authoritative source of data. This file defines a deployment with a single replica running the official Redis image and a ClusterIP service to expose it within the cluster.

**Reference YAML for Redis Master:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis-master
spec:
  replicas: 1
  selector:
    matchLabels:
      app: redis
      role: master
      tier: backend
  template:
    metadata:
      labels:
        app: redis
        role: master
        tier: backend
    spec:
      containers:
      - name: master-redis-devops
        image: redis
        ports:
        - containerPort: 6379
        resources:
          requests:
            cpu: 100m
            memory: 100Mi
---
apiVersion: v1
kind: Service
metadata:
  name: redis-master
spec:
  selector:
    app: redis
    role: master
    tier: backend
  ports:
  - protocol: TCP
    port: 6379
    targetPort: 6379
```

The deployment uses labels to identify the pod as the Redis master (role: master, tier: backend). Resource requests ensure the container gets at least 100m CPU (0.1 CPU cores) and 100Mi memory. The service uses these same labels as selectors to route traffic to the Redis master pod. The ClusterIP service type makes Redis accessible only within the cluster using the DNS name `redis-master`.

**Step 2:** Create Redis slave deployment and service configuration

```sh
vi k3s-redis-slave.yaml
```

Create the configuration for Redis slave deployments that replicate data from the master and handle read operations. Running 2 replicas provides redundancy and distributes read traffic across multiple instances. The slaves automatically sync with the master using DNS-based service discovery.

**Reference YAML for Redis Slave:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: redis-slave
spec:
  replicas: 2
  selector:
    matchLabels:
      app: redis
      role: slave
      tier: backend
  template:
    metadata:
      labels:
        app: redis
        role: slave
        tier: backend
    spec:
      containers:
      - name: slave-redis-devops
        image: gcr.io/google_samples/gb-redisslave:v3
        ports:
        - containerPort: 6379
        env:
        - name: GET_HOSTS_FROM
          value: dns
        resources:
          requests:
            cpu: 100m
            memory: 100Mi
---
apiVersion: v1
kind: Service
metadata:
  name: redis-slave
spec:
  selector:
    app: redis
    role: slave
    tier: backend
  ports:
  - protocol: TCP
    port: 6379
    targetPort: 6379
```

The Redis slave image is a special version that automatically discovers and connects to the Redis master using Kubernetes DNS. The `GET_HOSTS_FROM=dns` environment variable tells the slave to look up the `redis-master` service via DNS. With 2 replicas, Kubernetes distributes read requests across both slave pods for load balancing. The service selects only pods with role: slave, ensuring read operations don't hit the master.

**Step 3:** Create frontend deployment and service configuration

```sh
vi k3s-php-redis.yaml
```

Create the PHP web application configuration that serves the guestbook user interface. The frontend connects to Redis master for write operations (submitting guestbook entries) and Redis slaves for read operations (displaying entries). Three replicas provide high availability and distribute user traffic.

**Reference YAML for Frontend:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: guestbook
      tier: frontend
  template:
    metadata:
      labels:
        app: guestbook
        tier: frontend
    spec:
      containers:
      - name: php-redis-devops
        image: gcr.io/google-samples/gb-frontend@sha256:a908df8486ff66f2c4daa0d3d8a2fa09846a1fc8efd65649c0109695c7c5cbff
        ports:
        - containerPort: 80
        env:
        - name: GET_HOSTS_FROM
          value: dns
        resources:
          requests:
            cpu: 100m
            memory: 100Mi
---
apiVersion: v1
kind: Service
metadata:
  name: frontend
spec:
  type: NodePort
  selector:
    app: guestbook
    tier: frontend
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
    nodePort: 30009
```

The frontend image contains a PHP application that uses the Predis library to communicate with Redis. It discovers the `redis-master` and `redis-slave` services via DNS (GET_HOSTS_FROM=dns). The application sends write operations to redis-master and read operations to redis-slave. The NodePort service exposes the application externally on port 30009, making it accessible via any cluster node's IP address.

**Step 4:** Deploy Redis master to Kubernetes

```sh
kubectl apply -f k3s-redis-master.yaml
```

Apply the Redis master configuration to create the deployment and service. The `kubectl apply` command creates the deployment which starts a pod running the Redis container, then creates the service which registers the DNS entry `redis-master` pointing to the pod's IP. Wait 10-20 seconds for the pod to start before deploying the slaves, as they need to discover and connect to the master.

**Step 5:** Verify Redis master is running

```sh
kubectl get pods -l role=master
kubectl get svc redis-master
```

Check that the Redis master pod is in `Running` state before proceeding. The `-l role=master` flag filters to show only the master pod. Also verify the `redis-master` service was created and has a ClusterIP assigned. If the pod is still in `ContainerCreating` status, wait a few more seconds. The service should show port 6379 and type ClusterIP.

**Step 6:** Deploy Redis slaves to Kubernetes

```sh
kubectl apply -f k3s-redis-slave.yaml
```

Apply the Redis slave configuration to create the deployment and service. Kubernetes will create 2 pods running the Redis slave image. Each slave container will execute startup scripts that resolve `redis-master` via DNS, connect to it, and begin replicating data. The `redis-slave` service will load balance read requests across both slave pods.

**Step 7:** Verify Redis slaves are running and connected

```sh
kubectl get pods -l role=slave
kubectl get svc redis-slave
```

Confirm both Redis slave pods are running (you should see 2 pods). Use `kubectl logs <slave-pod-name>` to check the slave successfully connected to the master - look for messages like "MASTER <-> REPLICA sync started" and "MASTER <-> REPLICA sync: Finished with success". The redis-slave service should be created with ClusterIP type on port 6379.

**Step 8:** Deploy frontend to Kubernetes

```sh
kubectl apply -f k3s-php-redis.yaml
```

Apply the frontend configuration to create the PHP web application deployment and NodePort service. Kubernetes will create 3 frontend pods (for high availability and load distribution) and expose them externally via NodePort 30009. Each frontend pod will connect to the Redis backend using DNS-based service discovery, sending writes to redis-master and reads to redis-slave.

**Step 9:** Verify frontend deployment and service

```sh
kubectl get pods -l tier=frontend
kubectl get svc frontend
```

Check that all 3 frontend pods are running with status `Running` and readiness `1/1`. Verify the frontend service shows type `NodePort` with ports `80:30009/TCP`, indicating the application is accessible on port 30009 from outside the cluster. If any pod shows `ImagePullBackOff`, there may be an issue pulling the image from gcr.io.

**Step 10:** Verify complete application deployment

```sh
kubectl get all
```

Display all resources (deployments, services, pods) to get a comprehensive view of the guestbook application. You should see:
- 3 deployments: redis-master (1/1), redis-slave (2/2), frontend (3/3)
- 3 services: redis-master (ClusterIP), redis-slave (ClusterIP), frontend (NodePort)
- 6 pods total: 1 master, 2 slaves, 3 frontend (all Running)

This confirms the entire multi-tier application is deployed and operational.

**Step 11:** Access the guestbook application

Access the application by clicking the "App" button in the KodeKloud interface or navigating to `http://<node-ip>:30009` in your browser. You should see the guestbook interface where you can submit entries (which write to redis-master) and view entries (which read from redis-slave). Try adding several messages to test the write-through-master and read-from-slave architecture. The application demonstrates how frontend, backend master, and backend slaves work together in a distributed system.

---

## Key Concepts

**Multi-Tier Application Architecture:**
- **Frontend Tier**: User-facing web application layer (PHP)
- **Backend Tier**: Data persistence and caching layer (Redis)
- **Service Discovery**: DNS-based communication between tiers
- **Horizontal Scaling**: Multiple replicas for load distribution and availability
- **Separation of Concerns**: Each tier has distinct responsibilities

**Master-Slave Replication Pattern:**
- **Master**: Handles all write operations and is the source of truth
- **Slaves**: Replicate data from master and handle read operations
- **Data Synchronization**: Slaves continuously sync with master
- **Read Scalability**: Adding more slaves increases read capacity
- **Write Bottleneck**: All writes go to single master (limitation)

**Kubernetes Service Discovery:**
- **DNS Names**: Services accessible via name (e.g., redis-master)
- **GET_HOSTS_FROM=dns**: Environment variable enabling DNS-based discovery
- **Cluster DNS**: kube-dns or CoreDNS provides name resolution
- **Service Endpoints**: Kubernetes maintains list of pod IPs behind each service
- **Load Balancing**: Services automatically distribute traffic across pod replicas

**Resource Requests and Limits:**
- **CPU Requests**: Guaranteed CPU allocation (100m = 0.1 cores)
- **Memory Requests**: Guaranteed memory allocation (100Mi)
- **Limits**: Maximum resources a container can consume (optional)
- **QoS Classes**: Kubernetes assigns priority based on requests/limits
- **Resource Quotas**: Namespace-level limits on total resource consumption

**Kubernetes Labels and Selectors:**
- **Labels**: Key-value pairs attached to objects (app: redis, role: master)
- **Selectors**: Query labels to identify groups of objects
- **Service Selectors**: Services use selectors to find target pods
- **Deployment Selectors**: Deployments manage pods matching selector
- **Organizational Tool**: Labels enable flexible grouping and filtering

**Service Types:**
- **ClusterIP**: Internal-only access via cluster IP (redis-master, redis-slave)
- **NodePort**: External access via node IP and static port (frontend:30009)
- **LoadBalancer**: Cloud provider load balancer with external IP
- **ExternalName**: Maps service to external DNS name

**Production Considerations:**
- **Persistence**: Add PersistentVolumes to Redis master to prevent data loss
- **High Availability**: Use Redis Sentinel or Cluster for automatic failover
- **Resource Limits**: Set CPU and memory limits to prevent resource exhaustion
- **Health Checks**: Configure liveness and readiness probes
- **Monitoring**: Track request rates, error rates, latency, and resource usage
- **Security**: Implement network policies, enable Redis authentication, use TLS

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 66](day-66.md) | [Day 68 →](day-68.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
