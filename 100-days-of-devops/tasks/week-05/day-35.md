# Day 35: Setup Docker Installation

## Task Overview

Install Docker Engine (docker-ce) and Docker Compose on a Linux server to enable containerization capabilities. Docker provides a platform for packaging, distributing, and running applications in isolated containers.

**Technical Specifications:**
- Target server: App Server 2
- OS: CentOS Stream 9 (RHEL-based distribution)
- Package: docker-ce (Docker Community Edition)
- Additional package: docker-compose-plugin
- Service management: Enable and start Docker daemon
- Installation method: Convenience script (automated installation)

**Scenario:**
The DevOps team is adopting containerization to improve application deployment consistency and portability. The first step is installing Docker on the application servers. App Server 2 will serve as the initial containerization platform, where the team will test Docker-based application deployments before rolling out to other servers. This installation provides the foundation for running containerized applications.

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Connect to App Server 2

```sh
ssh steve@stapp02
# Use the provided password when prompted
```

Establish an SSH connection to App Server 2 using the user steve. SSH (Secure Shell) provides encrypted remote access to the Linux server, allowing you to execute commands and install software. The hostname stapp02 identifies App Server 2 in the infrastructure. Once connected, you'll have a command-line interface where you can perform system administration tasks with appropriate permissions.

**Step 2:** Identify the operating system and version

```sh
cat /etc/os-release
```

Display the operating system identification information to determine the Linux distribution and version. This file contains key-value pairs describing the OS, including the distribution name (CentOS Stream), version (9), and ID (centos). Knowing the OS is crucial because Docker installation methods vary between distributions (CentOS/RHEL, Ubuntu/Debian, etc.). The output shows CentOS Stream 9, which is RHEL-compatible and requires the CentOS installation procedure.

Expected output:
```
NAME="CentOS Stream"
VERSION="9"
ID="centos"
ID_LIKE="rhel fedora"
VERSION_ID="9"
PLATFORM_ID="platform:el9"
PRETTY_NAME="CentOS Stream 9"
ANSI_COLOR="0;31"
LOGO="fedora-logo-icon"
CPE_NAME="cpe:/o:centos:centos:9"
HOME_URL="https://centos.org/"
BUG_REPORT_URL="https://issues.redhat.com/"
REDHAT_SUPPORT_PRODUCT="Red Hat Enterprise Linux 9"
REDHAT_SUPPORT_PRODUCT_VERSION="CentOS Stream"
```

**Step 3:** Verify kernel version (optional)

```sh
uname -a
```

Display detailed system information including the kernel version, architecture, and hostname. The kernel version is important because Docker has minimum kernel requirements (typically 3.10+ for CentOS). The output shows the Linux kernel version, machine architecture (x86_64), and other system details. This verification ensures the system meets Docker's prerequisites.

**Step 4:** Download Docker installation script

```sh
curl -fsSL https://get.docker.com -o get-docker.sh
```

Download Docker's official convenience installation script from get.docker.com and save it as get-docker.sh. The `curl` command retrieves content from URLs, with flags: `-f` (fail silently on errors), `-s` (silent mode, no progress bar), `-S` (show errors even in silent mode), and `-L` (follow redirects). This script automates the Docker installation process by detecting your OS and configuring the appropriate Docker repository. The convenience script is the quickest installation method, though production environments often prefer manual repository setup for better control.

**Step 5:** Review the installation script (optional but recommended)

```sh
less get-docker.sh
# or
cat get-docker.sh | head -50
```

Examine the contents of the installation script before executing it. This security best practice allows you to verify what the script will do on your system. The script detects your Linux distribution, adds Docker's package repository, installs Docker Engine and related packages, and configures the service. Reading scripts from the internet before execution prevents malicious code execution. Press 'q' to exit less after reviewing.

**Step 6:** Execute the Docker installation script with sudo

```sh
sudo sh get-docker.sh
```

Run the installation script with root privileges using sudo. The script automatically performs several actions: detects CentOS Stream 9, adds Docker's official repository to the system, installs docker-ce (Docker Engine), docker-ce-cli (command-line interface), containerd.io (container runtime), and docker-compose-plugin. The installation process downloads packages, resolves dependencies, and configures Docker on the system. The script output shows progress and any warnings or errors.

**Step 7:** Verify Docker installation

```sh
docker --version
# or
docker version
```

Check that Docker was successfully installed by displaying its version information. The `--version` flag shows a brief version string, while `version` (without dashes) displays detailed version information for both the Docker client and server (daemon). Successful output confirms the installation completed and Docker is ready for use. You should see version numbers for Docker Engine, typically 20.10+ or newer.

