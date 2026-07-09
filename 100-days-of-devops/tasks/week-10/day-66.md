# Day 66: Deploy MySQL on Kubernetes

## Task Overview

Deploy a production-ready MySQL database server on Kubernetes with persistent storage, secure credential management using Secrets, and external access through NodePort service.

**Technical Specifications:**
- PersistentVolume name: `mysql-pv` with capacity `250Mi`
- PersistentVolumeClaim name: `mysql-pv-claim` requesting `250Mi`
- Deployment name: `mysql-deployment` using MySQL image
- Mount path: `/var/lib/mysql` (MySQL data directory)
- Service: NodePort type named `mysql` on port `30007`
- Secrets: `mysql-root-pass`, `mysql-user-pass`, `mysql-db-url`
- Environment variables: MYSQL_ROOT_PASSWORD, MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Create directory for persistent storage

```sh
mkdir -p /home/thor/pv
```

Create a directory on the host filesystem that will serve as the backing storage for the PersistentVolume. The `-p` flag ensures parent directories are created if they don't exist and doesn't throw an error if the directory already exists. This directory will store all MySQL database files, ensuring data persists even if the pod is deleted or recreated. In production environments, this would typically be replaced with network-attached storage (NAS), cloud block storage (EBS, Azure Disk), or distributed storage systems (Ceph, GlusterFS) for better durability and availability.

**Step 2:** Create the MySQL deployment configuration file

```sh
vi k3s-mysql-deployment.yml
```

Create a comprehensive YAML configuration file that defines all necessary Kubernetes resources for the MySQL deployment. This file will include Secrets for storing sensitive credentials, a PersistentVolume for storage allocation, a PersistentVolumeClaim to request storage, a Deployment to run MySQL, and a Service to expose MySQL to other applications.

**Reference YAML structure:**
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: mysql-root-pass
type: Opaque
stringData:
  password: YUIidhb667
---
apiVersion: v1
kind: Secret
metadata:
  name: mysql-user-pass
type: Opaque
stringData:
  username: kodekloud_sam
  password: BruCStnMT5
---
apiVersion: v1
kind: Secret
metadata:
  name: mysql-db-url
type: Opaque
stringData:
  database: kodekloud_db8
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: mysql-pv
spec:
  capacity:
    storage: 250Mi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: /home/thor/pv
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mysql-pv-claim
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 250Mi
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mysql-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mysql
  template:
    metadata:
      labels:
        app: mysql
    spec:
      containers:
      - name: mysql
        image: mysql:5.7
        ports:
        - containerPort: 3306
        env:
        - name: MYSQL_ROOT_PASSWORD
          valueFrom:
            secretKeyRef:
              name: mysql-root-pass
              key: password
        - name: MYSQL_DATABASE
          valueFrom:
            secretKeyRef:
              name: mysql-db-url
              key: database
        - name: MYSQL_USER
          valueFrom:
            secretKeyRef:
              name: mysql-user-pass
              key: username
        - name: MYSQL_PASSWORD
          valueFrom:
            secretKeyRef:
              name: mysql-user-pass
              key: password
        volumeMounts:
        - name: mysql-persistent-storage
          mountPath: /var/lib/mysql
      volumes:
      - name: mysql-persistent-storage
        persistentVolumeClaim:
          claimName: mysql-pv-claim
---
apiVersion: v1
kind: Service
metadata:
  name: mysql
spec:
  type: NodePort
  selector:
    app: mysql
  ports:
  - protocol: TCP
    port: 3306
    targetPort: 3306
    nodePort: 30007
