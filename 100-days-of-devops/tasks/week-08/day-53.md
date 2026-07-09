# Day 53: Resolve VolumeMounts Issue in Kubernetes

## Task Overview

Debug and fix a multi-container pod with volume mount path mismatches preventing proper file sharing between nginx and PHP-FPM containers. This troubleshooting exercise demonstrates volume configuration issues and their resolution.

**Technical Specifications:**
- Pod: nginx-phpfpm (existing, non-functional)
- Containers: nginx-container and php-fpm-container
- ConfigMap: nginx-config (contains nginx configuration)
- Problem: Volume mount path mismatch between containers
- Solution: Align shared volume paths and copy application files

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Export the existing pod configuration to a file

```sh
kubectl get pod nginx-phpfpm -o yaml > nginx-phpfpm.yml
```

Extract the current pod configuration in YAML format and save it to a file for editing. The `kubectl get pod` command with `-o yaml` flag outputs the complete pod specification including all Kubernetes-added fields like status, metadata, and system-managed volumes. The `>` operator redirects this output to a file named nginx-phpfpm.yml. This exported file serves as a working copy that you can modify to fix the volume mount issue. The file includes not just your original configuration but also runtime information added by Kubernetes, which needs to be considered when making changes.

**Step 2:** Analyze the ConfigMap to determine correct mount paths

```sh
kubectl get configmap nginx-config -o yaml
```

```yaml
apiVersion: v1
data:
  nginx.conf: |
    events {
    }
    http {
      server {
        listen 8099 default_server;
        listen [::]:8099 default_server;

        # Set nginx to serve files from the shared volume!
        root /var/www/html;
        index  index.html index.htm index.php;
        server_name _;
        location / {
          try_files $uri $uri/ =404;
        }
        location ~ \.php$ {
          include fastcgi_params;
          fastcgi_param REQUEST_METHOD $request_method;
          fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
          fastcgi_pass 127.0.0.1:9000;
        }
      }
    }
kind: ConfigMap
```

Examine the nginx ConfigMap to identify the correct document root path that nginx expects. The `kubectl get configmap` command with `-o yaml` displays the ConfigMap's data section. In this nginx configuration, the critical line is `root /var/www/html;` which specifies that nginx will serve files from `/var/www/html`. This is the **authoritative source** for determining the correct shared volume path. Both nginx and PHP-FPM must mount the shared volume at `/var/www/html` for them to access the same files. The nginx configuration also shows that PHP requests (location ~ \.php$) are forwarded to PHP-FPM on localhost:9000, requiring both containers to access files from the same directory.

**Step 3:** Edit the pod manifest to fix volume mount paths

```sh
vi nginx-phpfpm.yml
```

Open the exported pod configuration in a text editor to fix the volume mount mismatch. Look for the `volumeMounts` sections in both containers. The issue is that the containers are mounting the `shared-files` volume at different paths:
- **php-fpm-container**: Currently mounting at `/var/www/html` (correct)
- **nginx-container**: Currently mounting at `/usr/share/nginx/html` (incorrect - default nginx path)

The nginx-container's mount path must be changed from `/usr/share/nginx/html` to `/var/www/html` to match:
1. The PHP-FPM container's mount path
2. The document root specified in the nginx ConfigMap

Find this section in the YAML:
```yaml
- image: nginx:latest
  name: nginx-container
  volumeMounts:
  - mountPath: /usr/share/nginx/html  # Change this to /var/www/html
    name: shared-files
```

Change the mountPath to `/var/www/html`. You should also remove any Kubernetes-added fields from the exported YAML that shouldn't be in your manifest (like `status`, `resourceVersion`, `uid`, etc.) to create a clean configuration file.

**Step 4:** Delete and recreate the pod with corrected configuration

```sh
kubectl delete pod nginx-phpfpm
kubectl apply -f nginx-phpfpm.yml
```

Remove the broken pod and create a new one with the corrected volume mount configuration. The `kubectl delete pod` command terminates the existing pod and removes it from the cluster. This is necessary because pod specifications are immutable - you cannot modify volume mounts on a running pod. The `kubectl apply -f` command then creates a new pod using the fixed configuration. Kubernetes schedules the new pod, pulls the container images if needed, and starts both containers with the correct shared volume paths. Now both nginx and PHP-FPM can access the same files at `/var/www/html`, enabling proper communication between the web server and PHP processor.

**Step 5:** Copy the application file to the nginx container

```sh
kubectl cp /home/thor/index.php nginx-phpfpm:/var/www/html/index.php -c nginx-container
```

