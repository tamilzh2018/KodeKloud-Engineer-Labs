# Day 14: Linux Process Troubleshooting

## Task Overview

Diagnose and resolve Apache HTTP Server service failures on application servers. Investigate process issues, identify port conflicts, and implement corrective actions to restore service availability.

**Troubleshooting Objectives:**
- Identify which application server has Apache service failure
- Analyze systemd service status and error logs
- Diagnose port binding conflicts using network tools
- Resolve process conflicts blocking the required port
- Verify Apache is running and listening on port 3004

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Connect to the application server and check Apache status

```sh
sudo systemctl status httpd.service
```

Query the systemd service manager to check the current status of the Apache HTTP Server (httpd). This command displays comprehensive service information including active state (running/failed/inactive), recent log entries, process ID, memory usage, and any error messages. The output will immediately reveal if Apache is running correctly or has failed to start. Look for "Active: active (running)" for a healthy service or "Active: failed" indicating a problem requiring investigation.

**Step 2:** Analyze the service failure output

```sh
# Example failed output showing port conflict:
# httpd[1003]: (98)Address already in use: AH00072: make_sock: could not bind to address 0.0.0.0:3004
# httpd[1003]: no listening sockets available, shutting down
# httpd[1003]: AH00015: Unable to open logs
```

Examine the systemd status output carefully to identify the root cause of the failure. The key error message "(98)Address already in use" indicates that port 3004 is already bound to another process, preventing Apache from starting. The "AH00072: make_sock: could not bind to address" error confirms Apache cannot claim the required port. The "no listening sockets available" message means Apache has no ports to listen on and must shut down. These errors clearly point to a port conflict that must be resolved before Apache can start successfully.

**Step 3:** View detailed service logs with journalctl

```sh
sudo journalctl -u httpd.service -n 50 --no-pager
```

Retrieve the last 50 log entries for the httpd service using journalctl, systemd's centralized logging system. The `-u httpd.service` flag filters logs for only the Apache service, `-n 50` limits output to the most recent 50 lines, and `--no-pager` displays results directly without using a pager program. This command provides more detailed error messages and stack traces than the basic status output, helping you understand the complete failure timeline and any configuration issues that contributed to the service failure.

**Step 4:** Identify which process is using port 3004

```sh
sudo netstat -tlnup | grep 3004
```

Search for the process currently binding to port 3004 using netstat, a network statistics tool. The `-t` flag shows TCP connections, `-l` displays listening sockets, `-n` shows numeric addresses and ports (no DNS lookup), `-u` includes UDP connections, and `-p` displays the process ID and name. Piping to `grep 3004` filters for only port 3004. The output will reveal which process (likely sendmail with PID 680 in this scenario) is occupying the port that Apache needs, showing the process name and ID in the rightmost column.

**Step 5:** Alternative method using ss command (modern replacement for netstat)

```sh
sudo ss -tlnup | grep 3004
```

Use the ss (socket statistics) command as a modern alternative to netstat for identifying port usage. The ss command is faster and provides more detailed socket information. The flags are similar: `-t` for TCP, `-l` for listening, `-n` for numeric output, `-u` for UDP, and `-p` for process information. This command produces the same result as netstat but executes more quickly, especially on systems with many connections. You should see an entry showing port 3004 bound to sendmail or another conflicting process.

**Step 6:** Use lsof to identify the process holding port 3004

```sh
sudo lsof -i :3004
```

Query open files and network connections using lsof (list open files) to identify the process binding port 3004. The `-i :3004` flag specifically looks for any process with a network connection on port 3004. The output displays the command name, process ID (PID), user, file descriptor type, device, and connection details. This provides a clear view of which process is preventing Apache from starting. In this case, you'll likely see sendmail (PID 680) listening on 127.0.0.1:3004.

**Step 7:** Stop the conflicting service (sendmail)

```sh
sudo systemctl stop sendmail
```

Stop the sendmail service that is occupying port 3004 and blocking Apache from starting. The systemctl stop command sends a termination signal to the service, allowing it to shut down gracefully and release the port. After execution, the command completes silently if successful. You can verify the service stopped with `systemctl status sendmail`, which should show "Active: inactive (dead)". This action frees port 3004, making it available for Apache to bind.

**Step 8:** Verify port 3004 is now available

