# Day 79: Jenkins Deployment Job with Webhook Automation

## Task Overview

Configure a fully automated Jenkins deployment pipeline triggered by Git webhooks. When developers push code changes to the repository, Jenkins automatically detects the change, builds the job, and deploys the latest code to all application servers. This implements continuous deployment (CD) principles for rapid, automated software delivery.

**Technical Specifications:**
- Job type: Jenkins Freestyle Project
- Trigger mechanism: Git webhook (automatic on push)
- Web server: Apache (httpd) on port 8080
- Deployment target: /var/www/html (shared across app servers)
- Source control: Gitea repository (sarah/web)
- Automation level: Fully automated (no manual intervention)

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Access Jenkins and upgrade plugins

Navigate to Manage Jenkins > Manage Plugins > Updates:

```text
Actions:
1. Check for updates
2. Select all available updates
3. Download and install after restart
4. ☑ Restart Jenkins when installation is complete
```

Update all Jenkins plugins to their latest versions to ensure compatibility and security. Outdated plugins can cause unexpected behavior, security vulnerabilities, or compatibility issues with newer Jenkins versions. After selecting updates, check "Restart Jenkins when installation is complete and no jobs are running" to automatically restart the service. Jenkins may take 1-2 minutes to restart; the UI might appear frozen during this time. If the page doesn't load after restart, manually refresh your browser. Keeping plugins updated is a critical maintenance task for any Jenkins installation.

**Step 2:** Install required plugins for Git and SSH

Navigate to Manage Jenkins > Manage Plugins > Available:

```text
Required plugins:
- SSH Pipeline Steps (remote command execution)
- Gitea (Git server integration)
- Pipeline (pipeline job support)
- Git plugin (Git repository integration)
```

Install the plugins necessary for this deployment workflow. SSH Pipeline Steps enables Jenkins to execute commands on remote servers via SSH. The Gitea plugin provides native integration with Gitea Git servers, including webhook support. If installation fails, restart Jenkins and try again (plugin installation can be flaky). After installation, click "Restart Jenkins when installation is complete and no jobs are running". These plugins extend Jenkins core functionality to support remote deployment and Git-based automation.

**Step 3:** Configure Storage Server SSH credentials

Navigate to Manage Jenkins > Credentials > System > Global credentials > Add Credentials:

```yaml
Kind: Username with password
Scope: Global
Username: natasha
Password: Bl@kW
ID: storage-server-creds
Description: Storage Server (natasha)
```

Store the Storage Server credentials securely in Jenkins credential store. Jenkins encrypts credentials and injects them into jobs at runtime, preventing exposure in job configurations or console output. The credential ID `storage-server-creds` is a reference you'll use in jobs to access these credentials without hardcoding passwords. The scope "Global" makes credentials available to all Jenkins jobs. Never hardcode passwords directly in job configurations or pipeline scripts; always use the credentials system for security and maintainability.

**Step 4:** Install and configure Apache on all app servers

Create a temporary pipeline job to install httpd:

```groovy
pipeline {
    agent any

    parameters {
        string(name: 'HOSTNAME', description: 'Target server hostname')
        string(name: 'USER', description: 'SSH username')
        password(name: 'PASSWORD', description: 'SSH password')
        string(name: 'PACKAGE', defaultValue: 'httpd', description: 'Package to install')
    }

    stages {
        stage('Install Package') {
            steps {
                script {
                    def remote = [:]
                    remote.name = params.HOSTNAME
                    remote.host = params.HOSTNAME
                    remote.user = params.USER
                    remote.password = params.PASSWORD
                    remote.allowAnyHosts = true

                    sshCommand remote: remote, command: """
                        sudo yum install -y ${params.PACKAGE}
                        sudo sed -i 's/Listen 80/Listen 8080/g' /etc/httpd/conf/httpd.conf
                        sudo systemctl start httpd
                        sudo systemctl enable httpd
                        sudo systemctl status httpd
                    """
                }
            }
        }
    }
}
```

Create a reusable installation job that installs Apache on app servers. Run this job three times with different parameters for each app server (stapp01, stapp02, stapp03). The pipeline uses the SSH Pipeline Steps plugin to remotely execute commands. The `sed` command modifies Apache's configuration to listen on port 8080 instead of the default port 80. The `systemctl` commands start Apache, enable it to start on boot, and verify it's running. This separates infrastructure setup from deployment logic. After running for all three app servers, you can delete this temporary job.

**Step 5:** Configure Gitea server in Jenkins

Navigate to Manage Jenkins > System > Gitea Servers:

```yaml
Add Gitea Server:
  Name: gitea
  Server URL: http://gitea:3000
  Manage hooks: ☑ (checked)
```

