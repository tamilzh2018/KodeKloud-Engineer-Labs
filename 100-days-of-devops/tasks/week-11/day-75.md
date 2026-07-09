# Day 75: Jenkins Slave Nodes

## Task Overview

Configure Jenkins distributed build architecture by adding application servers as SSH build agents (slave nodes). This enables parallel build execution, workload distribution, and isolation of build environments across multiple machines.

**Technical Specifications:**
- Architecture: Master-slave distributed build system
- Agent type: SSH build agents
- Nodes: Three app servers (App_server_1, App_server_2, App_server_3)
- Labels: stapp01, stapp02, stapp03 (for job targeting)
- Remote directories: User-specific Jenkins workspaces
- Launch method: SSH with credential-based authentication

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Access Jenkins UI and log in

```
Username: admin
Password: Adm!n321
```

Open the Jenkins web interface and authenticate with administrator credentials. Admin access is required to install plugins, manage build agents, configure credentials, and create distributed build environments. The Jenkins master server coordinates all build activities and delegates work to slave agents.

**Step 2:** Install SSH Build Agents plugin

Navigate to Manage Jenkins > Manage Plugins > Available tab

Search for and install:
- SSH Build Agents plugin

Select "Restart Jenkins when installation is complete and no jobs are running"

The SSH Build Agents plugin enables Jenkins to launch and manage build agents on remote servers via SSH. This is the most common agent launch method for Linux/Unix servers. The plugin handles SSH connection establishment, Java process launching on remote machines, and agent lifecycle management. After installation, Jenkins restarts to load the plugin functionality.

**Step 3:** Prepare App Server 1 for Jenkins agent

SSH into App Server 1:
```sh
ssh tony@stapp01
```

Install Java (required for Jenkins agent):
```sh
sudo yum install java-21-openjdk -y
```

Verify Java installation:
```sh
java -version
```

Expected output:
```
openjdk version "21.0.x"
```

Jenkins agents require Java Runtime Environment (JRE) because Jenkins is a Java application. The agent runs as a Java process that communicates with the master. Java 21 is recommended for modern Jenkins versions. The `yum install` command downloads and installs OpenJDK from the CentOS/RHEL repositories. Verifying the version confirms successful installation and shows the Java executable is in the system PATH.

**Step 4:** Prepare App Server 2 and App Server 3

SSH into App Server 2:
```sh
ssh steve@stapp02
sudo yum install java-21-openjdk -y
java -version
```

SSH into App Server 3:
```sh
ssh banner@stapp03
sudo yum install java-21-openjdk -y
java -version
```

All three app servers need Java installed before Jenkins can launch agents on them. Each server has a different user (tony, steve, banner) corresponding to its configuration. Installing Java on all servers in parallel prepares the infrastructure for distributed builds. Without Java, the agent launch will fail with "java: command not found" errors.

**Step 5:** Add credentials for App Server 1

Navigate to Manage Jenkins > Credentials > System > Global credentials (unrestricted) > Add Credentials

Configure:
- Kind: Username with password
- Scope: Global
- Username: tony
- Password: Ir0nM@n
- ID: app-server-1-creds
- Description: App Server 1 SSH Credentials

The Jenkins credential store securely manages authentication for SSH connections to slave nodes. Global scope makes credentials available for node configuration. The ID uniquely identifies this credential set for reference in agent configuration. The username and password must match the SSH user account on App Server 1 that has permissions to create the Jenkins workspace directory.

**Step 6:** Add credentials for App Server 2 and App Server 3

Add credentials for App Server 2:
- Username: steve
- Password: Am3ric@
- ID: app-server-2-creds
- Description: App Server 2 SSH Credentials

Add credentials for App Server 3:
- Username: banner
- Password: BigGr33n
- ID: app-server-3-creds
- Description: App Server 3 SSH Credentials

Each server requires separate credentials because they use different user accounts. Jenkins will use these credentials to SSH into each server and launch the agent process. Proper credential management ensures secure, auditable access to slave nodes without hardcoding passwords in configuration files.

**Step 7:** Create agent node for App Server 1

Navigate to Manage Jenkins > Manage Nodes and Clouds > New Node

Configure:
- Node name: App_server_1
- Type: Permanent Agent
- Click "Create"

On configuration page:
- Number of executors: 2 (concurrent builds on this node)
- Remote root directory: /home/tony/jenkins
- Labels: stapp01
- Usage: Use this node as much as possible
- Launch method: Launch agents via SSH
  - Host: stapp01
  - Credentials: Select "app-server-1-creds (tony)"
  - Host Key Verification Strategy: Non verifying Verification Strategy
- Click "Save"

A permanent agent is a dedicated build node (as opposed to cloud-based dynamic agents). The remote root directory is where Jenkins creates workspaces for builds on this agent - it must be writable by the SSH user. Labels allow jobs to target specific agents (e.g., "build on stapp01 label"). The number of executors determines how many jobs can run simultaneously on this node. The Host Key Verification Strategy "Non verifying" skips SSH host key verification (suitable for controlled internal networks; less secure for internet-facing servers).

**Step 8:** Create agent nodes for App Server 2 and App Server 3

Create App_server_2 node:
- Node name: App_server_2
- Remote root directory: /home/steve/jenkins
- Labels: stapp02
- Launch method: Launch agents via SSH
  - Host: stapp02
  - Credentials: app-server-2-creds (steve)
  - Host Key Verification Strategy: Non verifying Verification Strategy

