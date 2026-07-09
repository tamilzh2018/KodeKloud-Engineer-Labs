# Day 47: Dockerize a Python Application

## Task Overview

Create a custom Docker image for a Python web application using a Dockerfile. This task demonstrates building containerized Python applications with proper dependency management, port configuration, and application deployment.

**Technical Specifications:**
- Application directory: /python_app
- Dockerfile location: /python_app/Dockerfile
- Source files: /python_app/src/ (requirements.txt, server.py)
- Base image: Python (preferably slim variant)
- Application port: 6300 (exposed in container)
- Container name: pythonapp_nautilus
- Image name: nautilus/python-app
- Port mapping: Host port 8096 to container port 6300

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Connect to the application server

```sh
ssh user@app-server-3
```

Establish an SSH connection to Application Server 3 in the Stratos Datacenter. This server contains the Python application source code that needs to be containerized.

**Step 2:** Switch to root user and navigate to application directory

```sh
sudo -i
cd /python_app
```

Elevate privileges to root user using `sudo -i` for easier file system operations without repeated sudo commands. Then change to the /python_app directory where the Dockerfile will be created. This directory already contains a src/ subdirectory with the application code (server.py) and dependencies file (requirements.txt).

**Step 3:** Examine the existing application structure

```sh
ls -la
ls -la src/
cat src/requirements.txt
```

List the directory contents to understand the application structure. The src/ directory contains the Python application files. The requirements.txt file lists all Python package dependencies needed for the application. Understanding the application structure helps in writing an appropriate Dockerfile.

**Step 4:** Create the Dockerfile

```sh
vi Dockerfile
```

