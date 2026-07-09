# Day 74: Jenkins Database Backup Job

## Task Overview

Automate MySQL database backups using a scheduled Jenkins job that creates SQL dumps and transfers them to a dedicated backup server. This ensures data protection, disaster recovery capability, and compliance with backup retention policies.

**Technical Specifications:**
- Job type: Freestyle project with periodic scheduling
- Database: MySQL database (kodekloud_db01)
- Schedule: Every 10 minutes (*/10 * * * *)
- Backup format: SQL dump with date-stamped filename
- Source: Database Server (MySQL instance)
- Destination: Backup Server (/home/clint/db_backups)
- Transfer method: SCP over SSH

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Access Jenkins UI and log in

```
Username: admin
Password: Adm!n321
```

Open the Jenkins web interface and authenticate with administrator credentials. Admin access is required to install plugins, configure SSH connections, manage credentials, and create automated backup jobs. The Jenkins dashboard provides centralized control for all infrastructure automation tasks including database backup workflows.

**Step 2:** Install required plugins

Navigate to Manage Jenkins > Manage Plugins > Available tab

Install these plugins:
- SSH Credentials plugin
- Publish Over SSH plugin

Select "Restart Jenkins when installation is complete and no jobs are running"

The SSH Credentials plugin provides secure credential storage for SSH authentication. The Publish Over SSH plugin enables file transfers and command execution on remote servers via SSH. Unlike the basic SSH plugin, Publish Over SSH offers additional features like file pattern matching and post-build transfers. After installation, Jenkins restarts to load the plugins into memory.

**Step 3:** Configure SSH servers in Jenkins

Navigate to Manage Jenkins > Configure System > Scroll to "SSH Servers" section (from Publish Over SSH plugin)

Click "Add" to add the Database Server:
- Name: database-server
- Hostname: stdb01 (Database Server hostname)
- Username: peter (Database Server user)
- Remote Directory: /tmp (working directory for operations)

Expand "Advanced" settings:
- Check "Use password authentication, or use a different key"
- Password: Sp!dy (Database Server password)
- Port: 22 (default SSH port)

Click "Test Configuration" to verify connectivity

The Publish Over SSH plugin manages SSH connections differently than the basic SSH plugin. Instead of using Jenkins credentials, it stores SSH configuration directly in system settings. The "Test Configuration" button verifies Jenkins can connect to the server with the provided credentials. The Remote Directory specifies where Jenkins starts command execution (can use absolute paths in commands).

**Step 4:** Add SSH server for Backup Server

Still in "SSH Servers" section, click "Add" again for Backup Server:
- Name: backup-server
- Hostname: stbkp01 (Backup Server hostname)
- Username: clint (Backup Server user)
- Remote Directory: /home/clint/db_backups

Expand "Advanced" settings:
- Check "Use password authentication, or use a different key"
- Password: H@wk3y3 (Backup Server password)
- Port: 22

Click "Test Configuration" and then "Apply" > "Save"

You need two SSH server configurations: one for the database server (to create backups) and one for the backup server (to store backups). The backup server's Remote Directory points directly to the backup storage location. Testing configuration before saving prevents job failures due to connectivity or authentication issues.

**Step 5:** Create scheduled database backup job

Dashboard > New Item
- Name: database-backup
- Type: Freestyle project
- Click OK

The job name clearly indicates its purpose. Freestyle projects are suitable for straightforward automation tasks like database backups. The GUI-based configuration makes it easy to set up scheduled operations without writing pipeline code.

**Step 6:** Configure build trigger schedule

In job configuration, under "Build Triggers" section:

Check "Build periodically"

Enter cron expression:
```
*/10 * * * *
```

This cron expression triggers the job every 10 minutes. The format `*/10` in the minute field means "every 10 minutes" (0, 10, 20, 30, 40, 50 minutes past each hour). The asterisks (*) in other fields mean "every hour, every day, every month, every weekday". This frequent schedule ensures recent backups are always available for disaster recovery, with maximum 10-minute data loss in worst-case scenarios.

**Step 7:** Add build step for database dump and transfer

In Build section, click "Add build step" > "Send files or execute commands over SSH"

Select SSH Server: database-server

In "Exec command" field, enter:
```sh
mkdir -p /tmp/db-backup
mysqldump -u kodekloud_roy -p'asdfgdsd' kodekloud_db01 > /tmp/db-backup/db_$(date +%F).sql
ls -lh /tmp/db-backup/
sudo apt install sshpass -y
sshpass -p 'H@wk3y3' scp -o StrictHostKeyChecking=no /tmp/db-backup/*.sql clint@stbkp01:/home/clint/db_backups
rm -rf /tmp/db-backup
```

This script executes on the database server. Line 1 creates a temporary backup directory. Line 2 performs the MySQL dump - `mysqldump` creates a SQL backup of the kodekloud_db01 database using credentials (username: kodekloud_roy, password: asdfgdsd). The output redirects to a file named with the current date (db_2025-01-15.sql format). Line 3 lists the backup file to verify creation. Line 4 installs sshpass for non-interactive password authentication. Line 5 transfers the backup to the backup server using SCP with the backup server password. Line 6 removes the temporary directory to clean up disk space.

**Step 8:** Alternative approach with multiple build steps

Instead of one complex script, you can split into multiple build steps for better logging:

