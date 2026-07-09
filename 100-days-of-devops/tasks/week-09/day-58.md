# Day 58: Deploy Grafana on Kubernetes Cluster

## Task Overview

Deploy Grafana, a popular open-source analytics and monitoring platform, on a Kubernetes cluster. This task demonstrates deploying production-grade applications with proper service exposure using NodePort, enabling external access to web-based applications running in the cluster.

**Technical Specifications:**
- Deployment name: grafana-deployment-datacenter
- Container image: grafana/grafana:latest
- Service type: NodePort
- Node port: 32000
- Application: Grafana monitoring and visualization platform

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Create a deployment manifest for Grafana

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: grafana-deployment-datacenter
  labels:
    app: grafana
spec:
  replicas: 1
  selector:
    matchLabels:
      app: grafana
  template:
    metadata:
      labels:
        app: grafana
    spec:
      containers:
      - name: grafana
        image: grafana/grafana:latest
        ports:
        - containerPort: 3000
          name: http-grafana
          protocol: TCP
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
```

Create a Deployment resource that manages the Grafana application. The deployment defines one replica of a pod running the official Grafana container image. The `selector.matchLabels` ensures the deployment manages pods with the label `app: grafana`. The container exposes port 3000, which is Grafana's default web interface port. Resource requests and limits ensure the application has adequate resources while preventing it from consuming excessive cluster resources.

**Step 2:** Create a NodePort service manifest

```yaml
---
apiVersion: v1
kind: Service
metadata:
  name: grafana-service
  labels:
    app: grafana
spec:
  type: NodePort
  selector:
    app: grafana
  ports:
  - port: 3000
    targetPort: 3000
    nodePort: 32000
    protocol: TCP
    name: http
```

Define a Service resource to expose the Grafana deployment outside the cluster. The `type: NodePort` makes the service accessible on a specific port (32000) on every cluster node's IP address. The `selector` matches pods with the label `app: grafana`, routing traffic to the Grafana pods. The `port` is the service's internal cluster port, `targetPort` is the container port (3000), and `nodePort` (32000) is the external port accessible from outside the cluster.

**Step 3:** Apply the configuration to the cluster

```bash
kubectl apply -f k3s-deployment.yaml
```

Deploy both the Grafana deployment and service to the Kubernetes cluster using a single YAML file containing both resources separated by `---`. The `kubectl apply` command creates or updates the resources declaratively. Kubernetes will schedule the Grafana pod on an available node, pull the Grafana image from Docker Hub if not cached, start the container, and create the NodePort service to route external traffic to the pod.

**Step 4:** Verify the deployment status

```bash
kubectl get deployments.apps
```

Check the status of all deployments in the current namespace. You should see `grafana-deployment-datacenter` with a READY status of 1/1, indicating one pod is running out of one desired. The AVAILABLE column shows how many replicas are available to serve traffic. If the deployment shows 0/1, the pod may still be pulling the image or starting up - wait a few moments and check again.

**Step 5:** Verify the service configuration

```bash
kubectl get svc
```

List all services in the namespace to confirm the NodePort service was created correctly. Look for the service with TYPE `NodePort` and note the PORT(S) column showing `3000:32000/TCP`. This indicates the service accepts traffic on port 32000 on any node and forwards it to port 3000 on the pods. The CLUSTER-IP shows the internal cluster IP address for service-to-service communication.

**Step 6:** Access the Grafana web interface

```bash
# Get node IP address
kubectl get nodes -o wide

# Access Grafana in browser (replace NODE_IP with actual node IP)
# http://NODE_IP:32000

# Or use port-forwarding for local access
kubectl port-forward deployment/grafana-deployment-datacenter 3000:3000
# Then access: http://localhost:3000
```

Access the Grafana web interface using either the NodePort or port-forwarding. For NodePort access, navigate to `http://<node-ip>:32000` in your browser. The default Grafana credentials are admin/admin (you'll be prompted to change the password on first login). Port-forwarding is useful for development when you don't have direct access to node IPs or when testing locally.

**Step 7:** Monitor pod logs and status

