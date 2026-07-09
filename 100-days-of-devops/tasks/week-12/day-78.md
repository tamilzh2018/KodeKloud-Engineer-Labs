# Day 78: Jenkins Conditional Pipeline

## Task Overview

Create a Jenkins pipeline with conditional logic that deploys code from different Git branches based on parameter values. This task demonstrates how to build flexible, parameter-driven CI/CD pipelines that can handle multiple deployment scenarios within a single job configuration.

**Technical Specifications:**
- Job type: Jenkins Pipeline (not Multibranch)
- Parameter: String parameter named BRANCH
- Conditional deployment: Master or feature branch based on parameter
- Deployment target: Storage server (mounted to app servers)
- Pipeline stage: Deploy (case-sensitive)

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Access Jenkins UI and login

```sh
# Jenkins credentials
Username: admin
Password: Adm!n321
```

Open the Jenkins interface by clicking the Jenkins button in the top bar of your lab environment. Use the admin credentials to log in. Jenkins is the leading open-source automation server that enables developers to build, test, and deploy their applications through automated pipelines. The admin user has full permissions to create and configure jobs, manage plugins, and configure system settings.

**Step 2:** Configure Storage Server as Jenkins slave node

Navigate to Manage Jenkins > Manage Nodes and Clouds > New Node:

```yaml
Node Name: Storage Server
Type: Permanent Agent
Labels: ststor01
Remote root directory: /var/www/html
Launch method: Launch agents via SSH
Host: ststor01
Credentials: (Add Storage Server credentials)
```

Create a Jenkins slave node to execute pipeline jobs on the Storage Server. A slave node (also called an agent) is a machine that Jenkins uses to execute builds and tasks. The label `ststor01` allows you to target this specific node in your pipeline. The remote root directory `/var/www/html` is where Jenkins will execute jobs and store workspace files. This directory is shared with all application servers, so deployments here automatically propagate to all apps. Setting up a dedicated slave node for deployment tasks isolates the execution environment and allows better resource management.

**Step 3:** Install required Jenkins plugins

Navigate to Manage Jenkins > Manage Plugins > Available:

```text
Required plugins:
- Git plugin
- Pipeline plugin
- Credentials Binding plugin
```

Install the necessary plugins and restart Jenkins when prompted. Jenkins plugins extend the functionality of the core system. The Git plugin enables Jenkins to interact with Git repositories, the Pipeline plugin provides the infrastructure for defining pipelines as code, and the Credentials Binding plugin allows secure credential handling within pipeline scripts. After installation, you may need to click "Restart Jenkins when installation is complete and no jobs are running" to activate the plugins. The UI may become unresponsive during restart; if this happens, refresh your browser after 1-2 minutes.

**Step 4:** Create parameterized pipeline job

Navigate to Jenkins Dashboard > New Item:

```yaml
Job name: devops-webapp-job
Type: Pipeline (not Multibranch Pipeline)
General section:
  ☑ This project is parameterized
  Add Parameter: String Parameter
    Name: BRANCH
    Default Value: master
    Description: Branch to deploy (master or feature)
```

Create a new pipeline job with parameter support. Parameterized jobs allow you to pass runtime values that control job behavior, making a single job definition flexible enough to handle multiple scenarios. The string parameter `BRANCH` will accept either "master" or "feature" as input, determining which Git branch gets deployed. Setting "master" as the default ensures that running the job without parameters deploys the production-ready master branch. This approach is more maintainable than creating separate jobs for each branch.

**Step 5:** Configure pipeline script with conditional logic

In the Pipeline section, select "Pipeline script" and add the following:

```groovy
pipeline {
    agent {
        label 'ststor01'
    }

    stages {
        stage('Deploy') {
            steps {
                script {
                    if (params.BRANCH == 'master') {
                        // Deploy master branch
                        sh '''
                            cd /var/www/html
                            git checkout master
                            git pull origin master
                        '''
                    } else if (params.BRANCH == 'feature') {
                        // Deploy feature branch
                        sh '''
                            cd /var/www/html
                            git checkout feature
                            git pull origin feature
                        '''
                    } else {
                        error "Invalid branch specified: ${params.BRANCH}"
                    }
                }
            }
        }
    }
}
```

Define a declarative pipeline with conditional deployment logic. The `agent { label 'ststor01' }` directive ensures this pipeline runs on the Storage Server slave node. The `Deploy` stage (note the exact capitalization) contains a script block with conditional logic that checks the BRANCH parameter value. If the parameter is "master", the pipeline checks out and pulls the master branch; if it's "feature", it deploys the feature branch. The `else` block provides error handling for invalid inputs. The `sh` command executes shell commands on the agent. The repository is already cloned at `/var/www/html`, so we only need to checkout and pull the specified branch. This approach allows a single pipeline to manage multiple deployment scenarios.

**Step 6:** Configure Git repository access

In the Pipeline section (if needed for your environment):

