# Day 82: Create Ansible Inventory for App Server Testing

## Task Overview

Create an Ansible inventory file that defines managed nodes and their connection parameters. Inventory files are fundamental to Ansible, mapping hostnames to actual servers and defining how Ansible connects to them. This task builds the foundation for running Ansible playbooks against infrastructure.

**Technical Specifications:**
- Inventory format: INI format
- Inventory location: /home/thor/playbook/inventory
- Target server: App Server 1 (stapp01)
- Connection method: SSH with password authentication
- Required variables: ansible_user, ansible_ssh_pass, ansible_ssh_common_args

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Navigate to the playbook directory

```bash
cd /home/thor/playbook
```

Change to the directory where playbooks are stored. The `/home/thor/playbook/` directory is the working location for this task, containing Ansible playbooks that need an inventory file to run. The `cd` command changes your current working directory. By navigating here first, you can create files and run commands in the correct location without specifying full paths. This directory structure follows Ansible conventions where playbooks and inventory files are kept together for easy management.

**Step 2:** List existing files in the directory

```bash
ls -la
```

List all files in the current directory to see what already exists. The `ls -la` command shows detailed file information including hidden files (`-a`), permissions, owner, size, and modification dates (`-l`). You should see existing playbook files (like `playbook.yml`) but no inventory file yet. Understanding the directory contents helps you avoid overwriting existing files and confirms you're in the correct location. The playbook files in this directory are what you'll eventually run against the inventory you're about to create.

**Step 3:** Create the inventory file

```bash
vi inventory
# or
nano inventory
```

Create a new file named `inventory` using a text editor. The `vi` or `nano` commands open text editors in the terminal. Choose the editor you're comfortable with: `vi` is powerful but has a learning curve (press `i` to enter insert mode, `Esc` to exit insert mode, `:wq` to save and quit), while `nano` is more beginner-friendly (edit directly, `Ctrl+O` to save, `Ctrl+X` to exit). The filename `inventory` is standard for Ansible inventory files, though you can use any name as long as you reference it correctly when running playbooks.

**Step 4:** Define the inventory structure with INI format

Add the following content to the inventory file:

```ini
[app]
stapp01

[app:vars]
ansible_user=tony
ansible_ssh_pass=Ir0nM@n
ansible_ssh_common_args='-o StrictHostKeyChecking=no'
```

Define the inventory structure using INI format. The `[app]` section creates a group named "app" containing the host `stapp01`. Groups allow you to target multiple servers with a single playbook run and organize hosts by function, environment, or location. The `[app:vars]` section defines variables that apply to all hosts in the "app" group. `ansible_user=tony` specifies the SSH username for connections. `ansible_ssh_pass=Ir0nM@n` provides the SSH password (note: storing passwords in plain text is convenient for labs but use Ansible Vault in production). `ansible_ssh_common_args='-o StrictHostKeyChecking=no'` passes additional SSH arguments, specifically disabling host key checking to prevent interactive prompts during first connection.

**Step 5:** Understand inventory components and alternatives

Alternative inventory format with explicit host definition:

```ini
# Explicit host with inline variables
[app]
stapp01 ansible_user=tony ansible_ssh_pass=Ir0nM@n ansible_ssh_common_args='-o StrictHostKeyChecking=no'

# Or using ansible_host for IP-based connection
[app]
stapp01 ansible_host=172.16.238.10 ansible_user=tony ansible_ssh_pass=Ir0nM@n ansible_ssh_common_args='-o StrictHostKeyChecking=no'
```

These alternative formats achieve the same result but structure data differently. The first approach defines all connection parameters inline with the hostname, which works well for single-host groups. The second approach uses `ansible_host` to map a friendly name (`stapp01`) to an IP address, useful when DNS isn't configured or you want memorable names instead of IP addresses. Choose the format that best fits your environment and makes the inventory most readable. Group variables (using `[group:vars]`) are cleaner when multiple hosts share the same settings.

**Step 6:** Verify inventory file syntax

```bash
# View the created inventory file
cat inventory

# Check file contents are correct
# Should show:
# [app]
# stapp01
#
# [app:vars]
# ansible_user=tony
# ansible_ssh_pass=Ir0nM@n
# ansible_ssh_common_args='-o StrictHostKeyChecking=no'
```