Build Step 1 - "Send files or execute commands over SSH" (database-server):
```sh
mkdir -p /tmp/db-backup
mysqldump -u kodekloud_roy -p'asdfgdsd' kodekloud_db01 > /tmp/db-backup/db_$(date +%F).sql
ls -lh /tmp/db-backup/
```

Build Step 2 - "Send files or execute commands over SSH" (database-server):
```sh
sudo apt install sshpass -y
sshpass -p 'H@wk3y3' scp -o StrictHostKeyChecking=no /tmp/db-backup/*.sql clint@stbkp01:/home/clint/db_backups
rm -rf /tmp/db-backup
```

Splitting the script into multiple build steps improves readability and makes it easier to identify which part failed if errors occur. Each step's output appears separately in the console log. Jenkins stops execution if any step fails, preventing incomplete backups from being transferred. The first step focuses on backup creation and verification; the second handles transfer and cleanup.

**Step 9:** Save and test the job

Click "Apply" and "Save"

Test immediately:
- Dashboard > database-backup > Build Now
- Click on build #1 > Console Output
- Monitor execution progress

Expected console output:
```
[SSH] Executing command: mkdir -p /tmp/db-backup...
[SSH] Executing command: mysqldump...
-rw-r--r-- 1 peter peter 2.5M Jan 15 10:30 db_2025-01-15.sql
[SSH] Executing command: sshpass...
[SSH] Exit code: 0
Finished: SUCCESS
```

The "Build Now" option allows immediate testing without waiting for the scheduled trigger. The console output shows each command execution on the remote server. You should see the mysqldump creating a database file with a reasonable size (not 0 bytes). The sshpass transfer should complete without errors. Exit code 0 indicates success. After this initial test, the job runs automatically every 10 minutes according to the cron schedule.

**Step 10:** Verify backup on Backup Server

```sh
ssh clint@stbkp01
ls -lh /home/clint/db_backups/
```

Expected output:
```
-rw-r--r-- 1 clint clint 2.5M Jan 15 10:30 db_2025-01-15.sql
```

Connect to the backup server to manually verify backup files. The `ls -lh` command shows file sizes in human-readable format (KB, MB, GB). You should see SQL backup files with today's date in the filename. The file size should be greater than zero (indicates successful dump). Check file timestamps to confirm backups are created according to the schedule. This verification ensures the complete backup workflow (dump, transfer, storage) works correctly.

**Step 11:** Test backup restoration (optional validation)

```sh
# On database server
mysql -u kodekloud_roy -p'asdfgdsd' -e "CREATE DATABASE test_restore;"
mysql -u kodekloud_roy -p'asdfgdsd' test_restore < /home/clint/db_backups/db_2025-01-15.sql
mysql -u kodekloud_roy -p'asdfgdsd' test_restore -e "SHOW TABLES;"
mysql -u kodekloud_roy -p'asdfgdsd' -e "DROP DATABASE test_restore;"
```

Testing backup restoration validates that backups are not just created but are actually usable for disaster recovery. Create a test database, restore from the backup file, verify tables were restored, then clean up. This confirms the backup contains valid SQL statements and can successfully recreate the database. Regular restoration testing is a critical best practice - backups are worthless if they can't be restored when needed.

---

## Key Concepts

**Database Backup Automation:**
- Regular Backups: Scheduled database dumps protect against data loss from hardware failure, corruption, or human error
- Disaster Recovery: Quick recovery capability minimizes downtime and data loss (RPO/RTO objectives)
- Point-in-time Recovery: Date-stamped backups allow restoration to specific points in time
- Compliance: Automated backups meet regulatory requirements for data retention and business continuity

**MySQL Backup Tools:**
- mysqldump: Logical backup tool that exports database as SQL statements (portable, version-independent)
- mysqlpump: Parallel backup utility with better performance for large databases
- Percona XtraBackup: Physical backup tool for hot backups without locking (minimal downtime)
- Binary Logs: Transaction logs enable point-in-time recovery between full backups

**Backup Best Practices:**
- Consistent Naming: Use timestamps in filenames for easy identification and sorting (YYYY-MM-DD format)
- Remote Storage: Store backups on separate servers/locations to survive server failures
- Compression: Reduce backup file size with gzip (mysqldump | gzip > backup.sql.gz)
- Encryption: Encrypt sensitive database backups to protect data at rest
- Testing: Regularly test backup restoration to ensure backups are valid and complete
- Retention: Implement retention policies (daily for 7 days, weekly for 1 month, monthly for 1 year)

**Jenkins Backup Jobs:**
- Scheduled Execution: Cron-based scheduling ensures backups run automatically without manual intervention
- Error Handling: Jenkins sends notifications on backup failures, preventing undetected backup gaps
- Retention Policy: Add cleanup steps to delete old backups and manage disk space
- Monitoring: Build history tracks backup success rates, file sizes, and duration trends
- Parallel Backups: Use Jenkins agents to back up multiple databases simultaneously

---

## Validation

Test your solution using KodeKloud's automated validation.

Verify:
1. Job named "database-backup" exists
2. Job scheduled with cron expression `*/10 * * * *`
3. Job successfully creates mysqldump of kodekloud_db01 database
4. Backup file uses naming format db_YYYY-MM-DD.sql
5. Backup file transferred to /home/clint/db_backups on backup server
6. Backup file size is reasonable (not zero bytes)
7. Job executes successfully on schedule

---

[← Day 73](day-73.md) | [Day 75 →](day-75.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
