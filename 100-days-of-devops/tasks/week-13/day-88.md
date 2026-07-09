# Day 88: Ansible Blockinfile Module

## Task Overview

Deploy and configure a web server with custom content using Ansible's blockinfile module. This task demonstrates installing httpd, managing its service, and inserting blocks of text into files with proper ownership and permissions.

**Technical Specifications:**
- Inventory file: /home/thor/ansible/inventory (pre-existing)
- Playbook location: /home/thor/ansible/playbook.yml (to be created)
- Web server: httpd (Apache HTTP Server)
- Content file: /var/www/html/index.html
- File ownership: apache:apache
- File permissions: 0644

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Navigate to the Ansible directory

```sh
cd ~/ansible
```

Change your working directory to the Ansible folder where the inventory file already exists. This directory will also house the playbook you'll create to automate web server installation and configuration. Keeping all related Ansible files in one directory maintains project organization and makes file references in playbooks more straightforward.

**Step 2:** Examine the existing inventory file

```sh
cat inventory
```

Display the contents of the existing inventory file to understand which hosts are defined and how they're configured. The inventory file should already contain definitions for the app servers with their connection parameters. Understanding the inventory structure helps you correctly target hosts in your playbook.

**Step 3:** Create an empty playbook file

```sh
touch playbook.yml
```

Create an empty playbook file using the `touch` command. This file will contain all the tasks needed to install httpd, start its service, create the index.html file, add content using blockinfile, and set proper ownership and permissions. Creating the file first allows you to edit it with your preferred text editor in the next step.

**Step 4:** Edit the playbook with web server configuration

```yaml
---
- name: Install and configure httpd with custom index page
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

    - name: Insert content block in index.html
      ansible.builtin.blockinfile:
        path: /var/www/html/index.html
        create: yes
        block: |
          Welcome to XfusionCorp!

          This is Nautilus sample file, created using Ansible!

          Please do not modify this file manually!
        owner: apache
        group: apache
        mode: '0644'
```

Open the playbook file with `vi playbook.yml` (or your preferred editor) and add the content shown above. The playbook performs multiple tasks: (1) installs the httpd package using the yum module, (2) ensures the httpd service is running and enabled at boot using the service module, and (3) uses the blockinfile module to insert a block of HTML content into /var/www/html/index.html. The `become: yes` directive enables privilege escalation for all tasks since they require root permissions. The blockinfile module's `create: yes` parameter creates the file if it doesn't exist, while `block: |` introduces a multi-line string containing the HTML content. The `owner`, `group`, and `mode` parameters ensure the file has correct ownership (apache:apache) and permissions (0644) for the web server to serve it properly. The blockinfile module automatically adds marker comments (`# BEGIN ANSIBLE MANAGED BLOCK` and `# END ANSIBLE MANAGED BLOCK`) to identify the managed content, making it safe to run the playbook multiple times without duplicating content.

**Step 5:** Execute the Ansible playbook

```sh
ansible-playbook -i inventory playbook.yml
```

Run the playbook using the `ansible-playbook` command with the `-i inventory` flag to specify the inventory file. Ansible will execute all tasks in sequence across all targeted hosts. The output will show the status of each task: "changed" when tasks modify the system (installing packages, starting services, creating files), or "ok" when the desired state already exists. Watch for any "failed" statuses that indicate errors requiring attention. The idempotent nature of Ansible ensures that running this playbook multiple times will only make necessary changes to achieve the desired state.

**Step 6:** Verify web server functionality

```sh
# Test httpd service is running
ansible all -i inventory -m shell -a "systemctl status httpd" --become

# Verify index.html file exists with correct ownership
ansible all -i inventory -m shell -a "ls -la /var/www/html/index.html" --become

# Test web server response with curl
curl http://stapp01
curl http://stapp02
curl http://stapp03
```

