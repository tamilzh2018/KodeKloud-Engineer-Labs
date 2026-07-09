# Day 89: Ansible Manage Services

## Task Overview

Automate web server installation and service management using Ansible playbooks. This task demonstrates installing httpd, starting the service, and configuring it to launch automatically at system boot.

**Technical Specifications:**
- Inventory file: /home/thor/ansible/inventory (pre-existing)
- Playbook location: /home/thor/ansible/playbook.yml (to be created)
- Package: httpd (Apache HTTP Server)
- Service management: Start service and enable at boot
- Execution user: thor on jump host

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Navigate to the Ansible directory and examine contents

```sh
cd ~/ansible
ls
```

Change to the Ansible directory where the inventory file is located, then list directory contents to confirm the inventory file exists. The `ls` command shows all files in the current directory, helping you verify that you're in the correct location and that the inventory file is present before creating the playbook.

**Step 2:** Examine the existing inventory file

```sh
cat inventory
```

Display the inventory file contents to understand which hosts are defined and their connection parameters. The inventory should contain definitions for all app servers with their SSH credentials. Understanding the inventory structure ensures you target the correct hosts in your playbook.

**Step 3:** Create an empty playbook file

```sh
touch playbook.yml
```

Create an empty playbook file using the `touch` command. This file will contain the tasks needed to install httpd and manage its service. Creating the file first allows you to edit it with your preferred text editor in the next step, whether that's vi, nano, or any other editor.

**Step 4:** Edit the playbook with httpd installation and service management

```yaml
---
- name: Install and manage httpd service on app servers
  hosts: all
  become: yes
  tasks:
    - name: Install httpd package
      ansible.builtin.yum:
        name: httpd
        state: present

    - name: Start and enable httpd service
      ansible.builtin.service:
        name: httpd
        state: started
        enabled: yes
```

Open the playbook file with `vi playbook.yml` (or your preferred editor) and add the content shown above. The playbook contains two tasks: (1) installing the httpd package using the yum module with `state: present` to ensure the package is installed, and (2) managing the httpd service using the service module. The service task has two important parameters: `state: started` ensures the service is currently running, and `enabled: yes` configures the service to start automatically at system boot. The `become: yes` directive at the play level enables privilege escalation for all tasks, which is necessary because package installation and service management require root permissions. This playbook targets `hosts: all`, meaning it will execute on every host defined in the inventory file.

**Step 5:** Execute the Ansible playbook

```sh
ansible-playbook -i inventory playbook.yml
```

Run the playbook using the `ansible-playbook` command with the `-i inventory` flag to specify the inventory file. Ansible will connect to each target host, install httpd if it's not already installed, start the service if it's not running, and enable it for boot if it's not already enabled. The output shows the status for each task on each host: "changed" indicates a modification was made (package installed, service started/enabled), "ok" means the desired state already exists, and "failed" indicates an error occurred. The playbook's idempotent design ensures that running it multiple times will only make changes when necessary to achieve the desired state.

**Step 6:** Verify httpd service status on all servers

```sh
# Check service status using Ansible ad-hoc command
ansible all -i inventory -m shell -a "systemctl status httpd" --become

# Verify service is enabled at boot
ansible all -i inventory -m shell -a "systemctl is-enabled httpd" --become

# Check if service is active
ansible all -i inventory -m shell -a "systemctl is-active httpd" --become
```

Verify that the httpd service is properly configured on all app servers using Ansible ad-hoc commands. The first command checks the full service status using `systemctl status httpd`, which shows whether the service is running, how long it's been active, and recent log entries. The second command uses `systemctl is-enabled httpd` to verify the service is configured to start at boot (should return "enabled"). The third command uses `systemctl is-active httpd` to check if the service is currently running (should return "active"). These verification steps confirm that both the runtime state and boot configuration are correct across all servers.

**Step 7:** Test web server functionality

```sh
# Test web server response on each host
curl http://stapp01
curl http://stapp02
curl http://stapp03

# Or test using Ansible ad-hoc command
ansible all -i inventory -m uri -a "url=http://localhost return_content=yes" --become
```

