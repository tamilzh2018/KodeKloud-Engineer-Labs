# Day 60: Persistent Volumes in Kubernetes

## Task Overview

Implement persistent storage for a web application using Kubernetes Persistent Volumes (PV) and Persistent Volume Claims (PVC). This task demonstrates how to decouple storage provisioning from consumption, enabling data persistence beyond pod lifecycles and supporting stateful applications.

**Technical Specifications:**
- PersistentVolume: pv-xfusion (3Gi, hostPath, manual storage class)
- PersistentVolumeClaim: pvc-xfusion (3Gi, ReadWriteOnce)
- Pod: pod-xfusion (httpd:latest with mounted volume)
- Service: web-xfusion (NodePort 30008)
- Access mode: ReadWriteOnce

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Create a PersistentVolume manifest

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-xfusion
spec:
  capacity:
    storage: 3Gi
  accessModes:
    - ReadWriteOnce
  storageClassName: manual
  hostPath:
    path: /mnt/security
```

Define a PersistentVolume that represents physical storage in the cluster. The `capacity.storage` field specifies 3GiB of storage capacity. The `accessModes` field with `ReadWriteOnce` means the volume can be mounted as read-write by a single node at a time. The `storageClassName: manual` indicates this is manually provisioned storage (not dynamically created). The `hostPath` type uses a directory on the host node (`/mnt/security`), which is suitable for development but not recommended for production multi-node clusters.

**Step 2:** Apply the PersistentVolume configuration

```bash
kubectl apply -f k3s-pv.yaml
```

Create the PersistentVolume resource in the cluster. This makes the storage available for consumption but doesn't yet allocate it to any application. The PV exists at the cluster level and can be bound to a PVC from any namespace (though the PVC must request compatible storage class, capacity, and access modes). Verify the PV was created with `kubectl get pv` - it should show status `Available` until bound to a claim.

**Step 3:** Create a PersistentVolumeClaim manifest

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-xfusion
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 3Gi
  storageClassName: manual
```

Define a PersistentVolumeClaim that requests storage resources. The PVC acts as a request for storage by pods, abstracting the underlying storage implementation. The `accessModes` and `storageClassName` must match the PV for binding to occur. The `resources.requests.storage` field requests 3Gi of storage. Kubernetes will automatically bind this PVC to the pv-xfusion PV since the requirements match (storage class, capacity, and access mode).

**Step 4:** Apply the PersistentVolumeClaim configuration

```bash
kubectl apply -f k3s-pvc.yaml
```

Create the PersistentVolumeClaim in the cluster. Kubernetes immediately attempts to find a suitable PV and bind them together. Once bound, the PVC status changes to `Bound` and the PV status also changes to `Bound`. The binding is exclusive - a PV bound to a PVC cannot be claimed by another PVC. Check binding status with `kubectl get pvc` - you should see `pvc-xfusion` with STATUS `Bound` and VOLUME `pv-xfusion`.

**Step 5:** Create a pod manifest with volume mount

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-xfusion
  labels:
    app: xfusion
spec:
  containers:
  - name: container-xfusion
    image: httpd:latest
    volumeMounts:
    - name: xfusion-volume
      mountPath: /usr/share/nginx/html/data
    resources:
      limits:
        memory: "128Mi"
        cpu: "500m"
      requests:
        memory: "64Mi"
        cpu: "250m"
  volumes:
  - name: xfusion-volume
    persistentVolumeClaim:
      claimName: pvc-xfusion
```

Define a pod that consumes the persistent storage via the PVC. The `volumes` section references the PVC by name (`pvc-xfusion`), creating a volume named `xfusion-volume` in the pod. The `volumeMounts` section in the container specification mounts this volume to `/usr/share/nginx/html/data` inside the container. Any data written to this path persists beyond the pod's lifecycle because it's stored on the persistent volume. The resource limits ensure the pod doesn't consume excessive cluster resources.

**Step 6:** Apply the pod configuration

```bash
kubectl apply -f k3s-pod.yaml
```

Create the pod with the mounted persistent volume. Kubernetes schedules the pod on a node that can access the storage (for hostPath volumes, this means the node where the directory exists). The kubelet on that node creates the container and mounts the volume before starting the application. If the pod is deleted and recreated, the data in the persistent volume remains intact because the PV and PVC continue to exist independently of the pod.

**Step 7:** Create a NodePort service manifest

```yaml
apiVersion: v1
kind: Service
metadata:
  name: web-xfusion
  labels:
    app: xfusion
