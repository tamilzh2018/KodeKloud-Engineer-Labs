# Day 52: Execute Rollback in Kubernetes Cluster

## Task Overview

Rollback a deployment to its previous version after discovering bugs or issues with the current release. Kubernetes maintains revision history enabling quick recovery from failed deployments without manual intervention.

**Technical Specifications:**
- Deployment: nginx-deployment (existing)
- Action: Rollback to previous revision
- Requirement: Restore previous working version quickly
- Zero downtime during rollback operation

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Verify current deployment and pod status

```sh
kubectl get deployments.apps
kubectl get pods
```

Check the current state of the deployment and its pods before performing the rollback. The `kubectl get deployments.apps` command displays the deployment's replica status, showing how many pods are ready, up-to-date, and available. The `kubectl get pods` command lists individual pod instances with their status, restart counts, and age. These commands help you confirm which deployment needs to be rolled back and verify that the current state is problematic (for example, pods might be in CrashLoopBackOff or the application might be reporting errors even though pods show as Running).

**Step 2:** Inspect pod details to identify the current image version

```sh
kubectl describe pod <pod-name>
```

Display detailed information about a running pod to confirm the current container image version that's causing issues. Replace `<pod-name>` with an actual pod name from the previous step. The describe command output includes comprehensive pod information - look for the "Containers" section which shows the "Image" field with the current version. The "Events" section at the bottom reveals the pod's history, potentially showing errors, failed health checks, or other issues that prompted the rollback decision. This verification step documents what version is currently deployed before rolling back.

**Step 3:** View deployment revision history (optional)

```sh
kubectl rollout history deployment/nginx-deployment
```

Display the revision history for the deployment to see all previous versions and their change causes. The output shows a table with revision numbers and change causes (if the `--record` flag was used during updates). This helps you understand what versions are available and confirm that a previous revision exists to rollback to. You can inspect a specific revision's details using `kubectl rollout history deployment/nginx-deployment --revision=2` to see exactly what configuration will be restored.

**Step 4:** Execute the rollback to previous revision

```sh
kubectl rollout undo deployment/nginx-deployment
```

Rollback the deployment to its immediately previous revision using `kubectl rollout undo`. This command triggers a new rolling update that reverts the pod template to the previous version. Kubernetes creates new pods using the old configuration while gradually terminating the problematic pods, maintaining availability throughout the rollback process. The undo operation works by scaling up the previous ReplicaSet (which was retained) and scaling down the current ReplicaSet. The rollback follows the same rolling update strategy (maxSurge, maxUnavailable) as forward updates, ensuring zero downtime during recovery.

**Step 5:** Monitor the rollback progress (optional)

```sh
kubectl rollout status deployment/nginx-deployment
```

Track the rollback operation in real-time using `kubectl rollout status`. This command monitors the deployment update and displays progress messages as pods are replaced with the previous version. The output shows status like "Waiting for rollout to finish...", the number of updated replicas, and finally "deployment nginx-deployment successfully rolled out" when the rollback completes. This blocking command is useful in scripts or manual operations where you need to wait for the rollback to finish before proceeding with other tasks.

**Step 6:** Verify rollback completed successfully

```sh
# Check deployment status
kubectl get deployments

# List pods to see new instances
kubectl get pods

# Confirm previous image version is restored
kubectl describe pod <new-pod-name> | grep Image:
```

Verify the rollback was successful by examining the deployment and pod states. The `kubectl get deployments` command should show all replicas ready and up-to-date with the previous version. The `kubectl get pods` command displays new pod instances (notice the different ReplicaSet hash in pod names) created during the rollback. Use `kubectl describe pod` to confirm the container image has been reverted to the previous working version. This verification ensures the application is now running the stable version and the problematic release has been replaced.

---

## Key Concepts

**Rollback Operations:**
- **Purpose**: Quickly revert to a previous stable version when issues are discovered in production
- **Automatic Trigger**: Can be configured to rollback automatically if new pods fail readiness checks
- **Manual Control**: DevOps teams can manually initiate rollbacks upon detecting problems
- **Speed**: Much faster than deploying fixes, as the previous version's ReplicaSet already exists

**Revision History Management:**
- **Revision Storage**: Kubernetes keeps old ReplicaSets (scaled to 0) for rollback capability
- **History Limit**: Controlled by `revisionHistoryLimit` in deployment spec (default: 10 revisions)
- **Revision Numbers**: Sequential numbers assigned to each deployment update
- **Change Cause**: Captured when using `kubectl apply --record` or through annotations

**Rollback Commands:**
- `kubectl rollout undo deployment/name`: Rollback to immediately previous revision
- `kubectl rollout undo deployment/name --to-revision=3`: Rollback to specific revision number
- `kubectl rollout history deployment/name`: View all revisions and their descriptions
- `kubectl rollout history deployment/name --revision=3`: Inspect specific revision details

**ReplicaSet Lifecycle:**
- **Current ReplicaSet**: The active ReplicaSet managing current pods (scaled to desired replica count)
- **Previous ReplicaSets**: Old ReplicaSets retained with 0 replicas for rollback capability
- **Rollback Process**: Previous ReplicaSet is scaled up while current is scaled down
- **Cleanup**: Old ReplicaSets beyond `revisionHistoryLimit` are automatically deleted

**Common Rollback Scenarios:**
- **Application Bugs**: Critical bugs discovered in new release after deployment
- **Performance Degradation**: New version causes unacceptable performance issues or high resource usage
- **Failed Health Checks**: New pods fail liveness or readiness probes repeatedly
- **Configuration Errors**: Incorrect environment variables or config causing application failures
- **Dependency Issues**: New version incompatible with dependent services or databases

**Rollback Best Practices:**
- Monitor deployments closely after updates to catch issues early
- Configure appropriate readiness probes to detect problems automatically
- Use `--record` flag during updates to track change causes in revision history
- Test rollback procedures in staging environment before production incidents
- Document rollback decisions and root causes for post-mortem analysis
- Consider implementing automatic rollback policies using admission controllers or GitOps tools
- Set appropriate `progressDeadlineSeconds` to detect stuck deployments
- Maintain sufficient `revisionHistoryLimit` to keep adequate rollback options

**Rollback Limitations:**
- Rollback only affects pod template (image, env vars, volumes) - not deployment-level settings like replica count
- StatefulSet rollbacks require additional care for data consistency
- External state changes (database migrations) may need manual intervention
- Cannot rollback beyond `revisionHistoryLimit` - old ReplicaSets are deleted

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 51](day-51.md) | [Day 53 →](day-53.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
