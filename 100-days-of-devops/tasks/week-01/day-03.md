# Day 3: Secure SSH Root Access

## Task Overview

Disable direct root login via SSH on all application servers to enhance security. This fundamental security hardening practice prevents attackers from directly targeting the root account and enforces the use of individual user accounts with sudo privileges for administrative tasks.

**Task Focus:**
- Disable direct root SSH access
- Maintain administrative capabilities through sudo
- Apply changes across all application servers
- Verify configuration persistence

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Connect to the application server via SSH

```sh
ssh user@app-server-1
```

Establish an SSH connection to the first application server. You'll need to repeat this process for each application server in your infrastructure. Use your regular user account credentials (not root) to login. This demonstrates the principle of using individual accounts for accountability before elevating privileges.

**Step 2:** Backup the SSH configuration file (recommended)

```sh
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup
```

Create a backup copy of the SSH daemon configuration file before making changes. This is a critical best practice that allows you to quickly restore the original configuration if something goes wrong. The backup file will be saved in the same directory with a `.backup` extension for easy identification and recovery.

**Step 3:** Modify SSH configuration to disable root login

```sh
sudo sed -i 's/PermitRootLogin yes/PermitRootLogin no/g' /etc/ssh/sshd_config
```

Use the `sed` (stream editor) command to find and replace the SSH configuration setting that controls root login access. The `-i` flag performs an in-place edit, directly modifying the file. The substitution pattern `'s/PermitRootLogin yes/PermitRootLogin no/g'` searches for "PermitRootLogin yes" and replaces it with "PermitRootLogin no" throughout the entire configuration file. This prevents any user from logging in directly as root via SSH, forcing administrators to login with personal accounts and use sudo for privilege escalation.

**Step 4:** Verify the configuration change

```sh
grep PermitRootLogin /etc/ssh/sshd_config
```

Search the SSH configuration file to confirm the change was applied correctly. This command will display any lines containing "PermitRootLogin" and you should see `PermitRootLogin no` in the output. This verification step is crucial before restarting the service to ensure the configuration is correct and won't lock you out of the system.

**Step 5:** Restart the SSH service to apply changes

```sh
sudo systemctl restart sshd
```

Restart the SSH daemon (sshd) service to load and apply the new configuration changes. The `systemctl restart` command stops and starts the service, ensuring all active SSH connections and future connections use the updated configuration. Note that your current SSH session will remain active during the restart, but new connections will be subject to the new root login restriction.

**Step 6:** Verify the SSH service is running properly

```sh
sudo systemctl status sshd
```

Check the status of the SSH daemon to ensure it restarted successfully and is running without errors. Look for "active (running)" in green text, which indicates the service is operational. If you see any errors or warnings, review the configuration file for syntax errors before logging out of your current session.

**Step 7:** Test the root login restriction (from another terminal)

```sh
ssh root@app-server-1
```

From a separate terminal session or machine, attempt to SSH directly as root to verify the restriction is working. This command should fail with a "Permission denied" error, confirming that root login has been successfully disabled. Never close your original administrative SSH session until you've verified that you can still access the server with your regular user account and can elevate privileges using sudo.

---

## Key Concepts

**Why Disable Root SSH Access:**
- **Accountability**: Individual user accounts create audit trails showing who performed actions
- **Attack Surface Reduction**: Eliminates a primary target for brute force attacks
- **Principle of Least Privilege**: Forces users to request only necessary privileges via sudo
- **Compliance**: Many security frameworks and regulations require disabling direct root access

**SSH Security Layers:**
- Direct root login disabled (this task)
- Password authentication disabled (use SSH keys instead)
- Non-standard SSH port (obscurity layer, not true security)
- Fail2ban or similar tools for brute force protection
- Two-factor authentication for additional security

**Alternative PermitRootLogin Values:**
- `yes`: Root can login with password or keys (insecure)
- `no`: Root cannot login via SSH at all (recommended)
- `prohibit-password`: Root can login with keys only, not passwords (moderate security)
- `forced-commands-only`: Root can only execute specific pre-defined commands

**Important Safety Notes:**
- Always maintain an active SSH session while testing configuration changes
- Ensure you have console access (physical or virtual console) as a backup
- Verify sudo access works before completely disabling root login
- Document all changes for your team and incident response procedures

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 2](day-02.md) | [Day 4 →](day-04.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
