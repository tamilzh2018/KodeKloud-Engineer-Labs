# Day 62: Manage Secrets in Kubernetes

## Task Overview

Implement secure secret management in Kubernetes by creating secrets from files and consuming them in pods via volume mounts. This task demonstrates how to protect sensitive information like passwords, API keys, and licenses while making them available to applications in a secure, controlled manner.

**Technical Specifications:**
- Secret name: media (generic type, created from file)
- Source file: /opt/media.txt
- Pod name: secret-devops
- Container: secret-container-devops (debian:latest)
- Mount path: /opt/cluster
- Secret consumption: Volume mount (not environment variables)

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Create a secret from a file

```bash
kubectl create secret generic media --from-file=/opt/media.txt
```

Create a Kubernetes Secret from an existing file using the imperative `kubectl create` command. The `generic` type creates a Secret for arbitrary user-defined data (as opposed to docker-registry or tls types). The `--from-file` flag reads the file content and stores it in the Secret with the filename as the key. This approach is convenient when you have existing credential files, certificates, or license files that need to be securely stored in Kubernetes without exposing them in YAML manifests.

**Step 2:** Verify the secret was created successfully

```bash
kubectl describe secret media
```

Inspect the created Secret to confirm it exists and contains the expected data. The `describe` command shows Secret metadata including the namespace, type, and data keys, but does not display the actual values (for security). You'll see that the Secret has a data key named `media.txt` (the source filename) with a certain size in bytes. This verification step ensures the Secret was created correctly before proceeding to use it in a pod.

**Step 3:** Create a pod manifest that mounts the secret

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secret-devops
spec:
  containers:
  - name: secret-container-devops
    image: debian:latest
    command: ["/bin/bash", "-c", "sleep 3600"]
    volumeMounts:
    - name: secret-volume
      mountPath: /opt/cluster
      readOnly: true
  volumes:
  - name: secret-volume
    secret:
      secretName: media
```

Define a pod that consumes the Secret via a volume mount. The `volumes` section creates a volume from the Secret named `media`. The `volumeMounts` section in the container spec mounts this volume at `/opt/cluster`. When mounted, Kubernetes creates individual files in the mount path for each key in the Secret - in this case, a file named `media.txt` containing the secret data. The `readOnly: true` flag ensures the container cannot modify the Secret data. The container runs a sleep command to keep it alive for inspection.

**Step 4:** Apply the pod configuration

```bash
kubectl apply -f k3s-pod.yaml
```

Deploy the pod to the Kubernetes cluster. Kubernetes schedules the pod, creates the container, and mounts the Secret as files before starting the application. The Secret data is injected into the container's filesystem at the specified mount path, making it accessible to the application as regular files. This approach is more secure than environment variables because the data is not visible in process listings and can be updated without recreating the pod (if the Secret is updated).

**Step 5:** Verify the pod and secret are ready

```bash
# Check secret status
kubectl get secret

# Check pod status
kubectl get pod
```

Confirm both the Secret and pod resources exist and are in the expected states. The Secret should be listed with TYPE `Opaque` (the type for generic secrets). The pod should show STATUS `Running`, indicating the container started successfully with the Secret mounted. If the pod shows `Error` or `CrashLoopBackOff`, there may be an issue with the Secret reference or mount path.

**Step 6:** Verify the secret is accessible inside the container

```bash
kubectl exec -it secret-devops -c secret-container-devops -- cat /opt/cluster/media.txt
```

Execute a command inside the running container to read the Secret file. This command connects to the `secret-container-devops` container in the `secret-devops` pod and runs `cat` to display the contents of `/opt/cluster/media.txt`. You should see the original content from `/opt/media.txt`, confirming the Secret was successfully mounted and is accessible to the application. This is the same data that would be used by your application for authentication, configuration, or licensing purposes.

**Step 7:** Inspect the mounted secret directory

```bash
# List files in the secret mount directory
kubectl exec secret-devops -c secret-container-devops -- ls -la /opt/cluster

# Check file permissions
kubectl exec secret-devops -c secret-container-devops -- stat /opt/cluster/media.txt
```

Explore the Secret mount directory to understand how Kubernetes exposes Secret data. The `ls -la` command shows all files in the directory, including symbolic links. You'll notice that Secret files are actually symlinks to files in a hidden directory (part of Kubernetes' Secret update mechanism). The `stat` command displays detailed file information including permissions (typically 0644), ownership, and timestamps. These commands help you understand the Secret filesystem structure for troubleshooting purposes.

**Step 8:** View secret data in base64 format

```bash
# Get secret YAML with base64-encoded data
kubectl get secret media -o yaml

