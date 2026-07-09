# Day 63: Deploy Iron Gallery App on Kubernetes

## Task Overview

Deploy a complete multi-tier web application on Kubernetes, consisting of a frontend (Iron Gallery) and backend database (MariaDB). This task demonstrates deploying complex applications with multiple components, proper service networking, namespace isolation, and environment-based configuration.

**Technical Specifications:**
- Namespace: iron-namespace-xfusion
- Frontend: iron-gallery-deployment-xfusion (kodekloud/irongallery:2.0)
- Backend: iron-db-deployment-xfusion (kodekloud/irondb:2.0)
- Services: ClusterIP for database, NodePort for frontend
- Volumes: emptyDir for temporary storage
- Resource limits: CPU and memory constraints

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Create a dedicated namespace

```bash
kubectl create namespace iron-namespace-xfusion
kubectl get namespaces
```

Create a Kubernetes namespace to logically isolate the Iron Gallery application from other workloads in the cluster. Namespaces provide scope for resource names, enable resource quotas, and allow RBAC policies to be applied at the namespace level. The `get namespaces` command verifies the namespace was created successfully. You should see `iron-namespace-xfusion` in the list along with default system namespaces like `default`, `kube-system`, and `kube-public`.

**Step 2:** Create the Iron Gallery frontend deployment manifest

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: iron-gallery-deployment-xfusion
  namespace: iron-namespace-xfusion
  labels:
    run: iron-gallery
spec:
  replicas: 1
  selector:
    matchLabels:
      run: iron-gallery
  template:
    metadata:
      labels:
        run: iron-gallery
    spec:
      containers:
      - name: iron-gallery-container-xfusion
        image: kodekloud/irongallery:2.0
        resources:
          limits:
            memory: "100Mi"
            cpu: "50m"
        volumeMounts:
        - name: config
          mountPath: /usr/share/nginx/html/data
        - name: images
          mountPath: /usr/share/nginx/html/uploads
      volumes:
      - name: config
        emptyDir: {}
      - name: images
        emptyDir: {}
```

Define the frontend deployment for the Iron Gallery web application. The deployment creates a single replica pod running the `kodekloud/irongallery:2.0` image. Resource limits ensure the container doesn't consume excessive cluster resources - 100MiB memory and 50 millicores CPU. The container mounts two emptyDir volumes: `config` for application data and `images` for user uploads. These volumes are ephemeral, existing only for the pod's lifetime. The `run: iron-gallery` label is critical for service discovery.

**Step 3:** Create the MariaDB database deployment manifest

```yaml
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: iron-db-deployment-xfusion
  namespace: iron-namespace-xfusion
  labels:
    db: mariadb
spec:
  replicas: 1
  selector:
    matchLabels:
      db: mariadb
  template:
    metadata:
      labels:
        db: mariadb
    spec:
      containers:
      - name: iron-db-container-xfusion
        image: kodekloud/irondb:2.0
        env:
        - name: MYSQL_DATABASE
          value: "database_blog"
        - name: MYSQL_ROOT_PASSWORD
          value: "R00tP@ssw0rd123"
        - name: MYSQL_PASSWORD
          value: "U$erP@ss456"
        - name: MYSQL_USER
          value: "appuser"
        volumeMounts:
        - name: db
          mountPath: /var/lib/mysql
      volumes:
      - name: db
        emptyDir: {}
```

Define the backend database deployment running MariaDB. The deployment configures the database using environment variables: `MYSQL_DATABASE` creates the initial database, `MYSQL_ROOT_PASSWORD` sets the root user password, `MYSQL_USER` and `MYSQL_PASSWORD` create an application user with its credentials. The database data is stored in an emptyDir volume mounted at `/var/lib/mysql`. In production, you would use a PersistentVolume for data durability, but emptyDir is acceptable for testing since we're not persisting data beyond the installation phase.

**Step 4:** Create the database ClusterIP service manifest

```yaml
---
apiVersion: v1
kind: Service
metadata:
  name: iron-db-service-xfusion
  namespace: iron-namespace-xfusion
