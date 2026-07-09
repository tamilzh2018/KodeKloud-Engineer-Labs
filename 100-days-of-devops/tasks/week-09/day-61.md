# Day 61: Init Containers in Kubernetes

## Task Overview

Implement init containers in a Kubernetes deployment to perform pre-requisite setup tasks before the main application container starts. Init containers enable separation of initialization logic from application logic, ensuring proper environment preparation and dependency satisfaction before application startup.

**Technical Specifications:**
- Deployment name: ic-deploy-devops
- Init container: ic-msg-devops (debian:latest, writes initialization message)
- Main container: ic-main-devops (debian:latest, reads and displays message)
- Shared volume: ic-volume-devops (emptyDir type)
- Replicas: 1

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Create a deployment manifest with init containers

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ic-deploy-devops
  labels:
    app: ic-devops
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ic-devops
  template:
    metadata:
      labels:
        app: ic-devops
    spec:
      initContainers:
      - name: ic-msg-devops
        image: debian:latest
        command: ['/bin/bash', '-c', 'echo Init Done - Welcome to xFusionCorp Industries > /ic/media']
        volumeMounts:
        - name: ic-volume-devops
          mountPath: /ic
      containers:
      - name: ic-main-devops
        image: debian:latest
        command: ['/bin/bash', '-c', 'while true; do cat /ic/media; sleep 5; done']
        volumeMounts:
        - name: ic-volume-devops
          mountPath: /ic
      volumes:
      - name: ic-volume-devops
        emptyDir: {}
```

Create a deployment that demonstrates init container functionality. The `initContainers` section defines containers that run before the main application containers. The init container `ic-msg-devops` writes a welcome message to `/ic/media` file in a shared volume. The main container `ic-main-devops` continuously reads and displays this message every 5 seconds. Both containers mount the same `emptyDir` volume at `/ic`, enabling data sharing. The init container must complete successfully before the main container starts.

**Step 2:** Apply the deployment configuration

```bash
kubectl apply -f k3s-deployment.yaml
```

Deploy the configuration to the Kubernetes cluster. Kubernetes creates a pod with both init and main containers. The init container runs first, executes its command to write the message file, and exits. Only after the init container completes successfully (exit code 0) does Kubernetes start the main container. This sequential execution ensures the main application has all necessary prerequisites in place before starting.

**Step 3:** Verify the deployment was created

```bash
kubectl get deployments.apps
```

Check that the deployment was successfully created. You should see `ic-deploy-devops` with READY showing 1/1, indicating one replica is running. The deployment manages the pod lifecycle, ensuring the desired state is maintained. If you delete the pod, the deployment automatically creates a new one, running the init container again before starting the main container.

**Step 4:** Monitor pod creation and init container execution

```bash
# Watch pods in real-time
kubectl get pods -w

# Check pod status
kubectl get pods

# View detailed pod information
kubectl describe pod -l app=ic-devops
```

Observe the pod creation process to see init containers in action. Initially, the pod shows status `Init:0/1`, indicating 0 of 1 init containers have completed. When the init container is running, you'll see `Init:Running`. After successful completion, the status changes to `PodInitializing`, then `Running` once the main container starts. The `describe` command shows the init container section with its completion status and logs.

**Step 5:** Verify init container completed successfully

```bash
# View init container logs
kubectl logs <pod-name> -c ic-msg-devops

# Check init container status in pod description
kubectl describe pod <pod-name> | grep -A 20 "Init Containers"
```

Examine the init container logs and status to confirm it executed properly. The logs should be empty or show any output from the echo command (which redirects to a file, so stdout is empty). The `describe` command shows the init container's state as `Terminated` with `Reason: Completed` and `Exit Code: 0`, proving it ran successfully. If the exit code is non-zero, the pod would be stuck in init phase and continuously retry.

**Step 6:** Verify main container is running and displaying the message

```bash
# View main container logs
kubectl logs <pod-name> -c ic-main-devops

# Follow logs in real-time
kubectl logs -f <pod-name> -c ic-main-devops
```

Check the main container logs to verify it's reading the file created by the init container. You should see "Init Done - Welcome to xFusionCorp Industries" printed repeatedly every 5 seconds. The `-f` flag follows the log stream in real-time, allowing you to see new messages as they're written. This confirms data sharing between init and main containers via the shared volume worked correctly.

**Step 7:** Verify the shared volume contains the expected data

```bash
# Execute into the running container
kubectl exec -it <pod-name> -c ic-main-devops -- /bin/bash

# Inside the container, check the file
cat /ic/media

