# Day 83: Troubleshoot and Create Ansible Playbook

## Task Overview

Debug and fix a broken Ansible inventory file, then create a playbook to perform file operations on a remote server. This task combines troubleshooting skills with playbook creation, teaching you how to identify and fix common Ansible configuration errors and write playbooks that automate system tasks.

**Technical Specifications:**
- Inventory location: /home/thor/ansible/inventory
- Playbook location: /home/thor/ansible/playbook.yml
- Target server: App Server 2 (stapp02)
- Task: Create empty file /tmp/file.txt
- Required fixes: Incorrect hostname and missing password

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Navigate to the ansible directory

```bash
cd /home/thor/ansible
```

Change to the ansible working directory where the inventory and playbook files will be created. The `cd` command changes your current working directory to `/home/thor/ansible`. This directory is the base location for this task's Ansible files. By navigating here first, you can work with relative paths and keep all related files organized in one location. This follows Ansible best practices of maintaining project structure with inventory and playbooks in dedicated directories.

**Step 2:** List and examine existing files

```bash
# List all files in the directory
ls -la

# Check if inventory file exists
cat inventory
```

List directory contents to see what files already exist. The `ls -la` command shows all files with detailed information. If an inventory file exists, display its contents with `cat inventory` to understand the current configuration. In this task, you'll find an inventory file with errors that need to be fixed. Examining existing files helps you understand what needs to be corrected rather than creating from scratch. This reflects real-world scenarios where you inherit configurations from others and need to debug them.

**Step 3:** Identify inventory file errors

```ini
# Existing (broken) inventory content:
stapp02 ansible_host=172.238.16.204 ansible_user=steve ansible_ssh_common_args='-o StrictHostKeyChecking=no'
```

Review the existing inventory to identify problems. The current inventory has two issues: (1) `ansible_host=172.238.16.204` uses a specific IP address instead of the hostname, which may not resolve correctly in your environment, and (2) `ansible_ssh_password` is missing, so Ansible cannot authenticate to the server. The `ansible_user=steve` is correct for App Server 2. The `ansible_ssh_common_args` is correct for disabling host key checking. Understanding what's wrong is the first step in troubleshooting; don't just blindly replace files without understanding the issues.

**Step 4:** Fix the inventory file

```bash
vi inventory
# or
nano inventory
```

Edit the inventory file to fix the identified issues:

```ini
stapp02 ansible_host=stapp02 ansible_user=steve ansible_ssh_password=Am3ric@ ansible_ssh_common_args='-o StrictHostKeyChecking=no'
```

Correct the inventory by replacing the IP address with the hostname `stapp02` and adding the missing `ansible_ssh_password=Am3ric@`. The hostname `stapp02` should resolve correctly in the lab environment's DNS or hosts file. Using hostnames instead of IP addresses makes configurations more portable and easier to maintain. The password `Am3ric@` is the correct SSH password for the steve user on App Server 2. The complete line now includes all required connection parameters: host, user, password, and SSH options.

**Step 5:** Verify inventory syntax with ansible command

```bash
# Test connectivity to verify inventory is correct
ansible -i inventory stapp02 -m ping

# Expected successful output:
# stapp02 | SUCCESS => {
#     "changed": false,
#     "ping": "pong"
# }
```

Test the corrected inventory by running an Ansible ping command. The `ansible -i inventory stapp02 -m ping` command uses the `-i` flag to specify the inventory file, targets the `stapp02` host, and runs the `-m ping` module. A successful "pong" response confirms: (1) the hostname resolves correctly, (2) SSH connection works, (3) authentication succeeds with the provided password, and (4) Python is available on the target server. If you get errors, review the inventory for typos in the hostname, username, or password. This verification step is crucial before writing playbooks.

**Step 6:** Create the playbook file

```bash
vi playbook.yml
# or
nano playbook.yml
```

