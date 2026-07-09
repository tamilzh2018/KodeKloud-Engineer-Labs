# Day 54: Kubernetes Shared Volumes

## Task Overview

Create a multi-container pod with a shared emptyDir volume to enable data sharing between containers. This exercise demonstrates how containers within the same pod can exchange data through a shared filesystem.

**Technical Specifications:**
- Pod: volume-share-nautilus
- Container 1: volume-container-nautilus-1 (fedora:latest, mount at /tmp/news)
- Container 2: volume-container-nautilus-2 (fedora:latest, mount at /tmp/demo)
- Volume: volume-share (type: emptyDir)
- Validation: Create file in container 1, verify visibility in container 2

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Create pod manifest with shared volume configuration

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: volume-share-nautilus
  labels:
    app: volume-share
spec:
  containers:
  - name: volume-container-nautilus-1
    image: fedora:latest
    command: ['sh', '-c', 'sleep 10000']
    volumeMounts:
    - name: volume-share
      mountPath: /tmp/news
  - name: volume-container-nautilus-2
    image: fedora:latest
    command: ['sh', '-c', 'sleep 10000']
    volumeMounts:
    - name: volume-share
      mountPath: /tmp/demo
  volumes:
  - name: volume-share
    emptyDir: {}
```

Create a pod manifest defining two containers that share a common emptyDir volume mounted at different paths. The pod specification includes two fedora containers, each configured with a `sleep` command to keep them running indefinitely. The key configuration is the **volumeMounts** section in each container and the **volumes** section at the pod level. The first container mounts the `volume-share` volume at `/tmp/news`, while the second mounts the same volume at `/tmp/demo`. The `emptyDir: {}` volume type creates an empty directory when the pod is assigned to a node - this directory is initially empty and exists for the lifetime of the pod. Both containers can read from and write to this shared storage, enabling inter-container communication and data sharing within the pod.

**Step 2:** Apply the pod configuration to create it

```sh
kubectl apply -f k3s-pod.yml
```

Deploy the pod to the Kubernetes cluster using the manifest file. The `kubectl apply` command submits the pod definition to the Kubernetes API server, which schedules the pod on an available node. The kubelet on that node creates the emptyDir volume (as a directory in the node's filesystem), starts both containers, and mounts the volume into each container at their specified paths. The pod enters the Running state once both containers start successfully. Behind the scenes, Kubernetes ensures the shared volume is accessible to both containers with appropriate permissions, creating a shared filesystem space that both containers can use simultaneously.

**Step 3:** Verify pod is running successfully

```sh
kubectl get pods
```

List all pods to confirm the volume-share-nautilus pod was created and is running. The output displays pod name, ready status (should show "2/2" indicating both containers are running), status (should be "Running"), restart count, and age. The "READY" column showing "2/2" is crucial - it confirms both fedora containers started successfully and are running. If the status shows anything other than Running (like Pending, CrashLoopBackOff, or Error), you'll need to troubleshoot using `kubectl describe pod` or `kubectl logs` before proceeding.

**Step 4:** Access the first container and create a test file

```sh
kubectl exec -it volume-share-nautilus -c volume-container-nautilus-1 /bin/sh
```

Start an interactive shell session in the first container to create a test file. The `kubectl exec` command executes commands in a running container. The `-it` flags enable interactive mode with a TTY, allowing you to interact with the shell. The `-c volume-container-nautilus-1` flag specifies which container to access (required for multi-container pods). The `/bin/sh` argument starts a shell session. Once inside the container, you have full access to its filesystem, including the mounted volume at `/tmp/news`.

**Step 5:** Create a test file in the shared volume

```sh
touch /tmp/news/news.txt
```

Create an empty file named news.txt in the first container's mount point. The `touch` command creates an empty file at the specified path. Since `/tmp/news` is where the shared volume is mounted in this container, the file is actually created in the emptyDir volume, not in the container's writable layer. This is the crucial point: **the file is written to the shared volume storage, not to container-specific storage**. After creating the file, exit the shell by typing `exit` or pressing Ctrl+D to return to your host terminal.

**Step 6:** Access the second container to verify file visibility

```sh
kubectl exec -it volume-share-nautilus -c volume-container-nautilus-2 /bin/sh
```

Start an interactive shell session in the second container to verify the shared file is accessible. This `kubectl exec` command is identical to Step 4, except it specifies `-c volume-container-nautilus-2` to access the second container instead of the first. Once you're inside the second container's shell, you can inspect its filesystem. Remember that this container mounts the same `volume-share` volume, but at a different path: `/tmp/demo`.

**Step 7:** Verify the file exists in the second container

```sh
ls /tmp/demo
```

List the contents of the second container's mount point to confirm the file created in the first container is visible here. The `ls` command should display `news.txt` in the `/tmp/demo` directory. This confirms that **both containers are accessing the same underlying storage** - the file created at `/tmp/news/news.txt` in container 1 appears at `/tmp/demo/news.txt` in container 2 because both paths are mount points for the same emptyDir volume. This demonstrates the fundamental concept of shared volumes in Kubernetes: multiple containers in a pod can share data by mounting the same volume at different (or same) paths.

**Step 8:** Additional verification (optional)

```sh
# In container 2, create or modify files
echo "Hello from container 2" > /tmp/demo/news.txt
cat /tmp/demo/news.txt
exit