spec:
  type: ClusterIP
  selector:
    db: mariadb
  ports:
  - protocol: TCP
    port: 3306
    targetPort: 3306
```

Define a ClusterIP service to expose the MariaDB database within the cluster. The service is internal-only (ClusterIP), making the database accessible to other pods in the cluster but not from outside. The `selector: db: mariadb` routes traffic to pods with this label (the database deployment). The service listens on port 3306 (MySQL/MariaDB standard port) and forwards to the same port on the pods. Other services can connect to the database using the DNS name `iron-db-service-xfusion.iron-namespace-xfusion.svc.cluster.local` or simply `iron-db-service-xfusion` from within the same namespace.

**Step 5:** Create the frontend NodePort service manifest

```yaml
---
apiVersion: v1
kind: Service
metadata:
  name: iron-gallery-service-xfusion
  namespace: iron-namespace-xfusion
spec:
  type: NodePort
  selector:
    run: iron-gallery
  ports:
  - protocol: TCP
    port: 80
    targetPort: 80
    nodePort: 32678
```

Define a NodePort service to expose the Iron Gallery frontend externally. The service makes the application accessible from outside the cluster on port 32678 on every node's IP address. The `selector: run: iron-gallery` routes traffic to the frontend pods. The service receives traffic on its cluster IP at port 80, forwards to port 80 on the pods (where nginx serves the application), and exposes externally on nodePort 32678. Users can access the gallery by navigating to `http://<node-ip>:32678` in a web browser.

**Step 6:** Apply all configurations to the cluster

```bash
kubectl apply -f k3s-iron-gallery.yaml
```

Deploy all the resources defined in the YAML file to the Kubernetes cluster in the specified namespace. The single YAML file contains all four resources (two deployments and two services) separated by `---`. Kubernetes creates them in the order they appear, though the order doesn't matter for this application. The frontend and backend pods start simultaneously, and the services begin routing traffic as soon as pods are ready. This demonstrates infrastructure-as-code principles where the entire application stack is defined declaratively.

**Step 7:** Verify namespace resources

```bash
kubectl get all -n iron-namespace-xfusion
```

List all resources in the iron-namespace-xfusion namespace to get a comprehensive view of the deployment. This single command shows deployments, replicasets, pods, and services together. You should see both deployments with 1/1 ready replicas, the pods in Running status, and both services with their respective types (ClusterIP and NodePort). This is the quickest way to verify the entire application stack deployed successfully.

**Step 8:** Verify deployments are ready

```bash
kubectl get deployments.apps -n iron-namespace-xfusion
```

Check the status of the deployments specifically. Both `iron-gallery-deployment-xfusion` and `iron-db-deployment-xfusion` should show READY as 1/1, indicating the desired number of replicas match the available replicas. The UP-TO-DATE column shows how many replicas are running the latest pod template. If either deployment shows 0/1, wait a moment for the images to pull and containers to start, or investigate with `kubectl describe deployment`.

**Step 9:** Verify pods are running

```bash
kubectl get pods -n iron-namespace-xfusion
```

Examine the pod status to ensure both the frontend and database containers are running. Each deployment creates one pod (as specified by replicas: 1). The pods should show STATUS as `Running` and READY as 1/1. If you see `ImagePullBackOff`, there may be an issue pulling the container images. If you see `CrashLoopBackOff`, the containers are starting but immediately failing - check logs with `kubectl logs -n iron-namespace-xfusion <pod-name>`.

**Step 10:** Verify services are configured correctly

```bash
kubectl get svc -n iron-namespace-xfusion
```

