# Day 15: Setup SSL for NGINX

## Task Overview

Configure SSL/TLS encryption for NGINX web server to secure HTTP traffic. Deploy self-signed certificates and implement HTTPS with automatic HTTP to HTTPS redirection.

**SSL Configuration:**
- Install and configure NGINX web server
- Deploy SSL certificates and private keys
- Configure HTTPS server blocks
- Implement HTTP to HTTPS redirection

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

### Step 1: Install NGINX Web Server

Install the NGINX package using YUM package manager with automatic yes to all prompts.

```sh
sudo yum install nginx -y
```

This command installs NGINX and all required dependencies. The `-y` flag automatically confirms the installation without prompting for user confirmation. NGINX is a high-performance web server that can also function as a reverse proxy, load balancer, and HTTP cache.

### Step 2: Create Welcome Page Content

Create a simple HTML welcome page in NGINX's default document root directory.

```sh
echo "Welcome!" | sudo tee /usr/share/nginx/html/index.html
```

This command uses `echo` to generate the content "Welcome!" and pipes it through `tee` to write it to NGINX's default index.html file. The `tee` command writes to the file while also displaying output to the terminal. The document root `/usr/share/nginx/html/` is NGINX's default location for serving static web content.

### Step 3: Start NGINX and Verify HTTP Access

Restart the NGINX service to load the new configuration and test HTTP connectivity.

```sh
sudo systemctl restart nginx
curl http://stapp03
```

The `systemctl restart` command stops and starts the NGINX service, ensuring all configurations are loaded. The `curl` command then tests HTTP access to the server using its hostname (stapp03), which should return the "Welcome!" message created in the previous step. This confirms NGINX is properly serving content over HTTP before configuring SSL.

### Step 4: Prepare SSL Certificate Directory

Create a dedicated directory for SSL certificates and copy the provided certificate files.

```sh
sudo mkdir -p /etc/certs
sudo cp /tmp/nautilus.* /etc/certs
```

The `mkdir -p` command creates the `/etc/certs` directory, with the `-p` flag ensuring parent directories are created if they don't exist. The second command copies both the SSL certificate (nautilus.crt) and private key (nautilus.key) from the temporary directory to the new certs directory. The wildcard pattern `nautilus.*` matches both files in a single command.

### Step 5: Edit NGINX Configuration File

Open the main NGINX configuration file for editing to add SSL configuration.

```sh
sudo vi /etc/nginx/nginx.conf
```

This opens NGINX's main configuration file in the vi text editor with sudo privileges. The configuration file contains server blocks, upstream definitions, and global settings. You'll need to modify this file to enable SSL and configure HTTP to HTTPS redirection.

### Step 6: Configure HTTP to HTTPS Redirection

Add a 301 permanent redirect inside the HTTP server block (port 80) to redirect all HTTP traffic to HTTPS.

```nginx
return 301 https://$host$request_uri;
```

This line should be added inside the `server { listen 80; }` block, just after the `server_name` directive. The `return 301` directive sends a permanent redirect response to clients. The `$host` variable contains the requested hostname, and `$request_uri` contains the full URI including query parameters. This ensures users accessing http://example.com/page will be redirected to https://example.com/page, maintaining the full path and query string.

### Step 7: Configure SSL Certificate Paths

Uncomment and configure the HTTPS server block (port 443) with SSL certificate locations.

```nginx
ssl_certificate     /etc/certs/nautilus.crt;
ssl_certificate_key /etc/certs/nautilus.key;
```

These directives should be added inside the `server { listen 443 ssl; }` block. The `ssl_certificate` directive specifies the path to the public SSL certificate file, while `ssl_certificate_key` points to the private key file. NGINX requires both files to establish secure HTTPS connections. The certificate file can be shared publicly, but the private key must be kept secure with restricted permissions (typically 600 or 400).

### Step 8: Test NGINX Configuration Syntax

Validate the NGINX configuration file syntax before applying changes.

```sh
sudo nginx -t
```

This command performs a configuration test without actually restarting NGINX. It checks for syntax errors, verifies file paths exist, and validates SSL certificate/key pairs match. If successful, it displays "syntax is ok" and "test is successful". Always run this test before restarting NGINX to avoid service disruption due to configuration errors.

### Step 9: Apply SSL Configuration

Restart NGINX to apply the new SSL configuration and enable HTTPS.

```sh
sudo systemctl restart nginx
```