Register the Gitea server with Jenkins to enable webhook integration. The server URL points to the Gitea instance in your lab environment. Enabling "Manage hooks" allows Jenkins to automatically create and manage webhooks in Gitea repositories. This configuration enables the Jenkins Gitea plugin to communicate with your Git server, detect repository changes, and trigger builds automatically. The name "gitea" is an identifier used in job configurations to reference this server.

**Step 6:** Generate Jenkins API token for webhook authentication

Navigate to Manage Jenkins > Users > admin > Configure > API Token:

```text
Actions:
1. Click "Add new Token"
2. Name: webhook-token
3. Generate
4. Copy the generated token (e.g., 11a3bafd516952ecf4b9103a02348f653c)
```

Generate an API token that Gitea will use to authenticate webhook requests to Jenkins. API tokens provide secure, programmatic access to Jenkins without using passwords. The token acts as a credential for webhook calls from Gitea to Jenkins. Copy this token immediately; Jenkins only shows it once. If you lose it, you'll need to generate a new one. This token allows external systems like Gitea to trigger Jenkins jobs while maintaining security through authentication.

**Step 7:** Create the deployment job with remote trigger

Navigate to Jenkins Dashboard > New Item:

```yaml
Job name: nautilus-app-deployment
Type: Freestyle project

Build Triggers section:
  ☑ Trigger builds remotely
  Authentication Token: kodekloud
```

Create a freestyle Jenkins job that can be triggered remotely via webhook. The authentication token "kodekloud" (you can choose any value) provides an additional layer of security for remote triggers. The webhook URL will include this token, ensuring that only requests with the correct token can trigger builds. Freestyle projects provide a simpler, UI-based configuration compared to pipeline jobs, making them suitable for straightforward deployment workflows.

**Step 8:** Configure deployment build steps

In the Build section, add "Execute shell" build step:

```bash
# Clean workspace and clone repository
rm -rf web
git clone http://sarah:Sarah_pass123@gitea:3000/sarah/web.git

# Deploy to Storage Server
cd web
sshpass -p "Bl@kW" scp -r -o StrictHostKeyChecking=no ./* natasha@ststor01:/var/www/html
```

Configure the deployment commands that will execute when the job runs. First, clean any existing `web` directory to ensure a fresh clone. Then clone the repository using Gitea credentials (replace with actual values from your lab). The `sshpass` command allows non-interactive SSH authentication by providing the password via command line. The `scp` command copies all files from the cloned repository to the Storage Server's `/var/www/html` directory. The `-r` flag enables recursive copy for directories, and `-o StrictHostKeyChecking=no` disables SSH host key verification (acceptable in lab environments but not recommended for production). Since `/var/www/html` on the Storage Server is mounted to all app servers, this single copy operation deploys to all servers simultaneously.

**Step 9:** Configure Gitea webhook to trigger Jenkins

Login to Gitea (click Gitea button, use sarah/Sarah_pass123):

Navigate to Repository: web > Settings > Webhooks > Add Webhook > Gitea:

```yaml
Target URL: https://admin:<API-TOKEN>@<JENKINS-URL>/job/nautilus-app-deployment/build?token=kodekloud

Example:
https://admin:11a3bafd516952ecf4b9103a02348f653c@8080-port-3c6aqh4fy2nkx3vf.labs.kodekloud.com/job/nautilus-app-deployment/build?token=kodekloud

HTTP Method: POST
Post Content Type: application/json
Trigger On: Push events
Active: ☑ (checked)
```

Configure the Git repository to send webhook notifications to Jenkins on every push. The webhook URL contains several components: the Jenkins admin username, the API token for authentication, your Jenkins URL, the job name, and the authentication token defined in the job. The format is `https://USERNAME:API_TOKEN@JENKINS_URL/job/JOB_NAME/build?token=AUTH_TOKEN`. When developers push code, Gitea sends an HTTP POST request to this URL, triggering a Jenkins build. After saving, click "Test Delivery" to verify the webhook works. A successful test returns HTTP 200 and triggers a Jenkins build.

**Step 10:** Set permissions on Storage Server deployment directory

SSH into the Storage Server and configure permissions:

```bash
# SSH to Storage Server
ssh natasha@ststor01
# Password: Bl@kW

# Set ownership for deployment directory
sudo chown -R natasha:natasha /var/www/html

# Verify permissions
ls -la /var/www/html
```

Grant the `natasha` user full ownership of `/var/www/html` so Jenkins can deploy files without permission errors. The `chown` command recursively (`-R`) changes the owner and group to `natasha`. Without proper permissions, the `scp` command in the Jenkins job will fail with "Permission denied" errors. After setting permissions, verify with `ls -la` to confirm `natasha` owns the directory and its contents. This is a critical step that must be completed before the first deployment.

**Step 11:** Test automated deployment workflow

SSH to Storage Server as sarah user and make a code change:

