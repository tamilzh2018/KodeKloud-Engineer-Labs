# Day 12: Linux Network Services

## Task Overview

The monitoring tool has reported an issue in Stratos Datacenter. One of the app servers has a problem where its Apache service is not reachable on port 3000 (which is the configured Apache port). The service itself could be down, the firewall could be at fault, or something else could be causing the issue.

**Objectives:**
1. Use diagnostic tools (telnet, netstat, etc.) to identify the root cause
2. Fix the issue without compromising security settings
3. Ensure Apache is reachable from the jump host
4. Test accessibility using: `curl http://stapp01:3000`

**Troubleshooting Areas:**
- Service status and configuration
- Port availability and conflicts
- Firewall rules
- Network connectivity

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

### Step 1: Connect to the App Server

Establish SSH connection to the problematic app server.

```bash
ssh tony@stapp01
```

**Explanation:** This command establishes a secure SSH connection to App Server 1 (stapp01) using the user account 'tony'. SSH provides encrypted communication for remote troubleshooting and administration. Once connected, you'll have terminal access to diagnose network and service issues on the target server.

### Step 2: Check Apache Service Status

Verify the current state of the Apache HTTP server.

```bash
sudo systemctl status httpd
```

**Explanation:** This command queries systemd for the Apache service (httpd) status, revealing whether the service is active, inactive, or failed. The output includes the current state, process information, recent log entries, and error messages that provide clues about failures. Systemd manages most services on modern Linux distributions, making this the primary diagnostic command for service health.

**Example output showing the problem:**
```bash
[tony@stapp01 ~]$ sudo systemctl status httpd
● httpd.service - The Apache HTTP Server
Loaded: loaded (/usr/lib/systemd/system/httpd.service; disabled; vendor preset: disabled)
Active: failed (Result: exit-code) since Wed 2025-08-06 01:38:21 UTC; 13min ago
    Docs: man:httpd.service(8)
Process: 491 ExecStart=/usr/sbin/httpd $OPTIONS -DFOREGROUND (code=exited, status=1/FAILURE)
Main PID: 491 (code=exited, status=1/FAILURE)
Status: "Reading configuration..."

Aug 06 01:38:21 stapp01.stratos.xfusioncorp.com httpd[491]: (98)Address already in use: AH00072: make_sock: could not bind to address 0.0.0.0:3000
Aug 06 01:38:21 stapp01.stratos.xfusioncorp.com httpd[491]: no listening sockets available, shutting down
```

**Analysis:** The status shows "failed" with a critical error message: "Address already in use" on port 3000. This indicates Apache cannot start because another process is already using port 3000, creating a port conflict that prevents Apache from binding to the required port.

### Step 3: Identify Port Conflicts

Investigate which process is occupying port 3000.

```bash
sudo netstat -tlnup | grep 3000
```

