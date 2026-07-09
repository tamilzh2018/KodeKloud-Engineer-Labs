# Day 19: Install and Configure Web Application

## Task Overview

Deploy static website content on Apache web server with custom port configuration. Transfer website files from jump host to application server and configure Apache to serve multiple website directories.

**Web Application Deployment:**
- Install Apache HTTP Server
- Configure custom port (6400)
- Transfer website files securely
- Deploy multiple static sites
- Verify web server functionality

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

### Step 1: Install Apache Web Server

Install the Apache HTTP Server package on the target application server.

```sh
sudo yum install -y httpd
```

This command uses YUM package manager to install the Apache HTTP Server (httpd package) along with all its dependencies. The `-y` flag automatically confirms the installation without prompting for user interaction. Apache is one of the most widely used web servers, known for its stability, performance, and extensive module ecosystem. After installation, the httpd binary and configuration files will be available, but the service won't start automatically.

### Step 2: Configure Custom Port and Backup Configuration

Create a backup of the Apache configuration file and change the listening port from default 80 to 6400.

```sh
sudo cp /etc/httpd/conf/httpd.conf /etc/httpd/conf/httpd.conf.bak
sudo sed -i 's/80/6400/g' /etc/httpd/conf/httpd.conf
```

The first command creates a backup copy of the main Apache configuration file, which is essential before making modifications. Having a backup allows you to revert changes if something goes wrong. The `sed` command performs an in-place substitution (`-i` flag) that replaces all occurrences of "80" with "6400" throughout the configuration file. This changes both the `Listen` directive and any `VirtualHost` definitions that reference port 80. Using a non-standard port is common when the default port is already in use, for security through obscurity, or when firewall rules require specific ports.

### Step 3: Start Apache Service

Restart the Apache service to apply the port configuration changes.

```sh
sudo systemctl restart httpd
```

The `systemctl restart` command stops and then starts the Apache service, loading the new configuration with the custom port 6400. If Apache was already running, this ensures all worker processes reload with the new settings. If this is the first start, it initializes Apache with the modified configuration. Any syntax errors in the configuration will prevent Apache from starting, so it's good practice to run `httpd -t` to test configuration syntax before restarting.

### Step 4: Transfer Website Files from Jump Host

Use secure copy (SCP) to transfer website directories from the jump host to the application server.

```sh
scp -r /home/thor/official banner@stapp03:/home/banner
scp -r /home/thor/games banner@stapp03:/home/banner/
```

The `scp` command securely copies files over SSH between hosts. The `-r` flag enables recursive copying, which copies entire directory structures including all subdirectories and files. The syntax is `scp source destination`, where the destination uses `user@host:path` format. The first command transfers the "official" website directory from the jump host to the banner user's home directory on stapp03. The second command transfers the "games" directory. These commands must be run from the jump host, and the banner user must have SSH access to stapp03.

### Step 5: Deploy Websites to Apache Document Root

Copy the website directories to Apache's document root directory.

```sh
sudo cp -r /home/banner/official /var/www/html/
sudo cp -r /home/banner/games /var/www/html
```

The `cp -r` command recursively copies the website directories to `/var/www/html/`, which is Apache's default document root. The `-r` flag ensures all subdirectories and files are copied. After these commands, the websites will be accessible at URLs like `http://server:6400/official/` and `http://server:6400/games/`. The `sudo` prefix is necessary because `/var/www/html/` is owned by root, and regular users don't have write permissions. This directory structure creates subdirectory-based hosting, where different applications are served from different URL paths.

### Step 6: Verify Web Server Functionality

Test that Apache is serving the websites correctly using curl from localhost.

```sh
curl http://localhost:6400/games/
curl http://localhost:6400/official/
```