Verify the deployment was successful using multiple verification methods. First, check that the httpd service is running on all servers using an Ansible ad-hoc command with systemctl. Second, verify the index.html file exists with the correct ownership and permissions using `ls -la`. Finally, test the actual web server response by using `curl` to fetch the index page from each server - you should see the HTML content you inserted with blockinfile. These verification steps confirm that httpd is installed, running, and serving the custom content correctly.

**Step 7:** View the index.html file with markers

```sh
ansible all -i inventory -m shell -a "cat /var/www/html/index.html" --become
```

Display the complete contents of the index.html file to see how blockinfile adds marker comments. The file will contain:
```
# BEGIN ANSIBLE MANAGED BLOCK
Welcome to XfusionCorp!

This is Nautilus sample file, created using Ansible!

Please do not modify this file manually!
# END ANSIBLE MANAGED BLOCK
```
These markers allow Ansible to identify and update the specific block of content in future playbook runs without affecting other content in the file. This makes blockinfile ideal for managing configuration file sections that might also contain manually added content.

---

## Key Concepts

**Ansible Blockinfile Module:**
- Inserts, updates, or removes blocks of multi-line text in files
- Automatically adds marker comments to identify managed content blocks
- Default markers: `# BEGIN ANSIBLE MANAGED BLOCK` and `# END ANSIBLE MANAGED BLOCK`
- Idempotent: Safe to run multiple times without duplicating content
- Useful for managing sections within larger configuration files
- Can be used with custom markers for multiple managed blocks in one file

**Blockinfile Module Parameters:**
- `path` - Target file path (required)
- `block` - Multi-line text content to insert (use `|` for multi-line strings)
- `create` - Create file if it doesn't exist (default: no)
- `marker` - Custom marker template (default: `# {mark} ANSIBLE MANAGED BLOCK`)
- `insertafter` - Insert block after line matching regex
- `insertbefore` - Insert block before line matching regex
- `state: present` - Ensure block exists (default)
- `state: absent` - Remove block from file
- `owner`, `group`, `mode` - Set file ownership and permissions

**Marker Customization:**
- Default marker format: `# {mark} ANSIBLE MANAGED BLOCK`
- `{mark}` is replaced with "BEGIN" and "END"
- Custom example: `marker: "<!-- {mark} CUSTOM BLOCK -->"`
- Use different markers for multiple blocks in the same file
- Markers must be unique to avoid conflicts
- Empty marker (`marker: ""`) creates blocks without markers (not recommended)

**Apache Web Server Management:**
- Document root: `/var/www/html/` is default location for web content
- Service name: `httpd` on Red Hat/CentOS, `apache2` on Debian/Ubuntu
- Default user: `apache` on Red Hat/CentOS, `www-data` on Debian/Ubuntu
- File ownership: Web content should be owned by the web server user
- File permissions: `0644` allows web server to read but not modify files
- Service management: Start, stop, restart, enable/disable at boot

**File Module vs Blockinfile Module:**
- `file` module - Creates empty files, manages permissions, creates directories
- `blockinfile` module - Inserts/manages blocks of text content in files
- `lineinfile` module - Manages single lines in files
- `copy` module - Copies entire files from controller to managed nodes
- `template` module - Processes Jinja2 templates and copies to managed nodes
- Use blockinfile when you need to manage a section within a larger file

**Service Module Parameters:**
- `name` - Service name (required)
- `state: started` - Ensure service is running
- `state: stopped` - Ensure service is stopped
- `state: restarted` - Restart the service
- `state: reloaded` - Reload service configuration without full restart
- `enabled: yes` - Enable service to start at boot
- `enabled: no` - Disable service from starting at boot

**Multi-line Strings in YAML:**
- Literal style (`|`) - Preserves line breaks, strips final newlines
- Folded style (`>`) - Converts line breaks to spaces (for long lines)
- Example: `block: |` followed by indented multi-line content
- Each line of the block must be indented consistently
- Useful for configuration files, HTML content, scripts, etc.

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 87](day-87.md) | [Day 89 →](day-89.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
