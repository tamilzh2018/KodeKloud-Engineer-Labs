# Day 45: Resolve Dockerfile Issues

## Task Overview

Troubleshoot and fix errors in an existing Dockerfile to successfully build a Docker image. This task develops debugging skills for common Dockerfile issues including build context problems, instruction syntax errors, and file path resolution.

**Technical Specifications:**
- Dockerfile location: /opt/docker/Dockerfile
- Base image: httpd:2.4.43
- Configuration: SSL module enablement, port modification
- Files needed: SSL certificates and HTML content
- Expected outcome: Successfully built Docker image

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Connect to the application server

```sh
ssh user@app-server-1
```

Establish an SSH connection to Application Server 1 in the Stratos Datacenter where the problematic Dockerfile is located. This server contains a Dockerfile that needs debugging and correction.

**Step 2:** Examine the existing Dockerfile

```sh
cat /opt/docker/Dockerfile
```

Display the contents of the Dockerfile to identify potential issues. The current Dockerfile contains:

```dockerfile
FROM httpd:2.4.43

RUN sed -i "s/Listen 80/Listen 8080/g" /usr/local/apache2/conf/httpd.conf

RUN sed -i '/LoadModule\ ssl_module modules\/mod_ssl.so/s/^#//g' conf/httpd.conf

RUN sed -i '/LoadModule\ socache_shmcb_module modules\/mod_socache_shmcb.so/s/^#//g' conf/httpd.conf

RUN sed -i '/Include\ conf\/extra\/httpd-ssl.conf/s/^#//g' conf/httpd.conf

RUN cp certs/server.crt /usr/local/apache2/conf/server.crt

RUN cp certs/server.key /usr/local/apache2/conf/server.key

RUN cp html/index.html /usr/local/apache2/htdocs/
```

Review the Dockerfile structure. It uses the httpd:2.4.43 base image, configures Apache to listen on port 8080 instead of 80, enables SSL modules, and attempts to copy certificate files and HTML content. At first glance, the `RUN cp` commands appear problematic.

**Step 3:** Navigate to the Dockerfile directory

```sh
cd /opt/docker
```

Change to the directory containing the Dockerfile. Docker builds use the current directory as the build context, so all COPY or ADD instructions must reference files relative to this location. This is essential for understanding path resolution issues.

**Step 4:** Attempt initial image build

```sh
docker build -t test:test .
```

Try to build the Docker image with tag 'test:test'. The build process fails with an error indicating it cannot pull the base image due to network timeout. This is a common issue in lab environments where the base image isn't cached locally. The error message shows: "failed to resolve source metadata for docker.io/library/httpd:2.4.43: dial tcp 10.0.0.6:443: i/o timeout". This indicates network connectivity issues with the Docker registry.

**Step 5:** Pull the base image separately

```sh
docker pull httpd:2.4.43
```

Download the httpd:2.4.43 base image directly from Docker Hub to the local cache before building. This separates the image pull operation from the build process, helping isolate network-related issues. The output shows layer downloads: "Pulling from library/httpd" followed by SHA digests for each layer. Once complete, the image is stored locally and the build won't need to fetch it again.

**Step 6:** Retry the Docker build

```sh
docker build -t test:test .
```

Attempt the build again now that the base image is cached locally. This time the build progresses further, successfully executing the first five RUN commands (the sed commands that modify httpd.conf). However, it fails at the sixth step with error: "cp: cannot stat 'certs/server.crt': No such file or directory". This reveals the real problem: the `RUN cp` commands are trying to copy files during the build using shell commands, but these files need to be copied from the build context using the COPY instruction instead.

**Step 7:** Identify the root cause

