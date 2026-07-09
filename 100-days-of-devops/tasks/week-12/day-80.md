# Day 80: Jenkins Chained Builds

## Task Overview

Implement a Jenkins pipeline architecture where multiple jobs are linked together in a dependency chain. The primary job deploys application code, and upon successful completion, it triggers a downstream job that manages services across all application servers. This approach demonstrates separation of concerns, reusability, and conditional execution in CI/CD workflows.

**Technical Specifications:**
- Job architecture: Upstream/downstream chained builds
- Primary job: nautilus-app-deployment (code deployment)
- Secondary job: manage-services (service management)
- Trigger condition: Downstream job runs only if upstream is stable
- Target servers: All three app servers (stapp01, stapp02, stapp03)
- Service management: Apache httpd restart

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Update Jenkins plugins and restart

Navigate to Manage Jenkins > Manage Plugins > Updates:

```text
Actions:
1. Select all available updates
2. Download now and install after restart
3. ☑ Restart Jenkins when installation is complete
```

Update all Jenkins plugins to ensure compatibility and access to the latest features. Plugin updates often include bug fixes, security patches, and new functionality. The restart ensures all updated plugins are properly loaded into Jenkins. Wait 1-2 minutes for Jenkins to restart completely. If the UI doesn't respond, refresh your browser. This maintenance step is crucial before configuring complex job chains to avoid compatibility issues.

**Step 2:** Install required plugins for Git and SSH

Navigate to Manage Jenkins > Manage Plugins > Available:

```text
Required plugins:
- Git plugin (Git repository integration)
- Publish Over SSH (SSH file transfer and command execution)
```

Install the necessary plugins for this workflow. The Git plugin enables Jenkins to clone and manage Git repositories. The Publish Over SSH plugin provides powerful SSH capabilities including file transfers and remote command execution across multiple servers simultaneously. After installation, click "Restart Jenkins when installation is complete and no jobs are running" to activate the plugins. If installation fails, restart Jenkins manually and try again.

**Step 3:** Configure SSH servers for all app servers

Navigate to Manage Jenkins > System > Publish over SSH > SSH Servers:

```yaml
Server 1:
  Name: stapp01
  Hostname: stapp01
  Username: tony
  Remote Directory: /home/tony

Server 2:
  Name: stapp02
  Hostname: stapp02
  Username: steve
  Remote Directory: /home/steve

Server 3:
  Name: stapp03
  Hostname: stapp03
  Username: banner
  Remote Directory: /home/banner

Common configuration for all servers:
  Use password authentication: ☑
  Passphrase/Password: [respective user password]
  Port: 22 (default)
```

Configure SSH connection profiles for all three application servers. The Publish Over SSH plugin uses these profiles to establish connections during job execution. The "Name" field is an identifier you'll reference in jobs. The "Hostname" is the server's network address (can be IP or hostname). "Username" specifies which user account to use for SSH connections. "Remote Directory" is the initial working directory on the remote server. Set passwords for each server (tony: Ir0nM@n, steve: Am3ric@, banner: BigGr33n). After adding all three servers, click "Test Configuration" for each to verify connectivity before saving.

**Step 4:** Create the primary deployment job

Navigate to Jenkins Dashboard > New Item:

```yaml
Job name: nautilus-app-deployment
Type: Freestyle project

Source Code Management section:
  ☑ Git
  Repository URL: http://sarah:Sarah_pass123@gitea:3000/sarah/web.git
  Branch Specifier: */master
  (or use your specific Gitea repository URL)
```

Create the primary job responsible for deploying application code. Select "Freestyle project" for a UI-based configuration approach. In the Source Code Management section, configure the Git repository details. Jenkins will clone this repository into its workspace before executing build steps. The repository URL includes authentication credentials embedded (not ideal for production, but acceptable in lab environments). The branch specifier `*/master` tells Jenkins to build the master branch. This job will focus solely on deployment; service management will be handled by the downstream job.

**Step 5:** Configure deployment build step

In the Build section, add "Execute shell" build step:

```bash
# Deploy files to Storage Server
sshpass -p "Bl@kW" scp -r -o StrictHostKeyChecking=no ./* natasha@ststor01:/var/www/html
```

Add the deployment command that copies files to the Storage Server. The `sshpass` command provides non-interactive password authentication for SSH/SCP. The `-p` flag specifies the password. The `scp` command with `-r` flag recursively copies all files from the current directory (Jenkins workspace, which contains the cloned repository) to `/var/www/html` on the Storage Server. The `-o StrictHostKeyChecking=no` option disables SSH host key verification, preventing interactive prompts. Since `/var/www/html` on ststor01 is a shared volume mounted to all app servers, this single copy operation makes files available to all applications.