spec:
  type: NodePort
  ports:
  - port: 80
    targetPort: 80
    nodePort: 30008
  selector:
    app: xfusion
```

Define a Service to expose the web application externally. The service uses `type: NodePort` to make the application accessible on port 30008 on all cluster nodes. The `selector` matches pods with label `app: xfusion`, routing traffic to the pod created in the previous step. The `port` field specifies the service's internal port (80), and `targetPort` specifies the container port to forward to (also 80, Apache's default HTTP port).

**Step 8:** Apply the service configuration

```bash
kubectl apply -f k3s-svc.yaml
```

Create the NodePort service to expose the web application. The service immediately starts routing traffic to the pod (if it's running). You can now access the Apache web server from outside the cluster using `http://<node-ip>:30008`. The web server serves content from its document root, and any files written to the mounted persistent volume path will be available even if the pod is recreated.

**Step 9:** Verify all resources are created and bound

```bash
# Check PersistentVolume status
kubectl get pv

# Check PersistentVolumeClaim status
kubectl get pvc

# Verify pod is running
kubectl get pods

# Check service
kubectl get svc web-xfusion

# View detailed PVC information
kubectl describe pvc pvc-xfusion
```

Perform comprehensive verification of all resources. The `get pv` command should show `pv-xfusion` with STATUS `Bound`. The `get pvc` command should show `pvc-xfusion` also with STATUS `Bound` and VOLUME `pv-xfusion`, confirming the binding. The pod should be in `Running` status. The service should show TYPE `NodePort` with PORT(S) `80:30008/TCP`. The `describe pvc` command shows which PV is bound and mount information.

**Step 10:** Test persistence by writing data to the volume

```bash
# Write test data to the persistent volume
kubectl exec pod-xfusion -- sh -c 'echo "Hello from persistent storage" > /usr/share/nginx/html/data/test.html'

# Verify data exists
kubectl exec pod-xfusion -- cat /usr/share/nginx/html/data/test.html

# Delete and recreate the pod
kubectl delete pod pod-xfusion
kubectl apply -f k3s-pod.yaml

# Verify data persists after pod recreation
kubectl exec pod-xfusion -- cat /usr/share/nginx/html/data/test.html
```

Test that data truly persists across pod lifecycles. Write a test file to the mounted volume path, then delete and recreate the pod. When you read the file again after pod recreation, it should still contain the original data, proving the storage is persistent. This demonstrates the key benefit of PersistentVolumes - data survives pod deletions, crashes, and rescheduling, which is essential for stateful applications like databases.

---

## Key Concepts

**Persistent Volumes (PV):**

PersistentVolumes represent storage resources in the cluster:
- **Cluster-wide resources**: Not namespaced, available to all namespaces
- **Lifecycle independent of pods**: Exist beyond pod lifecycles
- **Administrator provisioned**: Created by cluster admins (static provisioning)
- **Capacity**: Specify storage size (Gi, Ti, etc.)
- **Access modes**: Define how the volume can be accessed
- **Reclaim policy**: What happens when PVC is deleted (Retain, Delete, Recycle)

**Persistent Volume Claims (PVC):**

PVCs are requests for storage by users/pods:
- **Namespace-scoped**: Belong to specific namespace
- **Storage request**: Specify required capacity and access modes
- **Automatic binding**: Kubernetes binds PVC to suitable PV
- **Pod consumption**: Pods reference PVC, not PV directly
- **Portability**: Same PVC can work across different storage backends

**Access Modes:**

Define how volumes can be mounted:

- **ReadWriteOnce (RWO)**:
  - Volume mounted as read-write by a single node
  - Multiple pods on same node can access it
  - Most common for block storage (EBS, Azure Disk)
  - Used for databases, single-instance applications

- **ReadOnlyMany (ROX)**:
  - Volume mounted as read-only by many nodes
  - Useful for shared configuration or reference data
  - Examples: shared static content, lookup tables

