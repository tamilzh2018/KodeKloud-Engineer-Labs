# Day 91: Ansible Lineinfile Module

## Task Overview

Deploy a web server with custom HTML content using Ansible's lineinfile module to manage specific lines within files. This task demonstrates installing httpd, creating an index.html file, and using lineinfile to insert additional content at specific positions.

**Technical Specifications:**
- Inventory file: /home/thor/ansible/inventory (pre-existing)
- Playbook location: /home/thor/ansible/playbook.yml (to be created)
- Web server: httpd (Apache HTTP Server)
- Content file: /var/www/html/index.html
- File ownership: apache:apache
- File permissions: 0755
- Line insertion: Add heading at top of file using insertbefore: BOF

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Navigate to the Ansible directory and examine inventory

```sh
cd ~/ansible
cat inventory
```

Change to the Ansible directory where the inventory file is located, then display its contents to understand which hosts are defined and their connection parameters. The inventory should contain definitions for all app servers with their SSH credentials. Understanding the inventory structure helps ensure your playbook targets the correct hosts.

**Step 2:** Create an empty playbook file

```sh
touch playbook.yml
```

Create an empty playbook file using the `touch` command. This file will contain all the tasks needed to install httpd, start the service, create the index.html file with initial content, add additional content using lineinfile, and set proper ownership and permissions. Creating the file first allows you to edit it with your preferred text editor in the next step.

**Step 3:** Edit the playbook with web server and lineinfile configuration

```yaml
---
- name: Install httpd and configure index.html with lineinfile
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

    - name: Create index.html with initial content
      ansible.builtin.copy:
        content: "<p> This is a Nautilus sample file, created using Ansible! </p>\n"
        dest: /var/www/html/index.html
        owner: apache
        group: apache
        mode: '0755'

    - name: Add heading at top of index.html using lineinfile
      ansible.builtin.lineinfile:
        path: /var/www/html/index.html
        line: "<h1> Welcome to xFusionCorp Industries!</h1>"
        insertbefore: BOF
        state: present
```

Open the playbook with `vi playbook.yml` (or your preferred editor) and add the content shown above. The playbook performs multiple tasks in sequence: (1) installs the httpd package using the yum module, (2) starts and enables the httpd service for both runtime and boot, (3) creates the index.html file with initial paragraph content using the copy module, setting ownership to apache:apache and permissions to 0755, and (4) uses the lineinfile module to insert a heading line at the beginning of the file. The key lineinfile parameters are: `path` specifies the target file, `line` contains the exact text to insert, `insertbefore: BOF` (Beginning Of File) positions the line at the top of the file, and `state: present` ensures the line exists. The `become: yes` directive enables privilege escalation for all tasks since they require root permissions. The lineinfile module is idempotent - if the line already exists, it won't be added again, making the playbook safe to run multiple times.

**Step 4:** Execute the Ansible playbook

```sh
ansible-playbook -i inventory playbook.yml
```

Run the playbook using the `ansible-playbook` command with the `-i inventory` flag to specify the inventory file. Ansible will execute all tasks in sequence across all targeted hosts. The output displays task execution status for each host: "changed" indicates modifications were made (package installed, service started, file created, line added), "ok" means the desired state already exists, and "failed" indicates errors. Watch the lineinfile task - on the first run it should show "changed" as it adds the heading line; on subsequent runs it should show "ok" since the line already exists, demonstrating idempotency.

**Step 5:** Verify web server functionality with curl

```sh
curl http://stapp01
curl http://stapp02
curl http://stapp03
```

Test that the httpd web server is responding correctly and serving the configured HTML content. Use `curl` to send HTTP requests to each app server. The response should show the HTML content with the heading line first (added by lineinfile at BOF - Beginning Of File), followed by the paragraph line (from the initial file creation). The output should look like:
```html
<h1> Welcome to xFusionCorp Industries!</h1>
<p> This is a Nautilus sample file, created using Ansible! </p>
```
This confirms that httpd is installed, running, and serving the file, and that the lineinfile module correctly inserted the heading at the top of the file.

**Step 6:** View the index.html file structure

```sh
ansible all -i inventory -m shell -a "cat /var/www/html/index.html" --become
```

Display the complete contents of the index.html file on all servers using an Ansible ad-hoc command. This shows the final file structure after the lineinfile operation. You should see the heading line at the top (inserted by lineinfile with `insertbefore: BOF`), followed by the paragraph line (from the initial file creation). This verification confirms that lineinfile correctly positioned the new content at the beginning of the file as intended.

**Step 7:** Verify file ownership and permissions

```sh
ansible all -i inventory -m shell -a "ls -la /var/www/html/index.html" --become
```

Check that the index.html file has the correct ownership and permissions using `ls -la`. The output should show the file owned by apache:apache with permissions 0755 (rwxr-xr-x). The 0755 permissions allow the owner (apache) to read, write, and execute, while group and others can read and execute. For HTML files, execute permission isn't strictly necessary, but it doesn't cause issues. The apache ownership ensures the web server process can read and serve the file properly.

**Step 8:** Additional lineinfile operations (optional)

