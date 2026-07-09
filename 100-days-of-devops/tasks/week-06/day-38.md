# Day 38: Docker Pull and Tag Images

## Task Overview

Download Docker images from container registries and create custom tags for version management and organizational purposes. Image tagging is essential for managing multiple versions, environments, and maintaining clear image identification in production workflows.

**Technical Specifications:**
- Source image: busybox:musl (from Docker Hub)
- Registry: Docker Hub (default registry)
- New tag: busybox:blog
- Operation: Pull image and create alias tag

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Pull the BusyBox image from Docker Hub

```sh
sudo docker pull busybox:musl
```

Download the BusyBox image with the "musl" tag from Docker Hub using the `docker pull` command. Docker Hub is the default public registry where millions of container images are hosted. The image name `busybox:musl` consists of two parts separated by a colon: "busybox" is the repository name, and "musl" is the tag (version identifier). The musl tag specifically refers to a BusyBox build using musl libc instead of glibc, resulting in an even smaller binary size. During the pull operation, Docker downloads the image layers, displays progress bars showing download status for each layer, and verifies layer integrity using checksums. If the image already exists locally, Docker will skip the download unless a newer version is available.

**Step 2:** Verify the image was downloaded successfully

```sh
sudo docker images busybox
```

Display all locally available BusyBox images using the `docker images` command with the repository name filter. The output shows a table with columns: REPOSITORY (image name), TAG (version label), IMAGE ID (unique hash identifier), CREATED (how long ago the image was built), and SIZE (total image size). You should see `busybox:musl` in the list with its associated metadata. The IMAGE ID is a SHA256 hash (shown as first 12 characters) that uniquely identifies this specific image version. Multiple tags can point to the same IMAGE ID, which is what happens when you create tag aliases. The SIZE column shows the total uncompressed size; compressed download size is typically much smaller.

**Step 3:** Create a new tag for the image

```sh
sudo docker tag busybox:musl busybox:blog
```

Create a new tag "blog" that references the same image as "busybox:musl" using the `docker tag` command. This operation doesn't create a copy of the image - instead, it creates an additional reference (alias) pointing to the same underlying image data, identified by the IMAGE ID. The syntax is `docker tag source_image:tag new_image:tag`. Tagging is instantaneous and uses no additional disk space because both tags share the same image layers. This is useful for creating environment-specific tags (dev, staging, prod), version aliases (v1.2, latest), or organizational naming conventions. You can create unlimited tags for any image without duplication.

**Step 4:** Verify both tags exist and point to the same image

```sh
sudo docker images busybox
```

List all BusyBox images again to confirm both tags exist and reference the same image. The output now shows two entries: `busybox:musl` and `busybox:blog`, both with identical IMAGE ID, CREATED timestamp, and SIZE values. This confirms they are aliases for the same underlying image data. If you see different IMAGE IDs, something went wrong in the tagging process. Notice that the total disk space used hasn't increased - Docker's layered filesystem means multiple tags can share the same data. This makes tagging an efficient way to organize and version images without storage overhead.

**Step 5:** Additional image management commands

```bash
# List all local images
sudo docker images

# List images with detailed information
sudo docker images --digests

# Remove specific tag (doesn't delete image if other tags exist)
sudo docker rmi busybox:blog

# Remove image by ID (removes all tags)
sudo docker rmi <image-id>

# Remove dangling images (untagged)
sudo docker image prune

# Remove all unused images
sudo docker image prune -a

# Search for images on Docker Hub
sudo docker search busybox

# Pull all tags of an image
sudo docker pull busybox --all-tags

# Inspect image details and layers
sudo docker inspect busybox:musl

# View image history and layers
sudo docker history busybox:musl
```

These commands provide comprehensive image management capabilities. `docker images` without filters shows all local images from all repositories. The `--digests` flag adds a content-addressable hash for image verification. `docker rmi` removes image tags; if multiple tags exist for the same IMAGE ID, only the specified tag is removed, but if it's the last tag, the image data is deleted. `docker image prune` cleans up dangling images (layers without tags, usually from builds). `docker search` queries Docker Hub for available images. `docker inspect` shows detailed JSON metadata including layers, environment variables, exposed ports, and configuration. `docker history` displays the image build history showing each layer's command and size.

---

## Key Concepts

**Docker Images:**
- **Read-Only Template**: Images are immutable blueprints for creating containers
- **Layered Filesystem**: Built in layers using Union FS for efficiency and caching
- **Base Images**: Starting point images (ubuntu, alpine, scratch)
- **Derived Images**: Built on top of base images with added layers

**Image Tags:**
- **Version Identifiers**: Labels that identify different versions of images
- **Aliases**: Multiple tags can point to the same image
- **Format**: repository:tag (e.g., nginx:1.21.6, ubuntu:22.04)
- **Latest Tag**: Conventional tag for most recent version (not automatic)
- **Semantic Versioning**: Use version numbers for production (1.0.0, 2.1.3)

**Docker Registries:**
- **Docker Hub**: Default public registry with millions of images
- **Private Registries**: Self-hosted or cloud-based (AWS ECR, Google GCR, Azure ACR)
- **Image Names**: Format is [registry/][namespace/]repository[:tag]
- **Official Images**: Curated and maintained by Docker (single-word names)

**BusyBox Image:**
- **Minimal Linux**: Tiny (~1-5MB) Linux distribution
- **Swiss Army Knife**: Combines common Unix utilities in single executable
- **musl vs glibc**: musl libc is smaller and simpler than glibc
- **Use Cases**: Debugging containers, minimal base images, learning Docker

**Tag Naming Strategies:**
- **Environment Tags**: dev, staging, production
- **Version Tags**: v1.0, v1.1, v2.0 or 1.0.0, 1.1.0
- **Git SHA Tags**: Use commit hashes for traceability
- **Date Tags**: 2025-01-15 for time-based versioning
- **Feature Tags**: feature-auth, feature-payment for feature branches

**Best Practices:**
- **Avoid 'latest'**: Use specific version tags in production for predictability
- **Consistent Naming**: Establish tag naming conventions across organization
- **Immutable Tags**: Don't reuse tags for different image content
- **Clean Up**: Regularly remove unused images to save disk space
- **Documentation**: Document tag naming strategy in team guidelines

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 37](day-37.md) | [Day 39 →](day-39.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
