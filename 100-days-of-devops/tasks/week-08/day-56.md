# Day 56: Deploy Nginx Web Server on Kubernetes Cluster

## Task Overview

Deploy a highly available and scalable nginx web server using Kubernetes Deployment and Service resources. This exercise demonstrates production-ready application deployment with multiple replicas and external access.

**Technical Specifications:**
- Deployment: nginx-deployment with 3 replicas
- Container: nginx-container using nginx:latest image
- Service: nginx-service (NodePort type)
- NodePort: 30011 (external access port)
- High availability through replica distribution

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Create deployment and service manifest

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
  labels:
    app: nginx
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
      - name: nginx-container
        image: nginx:latest
        ports:
        - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: nginx-service
spec:
  type: NodePort
  selector:
    app: nginx
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
    nodePort: 30011
```

Create a manifest file defining both a Deployment and Service for nginx. The **Deployment** manages three replica pods (`replicas: 3`) running nginx containers. The `selector.matchLabels` field (`app: nginx`) connects the Deployment to pods it should manage. The `template` section defines the pod specification: a single container named nginx-container using the nginx:latest image, exposing port 80. The **Service** provides stable network access to the deployment. With `type: NodePort`, it exposes the service on each node's IP at port 30011. The `selector: app: nginx` matches the pod labels, routing traffic to any pod with this label. The `port: 80` is the service's internal port, `targetPort: 80` is the container port to forward to, and `nodePort: 30011` is the external port on each node.

**Step 2:** Apply the configuration to create resources

```sh
kubectl apply -f k3s-deployment.yml
```

Deploy both the Deployment and Service to the cluster using a single command. The `kubectl apply` command processes the manifest file, creating both resources. Kubernetes first creates the Deployment resource, which triggers the creation of a ReplicaSet. The ReplicaSet then creates three nginx pods distributed across available nodes. Simultaneously, the Service is created and immediately begins tracking pods matching the `app: nginx` label. The Service configures iptables rules or IPVS on each node to route traffic arriving on port 30011 to the nginx pods on port 80. The Deployment continuously monitors the pods, automatically replacing any that fail to maintain the desired replica count of 3.

**Step 3:** Verify the deployment was created successfully

```sh
kubectl get deployments.apps
```

List all deployments to confirm nginx-deployment was created and is managing replicas correctly. The output shows deployment name, desired replicas (3), current replicas, up-to-date replicas, available replicas, and age. The "READY" column should show "3/3" indicating all three desired replicas are running and ready. The "UP-TO-DATE" column shows how many replicas reflect the latest pod template. The "AVAILABLE" column indicates how many replicas are available to serve traffic (passed readiness checks). If these numbers don't match the desired count, the deployment may still be rolling out or experiencing issues.

**Step 4:** Verify all pods are running

```sh
kubectl get pods
```

List all pods to see the three individual nginx instances created by the deployment. Each pod name follows the format `nginx-deployment-<replicaset-hash>-<random-suffix>`. The output shows pod names, ready status (should be "1/1" for each), status (should be "Running"), restart count (should be 0), and age. All three pods should show as "Running" with "1/1" ready. The ReplicaSet hash in the pod names (middle section) will be identical for all three pods, indicating they were created from the same pod template. If any pod shows a different status (Pending, CrashLoopBackOff, Error), investigate using `kubectl describe pod <pod-name>`.

**Step 5:** Verify the service was created

```sh
kubectl get services
# or
kubectl get svc
```

List all services to confirm nginx-service was created with the correct configuration. The output displays service name, type (NodePort), cluster IP (internal IP), external IP (usually shows `<none>` for NodePort), ports, and age. The "PORT(S)" column should show `80:30011/TCP` - this means the service listens on port 80 internally and is exposed on port 30011 on all nodes. The cluster IP is a virtual IP accessible only within the cluster, while port 30011 on each node's IP provides external access. The service automatically load balances traffic across the three nginx pods.

**Step 6:** Test external access to the service (optional)

```sh
# Get node IP address
kubectl get nodes -o wide

# Access nginx via NodePort (replace NODE_IP with actual node IP)
curl http://NODE_IP:30011