# Decode the secret value
kubectl get secret media -o jsonpath='{.data.media\.txt}' | base64 --decode
```

Examine the raw Secret data as stored in Kubernetes. Secrets are stored base64-encoded in etcd (Kubernetes' data store). The first command shows the complete Secret YAML including the encoded data. The second command extracts just the Secret value and decodes it, which is useful for verifying the content without accessing a pod. Note that base64 is encoding, not encryption - it provides obfuscation but not security. For true encryption at rest, enable etcd encryption in your cluster.

**Step 9:** Test secret updates and pod sync

```bash
# Create a new version of the secret file
echo "Updated license key" > /tmp/new-media.txt

# Update the secret
kubectl create secret generic media --from-file=/tmp/new-media.txt --dry-run=client -o yaml | kubectl apply -f -

# Wait a moment for kubelet to sync (can take up to 1 minute)
# Then check if the pod sees updated content
kubectl exec secret-devops -c secret-container-devops -- cat /opt/cluster/media.txt
```

Demonstrate Secret update behavior when using volume mounts. When you update a Secret that's mounted as a volume, the kubelet eventually syncs the new data to the pod (this can take up to 1 minute by default). The container sees the updated content without needing to restart. This is a significant advantage over environment variables, which require pod recreation to update. However, your application must be designed to detect and reload the changed files.

**Step 10:** Clean up resources (optional)

```bash
# Delete the pod
kubectl delete pod secret-devops

# Delete the secret
kubectl delete secret media

# Verify deletion
kubectl get pods
kubectl get secrets
```

Remove the pod and Secret when done. Deleting these resources frees up cluster storage and ensures sensitive data is removed. In production, Secrets should be managed carefully with proper lifecycle management, rotation policies, and access controls. Never leave test Secrets containing actual credentials in the cluster. The Secret deletion is permanent and cannot be undone, so ensure you have backups if needed.

---

## Key Concepts

**Kubernetes Secrets Overview:**

Secrets are Kubernetes objects for storing and managing sensitive information:
- **Purpose**: Securely store passwords, tokens, keys, certificates
- **Namespace scoped**: Secrets belong to specific namespaces
- **Base64 encoded**: Data is encoded (not encrypted) in etcd
- **Access control**: RBAC controls who can read/write Secrets
- **Multiple consumption methods**: Environment variables, volume mounts, image pull secrets

**Secret Types:**

**Opaque (generic)**:
```bash
kubectl create secret generic my-secret --from-literal=password=secret123
```
- Default type for arbitrary user-defined data
- Most flexible, works for any key-value pairs
- Used for application passwords, API keys, custom data

**Docker registry**:
```bash
kubectl create secret docker-registry regcred \
  --docker-server=registry.example.com \
  --docker-username=user \
  --docker-password=pass \
  --docker-email=user@example.com
```
- Stores Docker registry authentication credentials
- Used in pod spec under `imagePullSecrets`
- Enables pulling images from private registries

**TLS**:
```bash
kubectl create secret tls tls-secret \
  --cert=path/to/cert.crt \
  --key=path/to/key.key
```
- Stores TLS certificate and private key
- Used with Ingress resources for HTTPS
- Certificate must be in PEM format

**Service Account Token**:
- Automatically created by Kubernetes
- Contains authentication token for service accounts
- Mounted into pods at `/var/run/secrets/kubernetes.io/serviceaccount`
- Used for pod-to-API-server authentication

**Creating Secrets:**

**From literal values**:
```bash
kubectl create secret generic db-credentials \
  --from-literal=username=admin \
  --from-literal=password=secret123
```

**From files**:
```bash
kubectl create secret generic ssl-certs \
  --from-file=cert.pem \
  --from-file=key.pem
```

**From YAML manifest**:
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: my-secret
type: Opaque
data:
  username: YWRtaW4=  # base64 encoded "admin"
  password: c2VjcmV0MTIz  # base64 encoded "secret123"
```

**From environment file**:
```bash
# .env file contains KEY=VALUE pairs
kubectl create secret generic app-config --from-env-file=.env
```

**Consuming Secrets in Pods:**

**As environment variables**:
```yaml
env:
- name: DB_PASSWORD
  valueFrom:
    secretKeyRef:
      name: db-credentials
      key: password
```
- Simple to use in applications
- Visible in `kubectl describe pod` and process listings
- Cannot be updated without pod restart
- Less secure than volume mounts

**All keys as environment variables**:
```yaml
envFrom:
- secretRef:
    name: db-credentials
```
- Automatically creates env vars for all Secret keys
- Key names become environment variable names
- Convenient for Secrets with multiple keys

**As volume mounts**:
```yaml
volumes:
- name: secret-volume
  secret:
    secretName: db-credentials
volumeMounts:
- name: secret-volume
  mountPath: /etc/secrets
  readOnly: true
```
- More secure (not in process listings)
- Can be updated without pod restart (kubelet syncs changes)
- Mounted as files in the container filesystem
- Each Secret key becomes a separate file

