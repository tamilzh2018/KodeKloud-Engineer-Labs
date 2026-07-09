# Day 48: Deploy Pods in Kubernetes Cluster

## Task Overview

Deploy containerized applications as Kubernetes pods, the smallest deployable units in a Kubernetes cluster. Pods encapsulate one or more containers with shared storage and network resources, providing a foundation for running applications in Kubernetes.

**Technical Specifications:**
- Pod name: pod-httpd
- Container image: httpd:latest
- Container name: httpd-container
- Label: app=httpd_app
- Kubernetes manifest: YAML configuration file
- Tool: kubectl (pre-configured on jump_host)

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Access the jump host

```sh
ssh user@jump_host
```

Connect to the jump host, which is a bastion server with kubectl pre-configured to communicate with the Kubernetes cluster. The jump host provides secure access to cluster management operations without exposing the Kubernetes API directly.

**Step 2:** Create a pod manifest file

```sh
vi k3s-pod.yml
```

Open a new YAML file in the vi text editor to define the pod specification. Add the following Kubernetes manifest:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-httpd
  labels:
    app: httpd_app
spec:
  containers:
    - name: httpd-container
      image: httpd:latest
      ports:
        - containerPort: 80
```

This YAML manifest defines a Kubernetes pod with the following structure:

- `apiVersion: v1`: Specifies the Kubernetes API version for Pod resources. The v1 API is stable and includes core resources like Pods, Services, and ConfigMaps.

- `kind: Pod`: Declares that this manifest creates a Pod resource, the smallest deployable unit in Kubernetes.

- `metadata`: Contains identifying information about the pod:
  - `name: pod-httpd`: Unique name for the pod within the namespace
  - `labels: app: httpd_app`: Key-value pairs used for organizing and selecting pods. Labels enable service discovery, monitoring, and management through selectors.

- `spec`: Defines the desired state of the pod:
  - `containers`: Array of container specifications (pods can have multiple containers)
    - `name: httpd-container`: Name of the container within the pod
    - `image: httpd:latest`: Container image to use (Apache HTTP Server)
    - `ports`: Array of ports the container exposes
      - `containerPort: 80`: Port on which the httpd service listens inside the container

Save and exit vi by pressing ESC, then typing `:wq` and pressing ENTER.

**Step 3:** Apply the pod configuration to the cluster

```sh
kubectl apply -f k3s-pod.yml
```

Submit the pod manifest to the Kubernetes cluster using kubectl. The `apply` command creates or updates resources defined in the YAML file. Kubernetes processes the manifest and:
1. Validates the YAML syntax and resource specifications
2. Schedules the pod to an available worker node
3. Pulls the httpd:latest image from Docker Hub (if not cached)
4. Creates the container with specified configuration
5. Attaches the pod to the cluster network
6. Starts the container and monitors its health

The output "pod/pod-httpd created" confirms successful pod creation. The pod transitions through several states: Pending (being scheduled), ContainerCreating (image pull and container creation), and Running (container started successfully).

**Step 4:** Verify the pod is running

```sh
kubectl get pods
```

List all pods in the current namespace (default namespace if not specified). The output displays:
- NAME: pod-httpd
- READY: 1/1 (one container ready out of one total)
- STATUS: Running
- RESTARTS: 0
- AGE: Time since pod creation

The "Running" status with "1/1" ready indicates the pod is healthy and the httpd container is operating normally.

**Step 5:** Get detailed pod information

```sh
kubectl describe pod pod-httpd
```

Display comprehensive information about the pod, including:
- Pod metadata (name, namespace, labels)
- Node assignment (which worker node hosts the pod)
- Container details (image, ports, environment variables)
- Conditions (PodScheduled, Initialized, ContainersReady, Ready)
- Events (pod scheduling, image pull, container creation timeline)

This command is invaluable for troubleshooting, showing exactly what happened during pod creation and any issues encountered.

**Step 6:** View pod logs

```sh
kubectl logs pod-httpd
```

Display the standard output (stdout) from the httpd-container. For the Apache HTTP server, this shows access logs, error logs, and server startup messages. Logs are essential for debugging application behavior and monitoring request traffic.

**Step 7:** Additional pod management commands

```bash
# Get pod with label selector
kubectl get pods -l app=httpd_app

