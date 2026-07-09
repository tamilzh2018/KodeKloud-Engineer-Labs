# Day 92: Managing Jinja2 Templates Using Ansible

## Task Overview

Develop Ansible playbooks to automate configuration management tasks. Playbooks define desired system states using YAML syntax.

**Playbook Development:**
- Write playbook with tasks
- Define hosts and variables
- Configure modules and parameters
- Execute and verify playbook

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Perform the initial setup or connection.

```sh
cd ansible
    ls
    cat inventory
    cat playbook.yml
    ls role
```

**Step 2:** Execute the command to complete this step.

```sh
vi role/httpd/templates/index.html.j2
```

**Step 3:** Execute the command to complete this step.

```j2
<p> This file was created using Ansible on {{ inventory_hostname }} </p>
```

**Step 4:** Execute the command to complete this step.

```sh
vi role/httpd/tasks/main.yml
```

**Step 5:** Configure the resource with required specifications.

```yaml
- name: Copy index.html template
      ansible.builtin.template:
        src: index.html.j2
        dest: /var/www/html/index.html
        mode: '0777'
        owner: "{{ ansible_user }}"
        group: "{{ ansible_user }}"
```

**Step 6:** Configure the resource with required specifications.

```yaml
hosts: all
```

**Step 7:** Configure the resource with required specifications.

```yaml
---
    - hosts: all 
      become: yes
      become_user: root
      roles:
        - role/httpd
```

**Step 8:** Execute the Ansible playbook to configure hosts.

```sh
ansible-playbook -i inventory playbook.yml
```

**Step 9:** Test the web server by making HTTP request.

```sh
curl http://stapp01
    curl http://stapp02
    curl http://stapp03
```

**Step 10:** Execute the command to complete this step.

```sh
ls -la /var/www/html
```

**Step 11:** Execute the command to complete this step.

```sh
[tony@stapp01 ~]$ ls -la /var/www/html
    total 12
    drwxr-xr-x 2 root root 4096 Oct 25 02:47 .
    drwxr-xr-x 4 root root 4096 Oct 25 02:46 ..
    -rwxrwxrwx 1 tony tony   57 Oct 25 02:47 index.html
    [tony@stapp01 ~]$
```

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 91](../week-13/day-91.md) | [Day 93 →](day-93.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
