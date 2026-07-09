# Day 20: Configure Nginx + PHP-FPM Using Unix Socket

## Task Overview

Deploy NGINX web server with PHP-FPM (FastCGI Process Manager) using Unix socket communication for optimal performance. Configure NGINX on a custom port, install a specific PHP version, and establish communication between NGINX and PHP-FPM through Unix sockets.

**NGINX + PHP-FPM Setup:**
- Update system packages
- Install NGINX web server
- Install PHP-FPM with specific version
- Configure Unix socket communication
- Integrate NGINX with PHP-FPM
- Enable and start services

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

### Step 1: Update Packages and Install NGINX and PHP

Update system repositories and install NGINX web server along with PHP 8.2 module.

```sh
sudo dnf update -y
sudo dnf install nginx -y
sudo dnf module install php:8.2 -y
```

The first command updates all installed packages and refreshes package repository metadata using the DNF package manager (the successor to YUM on modern RHEL-based systems). The `-y` flag automatically confirms all prompts. The second command installs NGINX, a high-performance web server and reverse proxy known for its efficiency in serving static content and proxying dynamic requests. The third command uses DNF's modular system to install PHP version 8.2 specifically, which includes PHP-FPM and all core extensions. The modular approach allows multiple PHP versions to coexist on the same system.

### Step 2: Create PHP-FPM Socket Directory

Create the directory that will contain the PHP-FPM Unix socket file.

```sh
sudo mkdir -p /var/run/php-fpm
sudo vi /etc/php-fpm.d/www.conf
```

The `mkdir -p` command creates the `/var/run/php-fpm` directory, with the `-p` flag ensuring parent directories are created if they don't exist and preventing errors if the directory already exists. This directory will house the Unix socket file that NGINX uses to communicate with PHP-FPM. The second command opens the main PHP-FPM pool configuration file in the vi text editor for modification. This file configures the default "www" pool, which handles PHP requests.

### Step 3: Configure PHP-FPM Unix Socket

Edit the PHP-FPM pool configuration to use the custom Unix socket path.

**Find and modify this line:**
```conf
listen = /run/php-fpm/www.sock
```

**Change it to:**
```conf
listen = /var/run/php-fpm/default.sock
```

The `listen` directive specifies how PHP-FPM accepts connections from the web server. By default, it's configured to listen on `/run/php-fpm/www.sock`, but we're changing it to `/var/run/php-fpm/default.sock` to match our directory structure and naming convention. Unix sockets provide faster inter-process communication than TCP sockets when both processes are on the same server, as they bypass the network stack entirely. The socket file will be created automatically when PHP-FPM starts.

### Step 4: Configure NGINX Port

Edit the main NGINX configuration file to change the listening port from 80 to 8093.

```sh
sudo vi /etc/nginx/nginx.conf
```

**Find and modify:**
```nginx
listen       80;
listen       [::]:80;
```

**Change to:**
```nginx
listen       8093;
listen       [::]:8093;
```

Open `/etc/nginx/nginx.conf` and locate the `server` block containing the `listen` directives. Change port 80 to 8093 for both IPv4 and IPv6 listeners. The first `listen` directive handles IPv4 connections, while `[::]:8093` handles IPv6 connections on the same port. Custom ports are used when standard ports are unavailable, for security reasons, or when running multiple web servers on the same host.

### Step 5: Configure NGINX PHP-FPM Integration

Create or edit the PHP configuration file to enable NGINX to process PHP files through PHP-FPM.

```sh
sudo vi /etc/nginx/default.d/php.conf
```

**Find this line:**
```nginx
fastcgi_pass php-fpm;
```

**Change it to:**
```nginx
fastcgi_pass unix:/var/run/php-fpm/default.sock;
```

This configuration file defines how NGINX handles PHP files. The `fastcgi_pass` directive tells NGINX where to forward PHP requests. The default configuration uses a named upstream called "php-fpm", but we're changing it to directly reference our Unix socket at `unix:/var/run/php-fpm/default.sock`. This creates a FastCGI connection to PHP-FPM through the socket we configured earlier. The `unix:` prefix is required to indicate a Unix socket path rather than a TCP address.

### Step 6: Enable and Start Services

Enable both services to start automatically on boot and start them immediately.

```sh
sudo systemctl enable --now nginx
sudo systemctl enable --now php-fpm
```

The `systemctl enable --now` command performs two operations: enabling the service to start automatically during system boot (creating appropriate systemd symlinks) and starting the service immediately. The first command handles NGINX, and the second handles PHP-FPM. This ensures both services are running and will restart automatically after system reboots, critical for production environments.