Test that the httpd web server is actually responding to HTTP requests. Using `curl` from the jump host, send HTTP requests to each app server. By default, httpd serves a test page or directory listing if no content has been configured. Alternatively, use Ansible's uri module to test HTTP connectivity from each server to itself (localhost). A successful response confirms that httpd is not only running as a service but is also properly listening on port 80 and responding to web requests. If you get connection errors, check firewall rules or SELinux policies that might be blocking access.

**Step 8:** Additional service management operations (optional)

```yaml
# Restart service (stop then start)
- name: Restart httpd service
  ansible.builtin.service:
    name: httpd
    state: restarted

# Reload service configuration without full restart
- name: Reload httpd service
  ansible.builtin.service:
    name: httpd
    state: reloaded

# Stop service
- name: Stop httpd service
  ansible.builtin.service:
    name: httpd
    state: stopped

# Disable service from starting at boot
- name: Disable httpd service
  ansible.builtin.service:
    name: httpd
    enabled: no
```

These examples demonstrate additional service management operations available through the service module. Use `state: restarted` to stop and start a service, which is useful after configuration changes. Use `state: reloaded` to reload configuration files without fully restarting the service, minimizing downtime (not all services support reload). Use `state: stopped` to ensure a service is not running, and `enabled: no` to prevent a service from starting automatically at boot. Understanding these options allows you to build comprehensive service management playbooks for different operational scenarios.

---

## Key Concepts

**Ansible Service Module:**
- Platform-agnostic module for managing system services
- Automatically detects the init system (systemd, SysV init, Upstart, etc.)
- Works across different Linux distributions with the same syntax
- Idempotent: Only makes changes when current state differs from desired state
- Part of `ansible.builtin` collection, always available without additional installation

**Service States:**
- `state: started` - Ensure service is currently running (starts if stopped)
- `state: stopped` - Ensure service is not running (stops if running)
- `state: restarted` - Stop and start the service (even if already running)
- `state: reloaded` - Reload service configuration without stopping (if supported)
- States are idempotent except `restarted`, which always restarts

**Service Boot Configuration:**
- `enabled: yes` - Configure service to start automatically at system boot
- `enabled: no` - Prevent service from starting automatically at boot
- Boot configuration persists across reboots unlike runtime state
- Use both `state: started` and `enabled: yes` for complete service management
- Enabling doesn't start the service; starting doesn't enable it

**Systemd vs SysV Init:**
- Systemd: Modern init system (RHEL 7+, CentOS 7+, Ubuntu 15.04+)
- SysV Init: Traditional init system (older distributions)
- Ansible service module abstracts the differences automatically
- Under the hood, uses systemctl for systemd, service command for SysV
- Both support start, stop, restart, enable, disable operations

**Service Module Parameters:**
- `name` - Service name (required, e.g., httpd, apache2, nginx)
- `state` - Desired runtime state (started, stopped, restarted, reloaded)
- `enabled` - Boot configuration (yes/no/true/false)
- `sleep` - Seconds to sleep between stop and start when restarting
- `arguments` - Additional arguments to pass to service command
- `pattern` - Pattern to match when checking service status (for non-standard services)

**Web Server Service Names:**
- Red Hat/CentOS/Fedora: `httpd` (Apache), `nginx` (Nginx)
- Debian/Ubuntu: `apache2` (Apache), `nginx` (Nginx)
- Service name differences are why cross-platform playbooks often use variables
- Example: `service: name={{ web_server_service }}` with variables per OS

**Service Management Best Practices:**
- Always use `become: yes` for service operations (requires root privileges)
- Combine installation and service management in the same playbook
- Use handlers for service restarts triggered by configuration changes
- Test service status after playbook execution to verify success
- Use `state: started` instead of `restarted` to avoid unnecessary downtime
- Document why services are enabled or disabled for team awareness

**Handlers for Service Management:**
```yaml
tasks:
  - name: Update httpd configuration
    ansible.builtin.copy:
      src: httpd.conf
      dest: /etc/httpd/conf/httpd.conf
    notify: Restart httpd

handlers:
  - name: Restart httpd
    ansible.builtin.service:
      name: httpd
      state: restarted
```
Handlers are special tasks that only run when notified by other tasks. They're ideal for service restarts triggered by configuration changes, running only once even if notified multiple times, and executing at the end of the play. This pattern ensures services are restarted only when necessary.

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 88](day-88.md) | [Day 90 →](day-90.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
