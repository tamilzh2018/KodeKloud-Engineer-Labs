# Day 81: Jenkins Multistage Pipeline

## Task Overview

Build a Jenkins pipeline with multiple sequential stages that deploy code and verify deployment success. This task introduces the concept of multistage pipelines where each stage has a specific purpose: deployment followed by testing. If any stage fails, the entire pipeline stops, preventing faulty code from reaching production.

**Technical Specifications:**
- Job type: Pipeline (not Multibranch Pipeline)
- Pipeline definition: Pipeline script (Jenkinsfile syntax)
- Stage 1: Deploy (deploy code to servers)
- Stage 2: Test (verify deployment success)
- Deployment target: Storage Server /var/www/html (shared volume)
- Test method: HTTP health check via curl

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Update Jenkins plugins and restart

Navigate to Manage Jenkins > Manage Plugins > Updates:

```text
Actions:
1. Select all available updates
2. Download and install after restart
3. ☑ Restart Jenkins when installation is complete
```

Update all Jenkins plugins to ensure you have the latest features and security patches. Plugin updates can include critical bug fixes and compatibility improvements. After selecting updates, check the restart option to automatically restart Jenkins when installation completes. Wait 1-2 minutes for Jenkins to fully restart. If the UI becomes unresponsive, refresh your browser. Regular plugin maintenance prevents compatibility issues and security vulnerabilities.

**Step 2:** Install required Pipeline plugin

Navigate to Manage Jenkins > Manage Plugins > Available:

```text
Required plugins:
- Pipeline (enables pipeline job type and Jenkinsfile syntax)
- Git plugin (if not already installed)
```

Install the Pipeline plugin, which provides the infrastructure for defining pipelines as code. The Pipeline plugin enables both declarative and scripted pipeline syntax, allowing you to define complex workflows with multiple stages, error handling, and conditional logic. The Git plugin (if needed) enables Jenkins to interact with Git repositories. After installation, restart Jenkins to activate the plugins. The Pipeline plugin is fundamental to modern Jenkins usage, replacing older freestyle job patterns with code-based pipeline definitions.

**Step 3:** Configure Storage Server credentials in Jenkins

Navigate to Manage Jenkins > Credentials > System > Global credentials > Add Credentials:

```yaml
Kind: Username with password
Scope: Global (Jenkins, nodes, items, all child items, etc)
Username: natasha
Password: Bl@kW
ID: storage-server-creds
Description: Storage Server credentials for deployment
```

Store the Storage Server credentials securely in Jenkins credential store. The credential ID `storage-server-creds` is a reference you'll use in the pipeline script to access these credentials without exposing passwords in code. Jenkins encrypts credentials at rest and injects them into jobs at runtime. The "Global" scope makes credentials available to all jobs on this Jenkins instance. Using the credentials system is a security best practice that prevents password exposure in job configurations, console output, or version control systems.

**Step 4:** Update Git repository with required content

Access Gitea UI (click Gitea button, login with sarah/Sarah_pass123):

Navigate to repository: sarah/web > index.html

```html
<!-- Edit index.html content to: -->
Welcome to xFusionCorp Industries
```

Update the repository content that will be deployed. Log into Gitea as the sarah user (the repository owner), navigate to the web repository, and edit the index.html file to contain the required content "Welcome to xFusionCorp Industries". Commit the change to the master branch. This content update ensures that when the pipeline deploys the code, the expected content will be deployed. In real-world scenarios, developers would make these changes locally and push to the repository; for lab purposes, you can edit directly in the Gitea web interface.

**Step 5:** Create the multistage pipeline job

Navigate to Jenkins Dashboard > New Item:

```yaml
Job name: deploy-job
Type: Pipeline (NOT Multibranch Pipeline)
```