Verify the inventory file was created correctly by displaying its contents. The `cat inventory` command prints the file to the terminal. Check that all sections are present: the `[app]` group header, the `stapp01` hostname, the `[app:vars]` group variables header, and all three required variables. Ensure there are no typos in variable names or values, as these will cause connection failures. The variable names are case-sensitive and must match exactly. This verification step catches errors before attempting to run playbooks.

**Step 7:** Test inventory with Ansible ad-hoc ping

```bash
# Test connectivity to the inventory
ansible -i inventory app -m ping

# Expected output:
# stapp01 | SUCCESS => {
#     "changed": false,
#     "ping": "pong"
# }
```

Test the inventory by running an Ansible ad-hoc command. The `ansible -i inventory app -m ping` command uses the `-i` flag to specify the inventory file, targets the `app` group, and uses the `-m ping` flag to run Ansible's ping module. This isn't a network ICMP ping; it's an Ansible module that tests connectivity and validates Python is available on the remote host. A "SUCCESS" response with "pong" confirms: (1) Ansible can connect via SSH, (2) authentication works with the provided credentials, (3) Python is installed on the target host, and (4) Ansible can execute modules. Any errors indicate problems with the inventory configuration or target host.

**Step 8:** Run the playbook using the inventory

```bash
# Execute the playbook with the inventory
ansible-playbook -i inventory playbook.yml

# The validation will run this exact command
# Ensure it completes successfully
```

Execute the existing playbook using your newly created inventory. The `ansible-playbook -i inventory playbook.yml` command runs the playbook file against hosts defined in the inventory. The `-i inventory` flag specifies which inventory to use. The playbook tasks will execute on `stapp01` (the host in your inventory). Monitor the output for any errors or failed tasks. A successful run shows "ok" or "changed" status for each task and a final recap showing no failures. The KodeKloud validation system will run this exact command, so it must work without additional parameters or manual intervention.

**Step 9:** Understand inventory variable hierarchy

```bash
# Variable precedence (lowest to highest):
# 1. Group vars (all group)
# 2. Group vars (specific group like [app:vars])
# 3. Host vars (defined inline or in host_vars/)
# 4. Extra vars (passed with -e flag)

# Example showing different variable locations:
[all:vars]
ansible_ssh_common_args='-o StrictHostKeyChecking=no'

[app]
stapp01

[app:vars]
ansible_user=tony
ansible_ssh_pass=Ir0nM@n

# Could also use host_vars/stapp01.yml for host-specific variables
```

Understand Ansible's variable precedence for better inventory management. Variables can be defined at multiple levels: `[all:vars]` applies to every host in the inventory, `[group:vars]` applies to all hosts in that group, and inline host variables apply to individual hosts. When the same variable is defined at multiple levels, the more specific definition wins (host vars override group vars, which override all vars). Extra variables passed with `-e` on the command line have the highest precedence. This hierarchy allows you to set common defaults and override them for specific groups or hosts, promoting DRY (Don't Repeat Yourself) principles.

**Step 10:** Advanced inventory patterns and best practices

```ini
# Multiple groups for the same host
[app]
stapp01

[web]
stapp01

[production]
stapp01

# Range patterns for multiple hosts
[app]
stapp[01:03]

# This expands to: stapp01, stapp02, stapp03

# Using group of groups
[datacenter:children]
app
web
database

[datacenter:vars]
ansible_ssh_common_args='-o StrictHostKeyChecking=no'
```

Explore advanced inventory patterns for complex environments. A single host can belong to multiple groups, allowing flexible targeting (e.g., target all "web" servers or all "production" servers). Range patterns like `stapp[01:03]` create multiple hosts with sequential numbering, reducing repetition. Group of groups using `[groupname:children]` creates parent groups containing other groups, enabling hierarchical organization. Variables defined on parent groups cascade to all child groups and their hosts. These patterns become invaluable in large-scale environments with dozens or hundreds of servers.

**Step 11:** Troubleshooting common inventory issues

```bash
# List all hosts in inventory
ansible -i inventory --list-hosts all

# View inventory structure
ansible-inventory -i inventory --list

# View inventory as YAML
ansible-inventory -i inventory --list -y

# Check which hosts match a pattern
ansible -i inventory --list-hosts app

# Verbose connection testing
ansible -i inventory app -m ping -vvv
```