```sh
sudo netstat -tlnup | grep 3004
# Should return no results
```

Confirm that port 3004 is no longer in use by running netstat again. If the previous step succeeded, this command should return no output, indicating the port is free. An empty result proves that sendmail has released the port and Apache can now successfully bind to it. This verification step is important before attempting to start Apache, as trying to start the service while the port is still occupied will result in the same failure.

**Step 9:** Disable sendmail from starting at boot (prevent future conflicts)

```sh
sudo systemctl disable sendmail
```

Prevent sendmail from automatically starting during system boot, which would recreate the port conflict. The `disable` command removes the systemd symlinks that trigger service startup, ensuring sendmail won't start on the next reboot and compete for port 3004. The output confirms "Removed symlink /etc/systemd/system/multi-user.target.wants/sendmail.service". This is a permanent fix that prevents the same issue from recurring after system maintenance or reboots.

**Step 10:** Start the Apache HTTP Server service

```sh
sudo systemctl start httpd
```

Start the Apache HTTP Server now that port 3004 is available. The systemctl start command launches the httpd service, which will bind to port 3004 as configured. If the command completes without error, Apache has started successfully. Any errors at this stage would indicate other issues such as configuration syntax errors, permission problems, or missing files. A silent completion indicates success.

**Step 11:** Verify Apache is running and listening on port 3004

```sh
sudo systemctl status httpd.service
```

Check the Apache service status to confirm it's running properly. Look for "Active: active (running)" in green text, which confirms the service started successfully and is currently operational. The output should also show the main httpd process ID, memory usage, and recent log entries indicating successful startup. You should see messages like "Server configured, listening on port 3004" or similar confirming the service is ready to handle requests.

**Step 12:** Confirm Apache is listening on port 3004

```sh
sudo netstat -tlnup | grep 3004
# Should show httpd process listening on port 3004
```

Verify that Apache (httpd) is now the process binding to port 3004. The output should display an entry showing httpd listening on `0.0.0.0:3004` or `:::3004`, indicating it's accepting connections on all network interfaces. The process name should be "httpd" and the state should be "LISTEN". This confirms Apache successfully claimed the port and is ready to receive HTTP requests.

**Step 13:** Enable Apache to start automatically at boot

```sh
sudo systemctl enable httpd
```

Configure Apache to start automatically during system boot, ensuring service availability after reboots. The `enable` command creates the necessary systemd symlinks that trigger httpd startup during the boot sequence. The output confirms "Created symlink from /etc/systemd/system/multi-user.target.wants/httpd.service to /usr/lib/systemd/system/httpd.service". This ensures your fix persists across reboots and Apache will always be running when the system starts.

**Step 14:** Test Apache connectivity with curl

```sh
curl http://localhost:3004
# or from jump host
curl http://stapp01:3004
```

Test that Apache is responding to HTTP requests on port 3004 using curl, a command-line HTTP client. The first command tests from the local server using localhost, while the second tests from the jump host using the server's hostname. Even if no web content is configured, you should receive a response (possibly a default page, 404 error, or connection success), confirming Apache is accepting and processing HTTP requests. A connection refusal or timeout would indicate Apache isn't listening properly.

**Step 15:** Additional diagnostic and verification commands

```bash
# Check Apache configuration syntax
sudo httpd -t

# View Apache error logs
sudo tail -f /var/log/httpd/error_log

# View Apache access logs
sudo tail -f /var/log/httpd/access_log

# Check which ports Apache is configured to listen on
sudo grep "^Listen" /etc/httpd/conf/httpd.conf

# Verify all listening ports on the system
sudo ss -tlnup

# Check Apache process details
ps aux | grep httpd
```

These supplementary commands provide comprehensive verification and troubleshooting capabilities. The `httpd -t` command tests Apache configuration files for syntax errors without starting the service. The tail commands display real-time log updates, showing requests and errors as they occur. The grep command reveals which ports are configured in Apache's main configuration file. The ss command shows all listening network services on the server. The ps command displays all Apache worker processes, confirming the service is fully operational with the expected number of child processes.

---

## Key Concepts