List the services to confirm both are created with the correct types and ports. The `iron-db-service-xfusion` should show TYPE `ClusterIP` with PORT(S) `3306/TCP`, indicating it's internal-only. The `iron-gallery-service-xfusion` should show TYPE `NodePort` with PORT(S) `80:32678/TCP`, confirming external accessibility. The CLUSTER-IP column shows the internal IP addresses used for service-to-service communication within the cluster.

**Step 11:** Test database connectivity (optional)

```bash
# Get the database pod name
DB_POD=$(kubectl get pod -n iron-namespace-xfusion -l db=mariadb -o jsonpath='{.items[0].metadata.name}')

# Test MySQL connectivity
kubectl exec -n iron-namespace-xfusion $DB_POD -- mysql -u appuser -pU\$erP@ss456 -e "SHOW DATABASES;"

# Verify the database was created
kubectl exec -n iron-namespace-xfusion $DB_POD -- mysql -u root -pR00tP@ssw0rd123 -e "SELECT schema_name FROM information_schema.schemata WHERE schema_name='database_blog';"
```

Verify the database is operational by executing MySQL commands inside the database pod. The first command retrieves the pod name dynamically using labels. The second connects as the application user and lists databases, which should include `database_blog`. The third verifies the database exists by querying the information_schema. These tests confirm the environment variables configured the database correctly and it's ready to accept connections from the frontend application.

**Step 12:** Access the Iron Gallery application

```bash
# Get the node IP address
kubectl get nodes -o wide

# Access the application in browser
# http://<node-ip>:32678

# Or use port-forwarding for local testing
kubectl port-forward -n iron-namespace-xfusion svc/iron-gallery-service-xfusion 8080:80
# Then access: http://localhost:8080
```

Access the Iron Gallery web interface to verify the complete deployment. Using NodePort, navigate to `http://<node-ip>:32678` where `<node-ip>` is any cluster node's IP address. You should see the Iron Gallery installation or welcome page. Alternatively, use port-forwarding to access the service locally on port 8080. The application may show a database setup page if it hasn't been configured yet, which is expected - the task only requires the application to be accessible, not fully configured.

**Step 13:** Check application and database logs

```bash
# View frontend logs
kubectl logs -n iron-namespace-xfusion -l run=iron-gallery

# View database logs
kubectl logs -n iron-namespace-xfusion -l db=mariadb

# Follow logs in real-time
kubectl logs -n iron-namespace-xfusion -l run=iron-gallery -f
```

Examine container logs to verify both the frontend and database are operating correctly. The frontend logs show web server access logs and any application errors. The database logs display MariaDB initialization, database creation, and user setup messages. Following logs in real-time with `-f` helps observe the application behavior as you interact with it through the web interface. These logs are essential for troubleshooting any issues that arise.

**Step 14:** Clean up resources (optional)

```bash
# Delete all resources in the namespace
kubectl delete namespace iron-namespace-xfusion

# Verify deletion
kubectl get namespaces
```

Remove the entire Iron Gallery application by deleting the namespace. This single command removes the namespace and all resources within it - deployments, pods, services, and volumes. This demonstrates the power of namespace isolation for resource management. The namespace deletion cascades to all contained resources, making cleanup simple and comprehensive. Verify the namespace is gone with `get namespaces` - you should no longer see `iron-namespace-xfusion` in the list.

---

## Key Concepts

**Multi-Tier Application Architecture:**

Typical web application layers in Kubernetes:

```
┌─────────────────────────────────────┐
│         Users / Internet            │
└──────────────┬──────────────────────┘
               │
               ▼
    ┌──────────────────────┐
    │  NodePort Service    │ (External access)
    │   Port 32678         │
    └──────────┬───────────┘
               │
               ▼
    ┌──────────────────────┐
    │  Frontend Pods       │ (Web application)
    │  Iron Gallery        │
    └──────────┬───────────┘
               │
               ▼
    ┌──────────────────────┐
    │  ClusterIP Service   │ (Internal only)
    │   Port 3306          │
    └──────────┬───────────┘
               │
               ▼
    ┌──────────────────────┐
    │  Database Pods       │ (Data persistence)
    │  MariaDB             │
    └──────────────────────┘
```

