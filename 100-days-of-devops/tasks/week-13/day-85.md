# Day 85: Create Files on App Servers using Ansible

## Task Overview

Automate file creation across multiple servers using Ansible playbooks. This task demonstrates using the Ansible file module to create files with specific ownership and permissions on remote hosts in a declarative, idempotent manner.

**Technical Specifications:**
- Inventory file: ~/playbook/inventory (contains all app servers)
- Playbook location: ~/playbook/playbook.yml
- File creation: /tmp/nfsshare.txt on all app servers
- File permissions: 0644 (rw-r--r--)
- File ownership: Different users per server (tony, steve, banner)

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Navigate to the playbook directory

```sh
cd ~/playbook
```

Change your working directory to the playbook folder in your home directory. This directory will contain both the inventory file (which defines the target hosts) and the playbook file (which defines the tasks to execute). Organizing Ansible files in a dedicated directory helps maintain project structure and makes it easier to manage related configuration files.

**Step 2:** Create the inventory file with app server definitions

```ini
[app]
stapp01 ansible_user=tony ansible_ssh_password=Ir0nM@n
stapp02 ansible_user=steve ansible_ssh_password=Am3ric@
stapp03 ansible_user=banner ansible_ssh_password=BigGr33n

[all:vars]
ansible_ssh_common_args='-o StrictHostKeyChecking=no'
```

Create the inventory file at `~/playbook/inventory` with the content shown above. The inventory file defines your target hosts and connection parameters. The `[app]` group contains three application servers (stapp01, stapp02, stapp03), each with their specific SSH user and password. The `ansible_user` parameter specifies which user to authenticate as, while `ansible_ssh_password` provides the password for authentication. The `[all:vars]` section defines variables that apply to all hosts - in this case, SSH common arguments that disable strict host key checking to prevent interactive prompts during first-time connections. While storing passwords in plain text like this is acceptable for lab environments, production environments should use Ansible Vault to encrypt sensitive data or leverage SSH key-based authentication.

**Step 3:** Create the playbook with file creation tasks

```yaml
---
- name: Create files on app servers with specific ownership
  hosts: app
  become: yes
  tasks:
    - name: Create /tmp/nfsshare.txt file
      ansible.builtin.file:
        path: /tmp/nfsshare.txt
        state: touch
        mode: '0644'
        owner: "{{ ansible_user }}"
        group: "{{ ansible_user }}"
        modification_time: preserve
        access_time: preserve
```

Create the playbook file at `~/playbook/playbook.yml` with the content shown above. This playbook targets hosts in the `app` group and uses privilege escalation (`become: yes`) to execute tasks with sudo/root permissions. The single task uses the `ansible.builtin.file` module to create an empty file at `/tmp/nfsshare.txt`. The `state: touch` parameter creates the file if it doesn't exist (similar to the Linux `touch` command). The `mode: '0644'` sets permissions to read/write for owner and read-only for group and others. The `owner` and `group` parameters use the `{{ ansible_user }}` variable, which dynamically resolves to the specific user for each server (tony for stapp01, steve for stapp02, banner for stapp03). The `modification_time: preserve` and `access_time: preserve` parameters ensure that if the file already exists, its timestamps won't be updated, maintaining idempotency.

**Step 4:** Execute the Ansible playbook

```sh
ansible-playbook -i inventory playbook.yml
```

Run the playbook using the `ansible-playbook` command. The `-i inventory` flag specifies which inventory file to use, telling Ansible which hosts to target. Ansible will connect to each server in the `app` group via SSH, authenticate using the provided credentials, execute the file creation task, and report the results. The output will show each task's status - "changed" if the file was created or modified, "ok" if the file already exists with correct attributes, or "failed" if an error occurred. Ansible's idempotent nature means running this playbook multiple times will only make changes when necessary to achieve the desired state.

**Step 5:** Verify file creation on each server

```sh
ssh tony@stapp01 "ls -la /tmp/nfsshare.txt"
ssh steve@stapp02 "ls -la /tmp/nfsshare.txt"
ssh banner@stapp03 "ls -la /tmp/nfsshare.txt"
```

Verify that the file was created correctly on each application server by using SSH to execute the `ls -la` command remotely. This will display detailed file information including permissions, ownership, size, and modification time. For stapp01, you should see owner and group as "tony", for stapp02 as "steve", and for stapp03 as "banner". The permissions should display as `-rw-r--r--` (0644), indicating read/write for owner and read-only for group and others. This verification step confirms that the playbook executed successfully and that the files have the correct attributes on each target server.

**Alternative verification method:**

```sh
ansible app -i inventory -m shell -a "ls -la /tmp/nfsshare.txt" --become
```

Alternatively, use Ansible ad-hoc commands to verify the file across all app servers simultaneously. This one-liner uses the `shell` module to execute the `ls -la /tmp/nfsshare.txt` command on all hosts in the `app` group. The `--become` flag ensures the command runs with elevated privileges if needed. This approach is more efficient than SSHing to each server individually and demonstrates Ansible's power for parallel command execution across multiple hosts.

---

## Key Concepts

**Ansible File Module:**
- `state: touch` - Creates an empty file (like Linux touch command)
- `state: file` - Ensures a file exists (fails if it doesn't)
- `state: directory` - Creates a directory
- `state: absent` - Removes files or directories
- `state: link` - Creates symbolic links
- `state: hard` - Creates hard links

**File Permissions in Ansible:**
- Octal notation: `'0644'`, `'0755'`, `'0777'` (quoted to preserve leading zero)
- Symbolic notation: `u=rw,g=r,o=r` (equivalent to 0644)
- Owner permissions: Read (4), Write (2), Execute (1)
- Group permissions: Same numbering scheme
- Other permissions: Same numbering scheme

**Ansible Variables:**
- `{{ ansible_user }}` - Built-in variable containing the SSH user
- `{{ ansible_hostname }}` - Short hostname of the target
- `{{ ansible_fqdn }}` - Fully qualified domain name
- `{{ inventory_hostname }}` - Hostname as defined in inventory
- Variables enable dynamic, reusable playbooks across different hosts

**Idempotency:**
- Running the same playbook multiple times produces the same result
- Ansible only makes changes when the current state differs from desired state
- File module checks if file exists with correct attributes before modifying
- Reduces risk of unintended changes in production environments

**Privilege Escalation:**
- `become: yes` - Use sudo/su to run tasks as another user (typically root)
- `become_user: root` - Specifies which user to become (default: root)
- `become_method: sudo` - Specifies escalation method (sudo, su, pbrun, etc.)
- Required for tasks that need elevated permissions like creating files in system directories

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 84](../week-12/day-84.md) | [Day 86 →](day-86.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
