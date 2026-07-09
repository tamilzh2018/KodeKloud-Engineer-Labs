# Day 9: Debugging MariaDB Issues

## Task Overview

There is a critical issue in the Nautilus application in Stratos DC. The production support team identified that the application is unable to connect to the database. After investigating, the team discovered that the MariaDB service is down on the database server.

**Objective:** Troubleshoot and resolve the MariaDB service failure on the database server, ensuring the service starts successfully and remains operational.

**Database Troubleshooting:**
- Analyze log files for error messages
- Check service status and configuration
- Identify and fix configuration issues
- Verify file permissions and directories
- Restart and validate service functionality

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

### Step 1: Connect to the Database Server

Establish SSH connection to the database server for troubleshooting.

```bash
ssh peter@stdb01
```

**Explanation:** This command establishes a secure SSH connection to the database server (stdb01) using the user account 'peter'. SSH (Secure Shell) provides encrypted communication for remote server management. Once connected, you'll have terminal access to diagnose and fix the MariaDB service issues directly on the database server.

### Step 2: Examine MariaDB Log Files

Review the MariaDB log file to identify error messages and the root cause of the service failure.

```bash
tail -f /var/log/mariadb/mariadb.log
```

**Explanation:** The `tail -f` command displays the last lines of the MariaDB log file and continues to follow new entries in real-time. The `-f` flag (follow) keeps the file open and displays new lines as they're written, useful for monitoring ongoing issues. Log files are the first place to look when troubleshooting service failures as they contain detailed error messages, timestamps, and diagnostic information about what went wrong during service startup or operation.

**Example Log Output:**
```bash
[root@stdb01 mariadb]# tail -f mariadb.log
2025-08-03  8:54:14 0 [Note] /usr/libexec/mariadbd (initiated by: unknown): Normal shutdown
2025-08-03  8:54:14 0 [Note] Event Scheduler: Purging the queue. 0 events
2025-08-03  8:54:14 0 [Note] InnoDB: FTS optimize thread exiting.
2025-08-03  8:54:14 0 [Note] InnoDB: Starting shutdown...
2025-08-03  8:54:14 0 [Note] InnoDB: Dumping buffer pool(s) to /var/lib/mysql/ib_buffer_pool
2025-08-03  8:54:14 0 [Note] InnoDB: Buffer pool(s) dump completed at 250803  8:54:14
2025-08-03  8:54:14 0 [Note] InnoDB: Removed temporary tablespace data file: "ibtmp1"
2025-08-03  8:54:14 0 [Note] InnoDB: Shutdown completed; log sequence number 45091; transaction id 21
2025-08-03  8:54:14 0 [Note] /usr/libexec/mariadbd: Shutdown complete
```

**Analysis:** The logs show a normal shutdown sequence, indicating MariaDB stopped cleanly. This suggests the issue is not a crash but rather a configuration or permission problem preventing restart.

### Step 3: Check MariaDB Service Status

Verify the current state of the MariaDB service using systemd.

```bash
sudo systemctl status mariadb
```

**Explanation:** This command queries systemd for the MariaDB service status, displaying whether it's active, inactive, failed, or disabled. The output includes the service state, recent log entries, process IDs, and any error messages from systemd's service manager. The `sudo` prefix provides root privileges necessary to view system service details.

**Example Status Output:**
```bash
[peter@stdb01 ~]$ systemctl status mariadb
○ mariadb.service - MariaDB 10.5 database server
Loaded: loaded (/usr/lib/systemd/system/mariadb.service; enabled; preset: disabled)
Active: inactive (dead) since Sun 2025-08-03 08:54:14 UTC; 5min ago
Duration: 5.819s
Docs: man:mariadbd(8)
      https://mariadb.com/kb/en/library/systemd/
...
Status: "MariaDB server is down"
```

**Analysis:** The service shows as "inactive (dead)", confirming MariaDB is not running. The "enabled" status means it's configured to start on boot, but something is preventing it from starting now.

### Step 4: Attempt to Start MariaDB Service

Enable and start the MariaDB service to see if it starts successfully or produces errors.

```bash
sudo systemctl enable mariadb
sudo systemctl start mariadb
```

**Explanation:** The first command ensures MariaDB is enabled to start automatically on system boot by creating symbolic links in systemd's target directories. The second command attempts to start the MariaDB service immediately. If the service fails to start, systemd will provide error messages that help identify the problem. These commands are executed separately to distinguish between enabling (boot-time behavior) and starting (immediate execution).

### Step 5: Investigate Configuration Files

If the service fails to start, examine the MariaDB configuration to identify misconfigurations.

```bash
cat /etc/my.cnf.d/mariadb-server.cnf
```

