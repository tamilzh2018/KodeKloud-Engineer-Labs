# Day 59: Troubleshoot Deployment Issues in Kubernetes

## Task Overview

Diagnose and fix a broken Redis deployment in a Kubernetes cluster. This task develops critical troubleshooting skills by identifying and resolving common deployment issues including misconfigured ConfigMap references and incorrect container image tags.

**Technical Specifications:**
- Deployment name: redis-deployment
- Issues: ConfigMap name mismatch, incorrect image tag
- Troubleshooting tools: kubectl describe, kubectl logs, kubectl get
- Resolution: YAML manifest correction and redeployment

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Check the pod status to identify issues

```bash
kubectl get pods
```

List all pods in the namespace to see their current status. You'll likely see the redis deployment pods in a non-running state such as `Pending`, `ContainerCreating`, or `ImagePullBackOff`. The STATUS column provides the first clue about what's wrong. If pods are stuck in `Pending` or `ContainerCreating`, it indicates issues with volume mounts, image pulls, or resource constraints. Take note of the exact pod name for detailed inspection in the next step.

**Step 2:** Get detailed pod information to diagnose the problem

```bash
kubectl describe pod <redis-deployment-pod-name>
```

Examine the detailed pod description, which includes configuration, events, and error messages. Look at the Events section at the bottom - this is where Kubernetes reports what's happening with the pod. In this case, you should see error messages like `MountVolume.SetUp failed for volume "config" : configmap "redis-cofig" not found`. This clearly indicates the pod is trying to mount a ConfigMap that doesn't exist, revealing a configuration error in the deployment specification.

**Step 3:** List ConfigMaps to verify available resources

```bash
kubectl get cm
```

Display all ConfigMaps in the namespace to see what's actually available. You should see a ConfigMap named `redis-config` (note the correct spelling). Comparing this with the error message from Step 2 reveals a typo: the deployment is looking for `redis-cofig` but the actual ConfigMap is named `redis-config`. This mismatch prevents the pod from starting because Kubernetes cannot find the referenced ConfigMap to mount into the container.

**Step 4:** Export the deployment configuration for editing

```bash
kubectl get deployment redis-deployment -o yaml > redis-deployment.yaml
```

Extract the current deployment specification to a YAML file for editing. The `-o yaml` flag outputs the deployment in YAML format, capturing the complete configuration including the error. Saving it to a file allows you to edit the configuration locally, track changes, and version control the fix. This is safer than using `kubectl edit` directly, as you have a backup and can review changes before applying them.

**Step 5:** Fix the ConfigMap name in the deployment YAML

Edit the `redis-deployment.yaml` file and locate the volumes section. Change:
```yaml
volumes:
- name: config
  configMap:
    name: redis-cofig  # Wrong - typo in name
```

To:
```yaml
volumes:
- name: config
  configMap:
    name: redis-config  # Correct - matches actual ConfigMap
```

Correct the typo in the ConfigMap name from `redis-cofig` to `redis-config` to match the actual ConfigMap resource in the cluster. This ensures the volume mount can successfully find and mount the ConfigMap data. Additionally, clean up any Kubernetes-generated fields like `resourceVersion`, `uid`, `creationTimestamp`, and `status` sections before reapplying to avoid conflicts.

**Step 6:** Apply the corrected configuration

```bash
kubectl apply -f redis-deployment.yaml
```

Apply the fixed deployment configuration to the cluster. Kubernetes will update the deployment with the corrected ConfigMap reference. This triggers a rolling update, creating new pods with the correct configuration while terminating the old broken pods. The deployment controller ensures zero-downtime updates by gradually replacing pods.

**Step 7:** Verify pods are starting and check for new issues

```bash
kubectl get pods
```

Monitor the pod status after applying the fix. You may see new pods with status `ImagePullBackOff` or `ErrImagePull`, indicating the next issue: the container image cannot be pulled. This happens because the deployment specifies an incorrect image tag `redis:alpin` (typo - should be `alpine`). The image pull error is now visible because we fixed the ConfigMap issue, demonstrating how problems can cascade.

**Step 8:** Fix the image tag in the deployment YAML

Edit `redis-deployment.yaml` again and locate the container image specification. Change:
```yaml
containers:
- name: redis-container
  image: redis:alpin  # Wrong - typo in tag
```

To:
```yaml
containers:
- name: redis-container
  image: redis:alpine  # Correct - valid image tag
```

Correct the image tag typo from `alpin` to `alpine`. The official Redis image uses the tag `alpine` for the Alpine Linux-based variant, which is a minimal Linux distribution that results in smaller container images. Using the correct tag allows Kubernetes to successfully pull the image from Docker Hub.

**Step 9:** Delete and recreate the deployment with all fixes

```bash
kubectl delete deployment redis-deployment
kubectl apply -f redis-deployment.yaml
```

Remove the existing deployment and create a new one with both fixes applied. While `kubectl apply` could update the deployment, deleting and recreating ensures a clean state and immediately applies all changes. The delete command removes the deployment and all its pods. The apply command then creates a fresh deployment with the corrected ConfigMap name and image tag, scheduling new pods that should start successfully.

**Step 10:** Verify the deployment is now healthy

```bash
# Check pod status
kubectl get pods

# Verify pod details
kubectl describe pod <redis-pod-name>

# Check container logs
kubectl logs <redis-pod-name>

# Test Redis functionality
kubectl exec <redis-pod-name> -- redis-cli ping
```

