# Day 43: Docker Port Mapping

## Task Overview

Configure port mapping for Docker containers to expose containerized services to the host network. Port mapping allows external clients to access applications running inside containers by routing traffic from host ports to container ports.

**Technical Specifications:**
- Container image: nginx:stable (web server)
- Container name: cluster
- Port mapping: Host port 5002 to container port 80
- Container state: running (detached mode)

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Connect to the application server

```sh
ssh user@app-server-2
```

Establish an SSH connection to Application Server 2 in the Stratos Datacenter. Replace 'user' with your actual username provided in the lab environment. This server will host the nginx container with port mapping configuration.

**Step 2:** Pull the nginx stable image from Docker Hub

```sh
docker pull nginx:stable
```

Download the nginx:stable image from Docker Hub's official repository to your local Docker image cache. The 'stable' tag ensures you get a production-ready version of nginx that has been thoroughly tested. This image contains a pre-configured nginx web server that listens on port 80 by default. The pull operation downloads all image layers and stores them locally, making subsequent container launches faster.

**Step 3:** Create and start the container with port mapping

```sh
docker run -d --name cluster -p 5002:80 nginx:stable
```

Launch a new container named 'cluster' from the nginx:stable image with port mapping configured. The `-d` flag runs the container in detached mode (background), allowing the terminal to remain available for other commands. The `--name cluster` flag assigns a human-readable name for easier container management. The critical `-p 5002:80` flag creates a port mapping that forwards all traffic from host port 5002 to container port 80, where nginx listens for HTTP requests. This mapping enables external clients to access the nginx web server by connecting to the host's IP address on port 5002.

**Step 4:** Verify the container is running

```sh
docker ps
```

Display a list of all currently running containers to confirm that the 'cluster' container was successfully created and is in the running state. The output shows container ID, image name, command, creation time, status, port mappings (0.0.0.0:5002->80/tcp), and container name. The port mapping column confirms that traffic to any host interface on port 5002 will be forwarded to the container's port 80.

**Step 5:** Test the nginx web server accessibility

```bash
# Test from the host machine
curl http://localhost:5002

# Test from another machine (if accessible)
curl http://<server-ip>:5002

# Verify port is listening on the host
sudo netstat -tlnp | grep 5002

# Check detailed container port mappings
docker port cluster
```

These verification commands test that the nginx web server is accessible through the port mapping. The `curl` command should return the default nginx welcome page HTML. The `netstat` command confirms that the Docker daemon is listening on host port 5002. The `docker port` command displays all port mappings for the cluster container, showing the relationship between host and container ports.

---

## Key Concepts

**Port Mapping Fundamentals:**
- Host Port: External port on the Docker host machine (5002)
- Container Port: Internal port where the application listens (80)
- Binding: Maps traffic from host port to container port
- Protocol: Defaults to TCP, can specify UDP with /udp suffix

**Port Mapping Syntax:**
- `-p 5002:80`: Bind host port 5002 to container port 80
- `-p 127.0.0.1:5002:80`: Bind only to localhost interface
- `-p 5002:80/tcp`: Explicitly specify TCP protocol
- `-P`: Automatically map all exposed ports to random host ports

**Network Access Patterns:**
- 0.0.0.0:5002 means the port is accessible from any network interface
- Containers can have multiple port mappings (e.g., -p 80:80 -p 443:443)
- Conflicting host ports will cause container creation to fail
- Port mappings cannot be changed on running containers

**Security Considerations:**
- Only map ports that need external access
- Use firewall rules to restrict access to mapped ports
- Bind to specific interfaces (127.0.0.1) for localhost-only access
- Consider using reverse proxies for production deployments

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 42](../week-06/day-42.md) | [Day 44 →](day-44.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