**Step 8:** Enable Docker service to start on boot

```sh
sudo systemctl enable docker.service
```

Configure the Docker daemon (dockerd) to start automatically when the system boots. The `systemctl enable` command creates a symbolic link in the system's boot configuration, ensuring Docker runs after every reboot. This is essential for production servers where containers should automatically restart after maintenance reboots or unexpected restarts. The command creates the necessary systemd links without starting the service immediately.

**Step 9:** Start the Docker service

```sh
sudo systemctl start docker.service
```

Immediately start the Docker daemon service without waiting for a reboot. The `systemctl start` command launches the Docker daemon process, which listens for Docker API requests and manages containers, images, networks, and volumes. Starting the service makes Docker operational and ready to run containers. The daemon runs in the background as a system service.

**Step 10:** Verify Docker service status

```sh
sudo systemctl status docker.service
```

Check the current status of the Docker daemon to confirm it's running properly. The status output shows whether the service is active (running), the process ID, memory usage, recent log entries, and any errors. Look for "active (running)" in green text to confirm successful operation. This verification ensures Docker is not just installed but actually operational and ready to manage containers.

**Step 11:** Test Docker functionality with hello-world container

```sh
sudo docker run hello-world
```

Run a simple test container to verify Docker can pull images and execute containers. The hello-world image is a minimal container that prints a welcome message and exits. Docker will: (1) check for the image locally, (2) pull it from Docker Hub if not found, (3) create a container from the image, (4) run the container, and (5) display the output. Successful execution confirms Docker is fully functional and can communicate with Docker Hub.

**Step 12:** Verify Docker Compose installation

```sh
docker compose version
```

Check that Docker Compose (the plugin version) was installed alongside Docker. Modern Docker installations include Compose as a plugin rather than a standalone binary. The command displays the Compose version, confirming it's available for orchestrating multi-container applications. Docker Compose allows you to define and manage multi-container applications using YAML configuration files.

**Step 13:** Optional - Add user to docker group (for non-root access)

```sh
sudo usermod -aG docker steve
# Then logout and login again for group membership to take effect
```

Add the user steve to the docker group, allowing Docker commands without sudo. By default, Docker requires root privileges because it interacts with the system daemon. Adding users to the docker group grants them Docker socket access. Note that this provides root-equivalent privileges, so only grant to trusted users. After adding, the user must logout and login for group membership to take effect.

**Step 14:** Verify Docker info and configuration

```sh
sudo docker info
```

Display comprehensive information about the Docker installation including the number of containers, images, storage driver, kernel version, operating system, Docker root directory, and runtime configuration. This command provides a complete overview of Docker's operational state and configuration. Use this to verify storage drivers, confirm plugins are loaded, and troubleshoot configuration issues.

---

## Key Concepts

**Docker Architecture:**
- **Docker Engine**: Core runtime that builds and runs containers
- **Docker Daemon (dockerd)**: Background service that manages containers, images, networks, and volumes
- **Docker CLI**: Command-line interface for interacting with Docker daemon
- **containerd**: High-level container runtime that manages container lifecycle
- **Docker Registry**: Storage and distribution system for Docker images (Docker Hub is the public registry)

**Docker Components:**
- **Images**: Read-only templates containing application code, runtime, libraries, and dependencies. Built from Dockerfile instructions.
- **Containers**: Running instances of images. Isolated, portable, and lightweight execution environments.
- **Volumes**: Persistent data storage that survives container restarts and removals
- **Networks**: Virtual networks that enable container-to-container and container-to-host communication
- **Dockerfile**: Text file with instructions for building Docker images

**Installation Methods:**

**1. Convenience Script (used in this task):**
```sh
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```
- **Pros**: Quick, automatic OS detection, one-command installation
- **Cons**: Less control over versions, requires internet access, not recommended for production
- **Use Case**: Testing, development, quick demos

**2. Repository Method (recommended for production):**
```sh
# Add Docker repository
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# Install Docker
sudo yum install docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Start and enable
sudo systemctl start docker
sudo systemctl enable docker
```
- **Pros**: Version control, official repositories, better security, repeatable
- **Cons**: More steps, OS-specific commands
- **Use Case**: Production servers, controlled environments

**3. Package Method:**
Download and manually install .rpm (RHEL/CentOS) or .deb (Debian/Ubuntu) packages
- **Pros**: Works without internet on target server
- **Cons**: Manual dependency resolution, harder to update
- **Use Case**: Air-gapped systems, restricted environments