### Step 7: Verify Configuration

Test the PHP-FPM integration by making a request to a PHP file.

```sh
curl http://stapp01:8093/index.php
```

This curl command tests the complete stack by requesting a PHP file through NGINX on port 8093. NGINX should receive the request, recognize index.php as a PHP file, forward it to PHP-FPM through the Unix socket, receive the processed output, and return it. If successful, you'll see the HTML output generated by the PHP script. If this fails, check NGINX error logs (`/var/log/nginx/error.log`) and PHP-FPM logs (`/var/log/php-fpm/www-error.log`) for troubleshooting.

---

## Key Concepts

### PHP-FPM (FastCGI Process Manager)

**Process Manager**: PHP-FPM is a high-performance FastCGI implementation specifically designed for PHP. It manages a pool of PHP worker processes that handle incoming requests from web servers like NGINX.

**Performance Benefits**: PHP-FPM significantly outperforms older methods like mod_php (Apache module) by using persistent processes that don't need to initialize PHP for each request. This reduces overhead and improves response times, especially under high load.

**Process Management Modes**: PHP-FPM supports three process management modes: static (fixed number of workers), dynamic (adjusts workers based on load), and ondemand (spawns workers only when needed). Dynamic mode balances performance and resource usage.

**Resource Isolation**: Each PHP-FPM pool can run under different user accounts, with different PHP configurations, and separate resource limits. This provides isolation between applications and improves security.

### Unix Socket vs TCP Socket Communication

**Unix Sockets**: Unix domain sockets are inter-process communication (IPC) mechanisms that work like network sockets but operate within a single host. They use filesystem paths (like `/var/run/php-fpm/default.sock`) as addresses.

**Performance Advantages**: Unix sockets are significantly faster than TCP sockets for local communication because they bypass the network stack entirely. No TCP/IP overhead, no routing tables, no network buffer management - just direct kernel memory operations.

**Security Benefits**: Unix sockets use filesystem permissions for access control. Only processes with read/write permissions on the socket file can connect, providing simple yet effective security without firewall configuration.

**Limitations**: Unix sockets only work for processes on the same machine. If your web server and PHP-FPM run on different servers, you must use TCP sockets instead (e.g., `fastcgi_pass 127.0.0.1:9000`).

### NGINX + PHP-FPM Architecture

**Request Flow**: Client sends HTTP request → NGINX receives request → NGINX determines request is for PHP → NGINX forwards to PHP-FPM via socket → PHP-FPM worker executes PHP code → Result sent back to NGINX → NGINX returns response to client.

**Separation of Concerns**: NGINX handles static content directly and efficiently. PHP-FPM only processes PHP scripts, allowing each component to excel at its specific task. NGINX can serve thousands of static file requests while a few PHP-FPM workers handle dynamic content.

**Scalability**: This architecture scales horizontally easily. You can run multiple PHP-FPM pools on different servers, with NGINX load balancing between them. You can also tune worker counts independently for web server and PHP processing.

**Stability**: PHP crashes don't affect NGINX. If PHP-FPM crashes, NGINX continues serving static content and returns 502 errors for PHP requests until PHP-FPM recovers. This is much better than Apache with mod_php, where a PHP crash could bring down the entire web server.

### PHP-FPM Configuration

**Pool Configuration**: PHP-FPM uses pools (defined in `/etc/php-fpm.d/`) to group worker processes. Each pool has its own configuration including listen address, process management settings, and PHP ini directives.

**Process Management**: Key directives include `pm` (process manager type), `pm.max_children` (maximum workers), `pm.start_servers` (initial workers), `pm.min_spare_servers` (minimum idle), and `pm.max_spare_servers` (maximum idle).

**Listen Socket**: The `listen` directive can be a Unix socket (`/path/to/socket`) or TCP socket (`127.0.0.1:9000`). For Unix sockets, configure `listen.owner`, `listen.group`, and `listen.mode` to ensure NGINX can access the socket.

**PHP Configuration**: Use `php_value` and `php_admin_value` directives in pool configuration to set PHP ini settings per pool. This allows different memory limits, error reporting, and other settings for different applications.

### NGINX FastCGI Configuration

**FastCGI Protocol**: FastCGI is a binary protocol that extends CGI (Common Gateway Interface) with persistent processes and multiplexing. It's more efficient than spawning a new process for each request.

**Essential Directives**: `fastcgi_pass` specifies where to send PHP requests. `fastcgi_param` directives set environment variables that PHP-FPM receives. `fastcgi_index` sets the default file when a directory is requested.

