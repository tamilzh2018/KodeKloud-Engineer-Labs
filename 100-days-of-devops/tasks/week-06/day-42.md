# Day 42: Create Docker Network

## Task Overview

Create and configure custom Docker networks to enable container communication and network isolation. Docker networking allows containers to communicate securely while maintaining isolation from other networks, supporting various network drivers for different use cases from single-host development to production multi-host deployments.

**Technical Specifications:**
- Network name: blog
- Network driver: macvlan
- Subnet configuration: 10.10.1.0/24
- IP range: 10.10.1.0/24
- Server location: App Server 2

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Connect to App Server 2

```sh
ssh user@app-server-2
# Replace with actual server credentials
```

Establish an SSH connection to App Server 2 where the network will be created. SSH (Secure Shell) provides encrypted remote access to the server. Replace 'user' with your actual username and 'app-server-2' with the server's hostname or IP address. You may be prompted for a password or SSH key passphrase. Once connected, your terminal prompt changes to reflect the remote server, confirming you're working on the correct system. This step ensures you create the network on the specified server rather than your local machine or a different server in the infrastructure.

**Step 2:** Verify Docker is installed and running

```sh
sudo docker --version
sudo systemctl status docker
```

Confirm Docker is installed and the Docker daemon is running on the server. The `docker --version` command displays the installed Docker version, confirming the Docker CLI is available. The `systemctl status docker` command shows the Docker daemon's status - look for "active (running)" in green, indicating the service is operational. If Docker isn't running, start it with `sudo systemctl start docker`. If Docker isn't installed, you'll need to install it before proceeding. These verification steps prevent errors when attempting to create networks.

**Step 3:** List existing Docker networks

```sh
sudo docker network ls
```