Perform comprehensive verification to ensure the deployment is fully operational. The pods should now show `Running` status. The describe command should show no error events. The logs should display normal Redis startup messages. The exec command tests Redis functionality by running the `redis-cli ping` command inside the container, which should return `PONG` if Redis is working correctly.

---

## Key Concepts

**Kubernetes Troubleshooting Methodology:**

Follow a systematic approach when troubleshooting Kubernetes issues:

1. **Identify Symptoms**: Check pod status with `kubectl get pods`
2. **Gather Information**: Use `kubectl describe` to see detailed information and events
3. **Analyze Logs**: Review container logs with `kubectl logs`
4. **Check Dependencies**: Verify ConfigMaps, Secrets, Services, and PVCs exist
5. **Test Incrementally**: Fix one issue at a time and verify
6. **Document Findings**: Keep track of what worked for future reference

**Common Pod States and Their Meanings:**

- **Pending**: Pod accepted but not scheduled (resource constraints, node selector mismatch)
- **ContainerCreating**: Pod scheduled, containers being created (image pull, volume mount issues)
- **Running**: All containers running successfully (normal healthy state)
- **Succeeded**: All containers terminated successfully (for Jobs)
- **Failed**: All containers terminated, at least one failed
- **Unknown**: Pod state cannot be determined (node communication issues)
- **CrashLoopBackOff**: Container repeatedly crashing and restarting
- **ImagePullBackOff**: Failed to pull container image (wrong image name/tag, registry auth)
- **Error**: Container failed to start or exited with error

**Common Kubernetes Deployment Issues:**

**ConfigMap/Secret Issues**:
- Referenced ConfigMap or Secret doesn't exist
- Typos in ConfigMap/Secret names
- Wrong namespace (ConfigMaps/Secrets are namespace-scoped)
- Missing required keys in ConfigMap/Secret

**Image Issues**:
- Incorrect image name or tag (typos like `alpin` instead of `alpine`)
- Image doesn't exist in the registry
- Missing authentication for private registries
- ImagePullPolicy conflicts (Always vs IfNotPresent)

**Resource Issues**:
- Insufficient CPU or memory on nodes
- Resource requests exceed node capacity
- Resource limits too restrictive for application
- No nodes match pod affinity/anti-affinity rules

**Volume Mount Issues**:
- PersistentVolume not bound to PersistentVolumeClaim
- HostPath pointing to non-existent directory
- Permission issues with volume mounts
- Volume already mounted by another pod (for ReadWriteOnce volumes)

**Network Issues**:
- Service selector doesn't match pod labels
- Wrong port configuration (port vs targetPort)
- Network policies blocking traffic
- DNS resolution failures

**Essential Troubleshooting Commands:**

**Pod Investigation**:
```bash
# List pods with wide output (shows node, IP)
kubectl get pods -o wide

# Watch pods in real-time
kubectl get pods -w

# Describe specific pod
kubectl describe pod <pod-name>

# Get pod YAML definition
kubectl get pod <pod-name> -o yaml

# Check previous container logs (if crashed)
kubectl logs <pod-name> --previous
```

**Events and Debugging**:
```bash
# View recent cluster events
kubectl get events --sort-by=.metadata.creationTimestamp

# View events for specific pod
kubectl describe pod <pod-name> | grep -A 10 Events

# Execute commands in running container
kubectl exec -it <pod-name> -- /bin/sh

# Port-forward to access application locally
kubectl port-forward <pod-name> 8080:80
```

**Resource Verification**:
```bash
# List all ConfigMaps
kubectl get configmaps

# List all Secrets
kubectl get secrets

# List all PersistentVolumeClaims
kubectl get pvc

# List all Services
kubectl get services
```

**Deployment Management**:
```bash
# View deployment status
kubectl get deployments

# Check deployment rollout status
kubectl rollout status deployment/<deployment-name>

# View deployment history
kubectl rollout history deployment/<deployment-name>

# Rollback to previous version
kubectl rollout undo deployment/<deployment-name>
```

**Best Practices for Preventing Issues:**

1. **Use declarative YAML files**: Store configurations in version control
2. **Validate YAML before applying**: Use `kubectl apply --dry-run=client -f file.yaml`
3. **Use specific image tags**: Avoid `latest` tag in production
4. **Implement health checks**: Add liveness and readiness probes
5. **Set resource requests/limits**: Prevent resource starvation
6. **Test in staging first**: Validate changes before production
7. **Monitor logs continuously**: Use logging solutions like EFK stack
8. **Document dependencies**: Clearly specify required ConfigMaps, Secrets, etc.

**Understanding Kubernetes Events:**

Events provide chronological information about cluster activities:
- **Normal events**: Scheduled, Pulling, Pulled, Created, Started
- **Warning events**: Failed, BackOff, FailedMount, FailedScheduling
- Events are retained for about 1 hour by default
- Events show the "what" and "when" but you need logs for the "why"

**Debugging Container Images:**

If you suspect image issues:
```bash
# Try pulling image manually
docker pull redis:alpine

# Verify image exists and check available tags
# Visit Docker Hub or use Docker CLI

# Use debug container with same image
kubectl run -it debug --image=redis:alpine --rm -- /bin/sh
```

**ConfigMap Troubleshooting:**

When ConfigMap issues occur:
```bash
# View ConfigMap contents
kubectl get configmap <name> -o yaml

# Describe ConfigMap
kubectl describe configmap <name>

# Edit ConfigMap directly
kubectl edit configmap <name>

# Create ConfigMap from file
kubectl create configmap <name> --from-file=<path>
```

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 58](day-58.md) | [Day 60 →](day-60.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