- **ReadWriteMany (RWX)**:
  - Volume mounted as read-write by many nodes
  - Requires network file systems (NFS, CephFS, GlusterFS)
  - Used for shared application data across multiple instances
  - Examples: shared user uploads, distributed applications

**Storage Classes:**

StorageClasses enable dynamic volume provisioning:

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast-ssd
provisioner: kubernetes.io/aws-ebs
parameters:
  type: gp3
  iops: "3000"
  encrypted: "true"
```

- **Dynamic provisioning**: Automatically creates PV when PVC is created
- **Provisioners**: Cloud-specific (AWS EBS, GCP PD, Azure Disk) or on-prem (NFS, Ceph)
- **Parameters**: Provisioner-specific options (disk type, IOPS, encryption)
- **Default class**: Used when PVC doesn't specify storage class

**Volume Types:**

**hostPath** (development only):
```yaml
hostPath:
  path: /mnt/data
  type: DirectoryOrCreate
```
- Mounts directory from host node
- Data tied to specific node (not portable)
- Security risk in multi-tenant clusters
- Only for testing, development, or single-node clusters

**NFS** (network file system):
```yaml
nfs:
  server: nfs-server.example.com
  path: /exported/path
```
- Shared storage across multiple nodes
- Supports ReadWriteMany access mode
- Requires NFS server setup
- Good for legacy applications

**Cloud Provider Volumes**:

AWS EBS:
```yaml
awsElasticBlockStore:
  volumeID: vol-0123456789abcdef
  fsType: ext4
```

GCP Persistent Disk:
```yaml
gcePersistentDisk:
  pdName: my-data-disk
  fsType: ext4
```

Azure Disk:
```yaml
azureDisk:
  diskName: my-disk
  diskURI: /subscriptions/.../disks/my-disk
```

**Reclaim Policies:**

Define what happens to PV when PVC is deleted:

- **Retain**: PV remains, data preserved, manual cleanup required
- **Delete**: PV and underlying storage automatically deleted
- **Recycle**: Deprecated, basic data scrubbing (rm -rf /volume/*)

**Binding Process:**

1. PVC created with storage requirements
2. Kubernetes control plane searches for suitable PV:
   - Matching storage class (or default)
   - Sufficient capacity (PV >= PVC request)
   - Compatible access modes
3. If match found, PVC and PV are bound
4. If no match and dynamic provisioning enabled, create new PV
5. If no match and no dynamic provisioning, PVC remains Pending
6. Bound PV cannot be claimed by other PVCs

**PersistentVolume Lifecycle:**

```
Available → Bound → Released → (Failed/Available/Deleted)
```

- **Available**: PV ready, not bound to any PVC
- **Bound**: PV bound to a PVC
- **Released**: PVC deleted but PV not yet reclaimed
- **Failed**: Automatic reclamation failed

**StatefulSet Integration:**

StatefulSets use VolumeClaimTemplates for persistent storage:

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: database
spec:
  serviceName: database
  replicas: 3
  volumeClaimTemplates:
  - metadata:
      name: data
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 10Gi
```

Each pod gets its own PVC automatically created and bound, providing stable storage across pod rescheduling.

**Best Practices:**

**For Production**:
- Use dynamic provisioning with StorageClasses
- Implement backup strategies for persistent data
- Monitor storage usage and set up alerts
- Use appropriate reclaim policies (Retain for important data)
- Encrypt sensitive data at rest
- Test disaster recovery procedures

**Storage Sizing**:
- Request realistic storage amounts (avoid over-provisioning)
- Monitor actual usage and adjust
- Consider growth over time
- Factor in overhead (filesystem, metadata)

**Performance Considerations**:
- Use SSD-backed storage for databases
- Consider IOPS requirements
- Network latency for network-attached storage
- Use local volumes for highest performance (with data replication)

**Security**:
- Use fsGroup for proper file permissions
- Enable encryption at rest for sensitive data
- Use RBAC to control PVC creation
- Audit volume access patterns

**Volume Expansion:**

Some storage classes support volume expansion:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-xfusion
spec:
  resources:
    requests:
      storage: 5Gi  # Increased from 3Gi
```

After editing, Kubernetes automatically expands the volume (if storage class allows expansion).

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 59](day-59.md) | [Day 61 →](day-61.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
