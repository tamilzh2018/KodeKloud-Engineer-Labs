# Day 46: Deploy Multi-Tier Application with Docker Compose

## Task Overview

Deploy a complete two-tier application stack using Docker Compose, consisting of a PHP web frontend and MariaDB database backend. This task demonstrates orchestration of multiple interconnected services with shared configuration, networking, and data persistence.

**Technical Specifications:**
- Compose file location: /opt/itadmin/docker-compose.yml
- Web service: PHP with Apache (php:apache image)
- Database service: MariaDB (mariadb:latest image)
- Web container name: php_web (host port 6400 to container port 80)
- Database container name: mysql_web (host port 3306 to container port 3306)
- Volume mounts: /var/www/html and /var/lib/mysql
- Database configuration: custom database name, user, and passwords

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Connect to the application server

```sh
ssh user@app-server-2
```

Establish an SSH connection to Application Server 2 in the Stratos Datacenter. This server will host the two-tier application stack consisting of a web server and database server.

**Step 2:** Create the docker-compose.yml file

```sh
sudo touch /opt/itadmin/docker-compose.yml
```

Create an empty Docker Compose configuration file at the required path /opt/itadmin/docker-compose.yml. The `sudo` command provides elevated privileges needed to create files in system directories. This file will define both the web and database services for the application stack.

**Step 3:** Edit the compose file with service configurations

```sh
sudo vi /opt/itadmin/docker-compose.yml
```

Open the newly created file in the vi text editor with sudo privileges. Add the following multi-service configuration:

```yaml
services:
  web:
    image: php:apache
    container_name: php_web
    ports:
      - "6400:80"
    volumes:
      - /var/www/html:/var/www/html

  db:
    image: mariadb:latest
    container_name: mysql_web
    ports:
      - "3306:3306"
    volumes:
      - /var/lib/mysql:/var/lib/mysql
    environment:
      - MARIADB_DATABASE=database_web
      - MARIADB_USER=kkloud
      - MARIADB_PASSWORD=Str0ngP@ssw0rd123
      - MARIADB_ROOT_PASSWORD=R00tP@ssw0rd456
```

This Docker Compose file defines a two-tier application architecture. The **web service** uses the official php:apache image which bundles PHP with Apache HTTP server. The container is named php_web and exposes port 80 internally, mapped to host port 6400 for external access. A bind mount connects the host's /var/www/html directory to the container's web root, allowing PHP files on the host to be served by Apache.

The **db service** uses the mariadb:latest image for the database tier. The container is named mysql_web and exposes MySQL's default port 3306 on both host and container. The volume mount at /var/lib/mysql persists database files on the host filesystem, ensuring data survives container restarts. Environment variables configure the MariaDB instance: MARIADB_DATABASE creates a database named 'database_web', MARIADB_USER and MARIADB_PASSWORD create a non-root user account, and MARIADB_ROOT_PASSWORD sets the root password. Replace the example passwords with strong, complex passwords as specified in the task requirements.

Save and exit vi by pressing ESC, then typing `:wq` and pressing ENTER.

**Step 4:** Start the multi-container application stack

```sh
docker compose -f /opt/itadmin/docker-compose.yml up -d
```

Launch the complete application stack using Docker Compose. The `-f` flag specifies the exact path to the compose file. The `up` command creates and starts both services (web and db) defined in the configuration. The `-d` flag runs containers in detached mode, allowing them to run in the background. Docker Compose will:
1. Pull the php:apache and mariadb:latest images if not already present
2. Create a default network for service communication
3. Create both containers with their respective configurations
4. Start the containers in dependency order
5. Establish port mappings and volume mounts

**Step 5:** Verify both containers are running

```sh
docker ps
```

List all running containers to confirm successful deployment of the two-tier stack. The output should display both containers:

**php_web container:**
- IMAGE: php:apache
- COMMAND: "docker-php-entrypoint apache2-foreground"
- PORTS: 0.0.0.0:6400->80/tcp
- STATUS: Up

**mysql_web container:**
- IMAGE: mariadb:latest
- COMMAND: "docker-entrypoint.sh mariadbd"
- PORTS: 0.0.0.0:3306->3306/tcp
- STATUS: Up

Both containers should show "Up" status, confirming they are running successfully.

