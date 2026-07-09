# Day 77: Jenkins Deploy Pipeline

## Task Overview

Create a Jenkins pipeline job that deploys a static web application from a Git repository to production web servers using a slave agent node. This implements a complete CI/CD deployment workflow with version control integration and centralized deployment management.

**Technical Specifications:**
- Job type: Pipeline (declarative, not multibranch)
- Source: Gitea repository (web_app)
- Build agent: Storage Server (label: ststor01)
- Deployment target: All app servers via shared NFS mount
- Pipeline stages: Single Deploy stage
- Web server: Apache running on port 8080

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Access Jenkins and Gitea UI

Jenkins credentials:
```
Username: admin
Password: Adm!n321
```

Gitea credentials:
```
Username: sarah
Password: Sarah_pass123
```

Open both Jenkins and Gitea interfaces. Jenkins is your CI/CD automation platform. Gitea is your Git repository hosting service (like GitHub/GitLab). The developer Sarah owns the web_app repository containing the static website code. You'll configure Jenkins to pull code from Gitea and deploy it to web servers.

**Step 2:** Verify Gitea repository

Log into Gitea as sarah

Navigate to the web_app repository

Review repository contents:
- HTML files (index.html, etc.)
- CSS stylesheets
- JavaScript files
- Images and assets

Note the repository clone URL (will be used in Jenkins pipeline)

Understanding the repository structure helps you plan the deployment. Static websites consist of HTML, CSS, JavaScript, and media files that don't require server-side processing. The repository represents the source of truth for the application code. Jenkins will clone this repository and deploy the files to the web server document root where Apache can serve them to users.

**Step 3:** Prepare Storage Server for Jenkins agent

SSH into Storage Server:
```sh
ssh natasha@ststor01
```

Install Java (required for Jenkins agent):
```sh
sudo yum install java-21-openjdk -y
```

Set ownership of deployment directory to natasha user:
```sh
sudo chown -R natasha:natasha /var/www/html
```

Verify permissions:
```sh
ls -ld /var/www/html
```

Expected output: `drwxr-xr-x ... natasha natasha ... /var/www/html`

The Storage Server will act as a Jenkins build agent, so it needs Java installed. The ownership change is critical - Jenkins agent runs as the natasha user, which must have write permissions to /var/www/html to deploy application files. Without correct permissions, deployment fails with "Permission denied" errors. The /var/www/html directory is NFS-mounted on all app servers, so deploying here makes the application available on all servers simultaneously.

**Step 4:** Install Jenkins Pipeline plugin

In Jenkins: Manage Jenkins > Manage Plugins > Available tab

Search for and install:
- Pipeline plugin (may already be installed)
- SSH Build Agents plugin (if not already installed from Day 75)

Select "Restart Jenkins when installation is complete and no jobs are running"

The Pipeline plugin enables Pipeline job types and supports both declarative and scripted pipeline syntax. This is a fundamental Jenkins plugin for modern CI/CD workflows. The SSH Build Agents plugin was covered in Day 75 but is essential for this task - it allows Jenkins to use the Storage Server as a build agent.

**Step 5:** Add credentials for Storage Server

Navigate to Manage Jenkins > Credentials > System > Global credentials > Add Credentials

Configure:
- Kind: Username with password
- Scope: Global
- Username: natasha
- Password: Bl@kW
- ID: ststor01
- Description: Storage Server SSH Credentials

These credentials authenticate Jenkins' SSH connection to the Storage Server for agent launch and Git operations. The ID "ststor01" matches the agent label you'll configure next. Credentials must be configured before creating the agent node.

**Step 6:** Create Storage Server agent node

Navigate to Manage Jenkins > Manage Nodes and Clouds > New Node

Configure:
- Node name: Storage Server
- Type: Permanent Agent
- Click "Create"

On configuration page:
- Number of executors: 2
- Remote root directory: /var/www/html
- Labels: ststor01
- Usage: Use this node as much as possible
- Launch method: Launch agents via SSH
  - Host: ststor01
  - Credentials: Select "ststor01 (natasha)"
  - Host Key Verification Strategy: Non verifying Verification Strategy