```bash
# View Grafana logs
kubectl logs deployment/grafana-deployment-datacenter

# Get detailed pod information
kubectl describe pod -l app=grafana

# Check resource usage
kubectl top pod -l app=grafana
```

These diagnostic commands help verify Grafana is running correctly. The logs command shows application startup messages and any errors. The describe command provides detailed pod information including events, which is useful for troubleshooting. The top command shows real-time CPU and memory usage (requires metrics-server to be installed in the cluster).

---

## Key Concepts

**Kubernetes Deployments:**
- **Purpose**: Manage stateless application replicas with declarative updates
- **Replicas**: Specify desired number of identical pods to maintain
- **Rolling Updates**: Update application versions without downtime
- **Rollback**: Revert to previous deployment versions if issues occur
- **Self-Healing**: Automatically replace failed pods to maintain desired state
- **Scaling**: Easily adjust replica count up or down based on demand

**Service Types in Kubernetes:**

**ClusterIP** (default):
- Exposes service on cluster-internal IP only
- Accessible only within the cluster
- Used for inter-service communication
- Example: Database services, internal APIs

**NodePort**:
- Exposes service on each node's IP at a static port (30000-32767 range)
- Makes service accessible from outside cluster via `<NodeIP>:<NodePort>`
- Automatically creates ClusterIP service as well
- Suitable for development and small-scale deployments

**LoadBalancer**:
- Exposes service externally using cloud provider's load balancer
- Provisions external IP address automatically
- Only works in cloud environments (AWS, GCP, Azure)
- Suitable for production workloads requiring high availability

**ExternalName**:
- Maps service to DNS name (CNAME record)
- Used to access external services via Kubernetes service abstraction
- No proxy or forwarding is configured

**Grafana Overview:**

Grafana is an open-source platform for monitoring and observability:
- **Data Visualization**: Create interactive dashboards with multiple chart types
- **Multi-Source**: Query data from Prometheus, InfluxDB, Elasticsearch, and more
- **Alerting**: Configure alerts based on metric thresholds and conditions
- **User Management**: Role-based access control for teams and organizations
- **Plugins**: Extend functionality with community and commercial plugins

**Typical Grafana Stack Architecture:**
```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Grafana   │────▶│  Prometheus  │────▶│ Kubernetes  │
│  (Queries)  │     │   (Metrics)  │     │   Metrics   │
└─────────────┘     └──────────────┘     └─────────────┘
```

**Production Deployment Considerations:**

For production Grafana deployments, consider:

**Persistent Storage**:
```yaml
volumeMounts:
- name: grafana-storage
  mountPath: /var/lib/grafana
volumes:
- name: grafana-storage
  persistentVolumeClaim:
    claimName: grafana-pvc
```
Store dashboards, users, and configuration persistently.

**ConfigMap for Configuration**:
```yaml
env:
- name: GF_SECURITY_ADMIN_PASSWORD
  valueFrom:
    secretKeyRef:
      name: grafana-secrets
      key: admin-password
```
Externalize configuration and credentials using ConfigMaps and Secrets.

**Ingress for HTTPS Access**:
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: grafana-ingress
spec:
  rules:
  - host: grafana.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: grafana-service
            port:
              number: 3000
```
Use Ingress for production with proper DNS and TLS certificates.

**Resource Management Best Practices:**
- Set memory requests based on expected dashboard complexity
- Monitor actual resource usage and adjust limits accordingly
- Use horizontal pod autoscaling for high-traffic environments
- Implement readiness and liveness probes for health checking

**Port Configuration:**
- Default Grafana port: 3000 (HTTP)
- NodePort range: 30000-32767 (Kubernetes default)
- Production: Use Ingress with port 80/443 instead of NodePort
- Load balancers provide better security and features than NodePort

**Application Deployment Patterns:**
- **Deployment**: For stateless apps like Grafana (can be easily replaced)
- **StatefulSet**: For stateful apps requiring stable network identity
- **DaemonSet**: For node-level services (monitoring agents, log collectors)
- **Job/CronJob**: For batch processing and scheduled tasks

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 57](day-57.md) | [Day 59 →](day-59.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