Open a new file named Dockerfile in the vi editor. Add the following content:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY ./src/* /app/

RUN pip install -r requirements.txt

EXPOSE 6300

CMD ["python", "server.py"]
```

This Dockerfile builds a containerized Python application following best practices:

- `FROM python:3.9-slim`: Uses the official Python 3.9 slim image as the base. The 'slim' variant is preferred because it excludes unnecessary packages, resulting in smaller image sizes while maintaining full Python functionality. This balances functionality with image size optimization.

- `WORKDIR /app`: Sets the working directory inside the container to /app. All subsequent commands execute in this directory, and it becomes the default directory when the container starts.

- `COPY ./src/* /app/`: Copies all files from the src/ directory in the build context to the /app directory in the container. This includes server.py and requirements.txt. The COPY instruction is more efficient than RUN cp because it properly handles build context files and supports layer caching.

- `RUN pip install -r requirements.txt`: Executes pip to install all Python dependencies listed in requirements.txt. This creates a layer in the image with all required packages, ensuring the application has everything it needs to run.

- `EXPOSE 6300`: Documents that the application listens on port 6300. While this doesn't actually publish the port, it serves as documentation for users and integrates with Docker's networking features. The actual port mapping happens at runtime with the -p flag.

- `CMD ["python", "server.py"]`: Defines the default command to execute when the container starts. This runs the Python interpreter with server.py as the script, launching the web application. The exec form (JSON array) is preferred because it doesn't invoke a shell, resulting in cleaner process management.

Save and exit vi by pressing ESC, then typing `:wq` and pressing ENTER.

**Step 5:** Build the Docker image

```sh
docker build -t nautilus/python-app .
```

Execute the docker build command to create an image from the Dockerfile. The `-t nautilus/python-app` flag tags the image with the specified name, making it easy to reference later. The `.` argument specifies the build context as the current directory (/python_app). Docker will:
1. Read the Dockerfile instructions
2. Pull the python:3.9-slim base image if not cached
3. Execute each instruction in sequence, creating layers
4. Copy application files from the src/ directory
5. Install Python dependencies
6. Tag the final image as nautilus/python-app

The build output shows each step's execution and layer creation. Successful completion results in a tagged image ready for deployment.

**Step 6:** Verify the image was created

```sh
docker images | grep nautilus/python-app
```

List Docker images and filter for the newly created image. The output displays the image name (nautilus/python-app), tag (latest by default), image ID, creation timestamp, and size. Confirming the image exists validates the build was successful.

**Step 7:** Run the container with port mapping

```sh
docker run -d --name pythonapp_nautilus -p 8096:6300 nautilus/python-app
```

Launch a container from the nautilus/python-app image with specific configurations:
- `-d`: Runs the container in detached mode (background)
- `--name pythonapp_nautilus`: Assigns the exact container name as required
- `-p 8096:6300`: Maps host port 8096 to container port 6300, making the application accessible externally
- `nautilus/python-app`: Specifies the image to use

The container starts and executes the CMD instruction (python server.py), launching the web application. The port mapping enables access to the application via http://localhost:8096 on the host.

**Step 8:** Verify the container is running

```sh
docker ps
```

List running containers to confirm the Python application container is active. The output shows:
- CONTAINER ID: Unique identifier
- IMAGE: nautilus/python-app
- COMMAND: "python server.py"
- STATUS: Up (with uptime)
- PORTS: 0.0.0.0:8096->6300/tcp
- NAMES: pythonapp_nautilus

The port mapping 0.0.0.0:8096->6300/tcp confirms the application is accessible on host port 8096.

**Step 9:** Test the Python application

```sh
curl http://localhost:8096
```

Send an HTTP request to the Python application running inside the container. The curl command should return a response from the application, confirming that:
1. The container is running
2. The Python application started successfully
3. Port mapping is working correctly
4. The application is responding to HTTP requests

The actual response content depends on what server.py implements (could be HTML, JSON, or plain text).

**Step 10:** Additional verification and management commands

```bash
# View container logs
docker logs pythonapp_nautilus

# View real-time logs
docker logs -f pythonapp_nautilus

# Execute commands inside the container
docker exec -it pythonapp_nautilus bash

# Check application process inside container
docker exec pythonapp_nautilus ps aux

# View resource usage
docker stats pythonapp_nautilus

# Stop the container
docker stop pythonapp_nautilus

# Start the stopped container
docker start pythonapp_nautilus

# Remove the container (must be stopped first)
docker rm pythonapp_nautilus
```

These commands provide comprehensive container management capabilities. The `logs` command displays application output, useful for debugging. The `exec` command allows you to run commands inside the container or access an interactive shell. The `stats` command shows real-time resource consumption (CPU, memory, network). Stop and start commands control the container lifecycle, while rm removes the container entirely.

---

## Key Concepts

**Python Application Containerization:**
- Dependency Isolation: Container provides a clean Python environment
- requirements.txt: Standard Python dependency specification file
- Reproducibility: Same dependencies across development, testing, and production
- Portability: Run anywhere Docker is available without Python installation
- Version Pinning: Specify exact package versions for consistency

**Python Docker Images:**
- Official Images: python:3.9, python:3.10, python:3.11, etc.
- Slim Variants: python:3.9-slim excludes unnecessary system packages
- Alpine Variants: python:3.9-alpine uses minimal Alpine Linux (smallest size)
- Full Images: python:3.9 includes build tools and additional utilities
- Trade-offs: Slim balances size and functionality, Alpine is smallest but may have compatibility issues

**Dockerfile Best Practices:**
- Base Image Selection: Choose appropriate base image for your needs
- WORKDIR: Set working directory for better organization and predictability
- Copy Order: Copy requirements.txt first, then source code for better caching
- Layer Optimization: Combine RUN commands when appropriate to reduce layers
- EXPOSE: Document application ports for clarity
- CMD vs ENTRYPOINT: Use CMD for default commands, ENTRYPOINT for immutable commands
- .dockerignore: Exclude unnecessary files from build context

**Build Context:**
- Definition: Directory and files available during docker build
- Context Transfer: Docker sends entire context to daemon
- Size Impact: Larger contexts slow down builds
- Relative Paths: COPY/ADD use paths relative to context root
- Exclusion: Use .dockerignore to exclude files/directories

**Image Layers:**
- Layer Caching: Docker caches each instruction's result
- Cache Invalidation: Changes invalidate cache for that layer and all subsequent layers
- Order Matters: Place frequently changing instructions last
- Layer Size: Each RUN/COPY/ADD creates a new layer
- Optimization: Minimize layers and layer sizes for smaller images

**Application Deployment:**
- Port Mapping: Container port 6300 mapped to host port 8096
- Detached Mode: Container runs in background as a service
- Logging: Application output captured by Docker logging driver
- Health Checks: Consider adding HEALTHCHECK instruction for monitoring
- Environment Variables: Use ENV or -e flag for configuration
- Data Persistence: Use volumes if application needs persistent storage

**Container Lifecycle:**
- Created: Container exists but not started
- Running: Container is actively executing
- Stopped: Container exists but processes are halted
- Removed: Container is deleted entirely
- Restart Policies: Control automatic restart behavior

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 46](day-46.md) | [Day 48 →](day-48.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