**Specific keys only**:
```yaml
volumes:
- name: secret-volume
  secret:
    secretName: db-credentials
    items:
    - key: password
      path: db-password.txt
      mode: 0400
```
- Mount only specific keys from the Secret
- Customize filename with `path`
- Set file permissions with `mode`

**As image pull secrets**:
```yaml
imagePullSecrets:
- name: regcred
```
- Automatically used when pulling container images
- No code changes needed
- Configured at pod or service account level

**Secret Security Considerations:**

**Encryption at Rest:**
```yaml
# Enable encryption in kube-apiserver
--encryption-provider-config=/etc/kubernetes/encryption-config.yaml
```

Encryption config:
```yaml
apiVersion: apiserver.config.k8s.io/v1
kind: EncryptionConfiguration
resources:
- resources:
  - secrets
  providers:
  - aescbc:
      keys:
      - name: key1
        secret: <base64-encoded-32-byte-key>
  - identity: {}
```
- Encrypts Secrets in etcd at rest
- Without this, Secrets are only base64-encoded
- Essential for production security compliance

**Access Control with RBAC:**
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: secret-reader
rules:
- apiGroups: [""]
  resources: ["secrets"]
  resourceNames: ["db-credentials"]
  verbs: ["get"]
```
- Limit who can read specific Secrets
- Use least privilege principle
- Separate Secrets for different teams/apps

**Best Practices:**

1. **Never commit Secrets to Git**: Use `.gitignore` for Secret YAML files
2. **Use external secret managers**: Consider Vault, AWS Secrets Manager, Azure Key Vault
3. **Rotate Secrets regularly**: Implement automated rotation policies
4. **Prefer volume mounts over env vars**: More secure and updatable
5. **Enable encryption at rest**: Protect Secrets in etcd
6. **Use RBAC strictly**: Limit Secret access to necessary users/apps
7. **Audit Secret access**: Enable Kubernetes audit logging
8. **Separate Secrets by environment**: Don't reuse prod Secrets in dev/test
9. **Use specific Secret names**: Avoid generic names like "password" or "secret"
10. **Scan for leaked Secrets**: Use tools to detect committed Secrets

**Secret Size Limits:**

- Maximum size: 1 MB per Secret
- Affects etcd performance if too large
- Split large data across multiple Secrets if needed
- Consider using ConfigMaps for non-sensitive large data

**Secret Update Behavior:**

**Volume mounts**:
- Kubelet syncs updated Secret data to pods
- Default sync period: 60 seconds (configurable)
- Application must reload files to see changes
- Uses symlinks and atomic directory swaps for updates

**Environment variables**:
- NOT updated when Secret changes
- Requires pod recreation to see new values
- Set during pod creation only

**Secret Rotation:**

Example rotation strategy:
```yaml
# Create new version
kubectl create secret generic db-creds-v2 --from-literal=password=newpass

# Update deployment to use new Secret
kubectl set env deployment/app --from=secret/db-creds-v2 --prefix=DB_

# After validation, delete old Secret
kubectl delete secret db-creds-v1
```

**External Secret Management:**

Integration with external systems:

**Sealed Secrets**:
```yaml
# Encrypt Secrets for Git storage
kubeseal < secret.yaml > sealed-secret.yaml
# Controller decrypts in-cluster
```

**External Secrets Operator**:
```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: db-credentials
spec:
  secretStoreRef:
    name: aws-secrets-manager
  target:
    name: db-credentials
  data:
  - secretKey: password
    remoteRef:
      key: prod/db/password
```

**Troubleshooting Secrets:**

Common issues and solutions:

**Secret not found**:
- Verify Secret exists: `kubectl get secret <name>`
- Check namespace: Secrets are namespace-scoped
- Verify spelling in pod spec

**Permission denied**:
- Check RBAC permissions
- Verify service account has access to Secret
- Review audit logs for access attempts

**Base64 encoding errors**:
```bash
# Correct encoding
echo -n "password" | base64

# Incorrect (includes newline)
echo "password" | base64
```

**Mount path issues**:
- Ensure mount path doesn't conflict with existing directories
- Check that container has permissions to access mount path
- Verify volumeMount name matches volume name

**Comparing Secrets and ConfigMaps:**

| Aspect | Secrets | ConfigMaps |
|--------|---------|------------|
| Purpose | Sensitive data | Non-sensitive config |
| Storage | Base64 encoded | Plain text |
| Size limit | 1 MB | 1 MB |
| Encryption | Optional (at rest) | No |
| Best for | Passwords, tokens, keys | App config, feature flags |
| Visibility | Hidden in kubectl describe | Visible in kubectl describe |

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 61](day-61.md) | [Day 63 →](day-63.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
