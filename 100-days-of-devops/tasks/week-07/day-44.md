# Day 44: Creating a Docker Compose File

## Task Overview

Create and deploy a Docker Compose configuration file to orchestrate containerized applications. Docker Compose enables declarative definition of multi-container environments through YAML configuration, simplifying container deployment and management.

**Technical Specifications:**
- Compose file location: /opt/docker/docker-compose.yml
- Service: httpd web server
- Container name: httpd
- Image: httpd:latest
- Port mapping: Host port 3003 to container port 80
- Volume mapping: Host /opt/itadmin to container /usr/local/apache2/htdocs

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Connect to the application server

```sh
ssh user@app-server-3
```

Establish an SSH connection to Application Server 3 in the Stratos Datacenter. This server will host the Docker Compose application stack with the httpd web server container.

**Step 2:** Verify Docker service is running

```sh
docker ps
```

Execute the `docker ps` command to confirm that the Docker daemon is running and accessible. This command displays all currently running containers. An empty list is expected at this stage, but successful execution confirms Docker is properly installed and operational. If this command fails, you may need to start the Docker service with `sudo systemctl start docker` or check Docker installation status.

**Step 3:** Create the docker-compose.yml file

```sh
sudo touch /opt/docker/docker-compose.yml
```

Create an empty Docker Compose configuration file at the exact path specified in the requirements (/opt/docker/docker-compose.yml). The `sudo` command provides elevated privileges necessary to create files in system directories. The `touch` command creates a new empty file. This file will define all services, networks, and volumes for the application stack.

**Step 4:** Edit the compose file with service configuration

```sh
sudo vi /opt/docker/docker-compose.yml
```

Open the newly created file in the vi text editor with sudo privileges. Add the following YAML configuration:

```yaml
services:
  httpd-service:
    image: httpd:latest
    container_name: httpd
    ports:
      - "3003:80"
    volumes:
      - /opt/itadmin:/usr/local/apache2/htdocs
```

This Docker Compose configuration defines a single service named 'httpd-service'. The `image: httpd:latest` directive pulls the latest Apache HTTP Server image from Docker Hub. The `container_name: httpd` ensures the container is named exactly as required. The `ports` section maps host port 3003 to container port 80, allowing external access to the web server. The `volumes` section creates a bind mount that maps the host directory /opt/itadmin (containing static website content) to the container's document root at /usr/local/apache2/htdocs. This enables the httpd server to serve content from the host filesystem. Save and exit vi by pressing ESC, then typing `:wq` and pressing ENTER.

**Step 5:** Start the application stack using Docker Compose

```sh
docker compose -f /opt/docker/docker-compose.yml up -d
```

Launch the multi-container application stack defined in the compose file. The `-f` flag specifies the exact path to the compose file. The `up` command creates and starts all services defined in the configuration. The `-d` flag runs containers in detached mode (background), freeing the terminal for other commands. Docker Compose will pull the httpd:latest image (if not already present), create the container with specified configurations, establish port mappings and volume mounts, and start the httpd service.

**Step 6:** Verify the container is running

```sh
docker ps
```

List all running containers to confirm successful deployment. The output should display a container with the following characteristics:
- CONTAINER ID: A unique 12-character identifier
- IMAGE: httpd:latest
- COMMAND: "httpd-foreground"
- STATUS: Up (with uptime in seconds)
- PORTS: 0.0.0.0:3003->80/tcp
- NAMES: httpd

This confirms the container is running and accessible on host port 3003.

**Step 7:** Test the web server accessibility

```bash
# Test the httpd server
curl http://localhost:3003

# View container logs
docker compose -f /opt/docker/docker-compose.yml logs

# View running services
docker compose -f /opt/docker/docker-compose.yml ps

# Stop the stack (if needed)
docker compose -f /opt/docker/docker-compose.yml down
```

These additional commands help verify and manage the Docker Compose deployment. The `curl` command tests that the web server is responding to HTTP requests. The `logs` command displays output from all services in the stack. The `ps` command shows the status of services defined in the compose file. The `down` command stops and removes all containers, networks, and default resources created by the compose file (useful for cleanup or redeployment).

---

## Key Concepts

**Docker Compose Fundamentals:**
- Declarative Configuration: Define desired state in YAML format
- Multi-Container Orchestration: Manage related containers as a single unit
- Service Abstraction: Define containers as services with specific configurations
- Reproducible Environments: Same configuration works across all systems

**Compose File Structure:**
- services: Define one or more containerized applications
- networks: Configure custom networking (uses default bridge if not specified)
- volumes: Define named volumes for persistent data storage
- version: (Optional in Compose V2) Specifies compose file format version

**Service Configuration Options:**
- image: Container image to use (pulls from registry if not local)
- container_name: Custom name for the container instance
- ports: Port mappings in "HOST:CONTAINER" format
- volumes: Bind mounts or named volumes for data persistence
- environment: Environment variables for container configuration
- depends_on: Define service startup order dependencies

**Docker Compose Commands:**
- `docker compose up -d`: Start all services in detached mode
- `docker compose down`: Stop and remove containers, networks
- `docker compose ps`: List containers for the current project
- `docker compose logs`: View combined logs from all services
- `docker compose restart`: Restart all services
- `docker compose stop`: Stop running services without removing them

**Volume Mounting:**
- Bind Mounts: Map host directory to container directory (used here)
- Named Volumes: Docker-managed volumes for data persistence
- Read-Only Mounts: Append :ro for read-only access
- Mount Propagation: Control how mounts are shared

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 43](day-43.md) | [Day 45 →](day-45.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