# In container 1, verify the changes
kubectl exec -it volume-share-nautilus -c volume-container-nautilus-1 -- cat /tmp/news/news.txt
```

Demonstrate bidirectional data sharing by modifying the file in container 2 and reading it from container 1. This confirms that changes made by either container are immediately visible to the other, as they're working with the same underlying storage. The `kubectl exec` command with `--` allows you to run a single command without starting an interactive shell, useful for quick checks or scripting.

---

## Key Concepts

**emptyDir Volumes:**
- **Lifecycle**: Created when pod is assigned to a node, deleted when pod is removed from that node
- **Initial State**: Starts as an empty directory, containers populate it with data
- **Storage Location**: Typically stored on node's disk, but can use memory with `emptyDir.medium: Memory`
- **Use Cases**: Scratch space, caching, sharing data between containers, temporary processing
- **Non-Persistent**: Data is lost when pod is deleted, rescheduled, or crashes
- **Performance**: Fast access as it's local to the node, no network overhead

**Volume Mount Paths:**
- **Different Paths Allowed**: Containers can mount the same volume at different paths (like /tmp/news and /tmp/demo)
- **Same Underlying Data**: All mount points access the same physical storage regardless of path
- **Path Independence**: Each container sees the volume data at its configured mountPath
- **Subdirectories**: Containers can also mount subdirectories using subPath field
- **Overlapping Mounts**: Mounting a volume over a non-empty directory hides original contents

**Multi-Container Communication:**
- **Shared Filesystem**: Primary method for data exchange between containers in a pod
- **Shared Network**: Containers share localhost network, can communicate via 127.0.0.1
- **Shared IPC**: Can optionally share IPC namespace for inter-process communication
- **Shared Process Namespace**: Optionally share process namespace (disabled by default)
- **Independent Filesystems**: Each container has its own root filesystem from its image

**Volume Types Comparison:**
- **emptyDir**: Temporary, pod-scoped, deleted with pod. Best for ephemeral data sharing
- **hostPath**: Mounts directory from host node. Survives pod restarts but is node-specific
- **persistentVolumeClaim**: Persistent storage that survives pod deletion and rescheduling
- **configMap**: Readonly configuration data mounted as files
- **secret**: Sensitive data mounted as files, encrypted at rest
- **downwardAPI**: Exposes pod/container metadata as files

**Common Use Cases for Shared Volumes:**
- **Data Processing Pipelines**: One container produces data, another consumes/processes it
- **Log Aggregation**: Application writes logs to volume, sidecar ships logs to central system
- **Content Serving**: Build container generates static files, web server container serves them
- **Caching**: One container populates cache, others read from it
- **Configuration Sharing**: Init container downloads configs, main containers read them
- **Backup Operations**: Main app writes data, backup container periodically backs it up

**emptyDir Memory Storage:**
```yaml
volumes:
- name: cache-volume
  emptyDir:
    medium: Memory
    sizeLimit: 128Mi
```
- **Faster Access**: RAM-based storage, much faster than disk
- **Size Limits**: Set sizeLimit to prevent memory exhaustion
- **Pod Resources**: Memory used counts against container memory limits
- **Use Case**: Temporary caches, fast scratch space for computation-intensive tasks

**Multi-Container Patterns:**
- **Sidecar**: Helper container extends main application (logging, monitoring, proxying)
- **Ambassador**: Proxy container handles network connections for main container
- **Adapter**: Transforms main container's output to match expected format
- **Init Containers**: Run before main containers, used for setup tasks
- **Ephemeral Containers**: Debugging containers attached to running pods (alpha feature)

**Volume Troubleshooting:**
- **Permission Issues**: Check container user has read/write permissions on mounted path
- **Mount Failures**: Use `kubectl describe pod` to see volume mount errors in events
- **Data Not Shared**: Verify volume name matches in both container volumeMounts and pod volumes
- **Path Conflicts**: Ensure mount paths don't conflict with critical container paths
- **Size Issues**: emptyDir size limited by node's available disk or memory

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 53](day-53.md) | [Day 55 →](day-55.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