Copy the PHP application file from the jump host into the shared volume inside the pod. The `kubectl cp` command transfers files between your local filesystem and containers running in Kubernetes. The syntax is `kubectl cp source destination -c container-name`. Here, we're copying `/home/thor/index.php` from the local machine to `/var/www/html/index.php` inside the pod. The `-c nginx-container` flag specifies which container to copy into (required for multi-container pods). Since the shared-files volume is mounted at `/var/www/html` in **both** containers, the file becomes immediately available to both nginx and PHP-FPM, even though we copied it into the nginx container.

**Step 6:** Test the application functionality

```sh
curl http://localhost:8080
```

Verify that the nginx and PHP-FPM setup is working correctly by making an HTTP request to the application. The `curl` command sends a request to the service endpoint (port 8080 on localhost maps to the pod's port 8099 via the Service). When the request hits nginx:
1. Nginx receives the request on port 8099
2. Nginx looks for index.php in /var/www/html (the shared volume)
3. Nginx forwards .php requests to PHP-FPM on localhost:9000
4. PHP-FPM processes index.php (also accessing it from /var/www/html shared volume)
5. PHP-FPM returns the processed content to nginx
6. Nginx sends the response back to the client

A successful response confirms that both containers can access the shared file and communicate properly.

---

## Key Concepts

**Volume Mount Paths:**
- **Consistency Requirement**: Containers sharing data must mount volumes at the same path or have coordinated paths
- **Application-Specific Paths**: Mount paths must align with application expectations (nginx document root, PHP-FPM working directory)
- **Path Conflicts**: Each container can mount the same volume at different paths, but shared data requires path coordination
- **Configuration Alignment**: Check ConfigMaps and application configs to determine correct mount paths

**Multi-Container Pods:**
- **Shared Volumes**: Primary mechanism for file sharing between containers in the same pod
- **Localhost Network**: Containers share network namespace, can communicate via localhost
- **Sidecar Pattern**: Helper containers alongside main application (nginx serving PHP-FPM processed files)
- **Lifecycle Coupling**: All containers in a pod start/stop together, scheduled on same node
- **Use Cases**: Web server + application server, app + log shipper, app + monitoring agent

**Volume Types in Kubernetes:**
- **emptyDir**: Temporary storage created when pod is assigned to node, deleted when pod is removed. Perfect for scratch space or sharing between containers
- **hostPath**: Mounts directory from host node filesystem. Risky for multi-node clusters as data is node-specific
- **persistentVolumeClaim**: Requests persistent storage that survives pod restarts and moves
- **configMap**: Mounts configuration data as files, ideal for config files like nginx.conf
- **secret**: Similar to ConfigMap but for sensitive data, with encryption at rest

**ConfigMap Volumes:**
- **Configuration Files**: Mount entire ConfigMaps or individual keys as files
- **subPath**: Mount specific ConfigMap entry to a file without overwriting entire directory
- **File Permissions**: Can set mode/permissions for mounted files via `defaultMode`
- **Dynamic Updates**: Changes to ConfigMap can propagate to mounted volumes (with delay), though not for subPath mounts
- **Use Cases**: Application configs, web server configs, script files, certificate configuration

**Troubleshooting Techniques:**
- **kubectl describe pod**: Shows events, mount points, and errors - first stop for debugging
- **kubectl logs pod-name -c container-name**: View container logs to identify application-level errors
- **kubectl exec**: Access container shell to inspect filesystem, check mounted files, test connectivity
- **kubectl get pod -o yaml**: Export complete pod configuration to analyze volume definitions
- **Check ConfigMaps/Secrets**: Verify configuration objects exist and contain expected data
- **Volume inspection**: Exec into containers and use `ls`, `cat`, `df` to verify mounts

**Common Volume Issues:**
- **Mount Path Mismatch**: Containers expect files at different locations (like this exercise)
- **Missing ConfigMap/Secret**: Pod references non-existent configuration object
- **Permission Problems**: Container user lacks permissions to read/write mounted files
- **Subpath Issues**: Incorrect subPath causes wrong file to be mounted or mount failure
- **HostPath Restrictions**: Security policies or node-specific paths prevent hostPath mounts
- **PVC Binding**: PersistentVolumeClaim remains unbound due to storage class or capacity issues

**Pod Immutability:**
- Most pod specifications cannot be changed after creation (including volumes, containers, images)
- To fix volume mounts, you must delete and recreate the pod
- Deployments handle this automatically during updates via pod replacement
- For standalone pods, manual delete/recreate is required
- Some fields like container image (in certain k8s versions) and resource limits may be mutable

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 52](day-52.md) | [Day 54 →](day-54.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
