# Day 40: Docker Execute Commands in Running Containers

## Task Overview

Execute commands inside running Docker containers to install software, modify configurations, and manage services. This task demonstrates using docker exec to interact with containers, install Apache web server, configure it to listen on a custom port, and start the service - all without stopping or rebuilding the container.

**Technical Specifications:**
- Target container: kkloud (running Ubuntu 18.04)
- Software to install: apache2 and vim
- Configuration change: Apache port 80 to 6000
- Service management: Start Apache and verify operation

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** List running containers

```sh
sudo docker ps
```

Display all currently running containers to verify the "kkloud" container is active. The `docker ps` command shows Container ID, Image, Command, Created timestamp, Status (uptime), Ports (exposed/mapped), and Names. Look for the "kkloud" container in the output - it should show Status as "Up" with its uptime. Note the container ID and image name for reference. If you don't see the container, it may be stopped; use `docker ps -a` to see all containers and `docker start kkloud` to start it if needed. Example output shows the container was created 8 minutes ago and is running the /bin/bash command.

**Step 2:** Access the container's shell

```sh
sudo docker exec -it kkloud /bin/bash
```

Open an interactive bash shell inside the running container using `docker exec`. The `-i` flag keeps STDIN open for interaction, and `-t` allocates a pseudo-TTY (terminal), together `-it` provides an interactive terminal session. The `kkloud` argument specifies the target container name, and `/bin/bash` is the command to execute inside the container. Once executed, your prompt changes from the host prompt to the container's prompt (e.g., `root@dcdc693d1175:/#`), indicating you're now inside the container. This is similar to SSH but doesn't require SSH server configuration inside the container. You can execute any command available in the container's environment.

**Step 3:** Update package repositories and install Apache

```sh
apt update && apt install apache2 vim -y
```

Update the APT package index and install Apache web server and Vim text editor in a single command. The `apt update` command refreshes the package lists from Ubuntu's repositories, ensuring you get the latest versions. The `&&` operator chains commands, executing the second only if the first succeeds. The `apt install apache2 vim -y` command installs both packages, with `-y` automatically answering "yes" to prompts, enabling unattended installation. Apache2 is the web server package, and Vim is installed for editing configuration files (as Ubuntu minimal images often lack full-featured editors). The installation process downloads packages, resolves dependencies, and configures the software automatically.

**Step 4:** Edit Apache port configuration file

```sh
vim /etc/apache2/ports.conf
```

Open the Apache ports configuration file using Vim to modify the default listening port. This file controls which network ports Apache monitors for incoming connections. Press `i` to enter insert mode in Vim, then locate the line that reads `Listen 80`. Change this to `Listen 6000` to make Apache listen on port 6000 instead of the standard HTTP port 80. This change is necessary because the task requires a custom port, or perhaps port 80 is already in use. After making the change, press `ESC` to exit insert mode, then type `:wq` and press Enter to save and quit Vim. The modified configuration will look like:

```conf
# Modified ports.conf
Listen 6000

<IfModule ssl_module>
        Listen 443
</IfModule>

<IfModule mod_gnutls.c>
        Listen 443
</IfModule>
```

**Step 5:** Update Apache virtual host configuration

```sh
vim /etc/apache2/sites-available/000-default.conf
```

Edit the default virtual host configuration to match the new port. Open the file with Vim and locate the `<VirtualHost *:80>` directive at the beginning. Change it to `<VirtualHost *:6000>` to match the port configured in ports.conf. This ensures the virtual host responds to requests on port 6000. Virtual hosts allow Apache to serve different content based on the requested hostname or port. The asterisk (*) means "any IP address" on this server. Save and exit with `:wq`. The modified section looks like:

```conf
<VirtualHost *:6000>
    ServerAdmin webmaster@localhost
    DocumentRoot /var/www/html
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

Changing only ports.conf without updating the VirtualHost would cause Apache to listen on port 6000 but the virtual host wouldn't respond, resulting in connection errors.

**Step 6:** Start Apache web server

```sh
/usr/sbin/apache2ctl start
```

Start the Apache service using the apache2ctl control interface. The `apache2ctl` command is Apache's primary control script for starting, stopping, and managing the web server. We use the full path `/usr/sbin/apache2ctl` to ensure we're calling the correct binary. The `start` argument initiates the Apache daemon, which forks into multiple worker processes to handle incoming requests. Unlike systemd services, containers often don't run init systems, so we use direct control scripts. If successful, Apache starts without output (silence means success in Unix tradition). If there are configuration errors, you'll see detailed error messages indicating what needs to be fixed.

**Step 7:** Verify Apache processes are running

```sh
ps aux | grep apache2
```

Confirm Apache is running by listing all processes and filtering for apache2. The `ps aux` command shows all running processes with detailed information: user, PID (Process ID), CPU usage, memory usage, start time, and command. The `grep apache2` filters to show only Apache-related processes. You should see multiple apache2 processes: one master process running as root, and several worker processes running as www-data (Apache's unprivileged user for security). The output shows processes like:
- Master process: `root 116 ... /usr/sbin/apache2 -k start`
- Worker processes: `www-data 117 ... /usr/sbin/apache2 -k start`

Multiple worker processes enable Apache to handle concurrent requests efficiently. If you don't see these processes, Apache didn't start successfully - check for configuration errors.

**Step 8:** Test Apache is responding on port 6000

```sh
curl localhost:6000
```

Verify Apache is serving content by making an HTTP request to localhost on port 6000 using `curl`. This command sends a GET request to the web server and displays the HTML response. If Apache is configured correctly and running, you'll receive the default Apache welcome page HTML, which includes `<title>Apache2 Ubuntu Default Page</title>` and welcome text. If the connection is refused, Apache isn't listening on port 6000 - recheck your configuration files. If you see "Connection refused," Apache may not be running - verify with `ps aux`. If successful, this confirms the complete workflow: Apache installed, configured for custom port, and serving content.

**Step 9:** Exit the container

```sh
exit
```

Leave the container shell and return to the host system by typing `exit` or pressing `Ctrl+D`. This closes the interactive session started by `docker exec`, but importantly, it does NOT stop the container - the container continues running because its main process (/bin/bash from the docker run command) is still active. The Apache processes you started will continue running inside the container. Your shell prompt changes back to the host prompt, confirming you've exited. You can re-enter the container anytime with `docker exec -it kkloud /bin/bash` to check status or make further changes.

**Step 10:** Additional container execution examples

```bash
# Run non-interactive commands
sudo docker exec kkloud ls -la /var/www/html

# Check Apache status from outside container
sudo docker exec kkloud ps aux | grep apache2

# View Apache logs
sudo docker exec kkloud tail -f /var/log/apache2/access.log

# Execute commands as specific user
sudo docker exec -u www-data kkloud whoami

# Execute commands with custom working directory
sudo docker exec -w /var/www/html kkloud pwd

# Run multiple commands
sudo docker exec kkloud bash -c "cd /var/www/html && ls -la"

# Copy files and verify
sudo docker cp index.html kkloud:/var/www/html/
sudo docker exec kkloud ls -la /var/www/html/index.html
```

These examples demonstrate various docker exec capabilities. Non-interactive commands execute and return output without opening a shell, useful for automation and scripts. The `-u` flag executes commands as a specific user (important for permissions). The `-w` flag sets the working directory before command execution. The `bash -c` technique allows executing multiple commands in sequence. Combining docker exec with other commands like cp enables complex workflows. All these operations occur without entering an interactive shell, making them suitable for scripts and automation pipelines.

---

## Key Concepts

**Docker Exec:**
- **Purpose**: Run commands in running containers without stopping them
- **Interactive Mode**: `-it` flags provide terminal for interactive work
- **Non-Interactive**: Execute single commands and return results
- **Multiple Sessions**: Multiple exec sessions can run simultaneously
- **No Container Restart**: Container's main process continues unaffected

**Interactive vs Non-Interactive:**
- **Interactive (-it)**: For shell access, manual configuration, debugging
- **Non-Interactive**: For automation, scripts, monitoring, log retrieval
- **Exit Behavior**: Exiting interactive shell doesn't stop container
- **Use Cases**: Interactive for exploration, non-interactive for automation

**Container Persistence:**
- **Ephemeral Changes**: Modifications lost when container is removed
- **Container vs Image**: Changes affect container, not source image
- **Data Volumes**: Use volumes for persistent data
- **Image Creation**: Use docker commit to preserve changes as new image
- **Best Practice**: Containerize configuration changes in Dockerfile

**Apache Configuration:**
- **ports.conf**: Controls which ports Apache listens on
- **Virtual Hosts**: Define how Apache responds to different requests
- **Port Matching**: VirtualHost port must match ports.conf Listen directive
- **Multiple Ports**: Apache can listen on multiple ports simultaneously
- **Configuration Syntax**: Apache uses directive-based configuration

**Service Management in Containers:**
- **No systemd**: Minimal containers often lack init systems
- **Direct Control**: Use service control scripts (apache2ctl, nginx, etc.)
- **Foreground vs Background**: Services should run in foreground for Docker
- **Process Supervision**: Container orchestrators handle restart policies
- **Logging**: Configure services to log to stdout/stderr for Docker logging

**Security Considerations:**
- **Root Access**: docker exec typically runs as root inside container
- **User Specification**: Use `-u` flag to run as non-privileged user
- **Container Escape**: Exec doesn't provide additional container security
- **Secrets**: Avoid passing sensitive data via command line (visible in ps)
- **Audit Trail**: Log docker exec usage for security auditing

**Best Practices:**
- **Automation**: Prefer Dockerfile RUN over manual exec for reproducibility
- **Troubleshooting**: Use exec for debugging running containers
- **Configuration**: Use environment variables or mounted configs over exec
- **State Management**: Document all exec changes for team knowledge
- **Testing**: Test configurations in development before production exec

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 39](day-39.md) | [Day 41 →](day-41.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