```

This configuration uses `stringData` instead of `data` in Secrets, which allows plain text values that Kubernetes automatically base64-encodes. The Secrets store sensitive credentials separately from the deployment configuration. The PersistentVolume allocates 250Mi of storage from the host directory, while the PersistentVolumeClaim requests this storage with ReadWriteOnce access mode (mountable by a single node). The Deployment references all three Secrets through environment variables using `secretKeyRef`, ensuring credentials are injected securely into the MySQL container. The Service exposes MySQL on NodePort 30007, making it accessible from outside the cluster.

**Step 3:** Deploy MySQL to Kubernetes

```sh
kubectl apply -f k3s-mysql-deployment.yml
```

Apply the complete MySQL configuration to the Kubernetes cluster. The `kubectl apply` command processes all resources in the YAML file in order: Secrets are created first to store credentials, then the PersistentVolume and PersistentVolumeClaim establish storage, followed by the Deployment which creates the MySQL pod, and finally the Service to expose MySQL externally. Kubernetes will pull the MySQL image (if not cached), mount the persistent volume, inject environment variables from Secrets, and start the MySQL server. The initial startup may take 30-60 seconds as MySQL initializes the database with the root password, creates the specified database, and sets up the user account.

**Step 4:** Verify deployment status

```sh
kubectl get deployments.apps
```

Check that the MySQL deployment was created successfully and has the desired number of replicas available. The output should show `mysql-deployment` with `READY 1/1`, indicating one pod is running out of one desired. If the ready count is `0/1`, the pod may still be starting or encountering issues. The `UP-TO-DATE` column shows how many replicas are at the latest version, and `AVAILABLE` indicates how many are ready to serve traffic.

**Step 5:** Examine detailed deployment configuration

```sh
kubectl describe deployments.apps mysql-deployment
```

Display comprehensive information about the MySQL deployment including pod template, environment variables, volume mounts, and events. This command shows the complete deployment specification, verifying that environment variables are correctly sourced from Secrets (without exposing the actual values), the PersistentVolumeClaim is properly mounted, and the deployment strategy is configured. The Events section at the bottom reveals any issues during deployment creation or pod scheduling.

**Step 6:** Verify pods are running

```sh
kubectl get pods
```

Confirm the MySQL pod is in `Running` state with readiness `1/1`. Look for a pod named `mysql-deployment-<random-hash>`. If the status shows `Pending`, the PersistentVolumeClaim may not be bound yet. `CrashLoopBackOff` indicates the MySQL container is failing to start, possibly due to incorrect environment variables or storage issues. `ContainerCreating` is normal during initial deployment while the volume is being mounted and the image pulled.

**Step 7:** Check PersistentVolume and claim binding

```sh
kubectl get pv
kubectl get pvc
```

Verify the PersistentVolume was created and the PersistentVolumeClaim successfully bound to it. Both commands should show `STATUS: Bound`, indicating the claim has been matched with an available volume. The `kubectl get pv` output displays the volume capacity (250Mi), access mode (RWO - ReadWriteOnce), reclaim policy, and claim reference. The `kubectl get pvc` output shows the requested storage, access modes, and which volume it's bound to. If the PVC status is `Pending`, there may not be a suitable PersistentVolume available that matches the claim's requirements.

**Step 8:** Verify service configuration

```sh
kubectl get svc
```

Confirm the MySQL service was created with the correct type and port configuration. The output should show the `mysql` service with type `NodePort`, cluster IP assigned by Kubernetes, and port mapping `3306:30007/TCP` indicating the service listens on internal port 3306 and exposes it externally on NodePort 30007. This means you can connect to MySQL from outside the cluster using `<node-ip>:30007`.

**Step 9:** Verify secrets were created

```sh
kubectl get secrets
```

List all secrets to confirm the three MySQL-related secrets were created: `mysql-root-pass`, `mysql-user-pass`, and `mysql-db-url`. The output shows the secret type (Opaque for generic secrets), the number of data items in each secret, and their age. These secrets are now available for the MySQL pod to reference through environment variables, keeping sensitive credentials out of the deployment configuration and pod logs.

**Step 10:** Test MySQL connectivity (optional)

```sh
kubectl exec -it <mysql-pod-name> -- mysql -u root -p
```

Optionally verify MySQL is functioning by connecting to the database. When prompted, enter the root password (`YUIidhb667`). Once connected, you can run SQL commands like `SHOW DATABASES;` to verify the `kodekloud_db8` database was created, `SELECT User FROM mysql.user;` to confirm the `kodekloud_sam` user exists, and `USE kodekloud_db8;` to switch to the database. Type `exit` to close the MySQL session. This confirms that MySQL is operational and all initialization based on environment variables succeeded.

---

## Key Concepts

**Persistent Storage in Kubernetes:**
- **PersistentVolume (PV)**: Cluster-wide storage resource provisioned by administrators
- **PersistentVolumeClaim (PVC)**: Request for storage by users/applications
- **Access Modes**: ReadWriteOnce (RWO), ReadOnlyMany (ROX), ReadWriteMany (RWX)
- **Reclaim Policies**: Retain (keep data), Delete (remove data), Recycle (deprecated)
- **Storage Classes**: Dynamic provisioning of volumes based on quality-of-service levels

**Kubernetes Secrets:**
- **Opaque Secrets**: Generic key-value pairs for passwords, tokens, keys
- **stringData vs data**: stringData accepts plain text, data requires base64 encoding
- **Secret References**: Inject as environment variables or mount as files
- **Security**: Secrets are base64-encoded (not encrypted) by default in etcd
- **Best Practices**: Enable encryption at rest, use RBAC to restrict access, rotate regularly

**Database Deployment Patterns:**
- **StatefulSets**: Better suited for databases requiring stable network identities
- **Deployments**: Suitable for single-instance databases or read replicas
- **Persistent Storage**: Essential for data durability across pod restarts
- **Init Containers**: Can run database migrations or initial setup before main container starts

**MySQL Environment Variables:**
- **MYSQL_ROOT_PASSWORD**: Sets the root user password (required)
- **MYSQL_DATABASE**: Creates a database on first startup
- **MYSQL_USER**: Creates a user with access to MYSQL_DATABASE
- **MYSQL_PASSWORD**: Password for MYSQL_USER
- **Data Directory**: MySQL stores all data in /var/lib/mysql by default

**Production Considerations:**
- **High Availability**: Use MySQL replication with master-slave or Galera cluster
- **Backups**: Implement regular backups using mysqldump, physical backups, or snapshots
- **Resource Limits**: Set CPU and memory limits to prevent resource exhaustion
- **Security**: Use network policies, enable SSL/TLS, implement least privilege access
- **Monitoring**: Track query performance, connection counts, replication lag, disk usage
- **Storage Performance**: Use SSDs or high-IOPS storage for production databases

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 65](day-65.md) | [Day 67 →](day-67.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
