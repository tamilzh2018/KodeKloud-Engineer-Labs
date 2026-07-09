# Day 37: Copy File to Docker Container

## Task Overview

Transfer files between the Docker host and running containers using the docker cp command. This essential operation enables deployment of configuration files, extraction of logs, data backup, and debugging workflows without rebuilding container images.

**Technical Specifications:**
- Source file: /tmp/nautilus.txt.gpg (on host)
- Target container: ubuntu_latest (running container)
- Destination path: /usr/src/ (inside container)
- Operation type: host-to-container file transfer

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Verify the source file exists on the host

```sh
ls -lh /tmp/nautilus.txt.gpg
```

Confirm the source file exists and check its permissions and size using the `ls -lh` command. The `-l` flag displays detailed file information including permissions, owner, group, size, and modification date. The `-h` flag shows file sizes in human-readable format (KB, MB, GB). This verification step prevents copy errors due to missing files or permission issues. Note the file size and permissions - these attributes will be preserved when copied to the container. If the file doesn't exist, you'll receive a "No such file or directory" error, indicating you need to create or locate the correct file first.

**Step 2:** Verify target container is running

```sh
sudo docker ps | grep ubuntu_latest
```

Check that the target container "ubuntu_latest" is currently running using `docker ps` combined with `grep` to filter results. The output should show the container with Status "Up" followed by its uptime (e.g., "Up 5 minutes"). If no output appears, the container either doesn't exist or isn't running. Use `docker ps -a` to see all containers including stopped ones. If the container is stopped, start it with `docker start ubuntu_latest` before attempting the copy operation. The `docker cp` command works with both running and stopped containers, but it's good practice to verify the container state first.

**Step 3:** Copy file from host to container

```sh
sudo docker cp /tmp/nautilus.txt.gpg ubuntu_latest:/usr/src/
```

Transfer the file from the host filesystem to the container using the `docker cp` command. The syntax follows the pattern: `docker cp source destination`, where source is the host file path `/tmp/nautilus.txt.gpg` and destination is specified as `container_name:path_inside_container`. The `ubuntu_latest:/usr/src/` destination uses the container name followed by a colon and the target directory path. The trailing slash in `/usr/src/` indicates the file should be copied into this directory with its original filename preserved. Docker automatically handles permission mapping and preserves file attributes. No output means success; if the destination directory doesn't exist, you'll receive an error requiring you to create it first using `docker exec ubuntu_latest mkdir -p /usr/src`.

**Step 4:** Verify file was copied successfully

```sh
sudo docker exec ubuntu_latest ls -lh /usr/src/nautilus.txt.gpg
```

Confirm the file exists inside the container by executing the `ls` command within the container context using `docker exec`. This command runs `ls -lh /usr/src/nautilus.txt.gpg` inside the ubuntu_latest container without entering an interactive shell. The output displays the file's properties including size, permissions, and modification date, which should match (or closely match) the original file on the host. If successful, you'll see something like `-rw-r--r-- 1 root root 1.2K Nov 18 10:30 /usr/src/nautilus.txt.gpg`. If the file doesn't exist, you'll receive a "No such file or directory" error, indicating the copy operation failed or was performed to a different location.

**Step 5:** Additional copy operation examples

```bash
# Copy directory from host to container
sudo docker cp /path/to/directory ubuntu_latest:/container/path/

# Copy from container to host
sudo docker cp ubuntu_latest:/usr/src/nautilus.txt.gpg /tmp/backup/

# Copy and preserve file attributes
sudo docker cp -a /path/to/file ubuntu_latest:/destination/

# Copy multiple files using tar
tar -czf /tmp/files.tar.gz /path/to/files
sudo docker cp /tmp/files.tar.gz ubuntu_latest:/tmp/
sudo docker exec ubuntu_latest tar -xzf /tmp/files.tar.gz -C /destination/

# View copied file content without extracting
sudo docker exec ubuntu_latest cat /usr/src/nautilus.txt.gpg
```

These examples demonstrate advanced copy scenarios. Directory copies work the same as file copies - just specify the directory path. Reverse copies (container-to-host) flip the source and destination, useful for extracting logs or backing up container data. The `-a` flag archives mode, preserving file ownership and permissions (requires appropriate privileges). For multiple files, creating a tar archive is more efficient than individual copies. The final example shows how to view file contents directly using `docker exec` with `cat`, useful for verifying text file contents without copying back to the host.

---

## Key Concepts

**Docker Copy Operations:**
- **Bidirectional**: Works both host-to-container and container-to-host
- **Container State**: Functions with both running and stopped containers
- **Path Syntax**: Uses `container_name:path` format for container paths
- **Attribute Preservation**: Maintains file permissions and ownership by default

**Copy vs Volume Mounts:**
- **docker cp**: One-time transfer, good for temporary files or configs
- **Volume Mounts**: Real-time sync, ideal for persistent data and development
- **Use Cases**: Use cp for deployment/extraction, volumes for continuous access
- **Performance**: Volumes are faster for frequently accessed data

**File Permissions:**
- **UID/GID Mapping**: User IDs map between host and container
- **Root Ownership**: Files may appear owned by root inside container
- **Permission Preservation**: File modes (rwx) are maintained
- **Security**: Be cautious copying sensitive files with world-readable permissions

**Best Practices:**
- **Build Time**: Use COPY/ADD in Dockerfile for files needed at build time
- **Runtime**: Use volumes for persistent data that changes during runtime
- **Configuration**: Use ConfigMaps/Secrets (Kubernetes) or environment variables
- **Temporary Transfers**: Reserve docker cp for debugging and one-off operations
- **Directory Structure**: Ensure target directories exist before copying

**Common Use Cases:**
- **Configuration Deployment**: Copy config files to containers
- **Log Extraction**: Retrieve application logs for analysis
- **Debugging**: Copy core dumps or debug files from containers
- **Data Backup**: Extract data before container removal
- **Development**: Quick file updates during testing

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 36](day-36.md) | [Day 38 →](day-38.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
