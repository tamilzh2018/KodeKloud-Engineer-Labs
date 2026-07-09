# Day 41: Create a Dockerfile

## Task Overview

Build a custom Docker image using a Dockerfile - a text file containing instructions for automating image creation. Dockerfiles enable reproducible, version-controlled image builds that document every step of the configuration process, making them essential for DevOps workflows and CI/CD pipelines.

**Technical Specifications:**
- Base image: ubuntu:24.04
- Software installation: apache2 web server
- Configuration: Configure Apache to listen on port 5002
- Dockerfile location: /opt/docker/Dockerfile
- Note: Use capital 'D' in Dockerfile name

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Create the directory structure

```sh
sudo mkdir -p /opt/docker
```

Create the necessary directory structure for the Dockerfile using `mkdir -p`. The `-p` flag creates parent directories as needed and doesn't error if the directory already exists. The path `/opt/docker` is a common location for Docker-related files in production systems. The `/opt` directory in Linux is conventionally used for optional or add-on software packages. Creating a dedicated directory helps organize Docker projects, especially when managing multiple Dockerfiles or related configuration files. This directory will contain the Dockerfile and potentially other build context files needed during image creation.

**Step 2:** Navigate to the docker directory

```sh
cd /opt/docker
```

Change your current working directory to `/opt/docker` where you'll create the Dockerfile. The working directory is important because Docker uses the current directory as the "build context" - all files in this directory are available to the `COPY` and `ADD` instructions during the build. Keeping the build context minimal improves build performance by reducing the amount of data sent to the Docker daemon. Working from the correct directory also makes relative paths in commands more intuitive and prevents accidental inclusion of unnecessary files in the build context.

**Step 3:** Create the Dockerfile with Apache configuration

```sh
sudo vim Dockerfile
```

Create and edit the Dockerfile using a text editor. Note that the filename must be exactly "Dockerfile" with a capital 'D' - Docker's build command looks for this specific filename by default. If you use a different name, you'll need to specify it explicitly with the `-f` flag during build. Now add the following content:

```dockerfile
# Use Ubuntu 24.04 as the base image
FROM ubuntu:24.04

# Set environment variable to prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Update package lists and install Apache2
RUN apt-get update && \
    apt-get install -y apache2 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Configure Apache to listen on port 5002
RUN sed -i 's/Listen 80/Listen 5002/g' /etc/apache2/ports.conf && \
    sed -i 's/:80/:5002/g' /etc/apache2/sites-available/000-default.conf

# Expose port 5002 to allow external connections
EXPOSE 5002

# Start Apache in the foreground
CMD ["apache2ctl", "-D", "FOREGROUND"]
```

Save and exit the editor (in Vim: press ESC, type `:wq`, press Enter).

**Step 4:** Verify Dockerfile syntax and content

```sh
cat Dockerfile
```

Display the Dockerfile contents to verify it was created correctly. This verification step helps catch syntax errors, typos, or missing instructions before attempting to build. Review each line to ensure: the FROM instruction specifies the correct base image, RUN commands are properly formatted with line continuations, port numbers match requirements (5002), and the CMD instruction will start Apache correctly. Pay special attention to quoting, escaping, and shell syntax within RUN instructions. A malformed Dockerfile will fail during build, potentially after downloading large base images, so verification saves time.

**Step 5:** Build the Docker image

```sh
sudo docker build -t custom-apache:5002 .
```

Build the Docker image from the Dockerfile using `docker build`. The `-t custom-apache:5002` flag tags the resulting image with a name (custom-apache) and tag (5002 - indicating the port configuration). The dot (`.`) at the end specifies the build context - the current directory where Docker finds the Dockerfile and any files to copy. During the build, Docker executes each instruction sequentially, creating intermediate layers and caching them for faster subsequent builds. You'll see output showing each step: pulling the base image if needed, running commands, and creating layers. The process concludes with "Successfully built" followed by an image ID and "Successfully tagged custom-apache:5002".

**Step 6:** Verify the image was created

```sh
sudo docker images | grep custom-apache
```

Confirm the image was built successfully by listing local images and filtering for your custom image. The output shows the repository name (custom-apache), tag (5002), unique image ID, creation timestamp, and total size. The image size will be larger than the base Ubuntu image due to Apache installation. The creation time should be very recent, confirming this is the image you just built. If you don't see the image, the build may have failed - scroll back through the build output to identify errors.

**Step 7:** Test the image by running a container

```sh
sudo docker run -d --name apache-test -p 5002:5002 custom-apache:5002
```

Create and run a container from your custom image to verify it works correctly. The `-d` flag runs the container in detached mode (background), `--name apache-test` assigns a recognizable name, `-p 5002:5002` maps port 5002 on the host to port 5002 in the container (making Apache accessible externally), and `custom-apache:5002` specifies the image to use. Docker creates a container, starts it, and returns the container ID. The container runs Apache in the foreground (as specified by the CMD instruction), keeping the container alive as long as Apache is running.

**Step 8:** Verify Apache is running and accessible

```sh
curl http://localhost:5002
```

Test that Apache is serving content on the configured port by sending an HTTP request. If successful, you'll receive the default Apache welcome page HTML, confirming that: the Dockerfile built correctly, Apache installed properly, port configuration was successful (listening on 5002), and the container networking is working. If you receive "Connection refused," the container may not be running - check with `docker ps`. If you see "Empty reply from server," Apache might be running but not configured correctly - examine logs with `docker logs apache-test`.

