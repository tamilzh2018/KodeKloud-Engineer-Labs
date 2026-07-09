# Day 8: Setup Ansible

## Task Overview

During the weekly meeting, the Nautilus DevOps team discussed automation and configuration management solutions. After considering several options, the team decided to use Ansible due to its simple setup and minimal prerequisites. The team wants to start testing with Ansible by using the jump host as an Ansible controller to test different tasks on the remaining servers.

**Objective:** Install Ansible version 4.8.0 on the jump host using pip3 only. Ensure the Ansible binary is available globally on the system, allowing all users to run Ansible commands.

**Playbook Development:**
- Write playbook with tasks
- Define hosts and variables
- Configure modules and parameters
- Execute and verify playbook

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

### Step 1: Install Ansible Using pip3

Install Ansible version 4.8.0 using Python's package manager with global accessibility.

```bash
sudo pip3 install ansible==4.8.0
```

**Explanation:** This command installs Ansible version 4.8.0 using pip3, Python's package manager. The `sudo` prefix ensures the installation happens system-wide in the global Python site-packages directory, making the `ansible` command available to all users on the system. Using pip3 provides precise version control and ensures compatibility with Python 3.x, which is required for modern Ansible versions. The `==4.8.0` syntax locks the installation to this specific version, preventing unexpected behavior from version mismatches.

### Step 2: Verify Ansible Installation

Confirm Ansible is installed correctly and accessible globally.

```bash
ansible --version
```

**Explanation:** This command displays the installed Ansible version, configuration file location, Python version, and module search paths. You should see output indicating Ansible 4.8.0 is installed. This verification step ensures the binary is in the system PATH and accessible to all users, confirming the installation was successful and meets the requirement for global availability.

---

## Understanding Ansible

### Ansible Fundamentals

**What is Ansible?**
Ansible is an open-source automation platform that simplifies IT infrastructure management, application deployment, and configuration management. Unlike other configuration management tools, Ansible is agentless, meaning it doesn't require any software installation on managed nodes.

**Core Characteristics:**
- **Agentless Architecture**: No agent software required on managed nodes, reducing maintenance overhead and potential security vulnerabilities
- **SSH-Based Communication**: Uses standard SSH for connectivity, leveraging existing security infrastructure
- **YAML Syntax**: Playbooks written in human-readable YAML format, making them easy to understand and version control
- **Idempotent Operations**: Safe to run multiple times, producing the same result without unintended side effects

### Ansible Components

**Control Node (Ansible Controller):**
The machine where Ansible is installed and from which you run commands and playbooks. In this task, the jump host serves as the control node. Requirements include Python 3.6+ and the Ansible package.

**Managed Nodes (Target Servers):**
The servers, network devices, or cloud resources that Ansible manages. These only require Python 2.7 or Python 3.5+ and SSH access. No Ansible installation needed on managed nodes.

**Inventory:**
A file or dynamic source listing managed nodes, organized into groups for targeted operations. Can be static (INI/YAML files) or dynamic (scripts querying cloud providers, CMDBs).

**Playbooks:**
YAML files defining automation workflows as a series of plays and tasks. Each play targets specific hosts and executes ordered tasks using Ansible modules.

**Modules:**
Reusable units of work that Ansible executes on managed nodes. Examples include `copy` (file operations), `service` (service management), `user` (user management), `yum/apt` (package management), and hundreds more built-in modules.

### Installation Methods

**pip/pip3 (Python Package Manager):**
Provides the latest versions and precise version control. Best for environments where you need specific versions or don't have OS packages available. Installs Ansible core and required dependencies from PyPI.

**Operating System Package Managers:**
- `yum install ansible` (RHEL/CentOS)
- `apt install ansible` (Ubuntu/Debian)
- `dnf install ansible` (Fedora)

OS packages are convenient but may lag behind the latest releases. They integrate with system package management for easier updates.

**Source Installation:**
Clone from GitHub for development versions or contributing to Ansible. Requires additional setup steps and dependency management. Generally used only for testing unreleased features.

**Virtual Environment:**
Create isolated Python environments with `python3 -m venv` to test different Ansible versions without affecting the system installation. Useful for development and testing scenarios.

### Version Considerations

**Version Compatibility:**
Different Ansible versions support different features and module parameters. Always check module documentation for your specific version. Ansible 4.x uses the collections-based architecture introduced in Ansible 2.10.

**Collections Model:**
Ansible 2.10+ separates content into collections, packaged units containing modules, plugins, and roles. This allows independent versioning and faster updates for specific technology integrations.

**Python Requirements:**
Ansible control nodes require Python 3.6 or newer. Managed nodes need Python 2.7 or Python 3.5+. Always verify Python availability on target systems before running playbooks.

**Dependencies:**
Ansible requires specific Python packages (PyYAML, Jinja2, cryptography) which pip automatically installs. Some modules require additional packages on control nodes or managed nodes.

---

## Key Concepts

### Why Use Ansible?

**Simplicity:** Ansible uses YAML for playbooks, which is human-readable and doesn't require programming expertise. The learning curve is gentle compared to other automation tools.

**Agentless:** No need to install and maintain agent software on hundreds or thousands of servers, reducing complexity, attack surface, and operational overhead.

**Powerful:** Despite its simplicity, Ansible can manage complex workflows, orchestrate multi-tier applications, and integrate with cloud providers, network devices, and containers.

**Efficient:** SSH multiplexing and parallel execution allow Ansible to manage large infrastructures efficiently. Connection caching reduces overhead for multiple tasks.

### Common Use Cases

**Configuration Management:** Ensure servers maintain desired state configurations, automatically correcting drift from defined standards.

**Application Deployment:** Automate application deployment workflows including code updates, dependency installation, service restarts, and smoke tests.

**Orchestration:** Coordinate complex multi-step processes across multiple systems in the correct order with error handling and rollback capabilities.

**Provisioning:** Automate infrastructure provisioning on cloud platforms (AWS, Azure, GCP), virtualization platforms, or bare metal servers.

---

## Validation

Test your solution using KodeKloud's automated validation system. The validation checks:
- Ansible 4.8.0 is installed
- Ansible binary is accessible in system PATH
- All users can execute ansible commands

---

[← Day 7](../week-01/day-07.md) | [Day 9 →](day-09.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