**Namespace Benefits:**

Namespaces provide isolation and organization:
- **Resource Isolation**: Separate environments (dev, staging, prod)
- **Access Control**: RBAC policies per namespace
- **Resource Quotas**: Limit resource consumption per namespace
- **Name Scoping**: Same resource names in different namespaces
- **Team Separation**: Assign namespaces to different teams
- **Network Policies**: Control traffic between namespaces

**Working with Namespaces:**

```bash
# Create namespace
kubectl create namespace my-app

# Set default namespace for context
kubectl config set-context --current --namespace=my-app

# List resources in specific namespace
kubectl get pods -n my-app

# List resources in all namespaces
kubectl get pods --all-namespaces

# Delete namespace and all its resources
kubectl delete namespace my-app
```

**Service Types Comparison:**

**ClusterIP** (Database Service):
- Internal cluster communication only
- Not accessible from outside the cluster
- Best for databases, internal APIs, backend services
- Provides stable internal DNS name
- Default service type

**NodePort** (Frontend Service):
- Exposes service on each node's IP at static port
- Accessible from outside cluster via `<NodeIP>:<NodePort>`
- Port range: 30000-32767 by default
- Simple external access for development
- Not recommended for production (use LoadBalancer or Ingress)

**LoadBalancer** (Production Alternative):
- Cloud provider provisions external load balancer
- Assigns external IP address
- Production-ready with high availability
- Only works in cloud environments (AWS, GCP, Azure)

**Ingress** (Production Best Practice):
- HTTP/HTTPS routing with domain names
- SSL/TLS termination
- Path-based routing to multiple services
- More efficient than multiple LoadBalancers

**emptyDir Volumes:**

Temporary storage that exists for pod lifetime:

```yaml
volumes:
- name: cache
  emptyDir: {}
```

**Characteristics**:
- Created when pod starts on a node
- Initially empty (hence the name)
- Shared between containers in the same pod
- Deleted when pod is removed from node
- Stored on node's filesystem (or in memory with `emptyDir: {medium: "Memory"}`)

**Use cases**:
- Temporary cache
- Scratch space for processing
- Sharing files between init containers and main containers
- Checkpointing long computations

**Not suitable for**:
- Data that must persist beyond pod lifecycle
- Production databases (use PersistentVolumes instead)
- Data that needs to survive pod crashes or rescheduling

**Environment Variables for Database Configuration:**

MariaDB/MySQL standard environment variables:

```yaml
env:
- name: MYSQL_DATABASE
  value: "myapp"  # Creates database on first start
- name: MYSQL_ROOT_PASSWORD
  value: "rootpass"  # Sets root user password
- name: MYSQL_USER
  value: "appuser"  # Creates non-root user
- name: MYSQL_PASSWORD
  value: "userpass"  # Sets user password
- name: MYSQL_ALLOW_EMPTY_PASSWORD
  value: "yes"  # Allow root with no password (dev only!)
```

**Best practices**:
- Use Secrets instead of plain text environment variables
- Create application-specific users (not root)
- Use strong, randomly generated passwords
- Rotate credentials regularly
- Limit user privileges to necessary databases only

**Resource Limits and Requests:**

Resource management ensures fair cluster utilization:

```yaml
resources:
  requests:
    memory: "64Mi"
    cpu: "100m"
  limits:
    memory: "128Mi"
    cpu: "200m"
```

**Requests** (minimum guaranteed):
- Used by scheduler to find suitable node
- Container guaranteed these resources
- Node must have available capacity >= requests

**Limits** (maximum allowed):
- Container cannot use more than limits
- Memory limit exceeded → Pod killed (OOMKilled)
- CPU limit exceeded → Throttled (not killed)
- Prevents resource starvation of other pods

**CPU units**:
- `1000m` = 1 CPU core
- `100m` = 0.1 CPU core (10% of one core)
- `1` = 1000m

