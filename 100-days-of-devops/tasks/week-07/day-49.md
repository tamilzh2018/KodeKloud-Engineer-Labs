# Day 49: Deploy Applications with Kubernetes Deployments

## Task Overview

Create a Kubernetes Deployment resource to manage application replicas with declarative updates. Deployments provide a higher-level abstraction than pods, offering features like rolling updates, rollback capabilities, and automated replica management.

**Technical Specifications:**
- Deployment name: nginx
- Container image: nginx:latest
- Replicas: 1 (scalable)
- Label selector: app=nginx
- Kubernetes manifest: YAML configuration file
- Tool: kubectl (pre-configured on jump_host)

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Access the jump host

```sh
ssh user@jump_host
```

Connect to the jump host server, which has kubectl configured to interact with the Kubernetes cluster. The jump host serves as the control plane access point for cluster management operations.

**Step 2:** Create a deployment manifest file

```sh
vi k3s-deployment.yml
```

Open a new YAML file in the vi text editor to define the deployment specification. Add the following Kubernetes manifest:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
  labels:
    app: nginx
spec:
  selector:
    matchLabels:
      app: nginx
  replicas: 1
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: nginx:latest
          ports:
            - containerPort: 80
```

This YAML manifest defines a Kubernetes Deployment with comprehensive configuration:

**API and Resource Definition:**
- `apiVersion: apps/v1`: Specifies the apps/v1 API group, which includes Deployments, ReplicaSets, and StatefulSets. This is the stable API version for deployment resources.
- `kind: Deployment`: Declares this manifest creates a Deployment resource, which manages ReplicaSets and provides declarative updates for pods.

**Metadata Section:**
- `name: nginx`: Unique identifier for the deployment within the namespace
- `labels: app: nginx`: Labels attached to the deployment object itself (not the pods). These help organize and query deployment resources.

**Deployment Specification (spec):**
- `selector`: Defines how the deployment identifies which pods it manages
  - `matchLabels: app: nginx`: The deployment manages all pods with the label `app=nginx`. This selector must match the pod template labels.

- `replicas: 1`: Specifies the desired number of pod instances. Kubernetes maintains exactly this many pods running at all times. If a pod fails, the deployment creates a replacement.

- `template`: Defines the pod template used to create new pods
  - `metadata`: Pod-level metadata
    - `labels: app: nginx`: Labels applied to pods created from this template. Must match the selector's matchLabels.
  - `spec`: Pod specification
    - `containers`: Array of container definitions within each pod
      - `name: nginx`: Container name within the pod
      - `image: nginx:latest`: Container image (nginx web server)
      - `ports`: Exposed ports
        - `containerPort: 80`: nginx listens on port 80 for HTTP requests

Save and exit vi by pressing ESC, then typing `:wq` and pressing ENTER.

**Step 3:** Apply the deployment to the cluster

```sh
kubectl apply -f k3s-deployment.yml
```

Submit the deployment manifest to the Kubernetes cluster. The `apply` command processes the YAML file and creates the deployment resource. Kubernetes then:
1. Validates the manifest syntax and configuration
2. Creates the Deployment object in the cluster
3. Creates a ReplicaSet to manage pod replicas
4. Schedules the specified number of pods (1 in this case)
5. Pulls the nginx:latest image from Docker Hub
6. Creates and starts the pod(s)
7. Continuously monitors and maintains the desired state

The output "deployment.apps/nginx created" confirms the deployment was successfully created. The deployment controller immediately begins creating the specified number of pod replicas.

**Step 4:** Verify the deployment was created

```sh
kubectl get deployments.apps
```

List all deployments in the current namespace. The output displays:
- NAME: nginx
- READY: 1/1 (one pod ready out of one desired)
- UP-TO-DATE: 1 (one pod at the current version)
- AVAILABLE: 1 (one pod available to serve traffic)
- AGE: Time since deployment creation

The "1/1" ready status indicates the deployment successfully created and started one pod, which is now running and healthy.

**Step 5:** View the deployment details

```sh
kubectl describe deployment nginx
```

Display comprehensive information about the deployment, including:
- Deployment metadata (name, namespace, labels, annotations)
- Replicas configuration (desired, current, updated, available)
- Selector (matchLabels criteria)
- Pod template specification (containers, images, ports)
- Conditions (Available, Progressing)
- Events (ScalingReplicaSet, replica creation timeline)

This detailed view shows the deployment's current state and history of scaling and update operations.

**Step 6:** Verify the associated ReplicaSet

```sh
kubectl get replicasets
```

List ReplicaSets created by the deployment. Each deployment creates at least one ReplicaSet to manage pod replicas. The output shows:
- NAME: nginx-<hash> (deployment name plus unique hash)
- DESIRED: 1
- CURRENT: 1
- READY: 1

The ReplicaSet is the mechanism that actually creates and maintains the pod replicas. Deployments manage ReplicaSets, which in turn manage pods.

**Step 7:** View the pods created by the deployment

```sh
kubectl get pods
```

List all pods to see the instances created by the deployment. The pod name follows the pattern: `nginx-<replicaset-hash>-<pod-hash>`. The output shows:
- NAME: nginx-xxxxxxxxxx-xxxxx
- READY: 1/1
- STATUS: Running
- RESTARTS: 0
- AGE: Time since creation

This pod was automatically created by the ReplicaSet, which was created by the Deployment. This three-tier hierarchy (Deployment > ReplicaSet > Pod) enables powerful management features.

**Step 8:** Additional deployment management commands

```bash
# Scale the deployment to 3 replicas
kubectl scale deployment nginx --replicas=3

