# Day 5: Install and Configuration SELinux

## Task Overview

Install and configure SELinux (Security-Enhanced Linux) on App Server 2 as part of a security hardening initiative. While SELinux will be temporarily disabled for initial configuration, this task prepares the system for future mandatory access control implementation.

**Task Requirements:**
- Install required SELinux packages
- Configure persistent SELinux state to disabled
- Changes take effect after scheduled reboot
- No immediate reboot required

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Connect to the application server via SSH

```sh
ssh user@app-server-2
```

Establish an SSH connection to App Server 2, the target server for SELinux installation and configuration. Use the credentials provided in your KodeKloud lab environment. This task focuses on a single server as a proof of concept before rolling out to the entire infrastructure.

**Step 2:** Install SELinux core packages

```sh
sudo dnf install selinux-policy selinux-policy-targeted policycoreutils policycoreutils-python-utils -y
```

Install the complete SELinux package suite using the DNF package manager (used on RHEL/CentOS 8+ systems). The `-y` flag automatically confirms the installation without prompting. This command installs four essential components: `selinux-policy` (core policy framework), `selinux-policy-targeted` (the targeted policy which is the default enforcement policy protecting specific system services), `policycoreutils` (command-line tools for managing SELinux), and `policycoreutils-python-utils` (Python-based utilities for policy management and troubleshooting). These packages provide the complete foundation for implementing mandatory access controls on the system.

**Step 3:** Verify SELinux packages installation

```sh
rpm -qa | grep selinux
```

Query the RPM package database to confirm all SELinux packages were installed successfully. This command lists all installed packages with "selinux" in their name, allowing you to verify that the installation completed without errors. You should see multiple packages including selinux-policy, selinux-policy-targeted, and related components in the output.

**Step 4:** Check current SELinux status

```sh
getenforce
```

Display the current SELinux enforcement mode using the `getenforce` command. This will show one of three states: Enforcing (policies actively enforced), Permissive (policies logged but not enforced), or Disabled (SELinux completely inactive). Understanding the current state before making configuration changes is essential for proper system management and troubleshooting.

**Step 5:** Open the SELinux configuration file for editing

```sh
sudo vi /etc/selinux/config
```

Open the primary SELinux configuration file using the vi text editor with sudo privileges. This file (`/etc/selinux/config`) controls the persistent SELinux state that applies after system reboots. You can also use `nano` or any other text editor if you prefer: `sudo nano /etc/selinux/config`.

**Step 6:** Set SELinux to disabled state

```
SELINUX=disabled
```

Modify or add the `SELINUX=disabled` directive in the configuration file. Locate the line that starts with `SELINUX=` and change its value to `disabled`. If the line doesn't exist, add it to the file. This setting instructs the system to completely disable SELinux after the next reboot. While SELinux provides robust security, organizations often disable it initially during testing phases or when it conflicts with application requirements. In vi, press `i` to enter insert mode, make your changes, then press `Esc` and type `:wq` to save and quit.

**Step 7:** Verify configuration file changes

```sh
grep ^SELINUX= /etc/selinux/config
```

Use grep to display the SELINUX directive from the configuration file, confirming your change was saved correctly. The `^SELINUX=` pattern searches for lines starting with "SELINUX=" (the caret anchors the search to line beginnings), filtering out comments and other content. You should see `SELINUX=disabled` in the output. This verification step ensures the configuration will persist across reboots.

**Step 8:** Check SELinux status details (optional)

```sh
sestatus
```

Display comprehensive SELinux status information including current mode, mode from configuration file, policy name, and policy version. This command provides a complete overview of the SELinux configuration. Note that the current mode may still show as enforcing or permissive even after configuration changes, because the configuration file setting only takes effect after a system reboot.

---

## Understanding SELinux

**What is SELinux:**

SELinux (Security-Enhanced Linux) is a Mandatory Access Control (MAC) security framework built into the Linux kernel. Unlike traditional Discretionary Access Control (DAC) where users control access to their own files, SELinux enforces system-wide security policies that even root cannot bypass. It provides an additional security layer that contains the damage from compromised processes by restricting their capabilities based on security policies.

**SELinux Operating Modes:**

- **Enforcing**: SELinux policies are actively enforced. Violations are blocked and logged. This is the production security mode.
- **Permissive**: SELinux policies are not enforced but violations are logged. This mode is useful for troubleshooting and policy development.
- **Disabled**: SELinux is completely turned off. No policies are loaded or enforced.

**SELinux Policies:**

- **Targeted**: Default policy that confines specific system services while leaving other processes unconfined
- **Strict**: Comprehensive policy that confines all processes (rarely used, complex to manage)
- **MLS (Multi-Level Security)**: Policy for systems requiring military-grade security classifications

**Key SELinux Concepts:**

- **Security Context**: Every file, process, and port has a context (user:role:type:level)
- **Type Enforcement**: Primary mechanism that associates types with processes and objects
- **Boolean Switches**: Runtime flags to modify policy behavior without recompiling
- **Policy Modules**: Loadable policy components for specific services

**Common SELinux Commands:**

```sh
# Check current mode
getenforce

# Set temporary mode (until reboot)
sudo setenforce 0     # Set to Permissive
sudo setenforce 1     # Set to Enforcing

# View detailed status
sestatus

# List security contexts
ls -Z /path/to/file

# Check process contexts
ps -eZ

# Troubleshoot denials
sudo sealert -a /var/log/audit/audit.log

# Manage booleans
getsebool -a                    # List all booleans
sudo setsebool -P httpd_can_network_connect on
```

**Configuration Files:**

- `/etc/selinux/config`: Main configuration file (persistent settings)
- `/var/log/audit/audit.log`: SELinux denial and violation logs
- `/etc/selinux/targeted/`: Targeted policy files and modules

**Why Disable SELinux:**

While disabling SELinux reduces security, organizations may do so when:
- Applications have compatibility issues with SELinux policies
- Custom applications lack proper SELinux policies
- Initial testing phase before policy development
- Development environments where rapid iteration is needed
- Legacy systems that weren't designed with SELinux in mind

**Best Practice**: Instead of disabling, consider using Permissive mode to log violations while you develop proper policies, then transition to Enforcing mode.

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 4](day-04.md) | [Day 6 →](day-06.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