The `curl` command makes HTTP requests to test web server functionality. Testing from localhost (127.0.0.1) verifies that Apache is listening on port 6400 and can serve content, independent of network firewall rules. The first command requests the games website, and the second requests the official website. Both should return HTML content. If these commands fail, check Apache's error logs at `/var/log/httpd/error_log` for troubleshooting information. Testing locally before testing remotely helps isolate whether issues are with the web server configuration or network connectivity.

**Expected Output:**
```html
<!DOCTYPE html>
<html>
<body>

<h1>KodeKloud</h1>

<p>This is a sample page for our official website</p>

</body>
</html>
```

This HTML output confirms that Apache is correctly serving static content from the official website directory. The games website should produce similar HTML output with different content.

---

## Key Concepts

### Apache Configuration Structure

**Main Configuration File**: The `/etc/httpd/conf/httpd.conf` file contains global Apache settings including the server root, document root, listening ports, user/group to run as, and module loading directives. This file controls the overall behavior of the Apache web server.

**Configuration Directories**: Additional configuration files can be placed in `/etc/httpd/conf.d/` for modular configuration. Apache automatically includes all `.conf` files from this directory, allowing you to separate concerns (SSL config, virtual hosts, etc.) into individual files.

**Document Root**: The `DocumentRoot` directive specifies the directory from which Apache serves files. The default is typically `/var/www/html/`. Requests to `http://server/path/file.html` map to `/var/www/html/path/file.html` on the filesystem.

**Directory Directives**: `<Directory>` blocks control access and behavior for specific filesystem paths. They can enable/disable directory indexing, set authentication requirements, and configure options like following symbolic links.

### Port Configuration

**Listen Directive**: The `Listen` directive tells Apache which IP addresses and ports to bind to. `Listen 80` listens on all interfaces on port 80. `Listen 192.168.1.100:8080` listens only on a specific IP and port.

**VirtualHost Ports**: When using virtual hosts, the `<VirtualHost>` directive must match a listening port. If you change `Listen 80` to `Listen 6400`, you must also change `<VirtualHost *:80>` to `<VirtualHost *:6400>`.

**Multiple Ports**: Apache can listen on multiple ports simultaneously by adding multiple `Listen` directives. This allows serving HTTP on port 80 and an admin interface on port 8080, for example.

**Port Selection**: Ports below 1024 are privileged and require root access to bind. Ports 1024-65535 can be used by non-privileged processes. Common alternative ports include 8080, 8000, and 8443 (HTTPS alternative).

### File Transfer Methods

**SCP (Secure Copy Protocol)**: Uses SSH for authentication and encryption, providing secure file transfer. SCP is simple but doesn't resume interrupted transfers or preserve all filesystem attributes in all cases.

**RSYNC**: More advanced than SCP, rsync efficiently transfers only changed portions of files, preserves permissions and timestamps, and can resume interrupted transfers. Useful for synchronizing large directory structures.

**SFTP (SSH File Transfer Protocol)**: Provides an interactive file transfer session over SSH with commands similar to FTP but with encryption. More flexible than SCP for browsing and selective file transfer.

**Configuration Management**: For production environments, tools like Ansible, Puppet, or Chef are preferred over manual file transfers, as they provide idempotency, version control, and automation.

### Static vs Dynamic Content

**Static Content**: HTML, CSS, JavaScript, images, and other files served directly from the filesystem without server-side processing. Apache excels at serving static content efficiently, using sendfile system calls when possible.

**Dynamic Content**: Content generated on-the-fly by server-side languages like PHP, Python, or Ruby. Requires additional modules (mod_php, mod_wsgi) or FastCGI/proxy configurations to connect Apache with application servers.

**Caching**: Static content can be cached at multiple levels - browser cache, CDN cache, and Apache's mod_cache. Dynamic content can also be cached but requires careful consideration of cache invalidation.

**Performance**: Static content has minimal server overhead. Dynamic content requires CPU for processing and often database queries, making it more resource-intensive per request.

### Directory-Based Website Hosting

