# Day 51: Execute Rolling Updates in Kubernetes

## Task Overview

Perform a rolling update to deploy a new application version with zero downtime. Rolling updates gradually replace old pods with new ones, ensuring the application remains available throughout the update process.

**Technical Specifications:**
- Deployment: nginx-deployment (existing)
- Current image: nginx:1.16
- Target image: nginx:1.18
- Update strategy: RollingUpdate (gradual pod replacement)
- Requirement: Zero downtime, all pods operational after update

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Verify existing deployment status

```sh
kubectl get deployments.apps
```

```
NAME               READY   UP-TO-DATE   AVAILABLE   AGE
nginx-deployment   3/3     3            3           4m33s
```

List all deployments in the current namespace to confirm the nginx-deployment exists and check its current state. The output shows the deployment name, ready replicas (3/3 means 3 out of 3 desired replicas are ready), up-to-date replicas (reflecting latest pod template), available replicas (ready to serve traffic), and deployment age. The "READY" column showing "3/3" indicates all replica pods are currently running and healthy, confirming the deployment is in a stable state before performing the update.

**Step 2:** List running pods managed by the deployment

```sh
kubectl get pods
```

```
NAME                               READY   STATUS    RESTARTS   AGE
nginx-deployment-989f57c54-mnznk   1/1     Running   0          4m52s
nginx-deployment-989f57c54-sqf5h   1/1     Running   0          4m52s
nginx-deployment-989f57c54-vgjd8   1/1     Running   0          4m52s
```

Display all pods to see the individual pod instances created by the deployment. Each pod name includes the deployment name, ReplicaSet hash (989f57c54), and a unique suffix. The "READY" column shows "1/1" meaning one container is running out of one total container per pod. The "STATUS" shows all pods are "Running", and "RESTARTS" shows no crashes have occurred. All three pods share the same ReplicaSet hash, indicating they were created from the same pod template version.

**Step 3:** Inspect current pod configuration and image version

```sh
kubectl describe pod nginx-deployment-989f57c54-mnznk
```

Display detailed information about a specific pod to verify the current configuration, especially the container image version. The describe output includes pod metadata (name, namespace, labels), scheduling information (node assignment), container specifications, and event history. In the "Containers" section, look for the "Image" field which shows `nginx:1.16` - this is the current version that needs to be updated. The "Events" section at the bottom shows the pod lifecycle, including when it was scheduled, when the image was pulled, and when the container started. This verification step confirms what version is currently running before performing the update.

**Step 4:** Update the deployment image to nginx:1.18

```sh
kubectl set image deployment/nginx-deployment nginx-container=nginx:1.18
```

Update the container image in the deployment using the `kubectl set image` command. The syntax is `deployment/deployment-name container-name=new-image:tag`. This command modifies the deployment's pod template to use the new image version. Kubernetes immediately begins a rolling update: it creates new pods with nginx:1.18 while gradually terminating old pods with nginx:1.16. The update respects the deployment's update strategy settings (maxSurge and maxUnavailable) to ensure continuous availability. The command returns immediately, but the actual rollout continues in the background as Kubernetes orchestrates the pod replacement process.

**Step 5:** Monitor the rollout progress and completion

```sh
kubectl rollout status deployment/nginx-deployment
```

Monitor the rolling update progress in real-time using `kubectl rollout status`. This command tracks the deployment update and displays messages as new pods are created and old pods are terminated. The output shows progression like "Waiting for deployment spec update to be observed...", "Waiting for deployment nginx-deployment rollout to finish: 1 out of 3 new replicas have been updated...", and finally "deployment nginx-deployment successfully rolled out" when complete. The command blocks until the rollout finishes or fails, making it perfect for automation scripts. Behind the scenes, Kubernetes is creating a new ReplicaSet with the nginx:1.18 image while scaling down the old ReplicaSet, ensuring the specified number of available pods is maintained throughout.

**Step 6:** Verify the update completed successfully (optional)

```sh
# Check deployment status
kubectl get deployments

# Verify all pods are running the new image
kubectl get pods

# Inspect a pod to confirm new image version
kubectl describe pod <new-pod-name> | grep Image:
```

Verify the update was successful by checking the deployment status and pod states. The `kubectl get deployments` command should show all replicas ready and up-to-date. The `kubectl get pods` command will display new pod names (with a different ReplicaSet hash) indicating they were created from the updated pod template. Use `kubectl describe pod` and grep for the Image field to confirm the pods are running nginx:1.18. You can also check the rollout history with `kubectl rollout history deployment/nginx-deployment` to see all revision numbers and change causes, providing a complete audit trail of deployment updates.

---

## Key Concepts

**Rolling Update Strategy:**
- **Zero Downtime**: Updates occur without service interruption by maintaining available pods during transition
- **Gradual Replacement**: Old pods are replaced incrementally, not all at once
- **Automatic Management**: Kubernetes handles pod creation, health checking, and old pod termination
- **Rollback Capability**: Failed updates can be automatically or manually rolled back to previous versions

**Update Configuration Parameters:**
- **maxUnavailable**: Maximum number or percentage of pods that can be unavailable during update (default: 25%)
- **maxSurge**: Maximum number or percentage of pods that can be created above desired count (default: 25%)
- **minReadySeconds**: Minimum time a pod should be ready without crashes before being considered available
- **progressDeadlineSeconds**: Maximum time for deployment to make progress before being considered failed (default: 600s)

**ReplicaSet Management:**
- **New ReplicaSet**: Created with updated pod template, scaled up during rollout
- **Old ReplicaSet**: Scaled down as new pods become ready, kept for rollback capability
- **Revision History**: Controlled by `revisionHistoryLimit` (default: 10 ReplicaSets retained)
- **Hash Suffix**: ReplicaSet names include pod template hash for uniqueness

**Health Checks During Updates:**
- **Readiness Probes**: Determine when new pods are ready to receive traffic
- **Liveness Probes**: Detect and restart unhealthy containers during and after update
- **Update Pausing**: Update automatically pauses if new pods fail health checks
- **Traffic Shifting**: Service endpoints updated to route traffic only to ready pods

**Rollout Commands:**
- `kubectl set image`: Update container image in deployment
- `kubectl rollout status`: Monitor update progress in real-time
- `kubectl rollout history`: View deployment revision history
- `kubectl rollout undo`: Rollback to previous revision
- `kubectl rollout pause/resume`: Manually control update progression

**Best Practices:**
- Always configure readiness probes to ensure traffic only routes to healthy pods
- Test updates in staging environment before production rollout
- Monitor application metrics during updates to detect issues early
- Use `--record` flag to annotate rollout history with change descriptions
- Set appropriate resource limits to handle temporary pod count increase during rollout
- Consider using progressive delivery tools (Argo Rollouts, Flagger) for advanced strategies like canary or blue-green deployments

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 50](day-50.md) | [Day 52 →](day-52.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