# View pod in YAML format
kubectl get pod pod-httpd -o yaml

# View pod in JSON format
kubectl get pod pod-httpd -o json

# Watch pod status changes in real-time
kubectl get pods -w

# Execute command inside pod container
kubectl exec pod-httpd -- ls -la /usr/local/apache2/htdocs

# Get interactive shell in container
kubectl exec -it pod-httpd -- /bin/bash

# Test the web server from within cluster
kubectl run curl-test --image=curlimages/curl -i --rm --restart=Never -- curl http://pod-httpd

# Delete the pod
kubectl delete pod pod-httpd

# Delete using manifest file
kubectl delete -f k3s-pod.yml
```

These commands provide comprehensive pod management capabilities. Label selectors filter pods based on metadata. Output formats (-o yaml, -o json) enable scripting and automation. The watch flag (-w) continuously monitors pod status changes. The exec command runs commands inside containers or provides interactive shell access. Testing connectivity validates that the pod is accessible within the cluster network. Delete operations remove pods, either by name or by manifest file.

---

## Key Concepts

**Kubernetes Pods:**
- Smallest Unit: Basic building block of Kubernetes deployments
- Container Grouping: One or more containers sharing resources
- Shared Network: Containers in a pod share IP address and ports
- Shared Storage: Volumes can be mounted to multiple containers
- Ephemeral: Pods are disposable and replaceable
- Pod IP: Each pod receives a unique IP address in the cluster

**Pod Lifecycle:**
- Pending: Pod accepted by cluster, awaiting scheduling
- ContainerCreating: Kubelet pulling images and creating containers
- Running: All containers started, at least one still running
- Succeeded: All containers terminated successfully (for job-style pods)
- Failed: At least one container terminated with error
- Unknown: Pod state cannot be determined (communication failure)

**YAML Manifest Structure:**
- apiVersion: Kubernetes API version for the resource type
- kind: Resource type (Pod, Deployment, Service, etc.)
- metadata: Resource identification (name, namespace, labels, annotations)
- spec: Desired state specification (containers, volumes, etc.)

**Pod Specifications:**
- containers: List of container definitions
- name: Container name within the pod
- image: Container image with optional tag
- ports: Container ports (documentation and service integration)
- env: Environment variables
- resources: CPU and memory requests/limits
- volumeMounts: Volume mount points

**kubectl Commands:**
- apply: Create or update resources from manifest files
- get: List resources with basic information
- describe: Show detailed information about resources
- logs: Display container logs (stdout/stderr)
- exec: Execute commands inside containers
- delete: Remove resources from cluster
- edit: Modify resource definitions in-place

**Labels and Selectors:**
- Labels: Key-value pairs attached to objects for organization
- Selectors: Query labels to identify object groups
- Use Cases: Service endpoints, deployment management, monitoring
- Flexibility: Objects can have multiple labels
- Best Practice: Use consistent labeling scheme

**Pod Networking:**
- Cluster IP: Each pod gets unique IP address
- Container Communication: Containers in pod communicate via localhost
- Pod-to-Pod: Pods communicate using cluster networking
- DNS: Kubernetes provides DNS resolution for services
- Network Policies: Control traffic flow between pods

**Container Images:**
- Image Tags: Specify version (latest, 2.4, v1.0.0)
- Image Pull Policy: Always, IfNotPresent, Never
- Private Registries: Require imagePullSecrets
- Latest Tag: Convenient but not recommended for production
- Version Pinning: Use specific tags for consistency

**Best Practices:**
- Avoid latest tag: Use specific versions for reproducibility
- Set resource limits: Prevent resource contention
- Add health checks: Configure liveness and readiness probes
- Use labels: Enable flexible pod organization and selection
- Single responsibility: One main process per container
- Declarative config: Define desired state in YAML manifests

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 47](day-47.md) | [Day 49 →](day-49.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