# In development/testing environments like minikube or kind
curl http://localhost:30011
```

Verify external access to the nginx deployment through the NodePort service. First, get a node's external IP address using `kubectl get nodes -o wide`. Then use curl to send an HTTP request to any node's IP on port 30011. The request is routed to one of the three nginx pods, and you should receive nginx's default welcome page HTML. In local development clusters (minikube, kind, Docker Desktop), you can typically use `localhost:30011`. The service automatically load balances requests across all three nginx pods using round-robin or other configured algorithm.

**Step 7:** Inspect service endpoints (optional)

```sh
kubectl get endpoints nginx-service
# or
kubectl describe service nginx-service
```

View the service endpoints to see which pod IPs the service is routing traffic to. The endpoints are automatically managed by Kubernetes based on the service selector and pod readiness. The output shows the endpoint name and a comma-separated list of pod IPs and ports (e.g., `10.244.0.5:80,10.244.0.6:80,10.244.0.7:80`). These represent the three nginx pods. As pods are created, deleted, or become ready/unready, Kubernetes automatically updates the endpoints. The `kubectl describe service` command provides more details including the selector, endpoints, and any events related to the service.

---

## Key Concepts

**Kubernetes Deployments:**
- **Purpose**: Manage stateless applications with declarative updates and scaling
- **ReplicaSet Management**: Automatically creates and manages ReplicaSets
- **Self-Healing**: Automatically replaces failed or deleted pods
- **Scaling**: Easily scale up or down by changing replica count
- **Rolling Updates**: Update application version with zero downtime
- **Rollback**: Revert to previous versions if updates fail

**Replica Management:**
- **Desired State**: Deployment maintains specified number of replicas
- **Pod Distribution**: Kubernetes spreads replicas across nodes for availability
- **Automatic Replacement**: Failed pods are immediately recreated
- **Load Distribution**: Multiple replicas share incoming traffic load
- **Resource Optimization**: Replicas can be scaled based on demand

**Kubernetes Services:**
- **Purpose**: Provide stable network endpoint for dynamic pod sets
- **Service Discovery**: Pods can discover services via DNS or environment variables
- **Load Balancing**: Distribute traffic across all healthy pods
- **Decoupling**: Clients access service, not individual pods
- **Persistence**: Service IPs remain stable even as pods are replaced

**Service Types:**
- **ClusterIP** (default): Internal-only service accessible within cluster
- **NodePort**: Exposes service on each node's IP at a static port (30000-32767)
- **LoadBalancer**: Cloud provider creates external load balancer (AWS ELB, GCP LB)
- **ExternalName**: Maps service to DNS name, returns CNAME record
- **Headless**: ClusterIP set to None, returns pod IPs directly

**NodePort Services:**
- **Port Range**: Default range is 30000-32767, configurable in API server
- **Node Access**: Service accessible on nodePort on all nodes, even those without pods
- **Port Allocation**: Kubernetes auto-assigns port if nodePort not specified
- **Firewall Requirements**: NodePort must be open in firewall for external access
- **Production Use**: Typically used for development; LoadBalancer or Ingress preferred for production
- **Load Balancing**: External load balancer can distribute across nodes' NodePort

**Labels and Selectors:**
- **Labels**: Key-value pairs attached to resources (pods, services, etc.)
- **Selectors**: Query labels to find matching resources
- **Service Selectors**: Determine which pods receive traffic from service
- **Deployment Selectors**: Determine which pods deployment manages
- **Loose Coupling**: Services and deployments are connected via labels, not hardcoded references

**High Availability Features:**
- **Multiple Replicas**: Running 3+ replicas provides redundancy
- **Node Distribution**: Pods spread across multiple nodes (with proper node count)
- **Self-Healing**: Automatic pod replacement on failures
- **Rolling Updates**: Update without downtime by replacing pods gradually
- **Health Checks**: Liveness and readiness probes detect unhealthy pods
- **Load Balancing**: Traffic distributed across healthy replicas

**Deployment Strategies:**
```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1        # Max pods above desired count during update
      maxUnavailable: 0   # Max pods unavailable during update
```
- **RollingUpdate**: Gradual replacement (default), zero downtime
- **Recreate**: Terminate all old pods before creating new ones
- **maxSurge**: Extra pods during update (absolute number or percentage)
- **maxUnavailable**: Pods allowed to be down during update

**Service Discovery:**
```sh
# DNS-based service discovery (recommended)
curl http://nginx-service.default.svc.cluster.local

# Environment variables (legacy)
echo $NGINX_SERVICE_SERVICE_HOST
echo $NGINX_SERVICE_SERVICE_PORT
```
- **DNS**: Each service gets DNS name `<service-name>.<namespace>.svc.cluster.local`
- **Short Names**: Within same namespace, use just `<service-name>`
- **Environment Variables**: Kubernetes injects service info into pods
- **ClusterIP**: Services get stable virtual IP for internal access

**Scaling Operations:**
```sh
# Imperative scaling
kubectl scale deployment nginx-deployment --replicas=5

# Declarative scaling (edit manifest and apply)
kubectl apply -f updated-deployment.yml

# Autoscaling based on CPU/memory
kubectl autoscale deployment nginx-deployment --min=3 --max=10 --cpu-percent=80
```

**Best Practices:**
- **Readiness Probes**: Configure to ensure only healthy pods receive traffic
- **Resource Limits**: Set CPU/memory requests and limits for predictable performance
- **Multiple Replicas**: Run at least 3 replicas for high availability
- **Pod Disruption Budgets**: Prevent too many pods from being down simultaneously
- **Anti-Affinity**: Spread replicas across nodes and availability zones
- **Health Checks**: Implement both liveness (restart unhealthy) and readiness (route traffic) probes
- **LoadBalancer over NodePort**: Use LoadBalancer or Ingress for production external access
- **Version Tags**: Avoid `:latest` tag in production; use specific version tags

**Monitoring and Troubleshooting:**
```sh
# View deployment status
kubectl rollout status deployment/nginx-deployment

# View deployment history
kubectl rollout history deployment/nginx-deployment

# Check pod distribution across nodes
kubectl get pods -o wide

# View detailed deployment info
kubectl describe deployment nginx-deployment

# Check service endpoints
kubectl get endpoints nginx-service

# Test service from within cluster
kubectl run -it --rm debug --image=alpine --restart=Never -- wget -qO- nginx-service
```

**Advanced Traffic Management:**
- **Ingress**: HTTP/HTTPS routing to multiple services, SSL termination
- **Service Mesh**: Advanced traffic management with Istio, Linkerd
- **Session Affinity**: Route requests from same client to same pod (sessionAffinity: ClientIP)
- **External Traffic Policy**: Control how NodePort/LoadBalancer traffic routes (Local vs Cluster)

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 55](day-55.md) | [Day 57 →](../week-09/day-57.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