Display all existing Docker networks on the system using `docker network ls`. By default, Docker creates three networks: 'bridge' (default network for containers), 'host' (removes network isolation, uses host's network), and 'none' (disables networking). Each network entry shows Network ID (unique identifier), Name, Driver (networking implementation), and Scope (local or swarm). Reviewing existing networks helps avoid naming conflicts and provides context for understanding your new network in relation to the default networks. Note any existing custom networks to ensure your new network name is unique.

**Step 4:** Create the macvlan network

```sh
sudo docker network create blog -d macvlan --ip-range 10.10.1.0/24 --subnet 10.10.1.0/24
```

Create a custom Docker network named "blog" using the macvlan driver with specified IP addressing. Breaking down the command: `docker network create` initiates network creation, `blog` is the network name (must be unique), `-d macvlan` specifies the macvlan driver (makes containers appear as physical devices on the network), `--subnet 10.10.1.0/24` defines the network's IP address range (256 addresses from 10.10.1.0 to 10.10.1.255), and `--ip-range 10.10.1.0/24` specifies the range from which Docker assigns container IPs (in this case, the entire subnet). Upon success, Docker returns the network ID, a long hexadecimal string uniquely identifying the network. The macvlan driver is particularly useful when you need containers to have MAC addresses and appear as physical devices on your network, enabling integration with legacy applications expecting direct network access.

**Step 5:** Verify the network was created

```sh
sudo docker network ls | grep blog
```

Confirm the new network appears in the network list by filtering for the "blog" network. The output should show a line with the network name "blog", its unique ID, the "macvlan" driver, and "local" scope. The "local" scope indicates this is a single-host network (as opposed to "swarm" scope for multi-host overlay networks). If you don't see the network, the creation command may have failed - scroll back to check for error messages. Common creation failures include: conflicting network names, invalid CIDR notation in subnet/IP range, or insufficient permissions.

**Step 6:** Inspect network configuration details

```sh
sudo docker network inspect blog
```

Examine the detailed configuration of the newly created network using `docker network inspect`. This command outputs comprehensive JSON-formatted information including: network Name, ID, Creation timestamp, Scope, Driver (macvlan), IPAM (IP Address Management) configuration showing the subnet (10.10.1.0/24) and IP range, and Containers currently connected to this network (initially empty). The IPAM section is particularly important as it confirms your subnet and IP range settings were applied correctly. This inspection is crucial for troubleshooting connectivity issues and verifying the network matches specifications.

**Step 7:** Test the network by running a container

```sh
sudo docker run -d --name test-blog --network blog nginx:alpine
```

Create a test container connected to the new network to verify it works correctly. The `docker run -d` runs the container in detached mode, `--name test-blog` assigns a descriptive name, `--network blog` connects the container to your newly created "blog" network instead of the default bridge network, and `nginx:alpine` is a lightweight web server image for testing. Docker assigns an IP address from the configured range (10.10.1.0/24) to this container. This test confirms the network is functional and containers can be attached to it successfully.

**Step 8:** Verify container network configuration

```sh
sudo docker inspect test-blog | grep -A 10 Networks
```

Check the container's network configuration to confirm it's connected to the "blog" network with the correct IP settings. The `docker inspect` command outputs detailed container information in JSON format. The `grep -A 10 Networks` filters to show the Networks section plus 10 lines after it, displaying the network name, IP address assigned, MAC address, and other network settings. You should see "blog" as the network name and an IP address within the 10.10.1.0/24 range. This verification ensures the container successfully attached to the custom network and received appropriate network configuration.

**Step 9:** Clean up test resources

```sh
sudo docker stop test-blog
sudo docker rm test-blog
```

Remove the test container now that you've verified the network works correctly. The `docker stop test-blog` gracefully stops the running container by sending a SIGTERM signal, giving it time to shut down cleanly. The `docker rm test-blog` permanently deletes the stopped container from the system. Note that removing the container does NOT delete the network - the "blog" network persists and can be used by other containers. Clean up prevents resource consumption and removes test artifacts, following good housekeeping practices in containerized environments.

**Step 10:** Additional network management commands

```bash
# View detailed help for network commands
sudo docker network --help

# Create network with gateway specification
sudo docker network create blog2 -d macvlan \
  --subnet 10.10.2.0/24 \
  --ip-range 10.10.2.0/24 \
  --gateway 10.10.2.1

# Connect running container to network
sudo docker network connect blog container-name

# Disconnect container from network
sudo docker network disconnect blog container-name

# Remove unused networks
sudo docker network prune

# Remove specific network (no containers can be connected)
sudo docker network rm blog

# Create bridge network (default driver)
sudo docker network create my-bridge-network

# Create overlay network (for swarm mode)
sudo docker network create -d overlay my-overlay-network
```

These commands provide comprehensive network management capabilities. The `--help` flag displays all available network options and subcommands. The gateway example shows how to specify a custom gateway IP for routing. `network connect` and `disconnect` allow dynamically modifying container network attachments without restarting. `network prune` removes all unused networks, freeing resources. `network rm` deletes specific networks but fails if containers are still connected (disconnect them first). The final examples show creating different network types - bridge for single-host container communication (most common), and overlay for multi-host Swarm deployments.

---

## Key Concepts

**Docker Networking Fundamentals:**
- **Container Isolation**: Each container has its own network namespace
- **Network Drivers**: Different drivers provide different networking capabilities
- **DNS Resolution**: Containers can communicate using container names as hostnames
- **Port Publishing**: Map container ports to host ports for external access
- **Network Scopes**: Local (single host) vs Swarm (multi-host)

**Network Drivers:**
- **bridge**: Default driver for single-host networking, creates private internal network
- **host**: Removes network isolation, container uses host's network directly
- **overlay**: Multi-host networking for Docker Swarm clusters
- **macvlan**: Assigns MAC addresses to containers, makes them appear as physical devices
- **none**: Disables all networking for the container
- **ipvlan**: Similar to macvlan but shares MAC address (Layer 3 mode)

**MACVLAN Driver:**
- **Purpose**: Make containers appear as physical devices on the network
- **MAC Addresses**: Each container gets unique MAC address
- **Direct Network Access**: Containers directly attached to physical network
- **Legacy Integration**: Useful for applications expecting physical network presence
- **VLAN Support**: Can trunk 802.1Q VLAN tags
- **Performance**: High performance, bypasses Docker's NAT
- **Limitations**: Not all network switches support promiscuous mode required

**Network Configuration:**
- **Subnet**: CIDR notation defining network address range (10.10.1.0/24 = 256 IPs)
- **IP Range**: Subset of subnet Docker uses for container assignments
- **Gateway**: Default route for outbound traffic (auto-assigned if not specified)
- **DNS**: Docker provides built-in DNS for container name resolution
- **MTU**: Maximum Transmission Unit (packet size)

**CIDR Notation:**
- **/24**: 256 IP addresses (10.10.1.0 through 10.10.1.255)
- **/16**: 65,536 IP addresses (entire class B)
- **/8**: 16,777,216 IP addresses (entire class A)
- **Network Address**: First IP (10.10.1.0) identifies the network
- **Broadcast Address**: Last IP (10.10.1.255) for broadcast packets

**Container Communication:**
- **Same Network**: Containers on same network communicate using container names
- **Different Networks**: Containers on different networks are isolated
- **Bridge Network**: Default, provides NAT for external connectivity
- **User-Defined Bridge**: Better than default bridge, provides automatic DNS
- **Network Aliases**: Containers can have multiple DNS aliases

**Use Cases by Driver:**
- **Bridge**: Development, simple single-host deployments, microservices on one server
- **Host**: Maximum performance, monitoring tools, network utilities
- **Overlay**: Production multi-host clusters, Docker Swarm, Kubernetes
- **Macvlan**: Legacy app integration, DHCP clients, network monitoring
- **None**: Maximum isolation, security-sensitive workloads, testing

**Network Security:**
- **Network Isolation**: Containers on different networks cannot communicate
- **Internal Networks**: Networks without external connectivity (--internal flag)
- **Encryption**: Overlay networks support automatic encryption
- **Firewall Rules**: Docker creates iptables rules for container networking
- **Least Privilege**: Only expose necessary ports and services

**Best Practices:**
- **User-Defined Networks**: Prefer user-defined networks over default bridge
- **Network Planning**: Plan IP addressing to avoid conflicts
- **Naming Conventions**: Use descriptive network names (project-env-network)
- **Documentation**: Document network topology and IP assignments
- **Resource Limits**: Set resource limits to prevent network exhaustion
- **Monitoring**: Monitor network performance and connectivity
- **Cleanup**: Remove unused networks to prevent clutter

**Troubleshooting:**
- **Connectivity Issues**: Use docker exec to run ping/curl inside containers
- **DNS Problems**: Check /etc/resolv.conf inside container
- **IP Conflicts**: Inspect networks to identify overlapping subnets
- **Driver Limitations**: Understand driver-specific constraints
- **Logs**: Check Docker daemon logs for network errors

**Network Inspection Commands:**
```bash
# See all networks
docker network ls

# Detailed network info
docker network inspect network-name

# See which containers are on a network
docker network inspect network-name --format '{{range .Containers}}{{.Name}} {{end}}'

# See container's IP address
docker inspect container-name --format '{{.NetworkSettings.IPAddress}}'
```

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 41](day-41.md) | [Day 43 →](../week-07/day-43.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