**Step 9:** Additional Dockerfile management commands

```bash
# View container logs
sudo docker logs apache-test

# Inspect image details
sudo docker inspect custom-apache:5002

# View image build history
sudo docker history custom-apache:5002

# Stop and remove test container
sudo docker stop apache-test
sudo docker rm apache-test

# Remove the image
sudo docker rmi custom-apache:5002

# Build with no cache (force rebuild all layers)
sudo docker build --no-cache -t custom-apache:5002 .

# Build and see detailed output
sudo docker build --progress=plain -t custom-apache:5002 .
```

These commands help manage and troubleshoot Dockerfile-based images. `docker logs` shows Apache's output, useful for debugging. `docker inspect` provides detailed JSON metadata about the image including layers, environment variables, exposed ports, and default command. `docker history` displays each layer's creation command and size, helping identify which instructions contribute most to image size. The cleanup commands stop, remove containers, and delete images when testing is complete. `--no-cache` forces a complete rebuild, useful when package repositories have updates or when debugging layer caching issues. `--progress=plain` shows detailed build output instead of the compressed view.

---

## Key Concepts

**Dockerfile Fundamentals:**
- **Declarative Syntax**: Instructions define the desired state, Docker handles execution
- **Layer-Based**: Each instruction creates a new read-only layer
- **Build Context**: Directory containing Dockerfile and files to copy
- **Caching**: Docker caches layers to speed up subsequent builds
- **Immutability**: Images are immutable; changes require rebuilding

**Essential Dockerfile Instructions:**
- **FROM**: Specifies base image (must be first instruction)
- **RUN**: Executes commands during build (installs packages, modifies files)
- **COPY**: Copies files from build context to image
- **ADD**: Like COPY but supports URLs and auto-extracts archives
- **ENV**: Sets environment variables
- **EXPOSE**: Documents which ports the container listens on
- **CMD**: Default command to run when container starts
- **ENTRYPOINT**: Configures container to run as executable
- **WORKDIR**: Sets working directory for subsequent instructions

**FROM Instruction:**
- **Base Image**: Starting point for your image
- **Official Images**: Use verified images from Docker Hub (ubuntu, nginx, python)
- **Version Tags**: Always specify version tags (ubuntu:24.04) not 'latest'
- **Scratch**: Special minimal base image with nothing in it
- **Multi-stage Builds**: Use multiple FROM statements for smaller final images

**RUN Instruction Best Practices:**
- **Combine Commands**: Use && to chain commands in single RUN (reduces layers)
- **Clean Up**: Remove caches and temporary files in same RUN statement
- **Line Continuation**: Use backslash (\) for readable multi-line commands
- **Package Installation**: Update and install in same RUN, clean in same layer
- **Order Optimization**: Place frequently changing RUN commands later

**Environment Variables:**
- **DEBIAN_FRONTEND=noninteractive**: Prevents interactive package installation prompts
- **Build vs Runtime**: ENV sets variables at build time and runtime
- **Security**: Don't hardcode secrets in ENV (use Docker secrets instead)
- **Overriding**: Can be overridden at runtime with docker run -e

**Port Configuration:**
- **EXPOSE**: Documents ports (doesn't actually publish them)
- **Port Mapping**: Use -p flag at runtime to map host to container ports
- **Multiple Ports**: Can expose multiple ports (EXPOSE 80 443 8080)
- **Protocol**: Can specify protocol (EXPOSE 53/udp)

**CMD vs ENTRYPOINT:**
- **CMD**: Default command, easily overridden by docker run arguments
- **ENTRYPOINT**: Main command, arguments append rather than override
- **Exec Form**: ["executable", "param1"] - preferred, no shell processing
- **Shell Form**: executable param1 - runs in shell, allows variable expansion
- **Together**: ENTRYPOINT for executable, CMD for default parameters

**Layer Optimization:**
```dockerfile
# Bad - Creates 3 layers, leaves caches
RUN apt-get update
RUN apt-get install -y apache2
RUN apt-get clean

# Good - Single layer, cleaned
RUN apt-get update && \
    apt-get install -y apache2 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

**Build Context Optimization:**
- **.dockerignore**: Exclude files from build context (like .gitignore)
- **Minimal Context**: Only include necessary files
- **Subdirectories**: Place Dockerfiles in subdirs with relevant files
- **Performance**: Smaller context = faster builds and less memory

**Apache in Containers:**
- **Foreground Mode**: Use "-D FOREGROUND" to keep Apache running
- **Signal Handling**: Foreground mode allows proper signal handling
- **Logging**: Configure Apache to log to stdout/stderr
- **Process ID**: Apache should run as PID 1 or use init system

**Best Practices:**
- **Specific Versions**: Use specific version tags for reproducibility
- **Minimize Layers**: Combine related operations in single RUN
- **Order Matters**: Put frequently changing instructions last for cache efficiency
- **Security**: Run as non-root user when possible (USER instruction)
- **Documentation**: Add LABEL instructions for metadata
- **Health Checks**: Add HEALTHCHECK instruction for container monitoring
- **Clean Up**: Remove unnecessary files in same layer where created

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 40](day-40.md) | [Day 42 →](day-42.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