```yaml
# Insert line after a specific pattern
- name: Add line after paragraph
  ansible.builtin.lineinfile:
    path: /var/www/html/index.html
    line: "<p> Additional content </p>"
    insertafter: "Nautilus sample file"
    state: present

# Replace a line matching a regex pattern
- name: Update heading text
  ansible.builtin.lineinfile:
    path: /var/www/html/index.html
    regexp: '^<h1>.*</h1>$'
    line: "<h1> Updated Welcome Message!</h1>"
    state: present

# Remove a specific line
- name: Remove paragraph line
  ansible.builtin.lineinfile:
    path: /var/www/html/index.html
    regexp: '^<p>.*Nautilus.*</p>$'
    state: absent

# Add line at end of file
- name: Add footer at end
  ansible.builtin.lineinfile:
    path: /var/www/html/index.html
    line: "<footer> Copyright 2024 </footer>"
    insertafter: EOF
    state: present
```

These examples demonstrate additional lineinfile capabilities. You can insert lines after specific patterns using `insertafter` with text or regex. You can replace existing lines by matching them with `regexp` and providing a new `line`. You can remove lines using `state: absent` with `regexp`. You can add content at the end using `insertafter: EOF` (End Of File). Understanding these options allows you to build sophisticated file manipulation playbooks for various configuration management scenarios.

---

## Key Concepts

**Ansible Lineinfile Module:**
- Manages individual lines within text files
- Ensures a specific line exists or doesn't exist in a file
- Can insert lines at specific positions (beginning, end, before/after patterns)
- Can replace lines matching regular expressions
- Idempotent: Safe to run multiple times without duplicating lines
- Useful for configuration files where you need to manage specific settings

**Lineinfile Module Parameters:**
- `path` - Target file path (required)
- `line` - Text content of the line to manage
- `regexp` - Regular expression to match existing lines
- `state: present` - Ensure line exists (default)
- `state: absent` - Ensure line doesn't exist (removes if found)
- `insertbefore` - Insert before line matching pattern or BOF (Beginning Of File)
- `insertafter` - Insert after line matching pattern or EOF (End Of File)
- `backrefs` - Use back-references in line when used with regexp
- `create` - Create file if it doesn't exist (default: no)
- `owner`, `group`, `mode` - Set file ownership and permissions
- `backup` - Create backup before modifying (default: no)

**Position Keywords:**
- `BOF` - Beginning Of File (insert at the very top)
- `EOF` - End Of File (insert at the very bottom)
- Pattern matching - Insert before/after line matching regex
- Use `insertbefore: BOF` to add content at file start
- Use `insertafter: EOF` to append content at file end

**Regular Expressions with Lineinfile:**
- `regexp` parameter matches existing lines to replace or identify position
- Python regex syntax (re module)
- `^` anchors to beginning of line, `$` anchors to end
- `.` matches any character, `.*` matches any sequence
- Use regex to find lines by pattern, then replace with `line` content
- Example: `regexp: '^ServerName'` matches lines starting with "ServerName"

**Lineinfile vs Blockinfile:**
- `lineinfile` - Manages single lines in files
- `blockinfile` - Manages multi-line blocks of text
- Use lineinfile for individual configuration directives
- Use blockinfile for inserting multiple related lines together
- Lineinfile doesn't add markers, blockinfile does
- Both are idempotent and safe for repeated execution

**Idempotency Behavior:**
- When `regexp` is used: Replaces first matching line or adds line if no match
- When `regexp` not used: Checks if exact line exists, adds if missing
- Multiple runs produce same result unless file is modified externally
- Safe to include in playbooks that run repeatedly
- Prevents duplicate lines from being added

**Common Use Cases:**
- Adding configuration directives to config files
- Enabling/disabling specific settings in application configs
- Updating single values in INI files, YAML files, shell configs
- Managing entries in /etc/hosts, /etc/environment
- Modifying Apache/Nginx configuration files
- Setting kernel parameters in /etc/sysctl.conf

**Best Practices:**
- Use `regexp` to make playbooks idempotent when line content might change
- Always use `state: present` explicitly for clarity
- Test regular expressions before using in production playbooks
- Use `backup: yes` when modifying critical configuration files
- Consider `blockinfile` for multi-line content instead of multiple lineinfile tasks
- Document why specific lines are being managed in task names/comments
- Use `validate` parameter when available to verify syntax before applying changes

**File Validation Example:**
```yaml
- name: Update sshd config with validation
  ansible.builtin.lineinfile:
    path: /etc/ssh/sshd_config
    regexp: '^#?PermitRootLogin'
    line: 'PermitRootLogin no'
    validate: '/usr/sbin/sshd -t -f %s'
    backup: yes
```
The `validate` parameter runs a command to test the file before applying changes. Use `%s` as placeholder for the temporary file path. If validation fails, changes are not applied, preventing broken configurations.

**Backreferences Example:**
```yaml
- name: Update port number in config
  ansible.builtin.lineinfile:
    path: /etc/myapp/config.ini
    regexp: '^(port\s*=\s*)\d+$'
    line: '\g<1>8080'
    backrefs: yes
```
Backreferences allow you to preserve part of a matched line while changing other parts. Use `\g<1>`, `\g<2>`, etc. to reference captured groups from the regex. This is useful for updating values while preserving keys and formatting.

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 90](day-90.md) | [Day 92 →](day-92.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