Use these troubleshooting commands to diagnose inventory problems. `ansible --list-hosts` shows which hosts Ansible recognizes in the inventory. `ansible-inventory --list` displays the complete inventory structure including all variables, useful for verifying variable definitions. The `-y` flag outputs in YAML format for better readability. The `-vvv` flag enables verbose output showing detailed SSH connection attempts, authentication steps, and module execution, invaluable for debugging connection issues. Common problems include typos in hostnames, incorrect passwords, network connectivity issues, or missing Python on target hosts.

**Step 12:** Security considerations for production environments

```bash
# NEVER store passwords in plain text in production
# Instead, use Ansible Vault:

# Create encrypted inventory
ansible-vault create inventory

# Edit encrypted inventory
ansible-vault edit inventory

# Run playbook with vault password
ansible-playbook -i inventory playbook.yml --ask-vault-pass

# Or use a vault password file
ansible-playbook -i inventory playbook.yml --vault-password-file ~/.vault_pass

# Encrypt only the password variable
ansible-vault encrypt_string 'Ir0nM@n' --name 'ansible_ssh_pass'
```

Understand security best practices for production inventories. Storing passwords in plain text exposes credentials if inventory files are committed to version control or accessed by unauthorized users. Ansible Vault encrypts inventory files or specific variables, protecting sensitive data. The `ansible-vault create` command creates a new encrypted file. `ansible-vault edit` allows editing encrypted files. When running playbooks, use `--ask-vault-pass` to prompt for the decryption password, or `--vault-password-file` to read it from a file. For fine-grained control, encrypt only password variables using `encrypt_string`. Always use vault encryption in production environments.

---

## Key Concepts

**Ansible Inventory Fundamentals:**
- **Inventory File**: Defines managed nodes and how to connect to them
- **Hosts**: Individual servers Ansible manages
- **Groups**: Logical collections of hosts (e.g., web, database, production)
- **Variables**: Connection parameters and host-specific data

**Inventory Formats:**
- **INI Format**: Simple, human-readable, suitable for small inventories
- **YAML Format**: More structured, better for complex hierarchies
- **Dynamic Inventory**: Generated by scripts or plugins (e.g., AWS, Azure)
- **Inventory Plugins**: Modern approach for dynamic inventories

**Connection Variables:**
- **ansible_user**: SSH username for remote connections
- **ansible_ssh_pass**: SSH password (use Ansible Vault in production)
- **ansible_host**: Target hostname or IP address
- **ansible_port**: SSH port (default 22)
- **ansible_ssh_common_args**: Additional SSH arguments
- **ansible_become**: Enable privilege escalation
- **ansible_become_user**: User to become (default root)

**Group Organization Strategies:**
- **By Function**: web, database, cache, load-balancer
- **By Environment**: production, staging, development
- **By Location**: us-east, eu-west, datacenter-1
- **By Role**: application-servers, monitoring-servers

**Inventory Best Practices:**
- **Use Groups**: Organize hosts logically for easy targeting
- **DRY Principle**: Use group variables to avoid repetition
- **Meaningful Names**: Use descriptive host and group names
- **Vault Encryption**: Encrypt sensitive data in production
- **Version Control**: Track inventory changes in Git
- **Documentation**: Comment complex inventory structures

**Variable Precedence:**
1. Extra vars (`-e` flag) - highest precedence
2. Task vars (defined in playbook tasks)
3. Block vars (defined in playbook blocks)
4. Role and include vars
5. Set_facts and registered vars
6. Host facts (discovered facts)
7. Playbook host_vars
8. Playbook group_vars
9. Inventory host_vars
10. Inventory group_vars
11. Inventory vars
12. Role defaults - lowest precedence

---

## Validation

Test your solution using KodeKloud's automated validation.

**Validation Checklist:**
- Inventory file created at /home/thor/playbook/inventory
- Inventory format is INI
- Host stapp01 defined in inventory
- Inventory includes [app] group containing stapp01
- ansible_user variable set to tony
- ansible_ssh_pass variable set correctly
- ansible_ssh_common_args includes StrictHostKeyChecking=no
- Running `ansible-playbook -i inventory playbook.yml` succeeds
- No additional arguments required for playbook execution
- Playbook runs without prompting for passwords or confirmation

---

[← Day 81](day-81.md) | [Day 83 →](day-83.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