**Subdirectory Access**: Placing websites in subdirectories of document root creates URL paths like `http://server/app1/` and `http://server/app2/`. This is simpler than virtual hosts but shares the same domain/IP.

**Index Files**: When accessing a directory URL (ending in `/`), Apache looks for index files defined by the `DirectoryIndex` directive (typically `index.html`, `index.php`). If found, that file is served; otherwise, a directory listing may be shown if enabled.

**Access Control**: Use `<Directory>` blocks to set different access controls for different subdirectories. For example, you might require authentication for `/admin/` but allow public access to `/public/`.

**URL Rewriting**: mod_rewrite can transform URLs before processing, allowing pretty URLs like `/article/123` to map to `/article.php?id=123` or routing all requests for an application through a single entry point.

### Apache Virtual Hosts

**Name-Based Virtual Hosts**: Multiple websites on a single IP, distinguished by the `Host` HTTP header (domain name). Apache routes requests to different `<VirtualHost>` blocks based on the `ServerName` directive.

**IP-Based Virtual Hosts**: Different websites on different IP addresses. Less common now due to IPv4 scarcity but sometimes used for SSL/TLS (though SNI has largely eliminated this need).

**Port-Based Virtual Hosts**: Different websites on different ports of the same IP. Useful for separating public and admin interfaces or running multiple applications on a single server.

**Virtual Host Configuration**: Each virtual host can have its own `DocumentRoot`, error/access logs, SSL certificates, and other settings, providing complete isolation between hosted sites.

### Filesystem Permissions

**Apache User**: Apache typically runs as the `apache` or `www-data` user (depending on distribution). Files must be readable by this user, and directories must be readable and executable (searchable).

**Recommended Permissions**: Files should be `644` (rw-r--r--) and directories `755` (rwxr-xr-x). This allows Apache to read content while preventing Apache from modifying files (defense in depth).

**Ownership**: Web content is often owned by a deployment user with Apache having group read access, or owned by root with world-readable permissions. Avoid making files writable by the Apache user unless necessary (upload directories, cache).

**SELinux Contexts**: On SELinux-enabled systems, files in document root need the `httpd_sys_content_t` context. Use `chcon` or `semanage fcontext` to set appropriate contexts.

### Testing and Troubleshooting

**Local Testing**: Test with `curl http://localhost:port/` before testing remotely. This isolates web server issues from network/firewall issues.

**Remote Testing**: Test from external hosts with `curl http://server:port/` or browsers. If local works but remote doesn't, investigate firewalls, SELinux, or network routing.

**Error Logs**: Apache logs errors to `/var/log/httpd/error_log`. Check this file for configuration errors, permission issues, or runtime errors.

**Access Logs**: Request logs at `/var/log/httpd/access_log` show all requests with timestamps, status codes, and bytes transferred. Useful for monitoring traffic and debugging.

**Configuration Testing**: Run `httpd -t` or `apachectl configtest` to validate configuration syntax without restarting Apache. This catches typos and structural errors before they cause downtime.

### Security Considerations

**Disable Directory Listing**: Set `Options -Indexes` to prevent Apache from displaying directory contents when no index file exists. Exposing directory structures can reveal sensitive information.

**Hide Server Information**: Use `ServerTokens Prod` and `ServerSignature Off` to minimize server information disclosed in HTTP headers and error pages, reducing attack surface reconnaissance.

**Access Control**: Use `Require` directives to restrict access to sensitive directories. `Require all denied` blocks all access, while `Require ip 192.168.1.0/24` allows only specific networks.

**Content Security**: Validate and sanitize any user-provided content before serving it. Even static sites can be vulnerable if user-uploaded content is served without proper validation.

**Regular Updates**: Keep Apache updated with security patches. Subscribe to security mailing lists and monitor CVE databases for vulnerabilities affecting your Apache version.

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 18](day-18.md) | [Day 20 →](day-20.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