**Explanation:** This command displays the contents of the main MariaDB server configuration file. Configuration files contain critical parameters like data directory location, socket file paths, port numbers, and performance settings. A common issue in this scenario is an incorrect `datadir` setting pointing to a non-existent or incorrectly named directory.

**Common Issue Identified:**
- Configuration specifies: `datadir=/var/lib/mysql/`
- Actual directory on system: `/var/lib/mysqld/`

This mismatch prevents MariaDB from finding its data files, causing startup failure.

### Step 6: Correct the Configuration

Edit the MariaDB configuration file to fix the incorrect data directory path.

```bash
sudo vi /etc/my.cnf.d/mariadb-server.cnf
```

**Correction needed:**
```ini
[mysqld]
datadir=/var/lib/mysqld
```

**Explanation:** Using a text editor (vi, nano, or similar), locate the `datadir` parameter in the `[mysqld]` section and update it to match the actual location of the data directory. After saving the changes, the configuration will point to the correct location where MariaDB's data files, including the InnoDB buffer pool file, database directories, and system tables are stored.

### Step 7: Verify File Permissions

Ensure the data directory has correct ownership and permissions.

```bash
sudo chown -R mysql:mysql /var/lib/mysqld
sudo chmod 755 /var/lib/mysqld
```

**Explanation:** MariaDB runs as the `mysql` user for security reasons and must own its data directory to read and write database files. The `chown -R` command recursively changes ownership of the directory and all its contents to the mysql user and group. The `chmod 755` command sets appropriate permissions (owner can read/write/execute, others can read/execute) ensuring MariaDB can access its files while maintaining security.

### Step 8: Restart MariaDB Service

Apply the configuration changes by restarting the MariaDB service.

```bash
sudo systemctl restart mariadb
```

**Explanation:** The restart command stops the MariaDB service (if running) and starts it again, forcing it to reload configuration files and reinitialize with the corrected settings. This is necessary after any configuration file changes. The command will fail with error messages if issues remain, or succeed silently if the problem is resolved.

### Step 9: Verify Service is Running

Confirm MariaDB is now operational and check the service status.

```bash
sudo systemctl status mariadb
```

**Explanation:** This final verification step confirms the MariaDB service is active and running without errors. The status should show "active (running)" with a green indicator, demonstrating successful troubleshooting and resolution of the service failure.

### Step 10: Test Database Connectivity

Validate database functionality by attempting to connect.

```bash
mysql -u root -p
```

**Explanation:** This command attempts to connect to the MariaDB server as the root database user. The `-p` flag prompts for the password. Successful connection confirms the database server is not only running but also accepting connections and functioning properly. Once connected, you can run `SHOW DATABASES;` to further verify database availability.

---

## Understanding MariaDB Troubleshooting

### MariaDB Architecture

**What is MariaDB?**
MariaDB is an open-source relational database management system (RDBMS) and a community-developed fork of MySQL. It maintains compatibility with MySQL while offering additional features, better performance, and an open development model. MariaDB is widely used for web applications, data warehousing, and enterprise database needs.

**Core Components:**
- **Server (mariadbd)**: The main database engine process that handles queries, manages connections, and ensures data integrity
- **Storage Engines**: InnoDB (default, ACID-compliant with transactions), MyISAM (older, non-transactional), and others for different use cases
- **Data Directory**: File system location storing databases, tables, indexes, logs, and system metadata
- **Socket File**: Unix socket for local connections between applications and database server

### Critical File Locations

**Log Files:**
- `/var/log/mariadb/mariadb.log`: Main server log containing startup messages, errors, warnings, and shutdown information
- `/var/log/mysql/error.log`: Alternative error log location on some distributions
- Application-specific logs configured in `/etc/my.cnf.d/`

**Configuration Files:**
- `/etc/my.cnf`: Main configuration file, often includes other config files
- `/etc/my.cnf.d/`: Directory containing modular configuration files for different aspects (server, client, replication)
- `~/.my.cnf`: User-specific configuration for database client settings

**Data Directory (Default):**
- `/var/lib/mysql/`: Standard location for MariaDB data files on most Linux distributions
- Contains subdirectories for each database, system tables, InnoDB files, and binary logs
- Must have correct ownership (mysql:mysql) and permissions (750 or 755)

**Socket File:**
- `/var/lib/mysql/mysql.sock`: Unix socket file for local client connections
- Faster than TCP connections for applications on the same host
- Must be accessible to both server and clients

### Common MariaDB Issues

**Permission Problems:**
Incorrect ownership or permissions on the data directory, socket file, or log files prevent MariaDB from reading or writing necessary files. The server runs as the `mysql` user and requires appropriate access. Symptoms include startup failures with "Permission denied" errors in logs.

