# Day 64: Fix Python App Deployed on Kubernetes Cluster

## Task Overview

Troubleshoot and repair a broken Python Flask application deployment in Kubernetes. The application has misconfigurations preventing it from running correctly and being accessible through the NodePort service.

**Technical Specifications:**
- Deployment name: `python-deployment-devops`
- Container image: `poroko/flask-demo-app` (currently misconfigured)
- NodePort: `32345`
- Target port: Flask default port `5000`
- Service name: `python-service-devops`

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Check pod status to identify issues

```sh
kubectl get pods
kubectl describe pod <pod-name>
```

List all pods in the default namespace and examine detailed information about the failing pod. The `kubectl get pods` command shows the overall status (Running, Pending, ImagePullBackOff, etc.), while `kubectl describe pod` provides comprehensive details including events, which are crucial for troubleshooting. Replace `<pod-name>` with the actual pod name from the get pods output, which will follow the pattern `python-deployment-devops-<random-hash>`.

**Step 2:** Analyze the error messages

```output
Events:
  Type     Reason     Age                    From               Message
  ----     ------     ----                   ----               -------
  Normal   Scheduled  37m                    default-scheduler  Successfully assigned default/python-deployment-devops-678b746b7-f25jg to kodekloud-control-plane
  Normal   Pulling    36m (x4 over 37m)      kubelet            Pulling image "poroko/flask-app-demo"
  Warning  Failed     36m (x4 over 37m)      kubelet            Failed to pull image "poroko/flask-app-demo": rpc error: code = Unknown desc = failed to pull and unpack image "docker.io/poroko/flask-app-demo:latest": failed to resolve reference "docker.io/poroko/flask-app-demo:latest": pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed
  Warning  Failed     36m (x4 over 37m)      kubelet            Error: ErrImagePull
  Warning  Failed     36m (x6 over 37m)      kubelet            Error: ImagePullBackOff
  Normal   BackOff    2m45s (x152 over 37m)  kubelet            Back-off pulling image "poroko/flask-app-demo"
```

The events section reveals the root cause: the deployment is attempting to pull `poroko/flask-app-demo` but this image doesn't exist or is inaccessible. The correct image name is `poroko/flask-demo-app` (note the reversed order of "demo" and "app"). The `ImagePullBackOff` error indicates Kubernetes has given up trying to pull the image after multiple failures and is backing off with exponential delay before retrying.

**Step 3:** Export deployment configuration to file

```sh
kubectl get deployments.apps python-deployment-devops -o yaml > k3s-deployment.yaml
```

Extract the current deployment configuration in YAML format and save it to a local file. This command queries the Kubernetes API for the deployment object and outputs its complete specification in YAML format, which can then be edited and reapplied. The `-o yaml` flag specifies the output format, and the `>` operator redirects the output to a file named `k3s-deployment.yaml` for editing.

**Step 4:** Fix the container image name in the deployment

```sh
vi k3s-deployment.yaml
```

Open the deployment YAML file in the vi text editor. Navigate to the `spec.template.spec.containers` section and locate the `image:` field. Change the incorrect image name from `poroko/flask-app-demo` to the correct `poroko/flask-demo-app`. Save and exit the editor (press ESC, type `:wq`, and press ENTER). This correction ensures Kubernetes will pull the actual existing image from Docker Hub.

**Step 5:** Delete and recreate the deployment with corrected configuration

```sh
kubectl delete deployments.apps python-deployment-devops
kubectl apply -f k3s-deployment.yaml
```

First, delete the existing broken deployment to ensure a clean slate, then apply the corrected deployment configuration. The `kubectl delete` command removes the deployment and its associated pods. The `kubectl apply` command creates resources from the YAML file, automatically detecting whether to create new resources or update existing ones. Wait 1-2 minutes for Kubernetes to pull the image, create new pods, and start the containers.

**Step 6:** Verify pods are running successfully

```sh
kubectl get pods
```

Check that the new pods are in the `Running` state with all containers ready (1/1). If pods are still in `ContainerCreating` status, wait a few more seconds. The output should show something like `python-deployment-devops-<hash> 1/1 Running 0 30s`, indicating one container is ready out of one total container, the pod is running, there have been zero restarts, and it's been running for 30 seconds.

**Step 7:** Examine the service configuration

```sh
kubectl get svc
```

List all services to check the service configuration and port mappings. Look for the `python-service-devops` service and verify its type, cluster IP, and port configuration. The output shows the service is type NodePort with port 8080 mapped to NodePort 32345.

**Step 8:** Identify service port misconfiguration

```output
NAME                    TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
kubernetes              ClusterIP   10.96.0.1       <none>        443/TCP          23m
python-service-devops   NodePort    10.96.109.187   <none>        8080:32345/TCP   12m
```

The service is listening on port 8080 and forwarding to NodePort 32345, but Flask applications typically run on port 5000 by default. The service needs to be reconfigured to forward traffic to the correct target port (5000) where the Flask application is actually listening inside the container. The format `8080:32345` means the service accepts traffic on port 8080 and makes it available externally on NodePort 32345.

**Step 9:** Export service configuration to file

```sh
kubectl get svc python-service-devops -o yaml > k3s-service.yaml
```

Extract the current service configuration in YAML format and save it to a file for editing. This exports the complete service specification including its type, ports, selectors, and other settings. You can now modify this file to fix the port configuration issue.

**Step 10:** Fix the target port in the service configuration

```sh
vi k3s-service.yaml
```

Open the service YAML file in vi editor. Navigate to the `spec.ports` section and locate the `targetPort:` field. Change it from `8080` to `5000` (Flask's default port). The `targetPort` is the port where the application inside the container is listening, while `port` is the port the service exposes. Also verify the `nodePort` is set to `32345` as required. Save and exit (ESC, `:wq`, ENTER).

**Step 11:** Apply the corrected service configuration

```sh
kubectl apply -f k3s-service.yaml
```

Update the service with the corrected port configuration. The `kubectl apply` command updates the existing service with the new targetPort setting. Kubernetes will automatically update the service endpoints to route traffic to port 5000 on the pod containers. This change takes effect immediately without requiring a service restart.

**Step 12:** Verify the service is correctly configured

```sh
kubectl get svc
```

Confirm the service configuration has been updated. You can also test accessing the application at `http://<node-ip>:32345` to verify it's working. The service should now properly route traffic from NodePort 32345 to the Flask application listening on port 5000 inside the container.

---

## Key Concepts

**Common Kubernetes Application Issues:**
- **Image Pull Errors**: Incorrect image names, tags, or registry authentication issues
- **Port Mismatches**: Service targetPort must match the container's listening port
- **Container Crashes**: Application errors, missing dependencies, or configuration issues
- **Resource Constraints**: Insufficient CPU/memory causing pod eviction

**Debugging Workflow:**
1. Check pod status with `kubectl get pods`
2. Examine events with `kubectl describe pod`
3. Review logs with `kubectl logs <pod-name>`
4. Verify service endpoints with `kubectl get endpoints`
5. Test connectivity with `kubectl port-forward` or `kubectl exec`

**Service Port Types:**
- **port**: The port the service exposes internally within the cluster
- **targetPort**: The port on the container where the application listens
- **nodePort**: The port exposed on each cluster node (30000-32767 range)

**Best Practices:**
- Always verify image names and tags before deployment
- Use `kubectl describe` to investigate pod failures
- Match service targetPort with container application port
- Export configurations to files for version control and review
- Test applications after deployment changes

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 63](../week-09/day-63.md) | [Day 65 →](day-65.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
