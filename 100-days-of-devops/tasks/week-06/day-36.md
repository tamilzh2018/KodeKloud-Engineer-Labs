# Day 36: Run a NGINX Container on Docker

## Task Overview

Deploy and run an NGINX web server as a Docker container using the lightweight Alpine Linux base image. This task introduces fundamental Docker container operations and demonstrates how to quickly deploy production-ready applications without manual server configuration.

**Technical Specifications:**
- Container name: nginx_1
- Base image: nginx:alpine
- Container state: running (detached mode)
- Port mapping: host port 80 to container port 80

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Run NGINX container in detached mode

```sh
sudo docker run -d --name nginx_1 -p 80:80 nginx:alpine
```

Launch an NGINX web server container using the `docker run` command. The `-d` flag runs the container in detached mode (background), allowing it to operate independently without blocking your terminal. The `--name nginx_1` flag assigns a custom name "nginx_1" to the container for easy identification and management. The `-p 80:80` flag maps port 80 on the host machine to port 80 inside the container, enabling external access to the web server. The `nginx:alpine` argument specifies the image to use - NGINX web server built on Alpine Linux, a minimal distribution (~5MB) that provides security benefits through a reduced attack surface and faster startup times compared to full-sized distributions.

**Step 2:** Verify container is running

```sh
sudo docker ps
```

Display all currently running containers on your system using the `docker ps` command. This command shows essential container information in a table format including Container ID (unique identifier), Image (base image used), Command (entry point command), Created (age), Status (uptime and health), Ports (port mappings), and Names (container name). Look for your "nginx_1" container in the output - it should show Status as "Up" indicating the container is running successfully. If the container is not visible, it may have stopped due to an error; use `docker ps -a` to see all containers including stopped ones.

**Step 3:** Test NGINX web server accessibility

```sh
curl http://localhost:80
# or
curl http://localhost
```

Test the NGINX web server by sending an HTTP request to the mapped port using the `curl` command. This verifies that the container is not only running but also properly serving web content. You should receive the default NGINX welcome page HTML in response, which begins with "<!DOCTYPE html>" and includes "Welcome to nginx!" in the title. This confirms that port mapping is working correctly and the NGINX service inside the container is accessible from the host machine. If the connection fails, check that the container is running with `docker ps` and verify no other service is using port 80.

**Step 4:** Additional container management commands

```bash
# View container logs
sudo docker logs nginx_1

# Access container shell
sudo docker exec -it nginx_1 /bin/sh

# Stop the container
sudo docker stop nginx_1

# Start stopped container
sudo docker start nginx_1

# Remove container (must be stopped first)
sudo docker rm nginx_1

# Force remove running container
sudo docker rm -f nginx_1
```

These commands provide comprehensive container lifecycle management. `docker logs nginx_1` displays the container's output and access logs, useful for debugging and monitoring. `docker exec -it nginx_1 /bin/sh` opens an interactive shell inside the running container (Alpine uses /bin/sh instead of /bin/bash), allowing you to inspect files, check processes, or troubleshoot issues. `docker stop nginx_1` gracefully stops the container by sending SIGTERM followed by SIGKILL if needed. `docker start nginx_1` restarts a stopped container, preserving its configuration. `docker rm nginx_1` permanently deletes the container (but not the image), requiring the container to be stopped first. `docker rm -f nginx_1` forcefully removes even a running container, combining stop and remove operations.

---

## Key Concepts

**Container vs Image:**
- **Image**: Read-only template containing the application and its dependencies
- **Container**: Running instance of an image with its own filesystem and processes
- **Relationship**: One image can spawn multiple containers
- **Stateless**: Containers can be destroyed and recreated without affecting the image

**Docker Run Flags:**
- `-d, --detach`: Run container in background and print container ID
- `--name`: Assign custom name for easier reference (vs random generated names)
- `-p, --publish`: Publish container port to host (format: host_port:container_port)
- `-v, --volume`: Mount host directory or volume into container
- `-e, --env`: Set environment variables
- `--rm`: Automatically remove container when it stops
- `-it`: Interactive mode with TTY allocation (for shell access)

**NGINX Alpine Benefits:**
- **Small Size**: Alpine-based image is ~23MB vs standard NGINX ~133MB
- **Security**: Minimal packages mean fewer vulnerabilities and smaller attack surface
- **Performance**: Faster pulls, starts, and uses less memory
- **Production Ready**: Used widely in production environments despite minimal size

**Container States:**
- **Created**: Container created but not started
- **Running**: Container is executing and active
- **Paused**: Container processes are paused (suspended)
- **Stopped/Exited**: Container has stopped running
- **Dead**: Container that failed to stop properly

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 35](../week-05/day-35.md) | [Day 37 →](day-37.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