```bash
# Switch to sarah user
sudo su - sarah

# Navigate to repository
cd /home/sarah/web

# Edit index.html
vi index.html
# Change content to: Welcome to the xFusionCorp Industries

# Commit and push changes
git add index.html
git commit -m "Update welcome message"
git push origin master
```

Trigger the automated deployment by making a code change as a developer would. Switch to the sarah user (the developer account), navigate to her repository, modify `index.html`, commit the change, and push to the origin. The git push triggers the Gitea webhook, which calls Jenkins, which automatically runs the nautilus-app-deployment job. Watch the Jenkins dashboard; you should see a new build start immediately after the push. This simulates the real-world continuous deployment workflow where developer commits automatically trigger deployments.

**Step 12:** Verify deployment and application accessibility

```bash
# Check Jenkins job status
# Navigate to: nautilus-app-deployment > Build History > Console Output

# Access application via load balancer
# Click "App" button in lab environment
# Verify URL: https://<LBR-URL>
# Content should show: Welcome to the xFusionCorp Industries
```

Verify the deployment was successful by checking multiple points. First, examine the Jenkins console output to ensure the build succeeded without errors. Look for "SUCCESS" status and verify all commands executed properly. Then access the application through the load balancer by clicking the "App" button. The page should display your updated content "Welcome to the xFusionCorp Industries". Verify the URL is at the root level (e.g., `https://LBR-URL/`) without subdirectories like `/web`. If content doesn't update, check file permissions, Jenkins console for errors, or manually verify files on the Storage Server.

**Step 13:** Validate repeatable builds and troubleshooting

```bash
# Test multiple deployments
# Make another change to index.html and push
# Verify Jenkins automatically triggers again

# Troubleshooting commands
# Check webhook delivery in Gitea
# Gitea > Repo > Settings > Webhooks > Recent Deliveries

# Verify SSH connectivity
ssh natasha@ststor01
ls -la /var/www/html

# Check Apache status on app servers
ssh tony@stapp01
sudo systemctl status httpd

# View Jenkins system log
# Manage Jenkins > System Log
```

Test that the deployment pipeline works reliably on multiple runs. Make additional changes and verify Jenkins triggers automatically each time. The validation system may run the job multiple times, so it must be idempotent (safe to run repeatedly without side effects). Use the troubleshooting commands to diagnose issues: check Gitea's webhook delivery history to see if webhooks are sent successfully, SSH to servers to verify files and services, and review Jenkins system logs for errors. Common issues include incorrect credentials, network connectivity problems, permission errors, or misconfigured webhook URLs.

---

## Key Concepts

**Continuous Deployment (CD):**
- **Automated Deployment**: Code changes automatically deployed to production
- **Git-Triggered**: Push events trigger deployment pipeline
- **Zero Manual Intervention**: No human approval required
- **Rapid Feedback**: Developers see changes live immediately

**Webhook-Based Automation:**
- **Event-Driven Architecture**: Repository events trigger actions
- **Push Notifications**: Git server notifies Jenkins of changes
- **HTTP Callbacks**: Webhooks are HTTP POST requests to specified URLs
- **Authentication**: Secured with API tokens and authentication tokens

**Jenkins Freestyle vs Pipeline Jobs:**
- **Freestyle**: UI-based configuration, simpler for basic workflows
- **Pipeline**: Code-based (Jenkinsfile), version controlled, more powerful
- **Use Cases**: Freestyle for simple tasks, Pipeline for complex workflows
- **Migration Path**: Start with Freestyle, migrate to Pipeline as needs grow

**Shared Storage Architecture:**
- **Network File System**: Shared directory across multiple servers
- **Single Point Deployment**: Deploy once, available on all servers
- **Consistency**: All servers serve identical content
- **Performance Consideration**: May become bottleneck at scale

**Security Best Practices:**
- **API Tokens**: Use tokens instead of passwords for automation
- **Credential Storage**: Store secrets in Jenkins credential store
- **Least Privilege**: Grant minimum necessary permissions
- **Audit Logging**: Track who deployed what and when

**Git Workflow Integration:**
- **Master Branch**: Production-ready code
- **Feature Branches**: Development work isolated from production
- **Pull Requests**: Code review before merge
- **Automated Deployment**: Merge to master triggers deployment

---

## Validation

Test your solution using KodeKloud's automated validation.

**Validation Checklist:**
- Apache (httpd) installed on all app servers running on port 8080
- Jenkins job "nautilus-app-deployment" created as Freestyle project
- Job configured with remote trigger token
- Git webhook configured in Gitea repository
- Webhook uses correct Jenkins API token and job URL
- /var/www/html ownership set to sarah user
- Git push to master branch triggers automatic deployment
- Entire repository content deployed (not just index.html)
- Application accessible via load balancer at root URL
- Job passes on multiple consecutive runs (idempotent)
- Index.html contains "Welcome to the xFusionCorp Industries"

---

[← Day 78](day-78.md) | [Day 80 →](day-80.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