The issue is that `RUN cp certs/server.crt` executes inside the container's filesystem during build, looking for files that don't exist there. The certs/ and html/ directories exist in the build context (the host's /opt/docker directory), but they need to be copied into the image using the COPY instruction, not accessed via RUN cp commands.

**Step 8:** Fix the Dockerfile

```sh
sudo vi /opt/docker/Dockerfile
```

Open the Dockerfile in an editor and replace all `RUN cp` commands with `COPY` instructions:

```dockerfile
FROM httpd:2.4.43

RUN sed -i "s/Listen 80/Listen 8080/g" /usr/local/apache2/conf/httpd.conf

RUN sed -i '/LoadModule\ ssl_module modules\/mod_ssl.so/s/^#//g' conf/httpd.conf

RUN sed -i '/LoadModule\ socache_shmcb_module modules\/mod_socache_shmcb.so/s/^#//g' conf/httpd.conf

RUN sed -i '/Include\ conf\/extra\/httpd-ssl.conf/s/^#//g' conf/httpd.conf

COPY certs/server.crt /usr/local/apache2/conf/server.crt

COPY certs/server.key /usr/local/apache2/conf/server.key

COPY html/index.html /usr/local/apache2/htdocs/
```

The key change is replacing `RUN cp` with `COPY`. The COPY instruction is designed to copy files from the build context (host) into the image. It reads files from the directory where docker build is executed and copies them to the specified destination in the container filesystem. Save and exit the editor.

**Step 9:** Build the corrected Docker image

```sh
docker build -t test:test .
```

Execute the build command again with the corrected Dockerfile. This time, all steps complete successfully. The output shows:
- Layers 2-5 are cached (sed commands)
- Layers 6-8 execute the COPY instructions successfully
- Final output: "exporting to image" and "naming to docker.io/library/test:test"

The build succeeds because COPY correctly accesses files from the build context and adds them to the image.

**Step 10:** Verify the image was created

```sh
docker images
```

List all Docker images to confirm the test:test image was successfully built. The output displays image repository, tag, image ID, creation time, and size. The presence of test:test confirms the Dockerfile issues have been resolved.

**Step 11:** Additional verification commands

```bash
# Inspect the image layers
docker history test:test

# Verify the image can run
docker run -d --name test-container -p 8080:8080 test:test

# Check if the copied files exist in the container
docker exec test-container ls -la /usr/local/apache2/conf/server.crt
docker exec test-container ls -la /usr/local/apache2/htdocs/index.html

# Clean up test container
docker stop test-container
docker rm test-container
```

These verification commands confirm the image is properly built and functional. The `docker history` command shows all layers and their sizes. Running the container tests that it starts successfully. The `docker exec` commands verify that files were correctly copied to their destinations. Clean up removes the test container.

---

## Key Concepts

**Dockerfile Troubleshooting:**
- Build Context: Directory from which docker build is executed
- Layer Caching: Successful layers are cached even if build fails later
- Error Messages: Docker provides detailed error messages with line numbers
- Incremental Debugging: Comment out problematic sections to isolate issues

**Common Dockerfile Errors:**
- File Not Found: Files must be in build context or accessible in container
- Permission Denied: File ownership and permission issues
- Network Timeouts: Base image pull failures (pre-pull images to avoid)
- Syntax Errors: Invalid instruction format or typos
- Path Resolution: Incorrect relative or absolute paths

**COPY vs RUN cp:**
- COPY: Dockerfile instruction that copies files from build context to image
- RUN cp: Shell command that copies files within the container filesystem
- Build Context: COPY accesses host files, RUN cp only sees container files
- Best Practice: Always use COPY for adding external files to images
- Performance: COPY is more efficient and leverages layer caching

**Dockerfile Best Practices:**
- Use COPY for build-time file transfers, not RUN cp
- Minimize layers by combining RUN commands where appropriate
- Order instructions from least to most frequently changed
- Use .dockerignore to exclude unnecessary files from build context
- Always specify exact versions for base images

**Build Context Management:**
- Context Directory: All files/directories in the build location
- Recursive Inclusion: Subdirectories are automatically included
- Context Size: Large contexts slow down builds
- .dockerignore: Exclude files similar to .gitignore

**Debugging Strategies:**
- Read error messages carefully for line numbers and specific issues
- Use `docker history` to inspect image layers
- Run containers interactively to test commands manually
- Comment out failing instructions to isolate problems
- Check that required files exist in build context

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 44](day-44.md) | [Day 46 →](day-46.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