# Exit the container
exit
```

Directly inspect the shared volume by executing into the main container. The `cat /ic/media` command displays the file contents written by the init container. This hands-on verification confirms the volume mount worked correctly and data persists for the main container to access. The file exists only in the pod's emptyDir volume and is lost if the pod is deleted (emptyDir volumes are ephemeral, created when pod is assigned to a node and deleted when pod is removed).

**Step 8:** Test init container restart behavior

```bash
# Delete the pod to trigger recreation
kubectl delete pod -l app=ic-devops

# Watch the pod recreate
kubectl get pods -w

# Verify init container runs again
kubectl get pods
```

Demonstrate that init containers run every time a pod is created. When you delete the pod, the deployment controller creates a new one. The init container executes again, writing the message file before the main container starts. This ensures consistent initialization regardless of how many times the pod is recreated. If the init container fails, Kubernetes restarts it according to the pod's restartPolicy until it succeeds.

**Step 9:** View all pod events including init container execution

```bash
# Get events sorted by timestamp
kubectl get events --sort-by=.metadata.creationTimestamp | grep ic-deploy

# View detailed events from pod description
kubectl describe pod <pod-name>
```

Review Kubernetes events to see the complete pod lifecycle including init container execution. Events show when the init container starts, completes, and when the main container begins. This chronological view helps understand the execution flow and is invaluable for troubleshooting init container issues. Events remain available for about an hour, providing a historical record of pod activities.

**Step 10:** Clean up resources (optional)

```bash
# Delete the deployment
kubectl delete deployment ic-deploy-devops

# Verify deletion
kubectl get deployments
kubectl get pods
```

Remove the deployment and its associated resources when done. Deleting the deployment automatically deletes all pods it manages. This cleanup step is important in shared environments to avoid consuming cluster resources unnecessarily. The deployment, pods, and emptyDir volumes are all removed, though the deployment YAML file remains for future use.

---

## Key Concepts

**Init Containers Overview:**

Init containers are specialized containers that run before application containers in a pod:
- **Sequential Execution**: Run one at a time in the order defined
- **Completion Required**: Each must complete successfully before the next starts
- **Separation of Concerns**: Isolate initialization logic from application logic
- **Different Images**: Can use different images than main containers
- **Always Restart**: Always run on pod start, even if main containers are restarted

**Init Container vs Regular Container:**

| Aspect | Init Containers | Regular Containers |
|--------|----------------|-------------------|
| Execution | Sequential, before main containers | Parallel, after init containers |
| Lifecycle | Must complete and exit | Run continuously (or as defined) |
| Restart | On pod creation or when failed | Per restartPolicy setting |
| Probes | No readiness/liveness probes | Support readiness/liveness probes |
| Resources | Can request different resources | Standard resource management |
| Purpose | Setup, preparation, preconditions | Application workload |

**Common Use Cases:**

**Dependency Checking:**
```yaml
initContainers:
- name: wait-for-db
  image: busybox:1.35
  command: ['sh', '-c', 'until nslookup db-service; do echo waiting for db; sleep 2; done']
```
Wait for dependent services to become available before starting the application.

**Configuration Setup:**
```yaml
initContainers:
- name: setup-config
  image: busybox:1.35
  command: ['sh', '-c', 'cp /config-source/* /config-dest/']
  volumeMounts:
  - name: config-source
    mountPath: /config-source
  - name: config-dest
    mountPath: /config-dest
```
Copy or generate configuration files required by the application.

**Database Schema Migration:**
```yaml
initContainers:
- name: db-migration
  image: myapp/migrations:latest
  command: ['./run-migrations.sh']
  env:
  - name: DATABASE_URL
    valueFrom:
      secretKeyRef:
        name: db-credentials
        key: url
```
Run database migrations before the application starts.

**File Downloads:**
```yaml
initContainers:
- name: download-assets
  image: curlimages/curl:latest
  command: ['sh', '-c', 'curl -o /data/model.bin https://example.com/model.bin']
  volumeMounts:
  - name: data
    mountPath: /data
```
Download large files, ML models, or assets needed by the application.

**Permission Setup:**
```yaml
initContainers:
- name: fix-permissions
  image: busybox:1.35
  command: ['sh', '-c', 'chown -R 1000:1000 /data']
  volumeMounts:
  - name: data
    mountPath: /data
  securityContext:
    runAsUser: 0  # Run as root to change permissions
```
Fix file permissions on mounted volumes before non-root application containers start.

**Certificate Management:**
```yaml
initContainers:
- name: fetch-certs
  image: vault:latest
  command: ['vault', 'pki', 'issue', 'app-cert', 'common_name=app.example.com']
  volumeMounts:
  - name: certs
    mountPath: /certs
```
Fetch TLS certificates from a secrets manager before application startup.

**Init Container Execution Flow:**

```
Pod Created
    ↓
