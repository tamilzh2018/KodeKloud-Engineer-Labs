# Day 73: Jenkins Scheduled Jobs

## Task Overview

Create a scheduled Jenkins job that automatically copies Apache web server logs from an application server to centralized storage at regular intervals. This implements automated log collection for centralized logging, monitoring, and troubleshooting.

**Technical Specifications:**
- Job type: Freestyle project with cron-based scheduling
- Schedule: Every 7 minutes (using cron expression)
- Source: App Server 2 Apache logs (/var/log/httpd/)
- Destination: Storage Server (/usr/src/itadmin)
- Method: SSH-based remote execution with SCP file transfer

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Access Jenkins UI and log in

```
Username: admin
Password: Adm!n321
```

Open the Jenkins web interface and authenticate with administrator credentials. Access to the admin account is required to install plugins, configure system settings, manage credentials, and create scheduled jobs. The Jenkins dashboard serves as the central control point for all automation and CI/CD workflows.

**Step 2:** Install required SSH plugins

Navigate to Manage Jenkins > Manage Plugins > Available tab

Install these plugins:
- SSH plugin
- SSH Credentials plugin

Select "Restart Jenkins when installation is complete and no jobs are running"

The SSH plugin enables Jenkins to execute commands on remote servers via SSH protocol. The SSH Credentials plugin provides secure, encrypted storage for SSH authentication details (usernames, passwords, private keys). These plugins are essential for remote log collection automation. After installation, Jenkins restarts to load the new plugins into memory, making their functionality available to jobs.

**Step 3:** Add SSH credentials for App Server 2

Navigate to Manage Jenkins > Credentials > System > Global credentials (unrestricted) > Add Credentials

Configure App Server 2 credentials:
- Kind: Username with password
- Scope: Global (available to all jobs)
- Username: steve (App Server 2 user)
- Password: Am3ric@ (App Server 2 password)
- ID: app-server-2-creds
- Description: App Server 2 SSH Credentials

The Jenkins credential store centralizes authentication data with encryption at rest. Global scope makes credentials reusable across multiple jobs. The ID serves as a unique reference when configuring job build steps. Never hardcode credentials in scripts - always use the credential store. This follows security best practices and provides audit trails of credential usage.

**Step 4:** Add SSH credentials for Storage Server

Add Credentials again for the storage server:
- Kind: Username with password
- Scope: Global
- Username: natasha (Storage Server user)
- Password: Bl@kW (Storage Server password)
- ID: storage-server-creds
- Description: Storage Server SSH Credentials

You need separate credentials because the job executes on App Server 2 but transfers files to Storage Server. The App Server 2 credentials authenticate the SSH connection for remote command execution. The Storage Server credentials are used within the script for SCP file transfer. Both credential sets must be configured before creating the job.

**Step 5:** Configure SSH remote hosts

Navigate to Manage Jenkins > Configure System > Scroll to "SSH remote hosts" section

Add SSH site for App Server 2:
- Hostname: stapp02 (App Server 2 hostname)
- Port: 22 (default SSH port)
- Credentials: Select "app-server-2-creds"
- Pty: Checked (enable pseudo-terminal)

Add SSH site for Storage Server:
- Hostname: ststor01 (Storage Server hostname)
- Port: 22
- Credentials: Select "storage-server-creds"
- Pty: Checked

This configuration registers both servers as known SSH targets. The hostnames must be DNS-resolvable or defined in /etc/hosts. Port 22 is standard for SSH. The Pty (pseudo-terminal) option is required for interactive commands and sudo operations. These configurations are reusable across multiple jobs that target the same servers.

**Step 6:** Create scheduled freestyle job

Dashboard > New Item
- Name: copy-logs
- Type: Freestyle project
- Click OK

The freestyle project type is ideal for script-based automation tasks. The job name "copy-logs" clearly describes its purpose. Unlike pipeline jobs that use code definitions, freestyle jobs use a GUI-based configuration interface, making them easier for beginners to set up and understand.

**Step 7:** Configure build trigger with cron schedule

In job configuration, under "Build Triggers" section:

Check "Build periodically"

Enter cron expression:
```
H/7 * * * *
```

This cron expression schedules the job to run every 7 minutes. The format is: `minute hour day-of-month month day-of-week`. The `H/7` uses Jenkins' hash-based distribution - instead of running at 0, 7, 14, 21 minutes (which creates load spikes when multiple jobs use the same schedule), Jenkins calculates a hash based on the job name to distribute builds evenly across the 7-minute interval. This prevents all scheduled jobs from running simultaneously. The `*` wildcards mean "any value" for hour, day, month, and weekday.

