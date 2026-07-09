# Day 55: Kubernetes Sidecar Containers

## Task Overview

Implement the sidecar pattern by deploying a multi-container pod where a helper container continuously reads and displays logs from the main nginx web server. This demonstrates the separation of concerns principle in container design.

**Technical Specifications:**
- Pod: webserver
- Main container: nginx-container (nginx:latest, serves web content)
- Sidecar container: sidecar-container (ubuntu:latest, reads nginx logs)
- Shared volume: shared-logs (emptyDir, mounted at /var/log/nginx)
- Sidecar command: Continuously output access and error logs every 30 seconds

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Create pod manifest with sidecar configuration

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: webserver
  labels:
    app: nginx
spec:
  containers:
  - name: nginx-container
    image: nginx:latest
    volumeMounts:
    - name: shared-logs
      mountPath: /var/log/nginx
  - name: sidecar-container
    image: ubuntu:latest
    command: ['sh', '-c', 'while true; do cat /var/log/nginx/access.log /var/log/nginx/error.log; sleep 30; done']
    volumeMounts:
    - name: shared-logs
      mountPath: /var/log/nginx
  volumes:
  - name: shared-logs
    emptyDir: {}
```

Create a pod manifest implementing the sidecar pattern with two containers sharing a log volume. The **nginx-container** runs the nginx web server using the official nginx:latest image. Nginx automatically writes access logs and error logs to `/var/log/nginx/access.log` and `/var/log/nginx/error.log` respectively. The **sidecar-container** runs Ubuntu with a custom command that continuously monitors these log files. The command uses an infinite while loop (`while true`) to repeatedly read both log files using `cat`, then sleeps for 30 seconds before repeating. Both containers mount the same **shared-logs** emptyDir volume at `/var/log/nginx`, enabling the sidecar to access logs written by nginx. This architecture separates concerns: nginx focuses solely on serving web content, while the sidecar specializes in log processing and aggregation.

**Step 2:** Deploy the pod to the cluster

```sh
kubectl apply -f k3s-pod.yml
```

Apply the pod configuration to create it in the Kubernetes cluster. The `kubectl apply` command submits the pod specification to the API server, which schedules the pod on an available node. The kubelet on that node creates the shared emptyDir volume, pulls both container images (nginx:latest and ubuntu:latest) if not already cached, and starts both containers simultaneously. The containers begin running in parallel: nginx starts its web server and immediately begins writing to its log files, while the sidecar container starts its infinite loop to read and display those logs. The shared volume ensures that as nginx writes logs, the sidecar can read them in real-time.

**Step 3:** Verify both containers are running (optional)

```sh
kubectl get pods
```

Check the pod status to confirm both containers started successfully. The output should show the webserver pod with "2/2" in the READY column, indicating both the nginx-container and sidecar-container are running. The STATUS should be "Running". If you see "1/2" or "0/2", one or both containers failed to start - use `kubectl describe pod webserver` to investigate. The AGE column shows how long the pod has been running, which is useful for monitoring log accumulation.

**Step 4:** View the sidecar container logs (optional)

```sh
kubectl logs webserver -c sidecar-container
```

Display the output from the sidecar container to see the nginx logs it's reading. The `kubectl logs` command retrieves container stdout/stderr. The `-c sidecar-container` flag specifies which container's logs to view (required for multi-container pods). The output shows the contents of nginx's access.log and error.log files as read by the sidecar's `cat` command every 30 seconds. Initially, you might see empty output or error messages like "cat: /var/log/nginx/access.log: No such file or directory" if nginx hasn't received requests yet. As traffic reaches nginx, you'll see log entries appearing in the sidecar's output.

**Step 5:** Generate traffic to produce logs (optional)

```sh
# Get the pod IP
kubectl get pod webserver -o wide

# Send requests to nginx (from within cluster or using port-forward)
kubectl exec webserver -c nginx-container -- curl localhost