Init Container 1 Starts
    ↓
Init Container 1 Completes (exit 0)
    ↓
Init Container 2 Starts
    ↓
Init Container 2 Completes (exit 0)
    ↓
Init Container N Completes (exit 0)
    ↓
Main Containers Start (parallel)
    ↓
Pod Running
```

**Failure Handling:**

If an init container fails (non-zero exit code):
- Kubernetes restarts the init container according to the pod's `restartPolicy`
- `restartPolicy: Always` or `OnFailure`: Init container restarts
- `restartPolicy: Never`: Pod fails, won't restart
- Subsequent init containers don't run until the failed one succeeds
- Main containers never start if any init container fails

**Resource Management:**

Init containers can have different resource requirements:
```yaml
initContainers:
- name: heavy-setup
  image: debian:latest
  resources:
    requests:
      memory: "512Mi"
      cpu: "500m"
    limits:
      memory: "1Gi"
      cpu: "1000m"
containers:
- name: app
  image: myapp:latest
  resources:
    requests:
      memory: "128Mi"
      cpu: "100m"
    limits:
      memory: "256Mi"
      cpu: "200m"
```

**Pod Resource Calculation:**
- **Highest init container requests**: Used during init phase
- **Sum of main container requests**: Used during running phase
- **Effective pod request**: Maximum of these two values

**Volume Sharing:**

Init and main containers share volumes for data exchange:

**emptyDir** (temporary, pod-lifetime):
```yaml
volumes:
- name: shared-data
  emptyDir: {}
```
- Created when pod starts, deleted when pod terminates
- Perfect for init containers that prepare data for main containers
- Lost on pod deletion or node failure

**Persistent Volume** (permanent):
```yaml
volumes:
- name: persistent-data
  persistentVolumeClaim:
    claimName: my-pvc
```
- Data survives pod restarts and deletions
- Useful when init containers prepare data that should persist

**ConfigMap/Secret** (read-only):
```yaml
volumes:
- name: config
  configMap:
    name: app-config
```
- Init containers can read configuration
- Cannot modify (mounted read-only)

**Best Practices:**

1. **Keep Init Containers Simple**: Single responsibility per init container
2. **Fast Execution**: Minimize startup time to reduce pod creation latency
3. **Idempotent Operations**: Safe to run multiple times without side effects
4. **Proper Error Handling**: Exit with appropriate codes (0 for success, non-zero for failure)
5. **Logging**: Log progress for troubleshooting
6. **Timeouts**: Set reasonable timeouts for network operations
7. **Resource Limits**: Prevent init containers from consuming excessive resources
8. **Specific Image Tags**: Avoid 'latest' tag for reproducibility

**Debugging Init Containers:**

```bash
# Check which init container is running
kubectl get pod <pod-name> -o jsonpath='{.status.initContainerStatuses[*].name}'

# View init container status
kubectl get pod <pod-name> -o jsonpath='{.status.initContainerStatuses[*].state}'

# Get init container logs
kubectl logs <pod-name> -c <init-container-name>

# Get previous init container logs (if restarted)
kubectl logs <pod-name> -c <init-container-name> --previous

# Describe pod for events and status
kubectl describe pod <pod-name>
```

**Init Container vs Sidecar:**

Init containers and sidecar containers serve different purposes:

**Init Containers:**
- Run to completion before main containers
- Sequential execution
- Used for setup and preconditions
- Temporary, exit after task completion

**Sidecar Containers:**
- Run alongside main containers
- Parallel execution
- Provide supporting functionality (logging, proxies, monitoring)
- Long-running, same lifecycle as main container

**Security Considerations:**

Init containers often need elevated privileges:
```yaml
initContainers:
- name: setup
  image: busybox:1.35
  securityContext:
    runAsUser: 0  # Root for permission changes
    capabilities:
      add: ["CHOWN", "FOWNER"]
  command: ['sh', '-c', 'chown -R 1000:1000 /data']
```

- Grant minimum required privileges
- Use specific capabilities instead of full root
- Audit init container actions
- Scan init container images for vulnerabilities

**Multiple Init Containers Example:**

```yaml
initContainers:
- name: check-db
  image: postgres:15
  command: ['pg_isready', '-h', 'db-service', '-U', 'postgres']
- name: run-migrations
  image: myapp/migrations:1.0
  command: ['./migrate.sh']
- name: download-assets
  image: curlimages/curl:latest
  command: ['sh', '-c', 'curl -o /assets/logo.png https://cdn.example.com/logo.png']
```

Each init container handles a specific initialization task, running in sequence.

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 60](day-60.md) | [Day 62 →](day-62.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
