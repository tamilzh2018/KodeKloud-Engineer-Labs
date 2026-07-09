# Day 86: Ansible Ping Module Usage

## Task Overview

Test connectivity between Ansible controller and managed nodes using the Ansible ping module. This task verifies SSH authentication, Python availability, and network connectivity - essential prerequisites before running any automation playbooks.

**Technical Specifications:**
- Ansible controller: Jump host (thor user)
- Inventory file: /home/thor/ansible/inventory
- Target host: App Server 3 (stapp03)
- Connection method: Password-based SSH authentication
- Validation: Successful ping response from target server

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Navigate to the Ansible directory

```sh
cd ~/ansible
```

Change your working directory to the Ansible folder in the home directory. This is where the inventory file is located and where you'll execute Ansible commands. Keeping a dedicated directory for Ansible files helps organize inventory files, playbooks, configuration files, and other automation artifacts in a structured manner.

**Step 2:** Examine the existing inventory file

```sh
cat inventory
```

Display the contents of the inventory file to understand the current configuration. The inventory file may contain host definitions but might be missing critical connection parameters like SSH users and passwords. Understanding the existing configuration helps determine what modifications are needed to establish successful connections to the managed nodes.

**Step 3:** Update the inventory file with connection parameters

```ini
stapp01 ansible_host=172.16.238.10 ansible_user=tony ansible_ssh_pass=Ir0nM@n
stapp02 ansible_host=172.16.238.11 ansible_user=steve ansible_ssh_pass=Am3ric@
stapp03 ansible_host=172.16.238.12 ansible_user=banner ansible_ssh_pass=BigGr33n

[all:vars]
ansible_ssh_common_args='-o StrictHostKeyChecking=no'
```

Edit the inventory file to include complete connection details for all three application servers. Each line defines a host with its IP address (`ansible_host`), SSH username (`ansible_user`), and SSH password (`ansible_ssh_pass`). The `ansible_host` variable allows you to use friendly names (stapp01, stapp02, stapp03) in commands while Ansible connects to the actual IP addresses. The `[all:vars]` section defines variables that apply to all hosts in the inventory. The `ansible_ssh_common_args` parameter passes additional SSH options - specifically `-o StrictHostKeyChecking=no`, which bypasses the SSH fingerprint verification prompt that would otherwise require interactive confirmation when connecting to hosts for the first time. While this is convenient for lab environments, production systems should properly manage SSH host keys for security.

**Step 4:** Test connectivity to App Server 3 using ping module

```sh
ansible stapp03 -i inventory -m ping
```

Execute the Ansible ping module against stapp03 to verify connectivity. The command syntax breaks down as follows: `ansible` invokes the ad-hoc command tool, `stapp03` specifies the target host from the inventory, `-i inventory` tells Ansible which inventory file to use, and `-m ping` specifies the module to execute. Despite its name, the ping module doesn't use ICMP packets like the traditional ping command. Instead, it establishes an SSH connection, verifies Python is available on the remote system, executes a small Python script, and returns a "pong" response if successful. A successful response looks like: `stapp03 | SUCCESS => { "changed": false, "ping": "pong" }`. The "changed": false indicates no system state was modified, and "ping": "pong" confirms successful connectivity. If the ping fails, you'll see error messages indicating network issues, authentication failures, or missing Python interpreters.

**Step 5:** Test connectivity to all app servers (optional verification)

```sh
ansible all -i inventory -m ping
```

Extend the connectivity test to all servers defined in the inventory file. Using `all` as the target tells Ansible to execute the ping module against every host in the inventory, rather than just a single server. This command runs in parallel across all hosts, making it efficient for testing connectivity to multiple servers simultaneously. The output will show individual results for each server (stapp01, stapp02, and stapp03), allowing you to quickly verify that all managed nodes are accessible and properly configured. This is particularly useful for validating the entire infrastructure before running more complex playbooks.

**Step 6:** Alternative ping test with specific server groups

```sh
# Create a group in inventory first
[app_servers]
stapp01
stapp02
stapp03

# Then ping the group
ansible app_servers -i inventory -m ping
```

Demonstrate inventory grouping by organizing hosts into logical groups. In the inventory file, create a group named `[app_servers]` and list the three hosts under it. Groups allow you to target multiple related hosts with a single command, which is more maintainable than using `all` (which includes every host) or listing hosts individually. After creating the group, you can use `ansible app_servers -i inventory -m ping` to ping all hosts in that specific group. This approach becomes invaluable in larger environments where you might have different groups like `[web_servers]`, `[database_servers]`, `[load_balancers]`, etc., each requiring different configurations or tasks.

---

## Key Concepts

**Ansible Ping Module:**
- NOT an ICMP ping - uses SSH connection and Python execution
- Tests three critical components: network connectivity, SSH authentication, Python availability
- Returns "pong" on success, error message on failure
- Does not modify system state (changed: false)
- First troubleshooting step for Ansible connectivity issues
- Lightweight and fast, suitable for regular health checks

**Inventory File Structure:**
- Lists managed nodes (hosts) that Ansible can control
- Supports INI or YAML format (INI shown in this task)
- Can define individual hosts or groups of hosts
- Variables can be set per-host or per-group
- Default location: `/etc/ansible/hosts` (can be overridden with `-i` flag)
- Supports static inventories (files) or dynamic inventories (scripts/plugins)

**Connection Variables:**
- `ansible_host` - IP address or hostname for SSH connection (overrides inventory hostname)
- `ansible_user` - SSH username for authentication
- `ansible_ssh_pass` or `ansible_password` - SSH password (prefer ansible-vault encryption)
- `ansible_port` - SSH port (default: 22)
- `ansible_ssh_private_key_file` - Path to SSH private key for key-based auth
- `ansible_ssh_common_args` - Additional SSH command-line arguments
- `ansible_become` - Enable privilege escalation (sudo/su)
- `ansible_become_user` - User to become (default: root)

**SSH Authentication Methods:**
- Password-based: Uses `ansible_ssh_pass` (shown in this task)
- Key-based: Uses `ansible_ssh_private_key_file` (more secure, recommended for production)
- SSH agent: Automatically uses keys loaded in ssh-agent
- Password-based authentication is simpler for labs but requires storing passwords
- Key-based authentication is more secure and doesn't require password storage
- For production: use SSH keys + ansible-vault for any remaining password variables

**Ad-hoc Commands vs Playbooks:**
- Ad-hoc commands: One-time tasks executed directly from command line
- Syntax: `ansible <hosts> -i <inventory> -m <module> -a <arguments>`
- Useful for quick checks, testing, one-off operations
- Playbooks: Reusable automation scripts written in YAML
- Playbooks support complex logic, loops, conditionals, error handling
- Use ad-hoc for simple tasks, playbooks for repeatable automation

**Troubleshooting Ping Failures:**
- Network issues: Check firewall rules, routing, DNS resolution
- Authentication failures: Verify username/password, SSH keys, permissions
- SSH service not running: Ensure sshd is active on target hosts
- Python not installed: Ansible requires Python 2.7+ or Python 3.5+ on managed nodes
- Privilege issues: Some tasks require sudo/root access via `become`
- SSH strict host checking: Add `-o StrictHostKeyChecking=no` for new hosts

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 85](day-85.md) | [Day 87 →](day-87.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