**Explanation:** The `netstat` command displays network connections, routing tables, and network statistics. The flags narrow the output to relevant information:
- `-t`: Show TCP connections
- `-l`: Show only listening sockets (servers waiting for connections)
- `-n`: Display numeric addresses and ports (don't resolve hostnames)
- `-u`: Include UDP connections
- `-p`: Show process IDs and program names using each socket

The `grep 3000` filter shows only lines containing port 3000. This command reveals which process is using the port that Apache needs.

**Example output revealing the conflict:**
```bash
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 127.0.0.11:36025        0.0.0.0:*               LISTEN      -
tcp        0      0 127.0.0.1:3000          0.0.0.0:*               LISTEN      430/sendmail: accep
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      298/sshd
tcp6       0      0 :::22                   :::*                    LISTEN      298/sshd
udp        0      0 127.0.0.11:56145        0.0.0.0:*                           -
```

**Analysis:** The output clearly shows that sendmail (PID 430) is listening on `127.0.0.1:3000`. Since Apache also needs port 3000, we have a port conflict. The sendmail service must be reconfigured to use a different port before Apache can start successfully.

**Alternative command using ss (modern replacement for netstat):**
```bash
sudo ss -tlnup | grep 3000
```

The `ss` command is faster and provides more detailed socket information than netstat.

### Step 4: Backup Sendmail Configuration

Create a backup of the sendmail configuration before making changes.

```bash
cd /etc/mail
sudo cp sendmail.mc sendmail.mc.bak
```

**Explanation:** These commands navigate to the sendmail configuration directory and create a backup copy of the main configuration file. The first command changes to `/etc/mail`, the standard location for sendmail configuration files. The second command copies `sendmail.mc` (the sendmail macro configuration source file) to `sendmail.mc.bak`. Backing up configuration files before editing is a critical best practice—if changes cause problems, you can quickly restore the working configuration.

### Step 5: Modify Sendmail Configuration

Change sendmail's listening port to resolve the conflict.

```bash
sudo vi /etc/mail/sendmail.mc
```

**Find the DAEMON_OPTIONS line and modify the port:**
```text
DAEMON_OPTIONS(`Port=3000,Addr=127.0.0.1, Name=MTA')dnl
```

**Change to a different port (e.g., 1234):**
```text
DAEMON_OPTIONS(`Port=1234,Addr=127.0.0.1, Name=MTA')dnl
```

**Explanation:** The `sendmail.mc` file contains sendmail configuration macros that define how the mail transfer agent operates. The `DAEMON_OPTIONS` directive configures the sendmail daemon's listening behavior:
- `Port=3000`: The port sendmail listens on (we change this to 1234 or another available port)
- `Addr=127.0.0.1`: Listen only on localhost (loopback interface), restricting access to local processes
- `Name=MTA`: Internal identifier for this daemon configuration
- `dnl`: "Delete to NewLine" macro comment delimiter

By changing the port from 3000 to 1234 (or any available port above 1024), we free port 3000 for Apache to use. The `127.0.0.1` address ensures sendmail only accepts local connections, maintaining security while resolving the conflict.

**Alternative ports to consider:** 25 (standard SMTP), 587 (submission), or any high port number above 1024 that doesn't conflict with other services.

### Step 6: Restart Sendmail Service

Apply the configuration changes by restarting sendmail.

```bash
sudo systemctl restart sendmail
```

**Explanation:** The restart command stops the sendmail service and starts it again, forcing it to reload its configuration files and bind to the new port (1234). This is necessary because configuration changes don't take effect until the service restarts. The command completes silently if successful, or displays error messages if the new configuration has issues. After restart, sendmail releases port 3000 and begins listening on the new port.

**Verify sendmail is running on the new port:**
```bash
sudo netstat -tlnup | grep sendmail
```

You should see sendmail listening on port 1234 instead of 3000.

### Step 7: Start Apache Service

Now that port 3000 is available, start the Apache service.

```bash
sudo systemctl start httpd
```

**Explanation:** This command starts the Apache HTTP server (httpd service). With the port conflict resolved, Apache can successfully bind to port 3000 and begin accepting HTTP connections. The start command initializes Apache, loading configuration files, modules, and virtual hosts. If the service starts without errors, Apache is ready to serve web requests.

**Verify Apache service status:**
```bash
sudo systemctl status httpd
```

You should see "active (running)" confirming successful startup.

### Step 8: Verify Port Binding

Confirm Apache is listening on the correct port.

```bash
sudo netstat -tlnup | grep :3000
```

**Explanation:** This command checks that Apache (httpd) is now successfully listening on port 3000. The output should show the httpd process bound to port 3000 on all interfaces (0.0.0.0:3000) or the specific server IP. This verification confirms the port conflict is resolved and Apache has claimed the required port.

**Expected output:**
```bash
tcp        0      0 0.0.0.0:3000           0.0.0.0:*               LISTEN      1234/httpd
```

The PID will differ, but you should see httpd (not sendmail) listening on port 3000.

### Step 9: Test Local Connectivity

Verify Apache responds to HTTP requests locally.

```bash
curl http://localhost:3000
```

**Explanation:** This command makes an HTTP GET request to Apache on localhost port 3000. Testing locally (from the same server) eliminates network and firewall variables, confirming Apache is running and serving content. If this succeeds, the issue (if any remains) is with external connectivity, not Apache itself. A successful response returns HTML content or HTTP headers from the web server.

**Example successful response:**
```html
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>Apache Test Page</title>
...
```

### Step 10: Test Hostname-Based Connectivity

Verify Apache is accessible using the server's hostname.

```bash
curl http://stapp01:3000
```

**Explanation:** This command tests whether Apache is accessible via the server's hostname (stapp01) rather than localhost. The hostname resolves to the server's IP address and tests that Apache is listening on the correct network interface (not just the loopback interface 127.0.0.1). If localhost works but the hostname doesn't, Apache might be configured to listen only on 127.0.0.1, requiring configuration changes to bind to all interfaces (0.0.0.0) or a specific IP.

### Step 11: Check Firewall Rules

Inspect firewall configuration to identify blocking rules.

```bash
sudo iptables -L -n
```

**Explanation:** This command lists all iptables firewall rules in numeric format (no DNS resolution). The `-L` flag lists rules, and `-n` shows IP addresses and ports numerically for faster output. Firewall rules control which network traffic is allowed or blocked. Even if Apache is running and listening, firewall rules can prevent external connections, causing the service to be unreachable from other servers.

**Example output showing problematic rules:**
```bash
Chain INPUT (policy ACCEPT)
target     prot opt source               destination
ACCEPT     all  --  0.0.0.0/0            0.0.0.0/0            state RELATED,ESTABLISHED
ACCEPT     icmp --  0.0.0.0/0            0.0.0.0/0
ACCEPT     all  --  0.0.0.0/0            0.0.0.0/0
ACCEPT     tcp  --  0.0.0.0/0            0.0.0.0/0            state NEW tcp dpt:22
REJECT     all  --  0.0.0.0/0            0.0.0.0/0            reject-with icmp-host-prohibited

Chain FORWARD (policy ACCEPT)
target     prot opt source               destination
REJECT     all  --  0.0.0.0/0            0.0.0.0/0            reject-with icmp-host-prohibited

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination
```

**Analysis:** The INPUT chain shows a problem: there's an ACCEPT rule for established connections and port 22 (SSH), but then a REJECT rule at the end that blocks all other new incoming connections. Port 3000 isn't explicitly allowed, so incoming HTTP requests on port 3000 are rejected by the catch-all REJECT rule. We need to add a rule accepting port 3000 before the REJECT rule.

### Step 12: Add Firewall Rule for Port 3000

Insert a firewall rule allowing incoming traffic on port 3000.

```bash
sudo iptables -I INPUT 4 -p tcp --dport 3000 -j ACCEPT
```

**Explanation:** This command inserts a new iptables rule to allow TCP traffic on port 3000. The command components:
- `iptables`: Firewall configuration utility
- `-I INPUT 4`: Insert the rule into the INPUT chain at position 4 (before the REJECT rule)
- `-p tcp`: Match TCP protocol packets
- `--dport 3000`: Match destination port 3000 (the Apache port)
- `-j ACCEPT`: Jump to ACCEPT target (allow the traffic)

By inserting at position 4, the rule is placed after the existing ACCEPT rules but before the catch-all REJECT rule, allowing port 3000 traffic to pass through while maintaining other security restrictions. Without this rule, all external attempts to connect to Apache on port 3000 would be blocked by the firewall.

**Verify the rule was added:**
```bash
sudo iptables -L INPUT -n --line-numbers
```

You should see the new rule at line 4, accepting tcp port 3000.

**Make the rule persistent (survives reboot):**
```bash
sudo service iptables save
```

or on systems with firewalld:
```bash
sudo firewall-cmd --permanent --add-port=3000/tcp
sudo firewall-cmd --reload
```

### Step 13: Test from Jump Host

Verify Apache is accessible from external systems.

**From the jump host:**
```bash
curl http://stapp01:3000
```

**Explanation:** This final test validates end-to-end connectivity from the jump host (external server) to Apache on the app server. This command verifies:
1. Apache is running and listening on port 3000
2. The server's network interface is correctly configured
3. Firewall rules allow external connections
4. Network routing between jump host and app server works correctly

A successful HTTP response (HTML content or headers) confirms the issue is fully resolved and Apache is reachable from other servers in the datacenter, meeting the task objective.

**Example successful response:**
```html
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>Welcome to App Server 1</title>
</head><body>
<h1>Apache is working!</h1>
</body></html>
```

---

## Understanding Network Troubleshooting

### Network Troubleshooting Methodology

**Systematic Approach:**
Effective troubleshooting follows a layered methodology, testing from the application layer down to the network layer:

1. **Service Layer**: Verify the service is running (`systemctl status`)
2. **Port Layer**: Confirm the service is listening on the correct port (`netstat`, `ss`)
3. **Firewall Layer**: Check firewall rules aren't blocking traffic (`iptables -L`)
4. **Network Layer**: Test connectivity at various levels (localhost → hostname → remote)
5. **Application Layer**: Validate service responds correctly to requests

This top-down approach quickly isolates issues to specific layers, enabling targeted fixes.

### Essential Troubleshooting Tools

**netstat - Network Statistics:**
```bash
netstat -tlnup
```
Displays network connections, listening ports, routing tables, and interface statistics. Despite being older, netstat remains widely used and available on most systems.

**Key flags:**
- `-t`: TCP connections
- `-u`: UDP connections
- `-l`: Listening sockets only
- `-n`: Numeric output (no DNS resolution)
- `-p`: Show PID and program name

**Use cases:** Identify port conflicts, verify services are listening, check established connections.

**ss - Socket Statistics:**
```bash
ss -tlnup
```
Modern replacement for netstat, providing faster performance and more detailed socket information. Syntax is similar to netstat, making it an easy transition.

**Advantages:** Faster execution, better filtering capabilities, more detailed connection state information, active development.

**telnet - TCP Connection Testing:**
```bash
telnet stapp01 3000
```
Tests whether a TCP connection can be established to a specific host and port. Useful for verifying network connectivity and port accessibility without sending actual application protocol data.

**Interpretation:**
- "Connected" → Port is open and accepting connections
- "Connection refused" → Port is closed or service isn't listening
- "No route to host" → Firewall blocking, or host unreachable

**Note:** Many modern systems don't include telnet by default. Install with `yum install telnet` or use alternatives like `nc` (netcat).

**nc (netcat) - Network Swiss Army Knife:**
```bash
nc -zv stapp01 3000
```
Versatile tool for TCP/UDP connectivity testing, port scanning, file transfers, and creating network connections.

**Flags:**
- `-z`: Zero I/O mode (scan without sending data)
- `-v`: Verbose output
- `-u`: UDP mode

**Use cases:** Port scanning, banner grabbing, file transfers, creating backdoor connections for troubleshooting.

**lsof - List Open Files:**
```bash
sudo lsof -i :3000
```
Lists open files, including network sockets. The `-i` flag filters for Internet connections, and `:3000` specifies port 3000. Shows which processes have the port open, their PIDs, and connection states.

**Advantages:** More detailed than netstat/ss, shows file descriptors, can filter by process, user, or file type.

**nmap - Network Mapper:**
```bash
nmap -p 3000 stapp01
```
Network discovery and security auditing tool. Scans hosts for open ports, identifies services, and detects operating systems.

**Use cases:** Port scanning, service detection, network inventory, security assessment.

**Note:** Use nmap only on systems you own or have permission to scan, as unauthorized scanning may be considered illegal or hostile.

**curl - HTTP Client:**
```bash
curl -I http://stapp01:3000
```
Command-line tool for making HTTP requests. The `-I` flag fetches only headers (HEAD request), useful for quick service verification without downloading full content.

**Additional flags:**
- `-v`: Verbose mode (shows request/response headers)
- `-k`: Ignore SSL certificate errors
- `-L`: Follow redirects

### Port Conflict Resolution

**Understanding Port Conflicts:**
Port conflicts occur when multiple services attempt to bind to the same port number on the same network interface. Since each port can only be used by one process at a time, the second service fails to start with "Address already in use" errors.

**Common Causes:**
- Multiple instances of the same service
- Different services configured for the same port
- Previous service instances that didn't properly release the port
- Services inheriting port configurations from conflicting defaults

**Resolution Strategies:**

**1. Identify the Conflicting Process:**
```bash
sudo netstat -tlnup | grep :PORT
sudo lsof -i :PORT
```
Determine which process owns the port and its PID.

**2. Determine Which Service Should Use the Port:**
Evaluate which service has legitimate claim to the port:
- Check requirements and documentation
- Consider default port assignments (HTTP: 80, HTTPS: 443, SSH: 22)
- Assess which service is more critical to operations

**3. Reconfigure the Less Critical Service:**
Modify the service configuration to use an alternative port:
- Edit service configuration files
- Choose an available high-numbered port (1024-65535)
- Document the change for operational awareness

**4. Stop/Disable the Conflicting Service:**
If the service isn't needed, stop or disable it:
```bash
sudo systemctl stop service-name
sudo systemctl disable service-name
```

**5. Restart Services in Correct Order:**
After configuration changes, restart affected services:
```bash
sudo systemctl restart modified-service
sudo systemctl start primary-service
```

**Prevention:**
- Document port assignments in a central registry
- Use configuration management to enforce standard port assignments
- Monitor for port conflicts in production
- Establish port allocation policies (web servers: 8080-8089, databases: 3306-3316, etc.)

### Firewall Troubleshooting

**Understanding iptables:**
iptables is the Linux kernel firewall and packet filtering framework. It examines network packets and decides whether to ACCEPT, DROP, or REJECT them based on rules organized into chains and tables.

**Core Concepts:**

**Tables:**
- **filter**: Default table for packet filtering (INPUT, OUTPUT, FORWARD chains)
- **nat**: Network address translation
- **mangle**: Packet alteration
- **raw**: Connection tracking exemption

**Chains:**
- **INPUT**: Packets destined for local system
- **OUTPUT**: Packets originating from local system
- **FORWARD**: Packets routed through the system

**Targets:**
- **ACCEPT**: Allow packet to continue
- **DROP**: Silently discard packet
- **REJECT**: Discard packet and send error response
- **LOG**: Log packet and continue processing

**Rule Processing:**
iptables processes rules top-to-bottom within each chain. The first matching rule determines the packet's fate. Default policy applies if no rules match.

**Common iptables Commands:**

**List rules:**
```bash
sudo iptables -L -n -v --line-numbers
```
Shows all rules with line numbers, packet/byte counters, and numeric addresses.

**Insert rule (at specific position):**
```bash
sudo iptables -I INPUT 4 -p tcp --dport PORT -j ACCEPT
```
Inserts rule at position 4 in INPUT chain.

**Append rule (at end):**
```bash
sudo iptables -A INPUT -p tcp --dport PORT -j ACCEPT
```
Adds rule to end of INPUT chain (use carefully with REJECT/DROP policies).

**Delete rule by number:**
```bash
sudo iptables -D INPUT 4
```
Removes rule at position 4 in INPUT chain.

**Delete rule by specification:**
```bash
sudo iptables -D INPUT -p tcp --dport PORT -j ACCEPT
```
Removes the specific matching rule.

**Flush all rules (caution!):**
```bash
sudo iptables -F
```
Removes all rules from all chains (can lock you out over SSH if default policy is DROP).

**Save rules (RHEL/CentOS):**
```bash
sudo service iptables save
```
Writes current rules to `/etc/sysconfig/iptables` for persistence across reboots.

**firewalld - Dynamic Firewall Manager:**
Modern RHEL/CentOS systems use firewalld, a higher-level firewall management tool built on iptables/nftables.

**Key commands:**
```bash
sudo firewall-cmd --list-all                           # Show current configuration
sudo firewall-cmd --add-port=3000/tcp                  # Add temporary rule
sudo firewall-cmd --permanent --add-port=3000/tcp      # Add persistent rule
sudo firewall-cmd --reload                             # Apply permanent rules
sudo firewall-cmd --remove-port=3000/tcp --permanent   # Remove rule
```

**Advantages:** Zone-based management, dynamic updates without connection disruption, integration with NetworkManager.

### Service Management with systemd

**systemd Fundamentals:**
systemd is the init system and service manager for modern Linux distributions. It manages service lifecycle, dependencies, and system state.

**Common Commands:**

**Check service status:**
```bash
sudo systemctl status service-name
```
Shows current state, PID, recent logs, and enabled/disabled status.

**Start service:**
```bash
sudo systemctl start service-name
```
Starts service immediately (doesn't affect boot behavior).

**Stop service:**
```bash
sudo systemctl stop service-name
```
Stops running service gracefully.

**Restart service:**
```bash
sudo systemctl restart service-name
```
Stops and starts service, reloading configuration.

**Reload configuration:**
```bash
sudo systemctl reload service-name
```
Reloads config without stopping service (if supported).

**Enable service (start on boot):**
```bash
sudo systemctl enable service-name
```
Creates symlinks to start service automatically at boot.

**Disable service:**
```bash
sudo systemctl disable service-name
```
Removes symlinks, preventing automatic start at boot.

**View service logs:**
```bash
sudo journalctl -u service-name -f
```
Follows (tails) the service's journal logs.

**systemd Dependencies:**
Services can depend on other services or system targets. The `After=network.target` directive in unit files ensures network is available before service starts, critical for network services like web servers.

---

## Key Concepts

### Why This Issue Occurs

**Default Port Conflicts:** Many services have default port configurations that may conflict in complex environments. Sendmail defaulting to port 3000 (non-standard) suggests previous customization that conflicts with Apache's configuration.

**Multiple Service Dependencies:** In integrated environments, services like sendmail (mail transfer) run alongside web servers. Without careful port management, conflicts are inevitable.

**Configuration Drift:** Manual changes, incomplete migrations, or automated provisioning can cause configurations to diverge from standards, creating unexpected conflicts.

**Security Hardening:** Default-deny firewall policies (REJECT all, then ACCEPT specific ports) enhance security but require explicit rules for each service, causing connectivity issues if rules are missing.

### Prevention Strategies

**Port Management:**
- Maintain a port allocation registry documenting which services use which ports
- Establish port ranges for service categories (web: 8080-8099, databases: 3306-3316)
- Use configuration management (Ansible, Puppet) to enforce standard port assignments
- Validate configurations before deploying to production

**Configuration Management:**
- Use version control (Git) for configuration files
- Implement code review for configuration changes
- Test changes in dev/staging environments
- Automate configuration deployment to reduce manual errors

**Monitoring and Alerting:**
- Monitor service availability continuously
- Alert on service failures immediately
- Track port usage and conflicts
- Log configuration changes for audit trails

**Documentation:**
- Document standard configurations and port assignments
- Create runbooks for common issues (port conflicts, firewall problems)
- Maintain network diagrams showing service dependencies
- Keep contact information for service owners

**Testing:**
- Validate service accessibility after changes
- Test from multiple network locations (localhost, same subnet, external)
- Automate health checks in deployment pipelines
- Perform regular disaster recovery drills

### Network Layers and Troubleshooting

**OSI Model Application:**
Understanding network layers helps isolate issues:

1. **Layer 7 - Application:** HTTP, FTP, SMTP - Is the application responding correctly?
2. **Layer 4 - Transport:** TCP, UDP - Are ports open? Can TCP connections establish?
3. **Layer 3 - Network:** IP, routing - Is the host reachable? Routes correct?
4. **Layer 2 - Data Link:** Ethernet, ARP - Is the network interface up?
5. **Layer 1 - Physical:** Cables, NICs - Physical connectivity issues?

Work top-down or bottom-up depending on symptoms. Service errors suggest application/transport layer issues. Complete unreachability suggests network/physical layer problems.

---

## Validation

Test your solution using KodeKloud's automated validation system. The validation checks:
- Apache service is running
- Apache is listening on port 3000
- Port 3000 is not blocked by firewall
- Apache is accessible from jump host
- HTTP requests return expected content

---

[← Day 11](day-11.md) | [Day 13 →](day-13.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
