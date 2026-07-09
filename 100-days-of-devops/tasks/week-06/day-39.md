# Day 39: Create a Docker Image From a Container

## Task Overview

Create a new Docker image from a running or stopped container by capturing its current state and modifications. This process, called "committing," is useful for preserving manual changes, creating backups of container states, or quickly prototyping images before converting them to proper Dockerfiles.

**Technical Specifications:**
- Source container: ubuntu_latest (existing container)
- Target image: ecommerce:nautilus
- Operation: docker commit (container-to-image conversion)
- Preserves: All filesystem changes, installed packages, configurations

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Verify the source container exists

```sh
sudo docker ps -a | grep ubuntu_latest
```

Check that the container "ubuntu_latest" exists on your system using `docker ps -a`, which lists all containers regardless of their state (running or stopped). The `grep ubuntu_latest` filters the output to show only the relevant container. The output displays the Container ID, Image used to create it, Command, creation time, current Status, exposed Ports, and Name. Note the container's current state - docker commit works with both running and stopped containers. If the container doesn't exist, you'll need to create it first. Record any important information like the container ID as you may need it for verification later.

**Step 2:** Check what changes were made to the container

```sh
sudo docker diff ubuntu_latest
```

Inspect the filesystem changes made to the container compared to its original image using `docker diff`. This command displays three types of modifications: 'A' indicates files or directories that were added, 'C' indicates files that were changed/modified, and 'D' indicates files that were deleted. The output lists all paths that differ from the base image, which helps you understand what will be captured in the new image. For example, if you installed Apache, you'll see numerous 'A' entries for /var/www, /etc/apache2, and related files. This verification step ensures you're committing the changes you intend to preserve.

**Step 3:** Create a new image from the container

```sh
sudo docker commit ubuntu_latest ecommerce:nautilus
```

Capture the container's current state and save it as a new image using `docker commit`. The syntax is `docker commit container_name new_image:tag`. This command creates a new Docker image named "ecommerce" with the tag "nautilus" containing all the filesystem modifications made to the ubuntu_latest container. The commit operation creates a new layer on top of the base image layers, preserving all changes including installed packages, modified configuration files, created directories, and added content. Upon successful completion, Docker returns the SHA256 ID of the newly created image. This operation doesn't affect the running container - it continues operating normally.

**Step 4:** Verify the new image was created

```sh
sudo docker images | grep ecommerce
```

Confirm the new image exists in your local image repository using `docker images` filtered by the repository name. The output should show the "ecommerce" repository with tag "nautilus", along with its Image ID, creation timestamp (should show "X seconds ago"), and total size. The size represents the cumulative size of all layers, including the base image and the committed changes layer. Compare this to the original ubuntu image size to see how much your modifications added. If multiple people create images with the same name, the IMAGE ID uniquely identifies your specific version.

**Step 5:** Test the new image by creating a container

```sh
sudo docker run -it --name test_ecommerce ecommerce:nautilus /bin/bash
```

Validate that the new image works correctly by creating and running a test container from it. The `docker run -it` command creates an interactive container with a TTY (terminal), `--name test_ecommerce` assigns a descriptive name, `ecommerce:nautilus` specifies your newly created image, and `/bin/bash` launches a bash shell inside the container. Once inside, verify that all your modifications are present - check installed packages, configuration files, and any custom content you added. For example, if you installed Apache, run `which apache2` or `apache2 -v` to confirm it's installed. Exit the container with `exit` when finished. This test ensures the commit captured everything correctly.

**Step 6:** Additional commit options and workflow

```bash
# Commit with a message and author information
sudo docker commit -m "Added Apache web server and custom config" -a "DevOps Team <devops@example.com>" ubuntu_latest ecommerce:v1.0

# Commit and change the CMD instruction
sudo docker commit --change='CMD ["apache2ctl", "-D", "FOREGROUND"]' ubuntu_latest ecommerce:apache

# Pause container during commit (ensures consistency)
sudo docker commit -p ubuntu_latest ecommerce:nautilus

# View commit history of the image
sudo docker history ecommerce:nautilus

# Export image to tarball
sudo docker save ecommerce:nautilus -o ecommerce-nautilus.tar

# Clean up test container
sudo docker rm test_ecommerce
```

These advanced commit options provide better documentation and control. The `-m` flag adds a commit message describing changes (similar to git commits), and `-a` specifies the author for tracking. The `--change` flag allows modifying Dockerfile instructions during commit, such as CMD, ENTRYPOINT, ENV, EXPOSE, LABEL, USER, VOLUME, or WORKDIR. The `-p` flag pauses the container during commit to ensure filesystem consistency, important for containers with active writes. `docker history` shows the image's layer history including your commit. `docker save` exports the image to a tar archive for sharing or backup. These commands help document changes and ensure image integrity.

---

## Key Concepts

**Docker Commit:**
- **Purpose**: Creates new image from container's current state
- **Snapshot**: Captures all filesystem changes as a new layer
- **Non-destructive**: Original container continues running unchanged
- **Incremental**: Only changes are stored, base layers are shared

**When to Use Commit:**
- **Quick Prototyping**: Rapidly test configurations before writing Dockerfile
- **Manual Changes**: Capture interactive modifications for later analysis
- **Debugging**: Save container state at specific points for troubleshooting
- **Backup**: Create checkpoint before risky operations
- **Learning**: Understand what changes your actions make to the filesystem

**Commit vs Dockerfile:**
- **Dockerfile Advantages**: Reproducible, version-controlled, automated, transparent
- **Commit Advantages**: Quick, captures complex manual changes, good for experimentation
- **Best Practice**: Use commit for exploration, convert to Dockerfile for production
- **Transparency**: Dockerfile shows exact commands; commit hides the process
- **Maintenance**: Dockerfile easier to update and maintain over time

**Image Layers:**
- **Layer Stacking**: Images composed of read-only layers stacked together
- **Union Filesystem**: Layers merged to present unified filesystem view
- **Shared Layers**: Multiple images can share base layers to save disk space
- **Commit Layer**: docker commit adds one new layer on top of existing layers
- **Layer Caching**: Docker caches layers to speed up subsequent builds

**Container Modifications:**
- **Filesystem Changes**: Any file created, modified, or deleted
- **Installed Packages**: Software added via package managers (apt, yum, apk)
- **Configuration Files**: Modified settings in /etc or application configs
- **User Data**: Files created in home directories or application folders
- **Not Captured**: Running processes, mounted volumes, network configurations

**Best Practices:**
- **Document Changes**: Always use -m flag to describe modifications
- **Minimize Layers**: Combine related changes before committing
- **Clean Before Commit**: Remove temporary files, caches, and logs
- **Migration Path**: Document commit as temporary; plan Dockerfile migration
- **Testing**: Always test committed images before using in production
- **Versioning**: Use meaningful tags (v1.0, dev-2025-01-15) not just "latest"

**Migration to Dockerfile:**
```dockerfile
# Convert committed changes to Dockerfile
FROM ubuntu:22.04
RUN apt-get update && apt-get install -y apache2
COPY custom-config.conf /etc/apache2/sites-available/
RUN a2ensite custom-config
CMD ["apache2ctl", "-D", "FOREGROUND"]
```
After using commit for prototyping, convert your manual steps into a Dockerfile for proper version control, documentation, and CI/CD integration.

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 38](day-38.md) | [Day 40 →](day-40.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