**Docker Editions:**
- **Docker CE (Community Edition)**: Free, open-source version for developers and small teams
- **Docker EE (Enterprise Edition)**: Paid version with support, certifications, and enterprise features (discontinued, replaced by Mirantis Docker Enterprise)
- **Docker Desktop**: GUI application for macOS and Windows with Docker Engine included

**Systemd Service Management:**
- **enable**: Configure service to start at boot (`systemctl enable docker`)
- **disable**: Prevent service from starting at boot (`systemctl disable docker`)
- **start**: Start service immediately (`systemctl start docker`)
- **stop**: Stop running service (`systemctl stop docker`)
- **restart**: Stop and start service (`systemctl restart docker`)
- **status**: Show current service state (`systemctl status docker`)
- **is-active**: Check if service is running (`systemctl is-active docker`)

**Docker Daemon Configuration:**
Configuration file: `/etc/docker/daemon.json`

Example configuration:
```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "storage-driver": "overlay2",
  "insecure-registries": ["myregistry.local:5000"]
}
```

After modifying daemon.json, restart Docker:
```sh
sudo systemctl restart docker
```

**Docker Storage Drivers:**
- **overlay2**: Recommended for most Linux distributions, efficient and fast
- **devicemapper**: Older driver, used on some CentOS/RHEL systems
- **btrfs/zfs**: For specific filesystems
- **vfs**: Slowest, no copy-on-write, useful for testing
- Check your driver: `docker info | grep "Storage Driver"`

**Docker Compose:**
- **Purpose**: Define and run multi-container applications
- **Configuration**: YAML file (docker-compose.yml) defining services, networks, volumes
- **Plugin vs Standalone**: Modern Docker includes Compose as a plugin (`docker compose`), older versions use standalone binary (`docker-compose`)
- **Commands**: `up`, `down`, `ps`, `logs`, `build`, `exec`

Example docker-compose.yml:
```yaml
version: '3.8'
services:
  web:
    image: nginx:latest
    ports:
      - "80:80"
  database:
    image: postgres:14
    environment:
      POSTGRES_PASSWORD: secret
    volumes:
      - db-data:/var/lib/postgresql/data
volumes:
  db-data:
```

**Docker Security Considerations:**
- **Root Privileges**: Docker daemon runs as root; container escape could compromise host
- **Docker Group**: Adding users to docker group grants root-equivalent access
- **Image Trust**: Only use images from trusted sources; verify image signatures
- **Network Isolation**: Use Docker networks to isolate containers
- **Resource Limits**: Set CPU and memory limits to prevent resource exhaustion
- **Secrets Management**: Use Docker secrets or external secret management (not environment variables)

**Common Docker Commands:**
```sh
# Image management
docker images                    # List images
docker pull nginx:latest         # Download image
docker build -t myapp:1.0 .     # Build image from Dockerfile
docker rmi image_id             # Remove image

# Container management
docker ps                        # List running containers
docker ps -a                     # List all containers
docker run -d -p 80:80 nginx    # Run container detached
docker stop container_id         # Stop container
docker rm container_id           # Remove container
docker logs container_id         # View logs
docker exec -it container_id bash # Execute command in container

# System management
docker system df                 # Show disk usage
docker system prune             # Remove unused data
docker info                     # Display system information
docker version                  # Show version information
```

**Docker Networking:**
- **Bridge**: Default network, containers on same host communicate
- **Host**: Container uses host's network stack (no isolation)
- **None**: No networking
- **Custom**: User-defined networks for better isolation and DNS

**Docker Volumes:**
- **Named Volumes**: Managed by Docker, persistent (`docker volume create mydata`)
- **Bind Mounts**: Mount host directory into container (`-v /host/path:/container/path`)
- **tmpfs Mounts**: Stored in memory only, not persisted

**Troubleshooting Docker:**
```sh
# Check daemon status
sudo systemctl status docker

# View daemon logs
sudo journalctl -u docker

# Check for port conflicts
sudo netstat -tulpn | grep docker

# Restart Docker daemon
sudo systemctl restart docker

# View all Docker events
docker events

# Inspect container details
docker inspect container_id
```

---

## Validation

Test your solution using KodeKloud's automated validation.

**Verification Checklist:**
1. Docker CE successfully installed on App Server 2
2. Docker version command shows version 20.10 or newer
3. Docker service enabled (will start on boot)
4. Docker service currently running
5. Docker Compose plugin installed and functional
6. hello-world container runs successfully
7. docker info command executes without errors

---

[← Day 34](day-34.md) | [Day 36 →](../week-06/day-36.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