**Memory units**:
- `Mi` = Mebibyte (1024² bytes)
- `Gi` = Gibibyte (1024³ bytes)
- `M` = Megabyte (1000² bytes)
- `G` = Gigabyte (1000³ bytes)

**Service Discovery in Kubernetes:**

Pods discover services through DNS:

**Within same namespace**:
```
service-name
service-name.namespace
service-name.namespace.svc.cluster.local
```

**Across namespaces**:
```
service-name.other-namespace
service-name.other-namespace.svc.cluster.local
```

**Environment variables** (legacy):
Kubernetes injects service information as env vars:
```
IRON_DB_SERVICE_XFUSION_SERVICE_HOST=10.96.0.5
IRON_DB_SERVICE_XFUSION_SERVICE_PORT=3306
```
Only for services created before the pod.

**DNS is preferred** because:
- Works for services created after pod
- More flexible and dynamic
- Cleaner application code
- Standard across environments

**Deployment Strategies:**

**Recreate**:
```yaml
strategy:
  type: Recreate
```
- Terminate all old pods, then create new ones
- Downtime during update
- Simple and fast
- Use for development or stateful apps that can't run multiple versions

**Rolling Update** (default):
```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1
    maxUnavailable: 0
```
- Gradually replace old pods with new ones
- Zero downtime updates
- `maxSurge`: How many extra pods during update
- `maxUnavailable`: How many pods can be unavailable
- Use for production stateless applications

**Application Configuration Best Practices:**

1. **Externalize Configuration**: Use ConfigMaps and Secrets
2. **12-Factor App**: Store config in environment
3. **Immutable Infrastructure**: Don't modify running containers
4. **Health Checks**: Implement readiness and liveness probes
5. **Graceful Shutdown**: Handle SIGTERM signals properly
6. **Logging**: Write logs to stdout/stderr for aggregation
7. **Metrics**: Expose Prometheus metrics for monitoring

**Database in Kubernetes Considerations:**

Running databases in Kubernetes requires careful planning:

**StatefulSet vs Deployment**:
- Use **StatefulSet** for production databases
- Provides stable network identity
- Ordered pod creation and deletion
- Stable persistent storage per pod
- Better for clustered databases (MySQL Galera, MongoDB replica sets)

**Persistent Storage**:
```yaml
volumeClaimTemplates:
- metadata:
    name: data
  spec:
    accessModes: [ "ReadWriteOnce" ]
    resources:
      requests:
        storage: 10Gi
```
- Use PersistentVolumes for production
- Regular backups are essential
- Test disaster recovery procedures

**High Availability**:
- Run multiple replicas with replication
- Use anti-affinity to spread across nodes
- Implement automated failover
- Monitor replication lag

**Alternative Approaches**:
- Use managed databases (AWS RDS, Google Cloud SQL)
- Run databases outside Kubernetes
- Use Kubernetes operators (Vitess, PostgreSQL Operator)

**Troubleshooting Multi-Tier Applications:**

**Check connectivity**:
```bash
# Test from frontend to database
kubectl exec -n namespace frontend-pod -- nc -zv database-service 3306

# Test DNS resolution
kubectl exec -n namespace frontend-pod -- nslookup database-service

# Check service endpoints
kubectl get endpoints -n namespace database-service
```

**Check logs**:
```bash
# Frontend logs
kubectl logs -n namespace -l app=frontend --tail=100

# Database logs
kubectl logs -n namespace -l app=database --tail=100

# Previous container logs (if crashed)
kubectl logs -n namespace pod-name --previous
```

**Check configuration**:
```bash
# Verify environment variables
kubectl exec -n namespace pod-name -- env | grep MYSQL

# Check mounted volumes
kubectl describe pod -n namespace pod-name | grep -A 10 Mounts
```

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 62](day-62.md) | [Day 64 →](../week-10/day-64.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