```groovy
// Alternative approach with git clone
pipeline {
    agent {
        label 'ststor01'
    }

    stages {
        stage('Deploy') {
            steps {
                script {
                    def branchName = params.BRANCH

                    sh """
                        cd /var/www/html
                        if [ -d .git ]; then
                            git fetch origin
                            git checkout ${branchName}
                            git pull origin ${branchName}
                        else
                            git clone -b ${branchName} http://git_username:git_password@gitea:3000/sarah/web_app .
                        fi
                    """
                }
            }
        }
    }
}
```

This alternative pipeline script handles scenarios where the repository might not exist yet. It checks if a `.git` directory exists (indicating an initialized repository); if so, it fetches updates and checks out the specified branch. If not, it clones the repository with the specified branch. The `-b` flag specifies the branch to clone. Replace `git_username` and `git_password` with actual credentials (preferably using Jenkins credentials binding for security). The `.` at the end of the clone command clones into the current directory instead of creating a subdirectory.

**Step 7:** Test the pipeline with different parameters

Build the job twice with different parameters:

```text
Build #1:
  BRANCH: master
  Expected: Deploys master branch

Build #2:
  BRANCH: feature
  Expected: Deploys feature branch
```

Execute the pipeline with different parameter values to verify conditional logic works correctly. Click "Build with Parameters" on the job page, enter "master" for the first test, then run again with "feature". Each build should checkout and pull the corresponding branch. Monitor the Console Output to verify the correct commands are executed. The deployment files should appear in `/var/www/html` on the Storage Server and, because this directory is mounted to app servers, changes should be visible through the load balancer URL. This testing validates that the conditional logic correctly routes to different code paths based on input.

**Step 8:** Verify deployment through load balancer

```sh
# Access the application
https://<LBR-URL>
```

Click the "App" button in your lab environment to access the deployed application through the load balancer. The content should reflect whichever branch you most recently deployed. Verify that the application loads from the root URL (not a subdirectory like `/web_app`), confirming that files are correctly placed in the document root. The load balancer distributes traffic across all application servers, so if the content displays correctly, it confirms the shared `/var/www/html` directory is properly mounted and accessible to all app servers.

**Step 9:** Additional validation and troubleshooting commands

```bash
# Check workspace on Storage Server
ssh natasha@ststor01
ls -la /var/www/html
cat /var/www/html/index.html

# View current Git branch
cd /var/www/html
git branch
git log -1 --oneline

# Check Jenkins job console output
# Navigate to: Job > Build #N > Console Output

# Test SSH connectivity from Jenkins
# In pipeline or Jenkins script console:
sh 'ssh -o StrictHostKeyChecking=no natasha@ststor01 "hostname"'
```

These commands help verify and troubleshoot your deployment. SSH into the Storage Server to manually inspect deployed files and confirm the correct branch is checked out. The `git branch` command shows which branch is currently active, and `git log` displays the latest commit. If deployments fail, check Jenkins console output for error messages. The SSH connectivity test ensures Jenkins can reach the Storage Server. Common issues include wrong credentials, network connectivity problems, or permission issues on `/var/www/html`.

---

## Key Concepts

**Conditional Pipeline Logic:**
- **Parameter-Driven Execution**: Use parameters to control pipeline behavior dynamically
- **if/else Statements**: Implement branching logic in script blocks
- **Environment-Based Deployment**: Deploy different branches to different environments
- **Single Job, Multiple Scenarios**: Reduce job proliferation through parameterization

**Jenkins Pipeline Components:**
- **Declarative Pipeline**: Structured, opinionated pipeline syntax with clear stages
- **Agent Directive**: Specifies where pipeline executes (master, specific node, or label)
- **Stages and Steps**: Logical grouping of related tasks
- **Script Blocks**: Embed imperative Groovy code for complex logic

**Git Branch Strategies:**
- **Master Branch**: Main production-ready codebase
- **Feature Branches**: Isolated development of new features
- **Branch-Based Deployment**: Different branches for different environments
- **Gitflow Workflow**: Common branching model for releases

**Jenkins Agent Architecture:**
- **Master Node**: Coordinates builds and manages configuration
- **Slave/Agent Nodes**: Execute actual build and deployment tasks
- **Labels**: Logical grouping of agents with similar capabilities
- **Remote Root Directory**: Agent's workspace for job execution

---

## Validation

Test your solution using KodeKloud's automated validation.

**Validation Checklist:**
- Slave node "Storage Server" exists with label "ststor01"
- Pipeline job "devops-webapp-job" created (not Multibranch)
- Job has string parameter named "BRANCH"
- Pipeline has single stage named "Deploy" (case-sensitive)
- Deploying with BRANCH=master deploys master branch
- Deploying with BRANCH=feature deploys feature branch
- Application accessible via load balancer at root URL
- No subdirectories in URL path

---

[← Day 77](../week-11/day-77.md) | [Day 79 →](day-79.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
