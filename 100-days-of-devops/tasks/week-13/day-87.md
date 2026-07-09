# Day 87: Ansible Install Package

## Task Overview

Automate software package installation across multiple servers using Ansible's package management modules. This task demonstrates using the yum module to install packages on Red Hat/CentOS systems with idempotent, declarative playbooks.

**Technical Specifications:**
- Inventory file: /home/thor/playbook/inventory (all app servers)
- Playbook location: /home/thor/playbook/playbook.yml
- Target package: samba (file sharing service)
- Package manager: yum (Red Hat/CentOS)
- Execution user: thor on jump host

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Navigate to the playbook directory

```sh
cd ~/playbook
```

Change your working directory to the playbook folder in your home directory. This directory will contain both the inventory file (defining target hosts) and the playbook file (defining installation tasks). Organizing Ansible files in dedicated directories helps maintain clean project structure and makes it easier to manage related automation artifacts.

**Step 2:** Create the inventory and playbook files

```sh
touch inventory playbook.yml
```

Create two empty files using the `touch` command: `inventory` for defining target hosts and their connection parameters, and `playbook.yml` for defining the package installation tasks. The `touch` command creates empty files if they don't exist, or updates timestamps if they do. Creating these files separately before editing allows you to use your preferred text editor to add content in subsequent steps.

**Step 3:** Define the inventory with app server details

```ini
[app]
stapp01 ansible_user=tony ansible_ssh_password=Ir0nM@n
stapp02 ansible_user=steve ansible_ssh_password=Am3ric@
stapp03 ansible_user=banner ansible_ssh_password=BigGr33n

[all:vars]
ansible_ssh_common_args='-o StrictHostKeyChecking=no'
```

Edit the inventory file to include all three application servers in an `[app]` group. Each server has a unique SSH user (tony, steve, banner) and password. The `ansible_user` variable specifies which user account to authenticate as, while `ansible_ssh_password` provides the password for SSH authentication. The `[all:vars]` section applies the `ansible_ssh_common_args` variable to all hosts, setting SSH options that disable strict host key checking - this prevents interactive prompts when connecting to hosts for the first time. While storing passwords in plain text is acceptable for lab environments, production systems should use Ansible Vault for encryption or SSH key-based authentication.

**Step 4:** Create the playbook for package installation

```yaml
---
- name: Install samba package on all app servers
  hosts: app
  become: yes
  tasks:
    - name: Install samba using yum
      ansible.builtin.yum:
        name: samba
        state: present
```

Create the playbook file with the content shown above. The playbook begins with `---` (YAML document start marker) and defines a single play targeting hosts in the `app` group. The `become: yes` directive enables privilege escalation (sudo), which is required for package installation operations that need root permissions. The `tasks` section contains one task that uses the `ansible.builtin.yum` module to manage packages on Red Hat/CentOS systems. The `name: samba` parameter specifies which package to install, and `state: present` ensures the package is installed (Ansible will install it if missing, skip if already installed). This idempotent approach means running the playbook multiple times will only install the package once, making it safe for repeated execution.

**Step 5:** Execute the Ansible playbook

```sh
ansible-playbook -i inventory playbook.yml
```

Run the playbook using the `ansible-playbook` command. The `-i inventory` flag specifies the inventory file to use, telling Ansible which hosts to target and how to connect to them. Ansible will read the playbook, connect to each server in the `app` group via SSH, check if samba is installed, and install it if necessary. The output displays task execution status for each host: "changed" if the package was installed, "ok" if already installed, or "failed" with error details if installation fails. The idempotent nature of Ansible means subsequent executions will show "ok" status instead of "changed" since the package is already present.

**Step 6:** Verify package installation on target servers

```sh
# Check package installation using Ansible ad-hoc command
ansible app -i inventory -m shell -a "rpm -q samba" --become

# Or verify on individual servers
ssh tony@stapp01 "rpm -qa | grep samba"
ssh steve@stapp02 "rpm -qa | grep samba"
ssh banner@stapp03 "rpm -qa | grep samba"
```

Verify that the samba package was successfully installed on all app servers. The first command uses an Ansible ad-hoc command with the shell module to run `rpm -q samba` across all hosts in the `app` group, checking if the package is installed. The `--become` flag ensures the command runs with sudo privileges if needed. Alternatively, you can SSH to each server individually and use `rpm -qa | grep samba` to query installed packages. Both methods should confirm that samba is installed on all three application servers, validating that the playbook executed successfully.

**Step 7:** Additional package management operations (optional)

```yaml
# Install specific package version
- name: Install specific samba version
  ansible.builtin.yum:
    name: samba-4.10.4
    state: present

# Install multiple packages
- name: Install multiple packages
  ansible.builtin.yum:
    name:
      - samba
      - samba-client
      - samba-common
    state: present

# Update package to latest version
- name: Update samba to latest
  ansible.builtin.yum:
    name: samba
    state: latest

# Remove package
- name: Remove samba package
  ansible.builtin.yum:
    name: samba
    state: absent
```

These examples demonstrate additional package management capabilities using the yum module. You can install specific package versions by appending the version number to the package name. Multiple packages can be installed in a single task by providing a list under the `name` parameter. Using `state: latest` ensures the package is updated to the newest available version, while `state: absent` removes the package completely. Understanding these options allows you to build more sophisticated package management playbooks for different scenarios.

---

## Key Concepts

**Ansible Package Management Modules:**
- `ansible.builtin.yum` - Red Hat, CentOS, Fedora (older versions)
- `ansible.builtin.dnf` - Fedora, RHEL 8+, CentOS 8+ (newer yum replacement)
- `ansible.builtin.apt` - Debian, Ubuntu
- `ansible.builtin.package` - Generic module that auto-detects package manager
- `ansible.builtin.zypper` - SUSE, openSUSE
- Each module is specific to its package manager but shares similar parameter syntax

**Package States:**
- `state: present` - Ensure package is installed (default behavior)
- `state: installed` - Alias for present, means the same thing
- `state: latest` - Ensure package is installed and updated to newest version
- `state: absent` - Ensure package is not installed (removes if present)
- `state: removed` - Alias for absent, means the same thing

**Yum Module Parameters:**
- `name` - Package name (string) or list of packages
- `state` - Desired package state (present, latest, absent)
- `enablerepo` - Enable specific yum repository for this operation
- `disablerepo` - Disable specific yum repository for this operation
- `disable_gpg_check` - Skip GPG signature verification (use cautiously)
- `update_cache` - Update package cache before operation (equivalent to yum clean all)
- `allow_downgrade` - Allow downgrading package versions

**Idempotency in Package Management:**
- Running the playbook multiple times produces the same result
- Ansible checks current state before making changes
- `state: present` - installs only if package is missing
- `state: latest` - updates only if newer version is available
- `state: absent` - removes only if package is installed
- Prevents unnecessary package operations and system changes

**Privilege Escalation for Package Management:**
- Package installation requires root/sudo privileges on most systems
- `become: yes` - Enable privilege escalation for the entire play
- `become: yes` in task - Enable privilege escalation for specific task only
- Package managers like yum, apt require root access
- Without proper privileges, package operations will fail with permission errors

**Best Practices:**
- Use `ansible.builtin.package` for cross-platform playbooks when possible
- Pin specific package versions for production environments to ensure consistency
- Use `state: present` instead of `state: latest` to avoid unexpected updates
- Enable only necessary repositories to reduce security risks
- Test playbooks in development before running in production
- Use Ansible Vault to encrypt sensitive repository credentials

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 86](day-86.md) | [Day 88 →](day-88.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