Click "Save"

The agent configuration makes the Storage Server available for pipeline execution. The remote root directory /var/www/html is where the Git repository will be cloned - this directory is the Apache document root, so files deployed here are immediately accessible via the web server. The label "ststor01" is used in the pipeline to target this specific agent. After saving, verify the agent shows "online" status before proceeding.

**Step 7:** Verify agent is online

Navigate to Manage Jenkins > Manage Nodes and Clouds

Check that "Storage Server" agent shows:
- Status: Online
- Executors: 2 idle

If offline, click the agent name and review the log for errors. Common issues:
- Java not installed
- Incorrect credentials
- /var/www/html directory permissions
- Firewall blocking SSH

The agent must be online before creating the pipeline job. An offline agent causes pipeline execution to fail with "No agent available" errors. The log provides detailed troubleshooting information if connection fails. Ensure all prerequisite steps (Java installation, permissions, credentials) are completed.

**Step 8:** Create pipeline job

Dashboard > New Item
- Name: datacenter-webapp-job
- Type: Pipeline (NOT Multibranch Pipeline)
- Click OK

The job name must be exactly "datacenter-webapp-job" per task requirements. A standard Pipeline job uses a single Jenkinsfile or inline pipeline script. Multibranch Pipeline is different - it scans a repository for multiple branches and creates jobs automatically. For this task, you need a simple Pipeline job with an inline script.

**Step 9:** Configure pipeline script

In job configuration, scroll to "Pipeline" section

Definition: Select "Pipeline script" (not "Pipeline script from SCM")

In the Script text area, enter:

```groovy
pipeline {
    agent {
        label 'ststor01'
    }

    stages {
        stage('Deploy') {
            steps {
                script {
                    // Clean existing files
                    sh 'rm -rf /var/www/html/*'

                    // Clone repository
                    sh 'git clone http://git.stratos.xfusioncorp.com/sarah/web_app.git /tmp/web_app'

                    // Copy files to document root
                    sh 'cp -r /tmp/web_app/* /var/www/html/'

                    // Clean up temporary clone
                    sh 'rm -rf /tmp/web_app'

                    // Set proper permissions
                    sh 'chmod -R 755 /var/www/html'
                }
            }
        }
    }
}
```

Click "Apply" and "Save"

This declarative pipeline defines the deployment workflow. The `agent { label 'ststor01' }` ensures execution on the Storage Server agent. The single "Deploy" stage (case-sensitive, required per task) performs the deployment. Step 1 removes old application files. Step 2 clones the latest code from the Gitea repository (adjust the URL if different in your environment). Step 3 copies files to the web server document root. Step 4 cleans up the temporary clone. Step 5 sets read/execute permissions so Apache can serve the files.

**Step 10:** Execute the pipeline

Dashboard > datacenter-webapp-job > Build Now

Monitor the build:
- Click on build #1
- Watch "Stage View" to see Deploy stage progress
- Click "Console Output" for detailed logs

Expected console output:
```
Running on Storage Server in /var/www/html
[Deploy] Cloning repository...
[Deploy] Copying files...
[Deploy] Setting permissions...
[Pipeline] End of Pipeline
Finished: SUCCESS
```

Executing the pipeline validates the entire deployment workflow. The Stage View provides a visual representation of pipeline execution with color-coded status (blue=success, red=failure). Console output shows each shell command execution and any errors. Successful completion (Finished: SUCCESS) means the application deployed correctly to /var/www/html.

**Step 11:** Verify deployment on web servers

Check files on Storage Server:
```sh
ssh natasha@ststor01
ls -la /var/www/html/
```

You should see:
- index.html
- CSS files
- JavaScript files
- Other web application files

Test the application in browser:
- Click the "App" button in the lab interface
- Or navigate to the Load Balancer URL
- Verify the website loads correctly