Create a new file named `playbook.yml` using your preferred text editor. Ansible playbooks use YAML (YAML Ain't Markup Language) format, which is human-readable and uses indentation to define structure. The `.yml` extension indicates a YAML file. Playbooks define the desired state of your infrastructure using declarative syntax. Unlike imperative scripts that define step-by-step procedures, playbooks describe what you want the end state to be, and Ansible figures out how to achieve it.

**Step 7:** Write the playbook to create a file

Add the following content to playbook.yml:

```yaml
---
- name: Create empty file on App Server 2
  hosts: stapp02
  become: no
  tasks:
    - name: Create /tmp/file.txt
      file:
        path: /tmp/file.txt
        state: touch
        mode: '0644'
```

Define a playbook with a single play that creates an empty file. The `---` marks the beginning of a YAML document. The `name` field provides a description of the play. `hosts: stapp02` targets App Server 2 (matching the hostname in your inventory). `become: no` means don't use sudo/privilege escalation (not needed for creating files in /tmp). The `tasks` section lists actions to perform. The `file` module manages file and directory attributes; with `state: touch`, it creates an empty file or updates the timestamp if the file exists. The `path` specifies the file location. The `mode: '0644'` sets file permissions to read/write for owner, read for group and others.

**Step 8:** Understand playbook structure and alternatives

```yaml
# Alternative playbook with additional features:
---
- name: Create empty file on App Server 2
  hosts: stapp02
  gather_facts: no  # Skip fact gathering for faster execution
  tasks:
    - name: Create /tmp/file.txt
      file:
        path: /tmp/file.txt
        state: touch
        owner: steve
        group: steve
        mode: '0644'
      register: file_result

    - name: Display result
      debug:
        msg: "File created: {{ file_result.changed }}"
```

This alternative playbook demonstrates additional features. `gather_facts: no` disables automatic fact collection, making execution faster when facts aren't needed. The `file` module includes `owner` and `group` parameters to explicitly set ownership (though these would default to the connection user anyway). The `register` keyword stores the task's result in a variable named `file_result`. The `debug` module displays the result, showing whether the file was created (changed: true) or already existed (changed: false). These features provide better visibility into what the playbook is doing.

**Step 9:** Run the playbook

```bash
# Execute the playbook with the inventory
ansible-playbook -i inventory playbook.yml

# Expected output:
# PLAY [Create empty file on App Server 2] ********************************
#
# TASK [Create /tmp/file.txt] *********************************************
# changed: [stapp02]
#
# PLAY RECAP **************************************************************
# stapp02 : ok=1 changed=1 unreachable=0 failed=0 skipped=0 rescued=0 ignored=0
```

Execute the playbook using the `ansible-playbook` command. The `-i inventory` flag specifies the inventory file, and `playbook.yml` is the playbook to run. Ansible connects to stapp02, runs the file creation task, and reports results. The output shows "changed: [stapp02]" indicating the file was created. The PLAY RECAP summarizes execution: ok=1 (one task succeeded), changed=1 (one change made), failed=0 (no failures). On subsequent runs, you'll see "ok: [stapp02]" instead of "changed" because the file already exists, demonstrating Ansible's idempotency.

**Step 10:** Verify file creation on the remote server

```bash
# SSH to App Server 2 to verify
ssh steve@stapp02
# Password: Am3ric@

# Check if file was created
ls -l /tmp/file.txt

# Expected output:
# -rw-r--r-- 1 steve steve 0 Nov 18 10:30 /tmp/file.txt

# Exit from app server
exit
```

Verify the playbook worked by manually checking the remote server. SSH to App Server 2 using the steve user credentials. The `ls -l /tmp/file.txt` command shows file details: permissions (-rw-r--r--), owner (steve), group (steve), size (0 bytes), and creation time. The file should exist with the specified permissions (0644). This manual verification confirms the playbook executed successfully. While Ansible's output is usually reliable, manual verification is valuable when troubleshooting or learning. Exit the SSH session with the `exit` command to return to the jump host.

**Step 11:** Test playbook idempotency

```bash
# Run the playbook again
ansible-playbook -i inventory playbook.yml

# Expected output shows "ok" instead of "changed":
# TASK [Create /tmp/file.txt] *********************************************
# ok: [stapp02]
#
# PLAY RECAP **************************************************************
# stapp02 : ok=1 changed=0 unreachable=0 failed=0 skipped=0 rescued=0 ignored=0
```

Run the playbook a second time to verify idempotency. Idempotency means running the same playbook multiple times produces the same result without unnecessary changes. On the second run, Ansible checks if /tmp/file.txt exists and, finding it does, reports "ok" rather than "changed". The PLAY RECAP shows changed=0, confirming no changes were made. This is a fundamental Ansible principle: playbooks should be safe to run repeatedly. Idempotent playbooks allow automated, scheduled execution without worrying about duplicate changes or errors from re-running tasks.

**Step 12:** Troubleshooting common playbook issues

```bash
# Run playbook with increased verbosity for debugging
ansible-playbook -i inventory playbook.yml -v   # verbose
ansible-playbook -i inventory playbook.yml -vv  # more verbose
ansible-playbook -i inventory playbook.yml -vvv # very verbose

# Check playbook syntax without executing
ansible-playbook -i inventory playbook.yml --syntax-check

# Dry-run to see what would change without making changes
ansible-playbook -i inventory playbook.yml --check

# Run only on specific hosts using limit
ansible-playbook -i inventory playbook.yml --limit stapp02

# List all tasks without executing
ansible-playbook -i inventory playbook.yml --list-tasks

# List all hosts affected by playbook
ansible-playbook -i inventory playbook.yml --list-hosts
```

Use these troubleshooting commands to debug playbook issues. The `-v`, `-vv`, and `-vvv` flags increase verbosity, showing progressively more detail about what Ansible is doing. Verbosity is invaluable for debugging connection issues, authentication problems, or understanding module behavior. The `--syntax-check` flag validates YAML syntax without executing the playbook, catching formatting errors. The `--check` flag performs a dry-run, showing what would change without actually making changes (some modules don't support check mode). The `--limit` flag restricts execution to specific hosts. `--list-tasks` and `--list-hosts` show what will run where, useful for understanding complex playbooks before execution.

**Step 13:** Advanced playbook error handling

```yaml
---
- name: Create empty file with error handling
  hosts: stapp02
  tasks:
    - name: Create /tmp/file.txt
      file:
        path: /tmp/file.txt
        state: touch
        mode: '0644'
      register: file_result
      ignore_errors: yes

    - name: Check if file creation failed
      debug:
        msg: "File creation failed"
      when: file_result.failed

    - name: Ensure directory exists before creating file
      file:
        path: /tmp
        state: directory
        mode: '0755'

    - name: Create file (will always succeed now)
      file:
        path: /tmp/file.txt
        state: touch
        mode: '0644'
```

This advanced playbook demonstrates error handling and conditional execution. The `ignore_errors: yes` directive allows the playbook to continue even if the task fails. The `when: file_result.failed` condition makes the debug task run only if the previous task failed. Creating the directory first ensures it exists before creating the file, though /tmp typically always exists. This pattern of checking prerequisites, handling errors gracefully, and using conditionals makes playbooks more robust. In production, you might combine this with notification tasks that alert you when errors occur.

---

## Key Concepts

**Ansible Troubleshooting Process:**
- **Examine Error Messages**: Read Ansible output carefully for clues
- **Check Inventory**: Verify hostnames, IPs, usernames, and passwords
- **Test Connectivity**: Use ansible ping module to test connections
- **Increase Verbosity**: Use -v flags to see detailed execution
- **Validate Syntax**: Use --syntax-check to catch YAML errors

**Common Inventory Issues:**
- **Wrong Hostname/IP**: Host doesn't resolve or isn't reachable
- **Missing Password**: ansible_ssh_password not defined
- **Wrong Username**: ansible_user doesn't exist on target
- **SSH Issues**: Host key verification or firewall blocking connection
- **Typos**: Misspelled variable names (ansible_ssh_pass vs ansible_ssh_password)

**Ansible File Module:**
- **state: touch**: Create empty file or update timestamp
- **state: file**: Ensure file exists (fail if it doesn't)
- **state: absent**: Remove file or directory
- **state: directory**: Create directory
- **mode**: File permissions (octal notation)
- **owner/group**: Set file ownership

**Playbook Structure:**
- **YAML Format**: Indentation-sensitive markup language
- **Play**: Collection of tasks targeting specific hosts
- **Tasks**: Individual actions to perform
- **Modules**: Reusable units that perform specific operations
- **Handlers**: Tasks triggered by notify directives

**Idempotency:**
- **Definition**: Safe to run multiple times without side effects
- **Ansible Design**: Modules designed to be idempotent
- **Check State**: Ansible checks current state before making changes
- **Reporting**: "changed" vs "ok" indicates if changes were made
- **Benefits**: Automated, scheduled playbook runs are safe

**Debugging Techniques:**
- **Verbosity Levels**: -v, -vv, -vvv for increasing detail
- **Check Mode**: Dry-run to preview changes (--check)
- **Syntax Check**: Validate YAML without executing (--syntax-check)
- **Debug Module**: Display variable values and messages
- **Register Variables**: Capture task results for inspection

---

## Validation

Test your solution using KodeKloud's automated validation.

**Validation Checklist:**
- Inventory file exists at /home/thor/ansible/inventory
- Inventory contains stapp02 host definition
- ansible_host set to stapp02 (not IP address)
- ansible_user set to steve
- ansible_ssh_password set to correct password
- ansible_ssh_common_args includes StrictHostKeyChecking=no
- Playbook file exists at /home/thor/ansible/playbook.yml
- Playbook targets stapp02 host
- Playbook creates /tmp/file.txt
- File module used with state: touch
- Running `ansible-playbook -i inventory playbook.yml` succeeds
- File /tmp/file.txt exists on stapp02 after playbook runs
- Playbook is idempotent (safe to run multiple times)

---

[← Day 82](day-82.md) | [Day 84 →](day-84.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