**Configuration Errors:**
Syntax errors in configuration files, invalid parameter values, or path mismatches (like incorrect `datadir`) prevent service startup. Always validate configuration changes before restarting. Use `mysqld --help --verbose` to check configuration parsing.

**Disk Space Issues:**
Insufficient disk space in the data directory or temporary directory causes MariaDB to fail during operations. InnoDB particularly requires space for transaction logs, buffer pool dumps, and temporary tables. Monitor disk usage with `df -h`.

**Port Conflicts:**
Default port 3306 might be used by another service or MySQL instance. Check with `netstat -tlnup | grep 3306` or `ss -tlnup | grep 3306`. Resolve by stopping conflicting service or changing MariaDB port in configuration.

**Corrupted System Tables:**
System table corruption prevents authentication and server startup. Recovery requires using `mysql_upgrade` or restoring from backup. Regular backups of the mysql schema are crucial.

### Diagnostic Commands

**Service Management:**
- `systemctl status mariadb`: Check service state, recent logs, and process information
- `systemctl start mariadb`: Start the database service
- `systemctl enable mariadb`: Configure service to start on boot
- `systemctl restart mariadb`: Stop and start service, reloading configuration

**Log Analysis:**
- `journalctl -u mariadb`: View systemd journal logs for MariaDB service
- `journalctl -u mariadb -f`: Follow MariaDB logs in real-time
- `tail -f /var/log/mariadb/mariadb.log`: Monitor log file for new entries

**Connectivity Testing:**
- `mysqladmin ping`: Quick test if server is responding to connections
- `mysqladmin -u root -p status`: Display server status information
- `mysql -u root -p`: Connect to database server interactively

**Process and Network Inspection:**
- `ps aux | grep mariadb`: Check if MariaDB processes are running
- `netstat -tlnup | grep 3306`: Verify MariaDB is listening on default port
- `lsof -i :3306`: Show which process is using port 3306

### File Permissions Best Practices

**Data Directory:**
- Ownership: `mysql:mysql` (user and group)
- Permissions: `755` (drwxr-xr-x) for directory
- Contents: Files should be `660` or `640`

**Configuration Files:**
- Ownership: `root:root` for system config files
- Permissions: `644` (readable by all, writable by root)
- Sensitive configs: `600` (readable only by root)

**Socket File:**
- Ownership: `mysql:mysql`
- Permissions: `777` or `755` depending on client access requirements
- Created automatically by MariaDB on startup

**Log Files:**
- Ownership: `mysql:mysql`
- Permissions: `644` or `640` (writable by mysql user)
- Ensure parent directory allows mysql to create new log files

### Troubleshooting Methodology

**1. Check Service Status:**
Start with `systemctl status mariadb` to get high-level service state and recent error messages.

**2. Review Logs:**
Examine log files for detailed error messages, stack traces, and warning indicators pointing to the root cause.

**3. Verify Configuration:**
Check configuration files for syntax errors, path mismatches, or invalid parameter values.

**4. Inspect File System:**
Verify data directory exists, has correct ownership/permissions, and sufficient disk space.

**5. Test Connectivity:**
After fixes, test that MariaDB accepts connections and responds to queries.

**6. Monitor Behavior:**
Observe service for stability over time, checking logs for recurring warnings or errors.

---

## Key Concepts

### Why This Problem Occurs

**Configuration Drift:** Manual changes, migrations, or system updates can cause configuration to diverge from actual system state. Documentation and configuration management tools prevent drift.

**Path Dependencies:** Databases rely on specific directory structures and file locations. Changes to file system layout must be reflected in configuration files.

**Security Context:** Database servers run with restricted user privileges (mysql user) for security. All required files must be accessible to this user context.

### Prevention Strategies

**Configuration Management:** Use tools like Ansible, Puppet, or Chef to maintain consistent configurations across environments and automate recovery.

**Documentation:** Document standard configurations, file locations, and operational procedures. Keep runbooks updated for common issues.

**Monitoring:** Implement proactive monitoring for service availability, log errors, disk space, and performance metrics. Alert on anomalies before they cause outages.

**Testing:** Test configuration changes in non-production environments first. Validate backup and restore procedures regularly.

**Version Control:** Store configuration files in version control (Git) to track changes, enable rollback, and facilitate code review.

---

## Validation

Test your solution using KodeKloud's automated validation system. The validation checks:
- MariaDB service is active and running
- Service is enabled for automatic startup on boot
- Database server accepts connections
- No critical errors in log files

---

[← Day 8](day-08.md) | [Day 10 →](day-10.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