This restart command reloads all configuration changes, enabling the SSL server block and HTTP to HTTPS redirection. After restart, NGINX will listen on both port 80 (HTTP) and port 443 (HTTPS). All HTTP requests will be automatically redirected to HTTPS, ensuring encrypted communication for all connections.

### Step 10: Verify SSL Configuration

Test HTTPS access to confirm SSL is properly configured.

```sh
curl -k https://stapp03
```

The `curl -k` command tests HTTPS connectivity, with the `-k` flag allowing insecure connections to self-signed certificates. This is necessary because self-signed certificates aren't trusted by default certificate authorities. In production, you would use certificates from trusted CAs like Let's Encrypt. The command should return the "Welcome!" message over an encrypted HTTPS connection.

---

## Key Concepts

### SSL/TLS Fundamentals

**Purpose and Security**: SSL/TLS (Secure Sockets Layer/Transport Layer Security) encrypts data transmitted between clients and servers, preventing eavesdropping and man-in-the-middle attacks. TLS is the modern successor to SSL, but the terms are often used interchangeably.

**Certificate Components**: An SSL certificate contains the server's public key, domain information, and is signed by a Certificate Authority (CA). The private key must be kept secure and is used to decrypt data encrypted with the public key.

**Self-Signed Certificates**: These certificates are signed by the same entity that uses them, rather than a trusted CA. They provide encryption but not authentication, making them suitable for testing and internal applications but not for public-facing production websites.

**Certificate Validation**: Browsers validate certificates by checking the CA signature, expiration date, domain name match, and revocation status. Self-signed certificates fail this validation, triggering security warnings.

### NGINX SSL Configuration

**SSL Directives**: NGINX uses `ssl_certificate` for the certificate chain file and `ssl_certificate_key` for the private key. Additional directives like `ssl_protocols` and `ssl_ciphers` control security settings.

**Server Blocks**: NGINX uses separate server blocks for HTTP (port 80) and HTTPS (port 443). The `listen 443 ssl` directive enables SSL for that server block.

**SSL Session Cache**: Configure `ssl_session_cache` and `ssl_session_timeout` to improve performance by reusing SSL session parameters, reducing the overhead of SSL handshakes.

**Perfect Forward Secrecy**: Use `ssl_prefer_server_ciphers on` and configure strong cipher suites to ensure secure key exchange mechanisms that protect past sessions even if the private key is compromised.

### HTTP to HTTPS Redirection

**301 vs 302 Redirects**: Use `return 301` for permanent redirects, which tells browsers and search engines that HTTP is permanently replaced by HTTPS. 302 is for temporary redirects and shouldn't be used for HTTPS enforcement.

**Variable Preservation**: The `$host` and `$request_uri` variables preserve the original hostname and full path, ensuring users reach the exact HTTPS version of the page they requested.

**SEO Impact**: Permanent HTTPS redirects maintain search engine rankings by properly signaling that content has moved to the secure protocol.

**Alternative Methods**: Instead of `return 301`, you can use `rewrite ^ https://$host$request_uri? permanent;` or configure all content to only serve over HTTPS by removing the HTTP server block entirely.

### Security Best Practices

**Strong Protocols**: Disable outdated protocols like SSLv3 and TLS 1.0. Use `ssl_protocols TLSv1.2 TLSv1.3;` to support only modern, secure protocols.

**Cipher Suite Selection**: Configure strong ciphers using `ssl_ciphers HIGH:!aNULL:!MD5;` to prevent weak encryption algorithms while maintaining compatibility.

**HSTS (HTTP Strict Transport Security)**: Add the header `Strict-Transport-Security: max-age=31536000; includeSubDomains` to force browsers to always use HTTPS for future requests.

**Certificate Permissions**: Set private key permissions to 600 (readable only by owner) using `chmod 600 /etc/certs/nautilus.key` to prevent unauthorized access to cryptographic keys.

### Certificate Management

**Let's Encrypt**: For production environments, use Let's Encrypt to obtain free, automated, trusted SSL certificates. The `certbot` tool automates certificate issuance and renewal.

**Certificate Renewal**: SSL certificates expire (typically 90 days for Let's Encrypt, 1 year for commercial CAs). Implement automated renewal processes to prevent service disruption.

**Certificate Chain**: Include intermediate certificates in the `ssl_certificate` file to complete the chain of trust from your certificate to the root CA that browsers trust.

**Monitoring**: Set up monitoring to alert before certificate expiration. Tools like `openssl s_client -connect domain.com:443` can verify certificate details and expiration dates.

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 14](../week-02/day-14.md) | [Day 16 →](day-16.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