**Systemd Service Management:**
- Service states: active (running), inactive (stopped), failed (error), activating (starting)
- Core commands: `systemctl start/stop/restart/reload/status service-name`
- Enable/disable: Control automatic service startup at boot time
- Service masking: `systemctl mask service-name` completely prevents service from starting
- Dependency management: Services can depend on other services, sockets, or targets

**Service Troubleshooting Methodology:**
1. Check service status: `systemctl status service-name` for immediate diagnosis
2. Review logs: `journalctl -u service-name -f` for detailed error messages
3. Test configuration: Service-specific syntax checks (httpd -t, nginx -t, etc.)
4. Verify dependencies: Check if required services/files are available
5. Check resources: Verify sufficient disk space, memory, file descriptors
6. Investigate conflicts: Port conflicts, file locks, permission issues

**Port Conflict Diagnosis:**
- Symptoms: "Address already in use" errors in service logs
- Detection tools: `netstat -tlnup`, `ss -tlnup`, `lsof -i :port`
- Process identification: Find PID and process name using port
- Resolution: Stop conflicting service, change port configuration, or kill process
- Prevention: Proper service planning, port documentation, service dependencies

**Network Diagnostic Tools:**
- netstat: Legacy tool showing network connections, routing tables, interface statistics
- ss: Modern replacement for netstat with faster performance and more features
- lsof: Lists open files including network sockets, useful for finding process by port
- fuser: Identifies processes using files or network ports (`fuser 3004/tcp`)
- tcpdump: Packet capture tool for analyzing network traffic

**Apache HTTP Server Administration:**
- Configuration files: `/etc/httpd/conf/httpd.conf` (main), `/etc/httpd/conf.d/*.conf` (modular)
- Log files: `/var/log/httpd/access_log` (requests), `/var/log/httpd/error_log` (errors)
- Configuration test: `httpd -t` or `apachectl configtest` validates syntax
- Graceful reload: `systemctl reload httpd` applies config changes without dropping connections
- Process model: One parent process spawns multiple worker processes to handle requests

**Common Service Failure Causes:**
- Port conflicts: Multiple services attempting to bind the same port
- Configuration errors: Syntax mistakes, invalid directives, typos in config files
- Permission issues: Service can't read config files or write to log directories
- Missing dependencies: Required modules, libraries, or certificates not installed
- Resource exhaustion: Out of memory, disk full, file descriptor limits exceeded
- File locks: Another process has exclusive lock on required files

**Process Management:**
- Process states: Running, sleeping, stopped, zombie, defunct
- Signal handling: SIGTERM (graceful shutdown), SIGKILL (force kill), SIGHUP (reload config)
- Parent-child relationships: Services often spawn child processes to handle work
- Process inspection: `ps aux`, `top`, `htop` for viewing process details
- Process termination: `kill PID` (TERM), `kill -9 PID` (KILL), `systemctl stop service`

**Troubleshooting Best Practices:**
- Always check logs first: Most issues leave clear error messages in logs
- Make one change at a time: Isolate which change fixes or causes issues
- Verify assumptions: Don't assume services are stopped/started without checking
- Document changes: Keep notes of modifications for rollback if needed
- Test incrementally: Verify each step before proceeding to the next
- Have rollback plan: Know how to restore previous working state

**Log Analysis Techniques:**
- Use journalctl filters: `-u` (unit), `-p` (priority), `--since`, `--until` for targeted searches
- Follow logs in real-time: `journalctl -f` or `tail -f /var/log/file`
- Search for errors: `grep -i error /var/log/httpd/error_log`
- Check timestamps: Correlate log entries with when issue occurred
- Log rotation: Understand where old logs are archived (logrotate)

---

## Validation

Test your solution using KodeKloud's automated validation.

**Manual Validation Checklist:**
- [ ] Identified the app server with Apache failure
- [ ] Analyzed systemd status output and identified error messages
- [ ] Used netstat/ss/lsof to identify port 3004 conflict
- [ ] Stopped conflicting sendmail service
- [ ] Verified port 3004 became available
- [ ] Started Apache HTTP Server successfully
- [ ] Confirmed httpd is listening on port 3004
- [ ] Enabled httpd service for automatic boot startup
- [ ] Disabled sendmail to prevent future conflicts
- [ ] Tested HTTP connectivity with curl
- [ ] Verified service survives system reboot

---

[← Day 13](day-13.md) | [Day 15 →](../week-03/day-15.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
