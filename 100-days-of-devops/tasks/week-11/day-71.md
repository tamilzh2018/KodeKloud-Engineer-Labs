# Day 71: Configure Jenkins Job for Package Installation

## Task Overview

Create a parameterized Jenkins job that installs software packages on remote servers via SSH. This automation enables centralized package management across infrastructure without manual intervention on each server.

**Technical Specifications:**
- Job type: Freestyle project with parameters
- Parameter: String parameter for package names
- Execution: Remote SSH command execution
- Target: Storage server in Stratos Datacenter
- Authentication: SSH credentials stored in Jenkins

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Access Jenkins UI and log in

```
Username: admin
Password: Adm!n321
```

Open the Jenkins web interface by clicking the Jenkins button in the top bar. Enter the administrator credentials to access the Jenkins dashboard. The admin user has full permissions to create jobs, manage plugins, configure system settings, and manage credentials. This is your central control point for all CI/CD automation tasks.

**Step 2:** Install required SSH plugins

Navigate to Manage Jenkins > Manage Plugins > Available tab and install:
- SSH plugin
- SSH Credentials plugin
- SSH Build Agents plugin

Then select "Restart Jenkins when installation is complete and no jobs are running"

Jenkins plugins extend functionality beyond the core features. The SSH plugin enables Jenkins to execute commands on remote servers via SSH protocol. The SSH Credentials plugin provides secure storage for SSH authentication (username/password or private keys). The SSH Build Agents plugin allows Jenkins to use remote servers as build agents. After installation, Jenkins must restart to load the new plugins into memory. The restart option ensures Jenkins waits for running jobs to complete before restarting, preventing job interruption.

**Step 3:** Add SSH credentials for storage server

Go to Manage Jenkins > Credentials > System > Global credentials (unrestricted) > Add Credentials

Configure credential details:
- Kind: Username with password
- Scope: Global
- Username: natasha (storage server user)
- Password: Bl@kW (storage server password)
- ID: storage-server-creds (descriptive identifier)
- Description: Storage Server SSH Credentials

The Jenkins credentials store provides centralized, encrypted storage for authentication data. Global scope means these credentials are available to all Jenkins jobs. The ID is a unique identifier you'll reference when configuring jobs. Never hardcode credentials in job scripts - always use the credential store. This follows security best practices by separating secrets from code and providing audit trails of credential usage.

**Step 4:** Configure SSH remote host

Go to Manage Jenkins > Configure System > Scroll to "SSH remote hosts" section

Add SSH site with:
- Hostname: ststor01 (storage server hostname)
- Port: 22 (default SSH port)
- Credentials: Select "storage-server-creds" from dropdown
- Pty: Check this box (enables pseudo-terminal)
- Server Alive Interval: 0 (disable keepalive)
- Timeout: 0 (no connection timeout)

This configuration registers the storage server as a known SSH target for Jenkins. The hostname must be resolvable via DNS or defined in /etc/hosts. Port 22 is the standard SSH port. The Pty (pseudo-terminal) option allocates a terminal for the SSH session, which some commands require. Server Alive Interval and Timeout settings control connection behavior - zero values use system defaults. This configuration is reusable across multiple jobs targeting the same server.

**Step 5:** Create parameterized freestyle job

Dashboard > New Item
- Name: install-packages
- Type: Freestyle project
- Click OK

In the job configuration page, enable "This project is parameterized"
- Click "Add Parameter" > "String Parameter"
- Name: PACKAGE
- Default Value: (leave empty)
- Description: Name of the package to install

The freestyle project is Jenkins' simplest job type, suitable for single-task automation. Parameterization makes jobs flexible and reusable - the same job can install different packages based on runtime input. The PACKAGE parameter becomes an environment variable accessible in build steps as $PACKAGE. String parameters accept any text input. Leaving the default value empty forces users to explicitly specify a package name, preventing accidental installations.

**Step 6:** Add build step for remote execution

In Build section, click "Add build step" > "Execute shell script on remote host using ssh"

Configure:
- SSH site: Select "ststor01" from dropdown
- Command:
```sh
sudo yum install -y $PACKAGE
```

This build step executes the installation command on the remote storage server via SSH. The $PACKAGE variable is replaced with the parameter value provided at build time. The `sudo` command runs the installation with elevated privileges (requires the remote user to have sudo access). The `yum install -y` command is the package manager for RHEL/CentOS systems - the `-y` flag automatically confirms installation prompts, enabling unattended automation. The command output appears in the Jenkins build console for troubleshooting.

**Step 7:** Save and test the job

Click "Apply" and "Save"

To execute:
1. Dashboard > install-packages > Build with Parameters
2. Enter package name (e.g., "httpd", "git", "wget")
3. Click "Build"
4. Monitor console output for success/failure

The "Build with Parameters" option appears because you configured the job as parameterized. Jenkins displays a form to collect parameter values before execution. After clicking Build, Jenkins creates a new build instance (build #1, #2, etc.). The console output shows real-time command execution on the remote server, including yum's package resolution, download progress, and installation confirmation. Successful completion returns exit code 0; failures return non-zero codes and mark the build as failed.

**Step 8:** Verify installation on storage server

```sh
ssh natasha@ststor01
rpm -qa | grep package-name
```

Connect to the storage server via SSH to manually verify the package installation. The `rpm -qa` command queries all installed packages on RPM-based systems (RHEL/CentOS). Piping to `grep package-name` filters the output to show only the package you installed. You should see the package name with its version number. This verification step confirms the Jenkins job worked correctly and validates your automation workflow end-to-end.

---

## Key Concepts

**Jenkins Remote Execution:**
- SSH Plugin: Executes shell commands on remote Linux/Unix servers via SSH protocol
- Credential Management: Centralized, encrypted storage for passwords, SSH keys, and tokens
- Remote Hosts: Pre-configured SSH targets (hostname, port, credentials) reusable across jobs
- Parameterized Jobs: Dynamic job configuration with user-supplied or triggered values

**SSH Configuration:**
- Host Key Verification: Disabled for automation (accepts any host key) - security consideration
- Authentication Methods: Username/password (simple) or SSH key-based (more secure)
- Connection Pooling: Reuses SSH connections for efficiency in multi-step jobs
- Timeout Settings: Connection timeout (initial connection) and execution timeout (command duration)

**Package Management Automation:**
- Remote Installation: Deploy packages to multiple servers from centralized control point
- Idempotent Operations: Safe to run multiple times (yum won't reinstall existing packages)
- Error Handling: Non-zero exit codes trigger Jenkins build failures with notifications
- Logging: Complete installation logs captured in Jenkins build console for audit and troubleshooting

**Best Practices:**
- Credential Security: Never hardcode passwords; always use Jenkins credential store with encryption
- Parameter Validation: Validate user inputs to prevent injection attacks or invalid package names
- Error Recovery: Configure build notifications and retry logic for network or execution failures
- Audit Trail: Jenkins logs all remote operations with timestamps, user info, and full output

---

## Validation

Test your solution using KodeKloud's automated validation.

Verify the job can:
1. Accept different package names as parameters
2. Successfully install packages on the storage server
3. Run multiple times without errors (idempotency)
4. Show clear success/failure status in build history

---

[← Day 70](../week-10/day-70.md) | [Day 72 →](day-72.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