Create App_server_3 node:
- Node name: App_server_3
- Remote root directory: /home/banner/jenkins
- Labels: stapp03
- Launch method: Launch agents via SSH
  - Host: stapp03
  - Credentials: app-server-3-creds (banner)
  - Host Key Verification Strategy: Non verifying Verification Strategy

Each agent gets its own dedicated workspace directory under the respective user's home directory. Labels are crucial for job targeting - you can specify which agent(s) should run specific jobs. All three agents use SSH launch method, which is reliable and works well for permanent, always-available build servers. The credentials match the usernames and passwords configured earlier.

**Step 9:** Verify agents are online

Navigate to Manage Jenkins > Manage Nodes and Clouds

Check agent status:
- App_server_1: Should show online with idle executors
- App_server_2: Should show online with idle executors
- App_server_3: Should show online with idle executors

If any agent is offline, click on it and check the log for errors (common issues: Java not installed, SSH connection failure, directory permissions)

The agent status page shows real-time information about all build nodes. "Online" status with idle executors means Jenkins successfully connected via SSH, launched the Java agent process, and is ready to accept builds. If an agent shows offline, the log provides detailed error messages. Common issues include firewall blocking SSH, incorrect credentials, missing Java installation, or insufficient permissions to create the workspace directory. All agents should be online before proceeding.

**Step 10:** Create test job to verify agent functionality

Dashboard > New Item
- Name: testNode
- Type: Freestyle project
- Click OK

In job configuration:
- Check "Restrict where this project can be run"
- Label Expression: stapp01 (or stapp02, stapp03)

Build section > Add build step > Execute shell:
```sh
echo "Hello from Agent"
pwd
echo "User: $USER"
hostname
```

Click "Apply" and "Save"

This test job verifies that builds can execute on the slave agent. The "Restrict where this project can be run" option forces the job to run only on nodes matching the label expression. The shell script prints diagnostic information: the agent identifier, current working directory (should be under /home/user/jenkins), the user executing the build, and the hostname (should match the agent server). This confirms the job is truly running on the slave agent, not the master.

**Step 11:** Execute test builds on each agent

Build on App_server_1:
- Edit testNode job
- Label Expression: stapp01
- Build Now
- Check Console Output

Expected output:
```
Hello from Agent
/home/tony/jenkins/workspace/testNode
User: tony
stapp01
```

Repeat for stapp02 and stapp03 labels:
- Change Label Expression to stapp02, build, verify output shows steve@stapp02
- Change Label Expression to stapp03, build, verify output shows banner@stapp03

Running the test job on each agent validates the entire distributed build infrastructure. The console output confirms the build executed on the correct server with the correct user. The workspace path shows Jenkins created the workspace in the configured remote root directory. Testing all three agents ensures you can distribute workloads across your entire build farm. This validation step is critical before running production builds.

**Step 12:** Verify workspace creation on agents

SSH into each app server and verify Jenkins created workspaces:

App Server 1:
```sh
ssh tony@stapp01
ls -la /home/tony/jenkins/
```

You should see:
- workspace/ directory
- remoting/ directory (Jenkins agent JAR files)

The Jenkins agent automatically creates this directory structure. The workspace/ directory contains subdirectories for each job that runs on this agent. The remoting/ directory holds the Jenkins agent JAR file and runtime files. The agent downloads the necessary files from the master on first connection. Verifying these directories exist confirms the agent setup is complete and functional.

---

## Key Concepts

**Jenkins Distributed Builds:**
- Master-Slave Architecture: Master coordinates and schedules builds; slaves execute build steps
- Scalability: Distribute build load across multiple machines to handle concurrent builds
- Isolation: Separate build environments prevent dependency conflicts and environment pollution
- Resource Optimization: Assign resource-intensive builds to powerful servers, lightweight builds to smaller nodes

**Build Agents (Slaves):**
- SSH Agents: Connect to permanent agents via SSH protocol (most common for Linux/Unix)
- JNLP Agents: Java Web Start agents initiated from slave to master (good for firewalled environments)
- Docker Agents: Containerized ephemeral agents created on-demand (cloud-native approach)
- Cloud Agents: Dynamic agents provisioned in cloud platforms (AWS, Azure, GCP) as needed

**Agent Configuration:**
- Labels: Tags that identify agent capabilities (linux, docker, java11, gpu, production)
- Remote Directory: Workspace root on agent where Jenkins creates job workspaces
- Executors: Number of concurrent builds an agent can run (typically matches CPU cores)
- Node Properties: Environment variables, tool locations (JDK, Maven), and custom properties
- Usage Strategy: "Use as much as possible" vs "Only for jobs matching label expression"

**Benefits:**
- Parallel Execution: Run multiple independent builds simultaneously across agents
- Environment Diversity: Different OS, tools, library versions on different agents
- Load Distribution: Prevent master server overload by delegating builds to agents
- Fault Tolerance: If some agents fail, builds continue on remaining healthy agents
- Dedicated Resources: Reserve high-performance agents for critical production builds

---

## Validation

Test your solution using KodeKloud's automated validation.

Verify:
1. Three agent nodes exist: App_server_1, App_server_2, App_server_3
2. Labels are correctly assigned: stapp01, stapp02, stapp03
3. Remote directories: /home/tony/jenkins, /home/steve/jenkins, /home/banner/jenkins
4. All agents show "online" status with available executors
5. Test jobs execute successfully on each agent
6. Console output confirms execution on correct server with correct user

---

[← Day 74](day-74.md) | [Day 76 →](day-76.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
