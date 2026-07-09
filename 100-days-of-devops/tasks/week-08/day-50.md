# Day 50: Set Resource Limits in Kubernetes Cluster

## Task Overview

Configure resource constraints for Kubernetes pods to prevent performance issues and ensure stable cluster operations. Resource limits and requests control how much CPU and memory each container can use, preventing resource starvation and maintaining quality of service.

**Technical Specifications:**
- Pod: httpd-pod with httpd-container
- Image: httpd:latest
- Memory requests: 15Mi (guaranteed minimum)
- Memory limits: 20Mi (maximum allowed)
- CPU requests: 100m (0.1 core guaranteed)
- CPU limits: 100m (0.1 core maximum)

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Create pod manifest with resource specifications

```yaml
apiVersion: v1
kind: Pod
metadata:
    name: httpd-pod
    labels:
        app: httpd_pod
spec:
    containers:
        - name: httpd-container
          image: httpd:latest
          ports:
            - containerPort: 80
          resources:
            limits:
                cpu: 100m
                memory: 20Mi
            requests:
                cpu: 100m
                memory: 15Mi
```

Create a pod manifest file with resource specifications. The `resources` section defines both requests and limits for CPU and memory. **Requests** specify the minimum guaranteed resources that Kubernetes reserves for the container - the pod will only be scheduled on nodes that can satisfy these requests. **Limits** define the maximum resources the container can consume - if exceeded, the container may be throttled (CPU) or terminated (memory). The CPU is measured in millicores (100m = 0.1 core), while memory uses standard units (Mi = mebibytes). This configuration ensures the httpd container has guaranteed access to 15Mi of memory and 100m CPU while preventing it from exceeding 20Mi memory or 100m CPU.

**Step 2:** Apply the pod configuration to the cluster

```sh
kubectl apply -f pod.yml
```

Deploy the pod to the Kubernetes cluster using `kubectl apply`. This command submits the pod manifest to the Kubernetes API server, which then schedules the pod on an appropriate node. The scheduler considers the resource requests when placing the pod, ensuring only nodes with sufficient available resources are selected. The `-f` flag specifies the file containing the pod definition. Kubernetes will create the pod and start the httpd container with the defined resource constraints applied by the kubelet on the selected node.

**Step 3:** Verify pod creation and resource configuration

```sh
kubectl get pods
```

List all pods in the current namespace to confirm the httpd-pod was created successfully. The output shows pod name, ready status (containers running vs total), current status (Running, Pending, etc.), restart count, and age. A successfully created pod should show status as "Running" with "1/1" containers ready.

**Step 4:** Inspect detailed resource configuration (optional)

```sh
kubectl describe pod httpd-pod
```

Display comprehensive information about the pod including resource specifications, events, and current state. In the output, look for the "Containers" section which shows the configured resource requests and limits. The "Events" section reveals the scheduling and startup process, including any issues related to insufficient resources. The "QoS Class" field indicates the Quality of Service tier assigned based on resource configuration:
- **Guaranteed**: Requests equal limits for all resources
- **Burstable**: Requests less than limits (like this pod)
- **BestEffort**: No requests or limits set

**Step 5:** Monitor resource usage (optional)

```sh
# View current resource usage
kubectl top pod httpd-pod

# View node resource capacity and allocation
kubectl top nodes
```

Monitor actual resource consumption using the `kubectl top` command, which requires the Metrics Server to be installed in the cluster. The `top pod` command shows current CPU and memory usage for the specified pod, allowing you to compare actual usage against configured requests and limits. The `top nodes` command displays resource utilization across all nodes, helping you understand cluster capacity and identify resource pressure. This data is crucial for right-sizing resource specifications and capacity planning.

---

## Key Concepts

**Resource Types:**
- **CPU**: Measured in cores or millicores (1000m = 1 core). Compressible resource that can be throttled
- **Memory**: Measured in bytes (Ki, Mi, Gi, Ti). Non-compressible resource - exceeding limits causes OOM kills
- **Ephemeral Storage**: Temporary storage for containers (optional configuration)
- **Extended Resources**: Custom resources like GPUs (device-specific)

**Requests vs Limits:**
- **Requests**: Minimum guaranteed resources reserved during scheduling. Pod placement considers node available capacity
- **Limits**: Maximum resources container can use. CPU is throttled at limit, memory triggers OOM killer
- **Overcommitment**: Cluster can schedule more requested resources than physically available if limits exceed requests
- **Right-sizing**: Set requests to typical usage, limits to peak expected usage

**Quality of Service (QoS) Classes:**
- **Guaranteed**: All containers have equal requests and limits for CPU and memory. Highest priority, last to be evicted
- **Burstable**: At least one container has requests or limits. Medium priority, evicted before Guaranteed
- **BestEffort**: No requests or limits set. Lowest priority, first to be evicted under resource pressure

**Resource Management Best Practices:**
- Monitor actual resource usage before setting limits to avoid over/under-provisioning
- Set requests based on typical workload requirements for proper scheduling
- Set limits to prevent resource monopolization while allowing bursting
- Use LimitRanges to enforce default limits and constraints at namespace level
- Implement ResourceQuotas to control total resource consumption per namespace
- Consider horizontal pod autoscaling for variable workloads

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 49](../week-07/day-49.md) | [Day 51 →](day-51.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