Create a new pipeline job with the exact name specified in the requirements. Select "Pipeline" as the job type, not "Multibranch Pipeline". Regular pipeline jobs use a single pipeline script and don't automatically create jobs for each branch. Multibranch pipelines, in contrast, scan repositories and create separate jobs for each branch. For this task, a standard pipeline job is simpler and meets the requirements. The job name is case-sensitive and must match exactly for validation to pass.

**Step 6:** Define the multistage pipeline script

In the Pipeline section, select "Pipeline script" and enter:

```groovy
pipeline {
    agent {
        label 'ststor01'
    }

    stages {
        stage('Deploy') {
            steps {
                script {
                    // Clone the repository to the deployment location
                    sh '''
                        cd /var/www/html
                        # Clean existing files
                        rm -rf *
                        # Clone the repository
                        git clone http://sarah:Sarah_pass123@gitea:3000/sarah/web.git temp
                        # Move files to current directory
                        mv temp/* .
                        # Remove temp directory
                        rm -rf temp
                    '''
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    // Test if the application is accessible
                    def response = sh(
                        script: 'curl -s -o /dev/null -w "%{http_code}" http://stlb01:8091',
                        returnStdout: true
                    ).trim()

                    if (response != '200') {
                        error "Application health check failed. HTTP status: ${response}"
                    } else {
                        echo "Application is accessible. HTTP status: ${response}"
                    }
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check logs for details.'
        }
    }
}
```