**Standard Parameters**: NGINX must send specific FastCGI parameters to PHP-FPM, including `SCRIPT_FILENAME` (filesystem path to the PHP file), `QUERY_STRING`, `REQUEST_METHOD`, and others. These are typically included via `include fastcgi_params;`.

**Security Considerations**: Always set `fastcgi_split_path_info` and check that the requested file exists before passing to PHP-FPM. This prevents security issues where malicious requests might execute PHP code in uploaded files.

### Communication Performance

**Latency Comparison**: Unix sockets have near-zero latency (microseconds) compared to TCP sockets (milliseconds) even on localhost. For high-traffic sites processing millions of requests daily, this difference compounds significantly.

**Throughput**: Unix sockets can handle higher throughput because they don't have TCP congestion control, windowing, or acknowledgment overhead. All data transfer happens through direct memory operations in the kernel.

**Resource Usage**: Unix sockets consume fewer system resources - no ports to manage, no TCP state machines, smaller memory footprint. This leaves more resources available for application processing.

**Connection Overhead**: Establishing Unix socket connections is faster than TCP connections (no three-way handshake). PHP-FPM maintains persistent connections, but the initial connection and reconnection after failures benefit from Unix socket speed.

### DNF Package Manager

**Modern Package Management**: DNF (Dandified YUM) is the next-generation package manager for RHEL, Fedora, and CentOS. It resolves dependencies better, has improved performance, and uses less memory than YUM.

**Modular Streams**: DNF modules allow multiple versions of software to be available simultaneously. `dnf module list php` shows available PHP versions. `dnf module install php:8.2` installs a specific version stream.

**Transaction Safety**: DNF uses libsolv for dependency resolution, providing more reliable installations. It can detect and prevent conflicting installations better than YUM.

**Automatic Updates**: Configure `dnf-automatic` for scheduled security updates. This keeps systems patched without manual intervention, critical for production servers.

### PHP Version Management

**Version Specificity**: Different applications may require different PHP versions. Using DNF modules allows installing specific versions like PHP 7.4, 8.0, 8.1, or 8.2 based on application compatibility.

**Multiple Versions**: You can run multiple PHP-FPM pools with different PHP versions simultaneously. Configure each pool with its own socket and PHP binary, allowing different applications to use different PHP versions on the same server.

**Upgrading Strategy**: Test applications with new PHP versions in staging before production. PHP-FPM's pool isolation allows gradual migration - run new PHP version in parallel, switch applications one at a time, then retire old version.

**Extensions**: Different PHP versions may have different available extensions. Use `dnf module install php:8.2/common` to install common extensions, or individual packages like `php-mysql`, `php-gd`, `php-mbstring`.

### Monitoring and Troubleshooting

**PHP-FPM Status**: Enable the PHP-FPM status page by adding `pm.status_path = /status` in pool configuration and configuring NGINX location block. This shows active workers, queue length, and request rates.

**Log Files**: PHP-FPM logs to `/var/log/php-fpm/www-error.log` (errors) and `/var/log/php-fpm/www-slow.log` (slow requests). NGINX logs to `/var/log/nginx/error.log` and `/var/log/nginx/access.log`.

**Socket Permissions**: If NGINX can't connect to PHP-FPM, check socket file permissions with `ls -l /var/run/php-fpm/default.sock`. Ensure NGINX user (usually `nginx`) has read/write access.

**Process Monitoring**: Use `systemctl status php-fpm` to check service status. Use `ps aux | grep php-fpm` to see running worker processes. Monitor with tools like `htop` or `top` to track resource usage.

### Security Best Practices

**Separate Users**: Run PHP-FPM pools under dedicated users, not root or the web server user. This limits damage if a PHP application is compromised.

**Disable Dangerous Functions**: Use `disable_functions` in PHP configuration to prohibit functions like `exec()`, `system()`, `shell_exec()` that aren't needed by your application.

**Open Basedir**: Set `open_basedir` to restrict PHP file access to specific directories. This prevents PHP scripts from accessing arbitrary files on the system.

**Limit Resources**: Configure `memory_limit`, `max_execution_time`, and `upload_max_filesize` appropriately. This prevents resource exhaustion attacks and constrains potential exploits.

**Keep Updated**: Regularly update PHP and PHP-FPM to patch security vulnerabilities. Subscribe to PHP security announcements and test updates in staging before production.

---

## Validation

Test your solution using KodeKloud's automated validation. Verify PHP is processing correctly by accessing the application through the LBR interface.

---

[← Day 19](day-19.md) | [Day 21 →](day-21.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