**Step 6:** Configure post-build action to trigger downstream job

In the Post-build Actions section:

```yaml
Add Post-build Action: Build other projects

Projects to build: manage-services
Trigger only if build is stable: ☑ (checked)
```

Configure the job to trigger the downstream job after successful completion. Post-build actions execute after the main build steps complete. "Build other projects" creates a dependency relationship between jobs. Enter "manage-services" as the project name (this is the downstream job you'll create next). Checking "Trigger only if build is stable" ensures the downstream job runs only if the deployment succeeds. If deployment fails or is unstable, the service restart won't trigger, preventing restarts on failed deployments. This conditional triggering is crucial for maintaining system stability.

**Step 7:** Create the downstream service management job

Navigate to Jenkins Dashboard > New Item:

```yaml
Job name: manage-services
Type: Freestyle project
```

Create the secondary job that will manage services on app servers. This job has a single, focused responsibility: restarting the Apache service on all application servers. By separating deployment from service management, you create reusable, modular jobs. The manage-services job could potentially be triggered by multiple different deployment jobs, promoting reusability. Freestyle project type provides a simple UI for configuring the SSH commands.

**Step 8:** Configure service restart commands for all app servers

In the Build section, add "Send files or execute commands over SSH" build step (three times, one for each server):

```yaml
Build Step 1:
  SSH Server: stapp01
  Transfers > Exec command:
    echo 'Ir0nM@n' | sudo -S systemctl restart httpd

Build Step 2:
  SSH Server: stapp02
  Transfers > Exec command:
    echo 'Am3ric@' | sudo -S systemctl restart httpd

Build Step 3:
  SSH Server: stapp03
  Transfers > Exec command:
    echo 'BigGr33n' | sudo -S systemctl restart httpd
```

Add three "Send files or execute commands over SSH" build steps, one for each app server. For each build step, select the corresponding SSH server name configured earlier (stapp01, stapp02, stapp03). In the "Exec command" field, enter the command to restart Apache. The `echo 'password' | sudo -S systemctl restart httpd` pattern provides the sudo password via stdin, allowing non-interactive sudo execution. The `-S` flag tells sudo to read the password from stdin. The `systemctl restart httpd` command restarts the Apache web server. These three steps execute sequentially, restarting Apache on all servers to pick up newly deployed files.

**Step 9:** Test the chained build workflow

Execute the primary job and monitor the build chain:

```text
Workflow:
1. Navigate to nautilus-app-deployment
2. Click "Build Now"
3. Monitor Console Output for deployment
4. Observe manage-services job automatically triggered
5. Check manage-services Console Output for service restarts
```

Test the complete workflow by manually triggering the primary job. Click "Build Now" on the nautilus-app-deployment job page. Watch the build progress in the Build History. Once deployment completes successfully, observe the manage-services job automatically appear in the build queue and execute. Click on each build number to view Console Output and verify: (1) deployment copied files successfully to ststor01, and (2) Apache restarted on all three app servers without errors. The entire chain should complete successfully, demonstrating the upstream/downstream relationship.

**Step 10:** Verify application accessibility

```bash
# Access the application via load balancer
# Click "App" button in lab environment
# URL should be: https://<LBR-URL>

# Verify no subdirectories in path
# Content should display from /var/www/html
```

Verify the deployed application is accessible through the load balancer. Click the "App" button in your lab environment to access the application. The load balancer distributes requests across all three app servers, so you're testing that: (1) files deployed correctly to the shared storage, (2) the shared volume is mounted on all app servers, (3) Apache is running on all servers, and (4) the load balancer can reach all backends. Verify the URL is at the root level without subdirectories like `/web`. The content should be the latest version from your Git repository.

**Step 11:** Test workflow with repository changes

Make a change and verify automatic propagation:

```bash
# SSH to Storage Server
ssh natasha@ststor01

# Navigate to repository
cd /var/www/html

# Make a change
echo "<h1>Updated Content</h1>" >> index.html

# Verify through load balancer
# Access app and confirm change is visible
```

Test that changes propagate correctly through the system. Make a simple modification to the deployed files and verify the change appears in the application. This confirms the shared storage architecture is working correctly. In a real workflow, changes would come through Git commits and Jenkins deployments, but this manual test validates the underlying infrastructure. After confirming the manual change works, you can trigger the Jenkins job again to deploy the original content from Git.

**Step 12:** Validate repeatable builds and failure scenarios

```bash
# Test multiple consecutive builds
# Navigate to nautilus-app-deployment
# Click "Build Now" multiple times

# Verify each build:
# - Completes successfully
# - Triggers downstream job
# - manage-services restarts Apache on all servers

# Test failure scenario (optional)
# Temporarily break the deployment (e.g., wrong credentials)
# Verify downstream job does NOT trigger on failure
# Restore configuration and verify it works again
```

Validate that the job chain is idempotent and handles failures correctly. Run the deployment job multiple times in succession to ensure it's safe to execute repeatedly (critical for automated environments). Each run should complete successfully and trigger the downstream job. Optionally, test the failure scenario: temporarily introduce an error in the deployment job (like incorrect credentials), run the job, and verify that the downstream service management job does NOT trigger. This confirms the "Trigger only if build is stable" condition is working. Restore the correct configuration and verify successful operation again.

**Step 13:** Additional monitoring and troubleshooting

```bash
# View job chain visualization
# Jenkins Dashboard > Build Pipeline View plugin (if installed)

# Check individual build details
# Job > Build #N > Console Output
# Look for error messages or warnings

# Verify Apache status on app servers
ssh tony@stapp01
systemctl status httpd

ssh steve@stapp02
systemctl status httpd

ssh banner@stapp03
systemctl status httpd

# Check Publish Over SSH configuration
# Manage Jenkins > System > Publish over SSH
# Use "Test Configuration" for each server

# View build history
# Each job page > Build History
# Shows success/failure trend over time
```

Use these monitoring and troubleshooting techniques to maintain and debug your job chain. The Console Output for each build provides detailed logs of all executed commands and their output. Check Apache status on each app server to confirm services are running after restarts. Test SSH configurations if connections fail. The build history provides a visual overview of job success/failure patterns over time. Common issues include SSH connectivity problems, incorrect credentials, permission errors on remote directories, or service failures due to configuration problems.

---

## Key Concepts

**Chained Builds Architecture:**
- **Upstream Jobs**: Jobs that trigger other jobs upon completion
- **Downstream Jobs**: Jobs triggered by successful upstream jobs
- **Build Dependencies**: Defined relationships between jobs
- **Conditional Triggers**: Execute downstream jobs based on upstream status

**Separation of Concerns:**
- **Single Responsibility**: Each job has one primary purpose
- **Modularity**: Jobs can be reused in different chains
- **Maintainability**: Changes to one job don't affect others
- **Debugging**: Easier to isolate problems to specific jobs

**Build Stability Conditions:**
- **Stable**: Build completed successfully
- **Unstable**: Build completed with warnings or test failures
- **Failed**: Build failed to complete
- **Trigger Logic**: Downstream jobs can require specific stability levels

**Post-Build Actions:**
- **Build Triggers**: Start other jobs after completion
- **Artifact Archiving**: Save build outputs
- **Notifications**: Email, Slack, or other alerts
- **Publishing**: Deploy artifacts or publish reports

**Publish Over SSH Plugin:**
- **SSH Server Profiles**: Reusable server configurations
- **File Transfer**: SCP-like file copying to remote servers
- **Remote Execution**: Run commands on multiple servers
- **Build Step Integration**: Used within freestyle and pipeline jobs

**Service Management Patterns:**
- **Rolling Restarts**: Restart services one server at a time
- **Parallel Restarts**: Restart all servers simultaneously (this task)
- **Health Checks**: Verify service health after restart
- **Graceful Shutdown**: Stop services cleanly before restart

---

## Validation

Test your solution using KodeKloud's automated validation.

**Validation Checklist:**
- All Jenkins plugins installed and updated
- SSH server profiles configured for stapp01, stapp02, stapp03
- Job "nautilus-app-deployment" created as Freestyle project
- nautilus-app-deployment pulls from Git repository
- Deployment copies files to /var/www/html on Storage Server
- Post-build action configured to trigger manage-services
- Trigger condition set to "only if build is stable"
- Job "manage-services" created as Freestyle project
- manage-services restarts httpd on all three app servers
- Building nautilus-app-deployment triggers manage-services automatically
- Application accessible via load balancer at root URL
- Jobs are idempotent (safe to run multiple times)
- Downstream job does NOT trigger if upstream fails

---

[← Day 79](day-79.md) | [Day 81 →](day-81.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
