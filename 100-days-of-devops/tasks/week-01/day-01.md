# Day 1: Linux User Setup with Non-interactive Shell

## Task Overview

Configure a system user account with shell access disabled. This type of account serves automation workflows and service operations that don't need interactive terminal sessions.

**Technical Specifications:**
- User account: service/system user type
- Shell assignment: /usr/sbin/nologin (prevents interactive login)
- Home directory: automatically created
- Access level: restricted (no shell access)

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Connect to the application server via SSH

```sh
ssh user@app-server-ip
# or
ssh user@server-name
```

Establish an SSH (Secure Shell) connection to the target application server. Replace 'user' with your actual username and 'server-name' (or 'app-server-ip') with the server's hostname or IP address. You'll be prompted for your password unless SSH key authentication is already configured. SSH provides an encrypted channel for secure remote access to Linux systems.

**Step 2:** Create a user with non-interactive shell

```sh
sudo useradd -m -s /usr/sbin/nologin user-name
```

Create a new system user account with restricted shell access using the `useradd` command. The `-m` flag creates a home directory for the user at `/home/user-name`, while the `-s /usr/sbin/nologin` flag assigns a non-interactive shell that prevents the user from logging in interactively. This configuration is ideal for service accounts, automated processes, or application runtime users that need to exist on the system but should never have interactive terminal access. Replace 'user-name' with your desired username as specified in the task requirements.

**Step 3:** Verify user creation in the system database

```sh
cat /etc/passwd
```

Display the contents of the `/etc/passwd` file, which stores essential user account information on Linux systems. Look for your newly created user entry, which should appear as a line formatted like: `username:x:1003:1004::/home/username:/usr/sbin/nologin`. The fields represent username, password placeholder (x indicates the encrypted password is in `/etc/shadow`), user ID (UID), group ID (GID), user description (empty here), home directory path, and the login shell. The `/usr/sbin/nologin` shell confirms that interactive login is disabled for this account.

**Step 4:** Test that interactive login is blocked

```sh
sudo su user-name
```

Attempt to switch to the newly created user account using the `su` (switch user) command with sudo privileges. When executed, this command will fail with the message "This account is currently not available." This confirms that the `/usr/sbin/nologin` shell is working correctly by preventing interactive shell access. This is the expected behavior for service accounts and validates that the account is properly configured for non-interactive use only.

**Step 5:** Additional verification and management commands

```bash
# List all users with nologin shell
grep nologin /etc/passwd

# Check detailed user information (UID, GID, groups)
id username

# Remove user and home directory if needed
sudo userdel -r username
```

These additional commands provide comprehensive verification and management capabilities. The `grep nologin /etc/passwd` command searches for all users with non-interactive shells, helping you audit service accounts on the system. The `id username` command displays detailed information including the user's UID, primary GID, and all group memberships. Finally, `sudo userdel -r username` completely removes a user account including their home directory and mail spool, which is useful for cleanup or testing scenarios (use with caution in production environments).

---

## Key Concepts

**Shell Types:**
- `/bin/bash`: Standard interactive shell for regular users
- `/usr/sbin/nologin`: Non-interactive shell that denies login access
- `/bin/false`: Another option that denies access and exits immediately

**Security Best Practices:**
- Service accounts and automated processes should always use non-interactive shells
- This prevents unauthorized interactive access even if credentials are compromised
- Follows the principle of least privilege by limiting account capabilities

**User Management Files:**
- `/etc/passwd`: Stores user account information (world-readable)
- `/etc/shadow`: Stores encrypted passwords (root-only access)
- `/etc/group`: Stores group information

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[Day 2 →](day-02.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
