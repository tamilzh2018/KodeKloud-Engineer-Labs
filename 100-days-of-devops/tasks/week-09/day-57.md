# Day 57: Environment Variables in Kubernetes Pods

## Task Overview

Configure a Kubernetes pod to use environment variables for dynamic application configuration. Environment variables provide a flexible way to inject configuration data into containerized applications without rebuilding images, enabling runtime customization and supporting the twelve-factor app methodology.

**Technical Specifications:**
- Pod name: print-envars-greeting
- Container: print-env-container (bash image)
- Environment variables: GREETING, COMPANY, GROUP
- Command: Echo statement using variable interpolation
- Restart policy: Never (prevents crash loops)

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Create a pod manifest with environment variables

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: print-envars-greeting
spec:
  restartPolicy: Never
  containers:
  - name: print-env-container
    image: bash
    command: ["/bin/sh", "-c", 'echo "$(GREETING) $(COMPANY) $(GROUP)"']
    env:
    - name: GREETING
      value: "Welcome to"
    - name: COMPANY
      value: "xFusionCorp"
    - name: GROUP
      value: "Group"
```

Create a YAML manifest file that defines a pod with three environment variables. The `env` section under the container specification declares each variable with a name-value pair. The `command` field uses shell variable interpolation syntax `$(VARIABLE_NAME)` to reference these environment variables within the container's execution context. The `restartPolicy: Never` ensures the pod runs once and terminates without restarting, which is appropriate for job-like workloads that execute a single task.

**Step 2:** Apply the pod configuration to the cluster

```bash
kubectl apply -f k3s-pod.yml
```

Deploy the pod to your Kubernetes cluster using `kubectl apply`. This command reads the YAML manifest and creates the pod resource in the default namespace. Kubernetes schedules the pod on an available node, pulls the bash image if not already cached, injects the environment variables into the container, and executes the specified command. The declarative approach allows you to version control your configuration and ensures reproducibility across environments.

**Step 3:** View the output from the environment variables

```bash
kubectl logs -f print-envars-greeting
```

Retrieve and display the container's stdout logs using `kubectl logs`. The `-f` flag follows the log stream (similar to `tail -f`), though with restartPolicy: Never, the pod will have already completed. You should see the output: "Welcome to xFusionCorp Group" which confirms that the environment variables were properly injected and interpolated by the shell command. This validates that your environment variable configuration is working correctly.

**Step 4:** Verify pod status and details

```bash
# Check pod status
kubectl get pods

# Get detailed pod information including environment variables
kubectl describe pod print-envars-greeting

# View environment variables inside a running container
kubectl exec print-envars-greeting -- env
```

These commands provide comprehensive verification of your pod deployment. The `get pods` command shows the pod status (should be Completed). The `describe` command displays the full pod specification including all environment variables in human-readable format. The `exec -- env` command runs the env utility inside the container to show all environment variables, including those automatically injected by Kubernetes for service discovery.

**Step 5:** Clean up resources

```bash
# Delete the pod
kubectl delete pod print-envars-greeting

# Verify deletion
kubectl get pods
```

Remove the pod from your cluster to clean up resources. The `delete` command removes the pod and its associated resources. Since this pod uses restartPolicy: Never, it won't be automatically recreated. Always clean up test resources to maintain a tidy cluster and avoid resource consumption. The second command verifies the pod has been successfully removed from the cluster.

---

## Key Concepts

**Environment Variable Types in Kubernetes:**
- **Static Values**: Hardcoded values defined directly in pod spec (as shown in this task)
- **ConfigMap References**: Environment variables sourced from ConfigMap key-value pairs
- **Secret References**: Sensitive data sourced from Kubernetes Secrets (base64 encoded)
- **Field References**: Dynamic values from pod metadata (pod name, namespace, IP)
- **Resource References**: Container resource limits and requests
- **Downward API**: Expose pod/container information as environment variables

**Environment Variable Sources:**

ConfigMaps provide a way to externalize configuration:
```yaml
env:
- name: DATABASE_HOST
  valueFrom:
    configMapKeyRef:
      name: app-config
      key: db_host
```

Secrets provide secure storage for sensitive data:
```yaml
env:
- name: DATABASE_PASSWORD
  valueFrom:
    secretKeyRef:
      name: db-secret
      key: password
```

Field references allow accessing pod metadata:
```yaml
env:
- name: POD_NAME
  valueFrom:
    fieldRef:
      fieldPath: metadata.name
- name: POD_IP
  valueFrom:
    fieldRef:
      fieldPath: status.podIP
```

**Container Restart Policies:**
- **Never**: Container never restarts, used for batch jobs and one-time tasks
- **OnFailure**: Restarts only if container exits with non-zero status
- **Always**: Always restarts regardless of exit status (default for pods)

**Environment Variable Best Practices:**
- Use ConfigMaps for non-sensitive configuration data to separate config from code
- Use Secrets for passwords, tokens, and certificates to protect sensitive information
- Validate required environment variables in application startup code
- Document expected environment variables in application documentation
- Use meaningful variable names that clearly indicate purpose (avoid cryptic names)
- Avoid storing large amounts of data in environment variables (use volumes instead)
- Consider using dotenv files during development and environment variables in production
- Never commit secrets to version control, even in environment variable form

**Twelve-Factor App Methodology:**
The third factor of the twelve-factor app methodology states that configuration should be stored in the environment. This means:
- Configuration varies between deployments (dev, staging, production) but code doesn't
- Environment variables are language and OS-agnostic
- Configuration is strictly separated from code
- There's little chance of accidentally committing config to source control
- Applications are easily portable across different environments

**Variable Interpolation in Containers:**
When using environment variables in commands, the interpolation happens based on the shell:
- `$(VARNAME)`: POSIX shell variable syntax, processed by the shell at runtime
- `$VARNAME`: Alternative syntax, also processed by the shell
- `${VARNAME}`: Braced syntax, useful for concatenation
- Shell interpolation requires command to be executed through a shell (`/bin/sh -c`)
- Without a shell, variable references are passed literally to the application

**Kubernetes Service Discovery via Environment Variables:**
Kubernetes automatically injects environment variables for services in the same namespace:
- `{SVCNAME}_SERVICE_HOST`: Service cluster IP address
- `{SVCNAME}_SERVICE_PORT`: Service primary port number
- Format: Service name is uppercased, hyphens become underscores
- These are created only for services that exist before the pod is created
- For dynamic service discovery, use DNS instead of environment variables

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 56](../week-08/day-56.md) | [Day 58 →](day-58.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
