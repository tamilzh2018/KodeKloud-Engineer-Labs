# Day 93: Using Ansible Conditions

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
    ls -la
    cat inventory
```

**Step 2:** Execute the command to complete this step.

```sh
touch playbook.yml
```

**Step 3:** Execute the Ansible playbook to configure hosts.

```sh
ansible-playbook -i inventory playbook.yml
```

**Step 4:** Execute the command to complete this step.

```sh
ls -la /opt/itadmin
```

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 92](day-92.md) | [Day 94 →](day-94.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