# Verify scaling
kubectl get deployments
kubectl get pods

# Update the image to a specific version
kubectl set image deployment/nginx nginx=nginx:1.25

# Check rollout status
kubectl rollout status deployment/nginx

# View rollout history
kubectl rollout history deployment/nginx

# Rollback to previous version
kubectl rollout undo deployment/nginx

# Rollback to specific revision
kubectl rollout undo deployment/nginx --to-revision=2

# Pause a rollout (for canary deployments)
kubectl rollout pause deployment/nginx

# Resume a paused rollout
kubectl rollout resume deployment/nginx

# View deployment in YAML format
kubectl get deployment nginx -o yaml

# Edit deployment in-place
kubectl edit deployment nginx

# Delete the deployment (cascading delete of ReplicaSet and pods)
kubectl delete deployment nginx

# Delete using manifest file
kubectl delete -f k3s-deployment.yml
```

These commands demonstrate the full lifecycle management capabilities of Kubernetes Deployments. Scaling adjusts the number of replicas. Image updates trigger rolling updates with zero downtime. Rollout commands manage update progress and enable rollback to previous versions. Pause and resume enable canary deployment strategies. Delete operations remove the entire hierarchy (deployment, ReplicaSet, and pods).

---

## Key Concepts

**Kubernetes Deployments:**
- Purpose: Declarative updates for pods and ReplicaSets
- Replica Management: Maintains specified number of pod instances
- Rolling Updates: Update pods gradually with zero downtime
- Rollback: Easy revert to previous application versions
- Self-Healing: Automatically replaces failed pods
- Higher Abstraction: Preferred over managing ReplicaSets directly

**Deployment Architecture:**
- Three-Tier Hierarchy: Deployment > ReplicaSet > Pod
- Deployment: Declares desired state and update strategy
- ReplicaSet: Ensures specified number of pod replicas exist
- Pod: Runs the actual application containers
- Automatic Management: Deployment creates and manages ReplicaSets

**Deployment Components:**
- Selector: Identifies which pods belong to this deployment
- Replicas: Desired number of pod instances
- Template: Pod specification for creating instances
- Strategy: Update strategy (RollingUpdate or Recreate)
- Revision History: Tracks deployment versions for rollback

**Labels and Selectors:**
- Label Declaration: Defined in template.metadata.labels
- Selector Match: spec.selector.matchLabels must match template labels
- Immutability: Selector cannot be changed after deployment creation
- Loose Coupling: Enables flexible pod association
- Multi-Criteria: Can match multiple label key-value pairs

**Rolling Update Strategy:**
- Default Behavior: Gradually replace old pods with new ones
- Zero Downtime: Old pods remain available until new ones are ready
- MaxSurge: Maximum additional pods created during update
- MaxUnavailable: Maximum pods that can be unavailable during update
- Progressive Rollout: Update happens incrementally across replicas

**Rollback Capabilities:**
- Revision History: Deployment stores previous ReplicaSet versions
- Undo Command: Quickly revert to previous working version
- Specific Revision: Rollback to any stored revision number
- Automatic Retention: Limited number of revisions kept (default 10)
- Quick Recovery: Essential for production incident response

**Scaling Operations:**
- Horizontal Scaling: Add or remove pod replicas
- Declarative: Update replicas in manifest and reapply
- Imperative: Use kubectl scale command for quick adjustments
- Automatic Scaling: Use HorizontalPodAutoscaler for auto-scaling
- Load Distribution: More replicas distribute traffic and load

**Deployment States:**
- Progressing: Deployment is actively updating or scaling
- Available: Minimum required replicas are available
- Complete: All replicas updated to desired state
- Failed: Update cannot complete (image pull errors, etc.)
- ReplicaFailure: Cannot create required replicas

**Update Strategies:**
- RollingUpdate (default): Gradual replacement with zero downtime
  - maxSurge: Extra pods during update (25% default)
  - maxUnavailable: Pods that can be down (25% default)
- Recreate: Terminate all old pods before creating new ones
  - Simpler but causes downtime
  - Useful when zero downtime isn't critical

**Best Practices:**
- Use Deployments, Not Pods: Leverage management features
- Specific Image Tags: Avoid 'latest' tag for production
- Resource Limits: Set CPU and memory requests/limits
- Health Probes: Configure liveness and readiness checks
- Label Strategy: Use consistent, meaningful labels
- Replica Count: Run multiple replicas for high availability
- Rollout Strategy: Test updates in staging before production
- Monitor Rollouts: Watch rollout status and check for issues

**Deployment vs Pod:**
- Deployments: Managed, self-healing, versioned, scalable
- Pods: Ephemeral, manual recreation, no built-in scaling
- Production Use: Always use Deployments for stateless apps
- Development: Pods acceptable for quick testing
- StatefulSets: Alternative for stateful applications

**ReplicaSet Role:**
- Created by Deployment: Deployments create and manage ReplicaSets
- Replica Maintenance: Ensures desired number of pods exist
- Version Tracking: Each deployment update creates new ReplicaSet
- Old ReplicaSets: Kept for rollback (scaled to 0 replicas)
- Direct Management: Rarely need to interact with ReplicaSets directly

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 48](day-48.md) | [Day 50 →](../week-08/day-50.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