**Step 6:** Test the web server

```bash
# Test web server accessibility
curl http://localhost:6400

# Or if there's a specific test file
curl http://localhost:6400/index.php
```

Verify the PHP/Apache web server is responding to HTTP requests on the mapped port 6400. The curl command should return HTML content or PHP output. If there's no content in /var/www/html yet, you might see a "403 Forbidden" response, which confirms Apache is running but no index file exists.

**Step 7:** Verify database connectivity

```bash
# Access the database container
docker exec -it mysql_web mysql -u kkloud -p

# Enter the password when prompted: Str0ngP@ssw0rd123

# Once connected, verify the database
SHOW DATABASES;

# Exit the MySQL client
EXIT;
```

Test database connectivity by executing the MySQL client inside the mysql_web container. The `-it` flags provide an interactive terminal. After entering the password, the MySQL prompt should appear, confirming the database is running and the user credentials are correct. The `SHOW DATABASES;` command should display the database_web database along with system databases.

**Step 8:** Additional management commands

```bash
# View logs from both services
docker compose -f /opt/itadmin/docker-compose.yml logs

# View logs for specific service
docker compose -f /opt/itadmin/docker-compose.yml logs web
docker compose -f /opt/itadmin/docker-compose.yml logs db

# Check service status
docker compose -f /opt/itadmin/docker-compose.yml ps

# Restart services
docker compose -f /opt/itadmin/docker-compose.yml restart

# Stop the stack (keeps containers)
docker compose -f /opt/itadmin/docker-compose.yml stop

# Remove the stack completely
docker compose -f /opt/itadmin/docker-compose.yml down
```

These commands provide comprehensive management capabilities for the Docker Compose stack. The `logs` command displays output from all or specific services, useful for debugging. The `ps` command shows only containers belonging to this compose project. The `restart` command restarts services without recreating containers. The `stop` command halts containers while preserving them. The `down` command completely removes containers and networks (but preserves volumes by default).

---

## Key Concepts

**Multi-Tier Architecture:**
- Separation of Concerns: Frontend and backend are isolated
- Presentation Tier: PHP/Apache handles HTTP requests and serves web content
- Data Tier: MariaDB manages persistent data storage
- Service Communication: Containers communicate via Docker network
- Scalability: Each tier can be scaled independently

**Two-Tier Application Design:**
- Stateless Web Tier: Web servers don't store persistent state
- Stateful Database Tier: Database maintains application data
- Shared Network: Docker Compose creates a default bridge network
- Service Discovery: Services can reference each other by service name
- Data Persistence: Database volumes ensure data survives container lifecycle

**Docker Compose Service Configuration:**
- Image Selection: Specify base images for each service
- Container Naming: Assign custom names for easier management
- Port Mapping: Expose services on host ports for external access
- Volume Mounts: Persist data and share files between host and containers
- Environment Variables: Configure application behavior at runtime
- Dependencies: Use depends_on to control startup order (optional)

**Database Configuration:**
- MARIADB_DATABASE: Creates initial database schema
- MARIADB_USER: Creates non-root user for application access
- MARIADB_PASSWORD: Sets password for the application user
- MARIADB_ROOT_PASSWORD: Sets administrator password
- Security: Always use strong, complex passwords in production

**Volume Persistence:**
- Bind Mounts: Direct mapping between host and container directories
- Data Survival: Data persists even when containers are removed
- Database Files: /var/lib/mysql contains all database data
- Web Content: /var/www/html contains PHP files and static assets
- Backup Strategy: Host directories can be backed up using standard tools

**Docker Networking:**
- Default Bridge Network: Compose creates a network for service communication
- Service Names as Hostnames: Services resolve each other by name
- Internal DNS: Docker provides DNS resolution for service discovery
- Network Isolation: Containers on same network can communicate freely
- Port Publishing: Only published ports are accessible from host

**Security Best Practices:**
- Strong Passwords: Use complex passwords for database credentials
- Non-Root Users: Create and use non-root database users
- Environment Variables: Consider using .env files for sensitive data
- Network Isolation: Don't publish database ports unless necessary
- Volume Permissions: Ensure proper file permissions on mounted volumes

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 45](day-45.md) | [Day 47 →](day-47.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