Define a declarative pipeline with two distinct stages. The `agent { label 'ststor01' }` directive runs this pipeline on the Storage Server (you'll need to configure this as a Jenkins agent/slave node). The **Deploy** stage clones the Git repository and deploys files to `/var/www/html`. It cleans existing files, clones the repo into a temporary directory, moves files to the target location, and removes the temp directory. The **Test** stage verifies deployment by using `curl` to check the application's HTTP status through the load balancer. It captures the HTTP status code and fails the pipeline if it's not 200. The `post` section defines actions after pipeline execution, logging success or failure messages.

**Step 7:** Alternative pipeline script for agent-less execution

If you don't have a configured Storage Server agent, use this version:

```groovy
pipeline {
    agent any

    stages {
        stage('Deploy') {
            steps {
                script {
                    withCredentials([usernamePassword(
                        credentialsId: 'storage-server-creds',
                        usernameVariable: 'USERNAME',
                        passwordVariable: 'PASSWORD'
                    )]) {
                        sh '''
                            # Deploy to Storage Server via SSH
                            git clone http://sarah:Sarah_pass123@gitea:3000/sarah/web.git
                            cd web
                            sshpass -p "${PASSWORD}" scp -r -o StrictHostKeyChecking=no ./* ${USERNAME}@ststor01:/var/www/html
                        '''
                    }
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    // Wait for deployment to propagate
                    sleep(time: 5, unit: 'SECONDS')

                    // Test application accessibility
                    def response = sh(
                        script: 'curl -s -o /dev/null -w "%{http_code}" http://stlb01:8091',
                        returnStdout: true
                    ).trim()

                    if (response == '200') {
                        echo "✓ Application health check passed (HTTP ${response})"
                    } else {
                        error "✗ Application health check failed (HTTP ${response})"
                    }
                }
            }
        }
    }
}
```

This alternative pipeline runs on any available Jenkins agent and uses SSH to deploy to the Storage Server. The `withCredentials` block securely injects credentials from the Jenkins credential store into environment variables. The Deploy stage clones the repository on the Jenkins master, then uses `sshpass` and `scp` to copy files to the Storage Server. The Test stage includes a 5-second sleep to allow deployment to propagate, then uses `curl` to verify the application is accessible through the load balancer. The `returnStdout: true` option captures the curl output (HTTP status code), which is then checked to determine success or failure.

**Step 8:** Configure Storage Server as Jenkins agent (if needed)

Navigate to Manage Jenkins > Manage Nodes and Clouds > New Node:

```yaml
Node name: Storage Server
Type: Permanent Agent
Number of executors: 2
Remote root directory: /var/www/html
Labels: ststor01
Usage: Only build jobs with label expressions matching this node
Launch method: Launch agents via SSH
  Host: ststor01
  Credentials: storage-server-creds
  Host Key Verification Strategy: Non verifying
```

Configure the Storage Server as a Jenkins agent so pipelines can execute directly on it. The label `ststor01` matches the label in the pipeline's agent directive. The remote root directory `/var/www/html` is where the agent workspace resides. Setting "Launch agents via SSH" allows Jenkins to connect to the server and start the agent process. Use the previously configured credentials. The "Non verifying" host key strategy skips SSH host key verification (acceptable in lab environments). After saving, click "Launch agent" to connect. The agent status should show "In sync" when ready.

**Step 9:** Run the pipeline and monitor stages

Execute the pipeline job:

```text
Actions:
1. Navigate to deploy-job
2. Click "Build Now"
3. Observe Stage View showing Deploy and Test stages
4. Click on build number in Build History
5. View Console Output for detailed logs
```

Trigger the pipeline execution by clicking "Build Now". Jenkins displays a Stage View visualization showing each stage's progress and status. The Deploy stage runs first; if it succeeds, the Test stage executes. If any stage fails, the pipeline stops and subsequent stages don't run. Click on the build number to view detailed Console Output, which shows all commands executed and their output. The Stage View provides a high-level overview, while Console Output offers detailed debugging information. A successful pipeline shows green checkmarks for both stages.

**Step 10:** Verify deployment through load balancer

```bash
# Access application via load balancer
# Click "App" button in lab environment
# URL: http://stlb01:8091 or https://<LBR-URL>

# Expected content:
# Welcome to xFusionCorp Industries

# Verify URL structure
# Should be at root: http://stlb01:8091/
# NOT subdirectory: http://stlb01:8091/web/
```

Verify the deployed application is accessible and displays correct content. Click the "App" button in your lab environment to access the application through the load balancer. The page should display "Welcome to xFusionCorp Industries" as specified in the requirements. Verify the URL is at the root level without subdirectories. The load balancer (stlb01:8091) distributes requests across all app servers, confirming that: (1) files deployed to the Storage Server, (2) the shared volume works correctly, (3) all app servers can serve the content, and (4) the Test stage's curl check passed.

**Step 11:** Test pipeline failure scenarios

Temporarily break the deployment to verify error handling:

```groovy
// In Deploy stage, introduce an error:
stage('Deploy') {
    steps {
        script {
            sh '''
                cd /var/www/html
                # Wrong credentials to cause failure
                git clone http://wrong:wrong@gitea:3000/sarah/web.git
            '''
        }
    }
}
```

Test that the pipeline correctly handles failures. Temporarily modify the pipeline to use wrong Git credentials, causing the Deploy stage to fail. Run the pipeline and observe that: (1) the Deploy stage fails with an error, (2) the Test stage doesn't execute (because the previous stage failed), and (3) the pipeline overall status is "Failed". This validates that stage failures prevent subsequent stages from running, protecting against deploying or testing broken code. After testing, restore the correct credentials and verify the pipeline succeeds again.

**Step 12:** Validate pipeline idempotency and repeatability

```bash
# Run the pipeline multiple consecutive times
# Navigate to deploy-job
# Click "Build Now" several times

# Verify each build:
# - Both stages complete successfully
# - Application remains accessible
# - No errors in console output
# - Build history shows consistent success

# Check deployment consistency
# SSH to Storage Server
ssh natasha@ststor01
ls -la /var/www/html
cat /var/www/html/index.html
```

Test that the pipeline is idempotent (safe to run multiple times without adverse effects). Execute the pipeline several times in succession and verify each run completes successfully. Idempotency is crucial for automated pipelines that might run frequently. The validation system may test the job multiple times, so it must handle repeated execution gracefully. SSH to the Storage Server to manually inspect deployed files and confirm they're consistent across runs. The pipeline should clean and redeploy files each time, ensuring a consistent state regardless of previous runs.

**Step 13:** Advanced pipeline enhancements and troubleshooting

```groovy
// Enhanced pipeline with additional features
pipeline {
    agent any

    options {
        timeout(time: 10, unit: 'MINUTES')
        timestamps()
    }

    stages {
        stage('Deploy') {
            steps {
                script {
                    echo "Deploying to Storage Server..."
                    // Deployment commands
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    echo "Running health checks..."
                    retry(3) {
                        // Health check with retry logic
                        sh 'curl -f http://stlb01:8091'
                    }
                }
            }
        }
    }

    post {
        always {
            echo "Pipeline execution completed"
        }
        success {
            echo "✓ Deployment successful and verified"
        }
        failure {
            echo "✗ Deployment failed - check logs"
        }
    }
}
```

This enhanced pipeline demonstrates additional features. The `options` block sets a 10-minute timeout (preventing hung builds) and adds timestamps to console output. The `retry(3)` wrapper in the Test stage retries the health check up to 3 times before failing, handling transient network issues. The `post` section defines actions for different build outcomes: `always` runs regardless of result, `success` runs only on success, `failure` runs only on failure. These enhancements make pipelines more robust and provide better debugging information. The `curl -f` flag causes curl to fail on HTTP errors, properly failing the stage if the health check doesn't return a success status.

---

## Key Concepts

**Multistage Pipeline Architecture:**
- **Sequential Execution**: Stages run in defined order
- **Fail-Fast Behavior**: Pipeline stops on first stage failure
- **Logical Organization**: Each stage has a single, clear purpose
- **Visual Feedback**: Stage View shows progress and status

**Pipeline Stages:**
- **Deploy Stage**: Retrieve and deploy application code
- **Test Stage**: Verify deployment succeeded
- **Build Stage**: Compile/package code (if applicable)
- **Integration Stage**: Run integration tests
- **Promote Stage**: Promote to next environment

**Declarative vs Scripted Pipelines:**
- **Declarative**: Structured syntax with predefined sections (recommended)
- **Scripted**: Groovy-based, more flexible but complex
- **Script Blocks**: Use script {} for imperative code within declarative pipelines
- **Best Practice**: Start with declarative, add script blocks when needed

**Health Checks and Testing:**
- **HTTP Health Checks**: Verify web applications respond correctly
- **Smoke Tests**: Basic functionality verification
- **Integration Tests**: Test component interactions
- **Deployment Verification**: Ensure deployment succeeded before proceeding

**Pipeline as Code Benefits:**
- **Version Control**: Pipeline definitions stored in Git
- **Code Review**: Pipeline changes go through review process
- **Repeatability**: Same pipeline runs consistently
- **Portability**: Pipeline can be shared across teams/projects

**Error Handling:**
- **Stage Failures**: Stop pipeline on stage failure
- **Retry Logic**: Retry transient failures before failing
- **Timeout**: Prevent infinite hangs
- **Post Actions**: Cleanup or notifications on failure

---

## Validation

Test your solution using KodeKloud's automated validation.

**Validation Checklist:**
- Pipeline plugin installed and configured
- Job named "deploy-job" created (exact name, case-sensitive)
- Job type is Pipeline (NOT Multibranch Pipeline)
- Pipeline has two stages: "Deploy" and "Test" (exact names, case-sensitive)
- Deploy stage deploys code to /var/www/html on Storage Server
- Test stage verifies application accessibility
- Repository index.html updated to "Welcome to xFusionCorp Industries"
- Application accessible via load balancer at http://stlb01:8091
- URL at root level (no subdirectories like /web)
- Pipeline completes successfully with both stages passing
- Test stage fails if deployment didn't work
- Pipeline is idempotent (safe to run multiple times)

---

[← Day 80](day-80.md) | [Day 82 →](day-82.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