**Step 8:** Add remote execution build step

In Build section, click "Add build step" > "Execute shell script on remote host using ssh"

Select SSH site: stapp02 (App Server 2)

Enter the command script:
```sh
echo "Am3ric@" | sudo -S yum install -y sshpass
echo "Am3ric@" | sudo -S sshpass -p "Bl@kW" scp -o StrictHostKeyChecking=no -r /var/log/httpd/* natasha@ststor01:/usr/src/itadmin
```

This script executes on App Server 2 via SSH. Line 1 installs `sshpass` (enables non-interactive password authentication for SCP). The `echo "password" | sudo -S` pattern provides the sudo password via stdin. Line 2 uses sshpass to transfer all Apache logs from `/var/log/httpd/` to the storage server. The `-o StrictHostKeyChecking=no` option skips SSH host key verification (for automation in controlled environments). The `-r` flag enables recursive copy for directories. The `/var/log/httpd/*` glob captures both access_log and error_log files.

**Step 9:** Save and verify job execution

Click "Apply" and "Save"

The job will automatically run according to the schedule. To test immediately:
- Dashboard > copy-logs > Build Now
- Click on build number > Console Output
- Verify log transfer completion

After saving, Jenkins starts monitoring the cron schedule. The job executes automatically every 7 minutes without manual intervention. The "Build Now" option allows manual testing before waiting for the scheduled trigger. The console output shows SSH connection establishment, sshpass installation, file transfer progress, and completion status. Successful execution returns exit code 0; failures show error messages and mark the build as failed.

**Step 10:** Verify logs on Storage Server

```sh
ssh natasha@ststor01
ls -lh /usr/src/itadmin/
```

Expected files:
- access_log (HTTP access logs)
- error_log (HTTP error logs)

Connect to the storage server to manually verify that log files were successfully transferred. The `ls -lh` command lists files with human-readable sizes. You should see Apache log files with recent timestamps matching the last job execution. The file sizes should be non-zero. This verification confirms the entire automation workflow (scheduling, SSH connection, log transfer) works correctly end-to-end.

---

## Key Concepts

**Scheduled Jobs:**
- Cron Syntax: Standard Unix cron format for time-based scheduling (minute, hour, day, month, weekday)
- Build Triggers: Multiple trigger types - manual, SCM polling, scheduled, webhook, upstream job completion
- Distributed Builds: Jenkins hash-based scheduling spreads load across time to prevent resource contention
- Resource Management: Schedule heavy jobs during off-peak hours to minimize production impact

**Cron Expression Format:**
- Fields: `minute hour day-of-month month day-of-week` (all required)
- Special Characters: `*` (any value), `H` (hash/spread), `/` (step/interval), `,` (list), `-` (range)
- Examples:
  - `H/7 * * * *` - Every 7 minutes (hash-distributed)
  - `0 2 * * 1` - Every Monday at 2:00 AM
  - `0 */4 * * *` - Every 4 hours at minute 0
  - `0 0 1 * *` - First day of every month at midnight
- Hash Symbol: Jenkins calculates consistent distribution based on job name to prevent synchronized execution

**Log Management:**
- Centralized Logging: Aggregate logs from distributed systems to single location for analysis
- Log Rotation: Prevent disk space exhaustion by archiving/deleting old logs automatically
- Real-time Monitoring: Enable proactive issue detection through log analysis and alerting
- Compliance: Meet regulatory requirements for log retention, audit trails, and security monitoring

**Automation Benefits:**
- Consistency: Reliable, predictable execution without human error or forgotten manual tasks
- Reliability: No dependency on manual intervention; runs even during nights, weekends, holidays
- Scalability: Easily extend to collect logs from dozens or hundreds of servers
- Monitoring: Build history provides audit trail and alerts on collection failures

---

## Validation

Test your solution using KodeKloud's automated validation.

Verify:
1. Job named "copy-logs" exists and is configured correctly
2. Cron schedule `H/7 * * * *` (every 7 minutes) is set
3. Job executes successfully and transfers logs
4. Apache access_log and error_log appear in /usr/src/itadmin on Storage Server
5. Build history shows regular successful executions

---

[← Day 72](day-72.md) | [Day 74 →](day-74.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