The /var/www/html directory on Storage Server is NFS-mounted to all app servers' document roots. Apache on each app server (running on port 8080) serves files from this shared directory. The load balancer distributes traffic across app servers. Accessing the application through the load balancer confirms end-to-end deployment success. The website should display without 404 errors or missing resources.

**Step 12:** Test pipeline redeployment

Make a change in the Gitea repository (or trigger a rebuild):

Dashboard > datacenter-webapp-job > Build Now

Verify:
- Build completes successfully
- Latest changes appear on the website
- No permission or deployment errors

The pipeline should be idempotent - running it multiple times produces the same result without errors. The `rm -rf` command ensures old files are removed before deploying new ones, preventing file accumulation. Testing redeployment validates the pipeline handles updates correctly. In production, you'd trigger this pipeline automatically via webhooks when developers push code to the repository.

**Step 13:** Alternative pipeline with Git checkout

A cleaner pipeline approach using Jenkins Git plugin:

```groovy
pipeline {
    agent {
        label 'ststor01'
    }

    stages {
        stage('Deploy') {
            steps {
                // Jenkins automatically clones to workspace
                git branch: 'main',
                    url: 'http://git.stratos.xfusioncorp.com/sarah/web_app.git'

                // Workspace is already /var/www/html (agent's remote directory)
                // Files are automatically in the right place
                sh 'chmod -R 755 /var/www/html'
            }
        }
    }
}
```

This approach leverages Jenkins' native Git integration. The `git` step clones the repository directly into the agent's workspace (/var/www/html). Since the workspace IS the deployment target, no copying is needed. Jenkins handles repository cloning, updating, and cleanup automatically. This is cleaner but requires understanding that the agent's remote root directory becomes the Git workspace.

---

## Key Concepts

**Jenkins Pipelines:**
- Pipeline as Code: Define CI/CD workflows in code (Jenkinsfile) for version control and review
- Declarative Syntax: Structured, easy-to-read format with predefined sections (agent, stages, steps)
- Scripted Syntax: Flexible Groovy-based syntax for complex logic and dynamic workflows
- Version Control: Store pipeline definitions in Git alongside application code

**Pipeline Components:**
- Agent: Specifies where pipeline executes (master, specific node label, Docker container)
- Stages: Logical groupings of steps (Build, Test, Deploy, Release)
- Steps: Individual actions (shell commands, Git operations, file manipulation)
- Post Actions: Cleanup, notifications, artifact archiving executed after stages complete

**Deployment Pipelines:**
- Source Control: Pull code from version control (Git, SVN, Mercurial)
- Build: Compile code, run tests, create artifacts (for compiled languages)
- Test: Execute unit tests, integration tests, security scans
- Deploy: Deploy application to staging, production, or multiple environments
- Rollback: Ability to revert to previous version if deployment fails

**Best Practices:**
- Modular Stages: Break pipeline into logical, reusable stages (separate build, test, deploy)
- Error Handling: Use try-catch blocks and post sections for failure handling
- Parallel Execution: Run independent tasks (tests, builds) in parallel for speed
- Shared Libraries: Extract common pipeline code into shared libraries for reuse across projects
- Declarative over Scripted: Use declarative syntax when possible (easier to read and maintain)
- Credentials Management: Never hardcode passwords; use Jenkins credentials binding
- Idempotency: Pipeline should produce same result when run multiple times

---

## Validation

Test your solution using KodeKloud's automated validation.

Verify:
1. Storage Server agent named "Storage Server" with label "ststor01" is online
2. Remote root directory is /var/www/html
3. Pipeline job named "datacenter-webapp-job" exists
4. Job type is Pipeline (not Multibranch Pipeline)
5. Pipeline has single stage named "Deploy" (case-sensitive)
6. Pipeline executes on ststor01 agent
7. Build completes successfully
8. Application files deployed to /var/www/html
9. Website accessible via load balancer URL (App button)
10. No subdirectories in URL (content at root, not /web_app)

---

[← Day 76](day-76.md) | [Day 78 →](../week-12/day-78.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