# Or use port-forward for external access
kubectl port-forward webserver 8080:80
# Then in another terminal: curl http://localhost:8080
```

Generate HTTP requests to nginx to populate the access logs, making the sidecar's purpose more visible. The `kubectl exec` command sends a curl request from within the nginx container to itself, creating access log entries. Alternatively, use `kubectl port-forward` to expose nginx on your local machine's port 8080, then send requests using curl or a browser. Each request generates a log entry that nginx writes to `/var/log/nginx/access.log`, which the sidecar reads and outputs every 30 seconds.

**Step 6:** Monitor real-time log output (optional)

```sh
kubectl logs -f webserver -c sidecar-container
```

Follow the sidecar logs in real-time to observe the continuous log aggregation. The `-f` flag (follow) keeps the connection open and streams new log output as it appears, similar to `tail -f`. You'll see the sidecar outputting the log file contents every 30 seconds. As you generate traffic to nginx, new access log entries appear in subsequent iterations. Press Ctrl+C to stop following the logs. This demonstrates how the sidecar pattern enables log aggregation without modifying the main application - nginx remains completely unaware of the sidecar container reading its logs.

---

## Key Concepts

**Sidecar Pattern:**
- **Definition**: Helper container that extends or enhances the main application container's functionality
- **Separation of Concerns**: Each container has a single, well-defined responsibility
- **Shared Resources**: Sidecar and main container share pod network, volumes, and lifecycle
- **Independence**: Sidecar can be updated, replaced, or configured without changing main application
- **Reusability**: Same sidecar containers can be used across different applications

**Sidecar Use Cases:**
- **Log Aggregation**: Collect, process, and forward logs to centralized logging systems (Fluentd, Logstash)
- **Monitoring & Metrics**: Export application metrics to monitoring systems (Prometheus exporters)
- **Service Mesh**: Handle service-to-service communication, TLS, retries (Envoy, Linkerd)
- **Configuration Sync**: Keep configuration files updated from external sources
- **Security**: Add authentication, authorization, or encryption layers
- **Backup**: Periodically backup application data to external storage

**Log Shipping Sidecar:**
- **Purpose**: Forward logs from applications that write to files or stdout
- **Benefits**: Centralized logging without modifying application code
- **Tools**: Fluentd, Filebeat, Logstash commonly used as log shipping sidecars
- **Processing**: Can parse, filter, transform logs before forwarding
- **Destinations**: Send to Elasticsearch, S3, CloudWatch, Splunk, etc.

**Shared Volume Requirements:**
- **Same Volume**: Both containers must reference the same volume name in volumeMounts
- **Same Mount Path**: For log access, mount at the path where app writes logs (/var/log/nginx)
- **emptyDir Lifecycle**: Logs exist only for pod lifetime, not persistent across pod recreation
- **Volume Type Choice**: Use emptyDir for ephemeral logs, PVC for persistent log storage

**Container Communication in Pods:**
- **Shared Network Namespace**: Containers can communicate via localhost (127.0.0.1)
- **Shared Volumes**: Primary method for sharing files and data
- **Shared IPC**: Inter-process communication namespace (optional, via shareProcessNamespace)
- **Localhost Ports**: Main app and sidecar can bind to different ports on localhost
- **DNS Resolution**: Both containers resolve same service names to same IPs

**Sidecar vs Init Containers:**
- **Sidecar Containers**: Run alongside main container for entire pod lifetime
- **Init Containers**: Run sequentially before main containers, then terminate
- **Lifecycle**: Sidecars start with main containers; init containers run to completion first
- **Use Cases**: Sidecars for ongoing tasks; init containers for setup/initialization

**Best Practices for Sidecars:**
- **Resource Limits**: Set appropriate CPU/memory limits for sidecar to prevent resource starvation
- **Health Checks**: Configure liveness/readiness probes for both main and sidecar containers
- **Log Verbosity**: Balance between log detail and performance/storage costs
- **Failure Handling**: Decide if sidecar failure should restart entire pod (default) or just sidecar
- **Security**: Apply same security contexts and policies to sidecar as main container
- **Image Selection**: Use minimal base images (alpine, distroless) to reduce attack surface

**Advanced Sidecar Patterns:**

**Service Mesh Sidecar (Envoy Proxy):**
```yaml
- name: envoy-sidecar
  image: envoyproxy/envoy:v1.20
  volumeMounts:
  - name: envoy-config
    mountPath: /etc/envoy
```
- Handles all network traffic to/from main container
- Provides load balancing, retries, circuit breaking, TLS
- Enables observability with distributed tracing

**Metrics Exporter Sidecar:**
```yaml
- name: prometheus-exporter
  image: nginx/nginx-prometheus-exporter
  args:
  - -nginx.scrape-uri=http://localhost/stub_status
```
- Scrapes application metrics and exposes in Prometheus format
- Main app doesn't need metrics export code
- Centralized monitoring without app modification

**Log Rotation Sidecar:**
```yaml
- name: log-rotator
  image: busybox
  command: ['sh', '-c', 'while true; do find /logs -name "*.log" -size +100M -exec gzip {} \; ; sleep 3600; done']
```
- Manages log file sizes to prevent disk exhaustion
- Compresses or deletes old logs automatically
- Prevents main container from running out of disk space

**Configuration Sync Sidecar:**
```yaml
- name: config-sync
  image: config-sync-tool
  env:
  - name: CONFIG_SOURCE
    value: "s3://my-bucket/configs"
  volumeMounts:
  - name: app-config
    mountPath: /config
```
- Periodically fetches updated configuration from external source
- Main container reads configuration from shared volume
- Enables dynamic configuration updates without pod restart

**Sidecar Injection:**
- **Manual**: Define sidecar in pod spec (like this exercise)
- **Automatic**: Use Mutating Admission Webhooks to inject sidecars (Istio, Linkerd)
- **Namespace-level**: Configure automatic injection per namespace
- **Annotation-based**: Control injection with pod annotations

**Monitoring Sidecar Performance:**
- Track sidecar resource usage with `kubectl top pod webserver --containers`
- Monitor sidecar logs for errors: `kubectl logs webserver -c sidecar-container`
- Check sidecar restarts: `kubectl get pod webserver -o json | jq '.status.containerStatuses'`
- Set alerts for sidecar failures or resource exhaustion

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 54](day-54.md) | [Day 56 →](day-56.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
