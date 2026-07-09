# Day 16: Install and Configure NGINX as Load Balancer

## Task Overview

Configure NGINX as a load balancer to distribute incoming traffic across multiple backend application servers. Implement reverse proxy functionality with proper header forwarding to improve application availability, scalability, and fault tolerance.

**Load Balancer Setup:**
- Install and configure NGINX on load balancer server
- Identify backend application server ports
- Configure upstream server pool
- Implement reverse proxy with load balancing
- Test traffic distribution

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

### Step 1: Identify Backend Server Ports

Check which ports the Apache web servers are listening on across all application servers.

```sh
sudo ss -tlnup
```

This command displays all listening TCP and UDP sockets with process information. The flags mean: `-t` shows TCP sockets, `-l` shows listening sockets, `-n` displays numeric addresses and ports (no DNS resolution), `-u` shows UDP sockets, and `-p` displays process information. The output reveals that Apache (httpd) is listening on port 5001 across the application servers.

**Example Output:**
```shell
Netid     State      Recv-Q     Send-Q         Local Address:Port            Peer Address:Port     Process
udp       UNCONN     0          0                 127.0.0.11:45089                0.0.0.0:*
tcp       LISTEN     0          511                  0.0.0.0:5001                 0.0.0.0:*         users:(("httpd",pid=1690,fd=3),("httpd",pid=1689,fd=3),("httpd",pid=1688,fd=3),("httpd",pid=1680,fd=3))
tcp       LISTEN     0          128                  0.0.0.0:22                   0.0.0.0:*         users:(("sshd",pid=1102,fd=3))
tcp       LISTEN     0          4096              127.0.0.11:42483                0.0.0.0:*
tcp       LISTEN     0          128                     [::]:22                      [::]:*         users:(("sshd",pid=1102,fd=4))
```

From this output, we can see Apache is running on port 5001. This information is crucial for configuring the load balancer to forward traffic to the correct backend port.

### Step 2: Install and Enable NGINX on Load Balancer Server

Install NGINX on the LBR server, enable it to start on boot, and start the service immediately.

```sh
sudo yum install nginx -y
sudo systemctl enable nginx
sudo systemctl start nginx
```

The first command installs NGINX using the YUM package manager with automatic confirmation. The `systemctl enable` command creates symbolic links to start NGINX automatically during system boot, ensuring the load balancer is always available after restarts. The `systemctl start` command immediately starts the NGINX service without waiting for a reboot. This three-step process ensures NGINX is installed, configured for persistence across reboots, and running immediately.

### Step 3: Configure Upstream Backend Servers

Define the pool of backend application servers in NGINX's upstream block.

```nginx
upstream stapp {
    server stapp01:5001;
    server stapp02:5001;
    server stapp03:5001;
}
```

This upstream configuration block defines a group of backend servers named "stapp" that NGINX will distribute traffic across. Each `server` directive specifies a backend hostname and port. NGINX will use round-robin load balancing by default, distributing requests evenly across all three servers. This block should be placed inside the `http {}` context in `/etc/nginx/nginx.conf`, before the server block definitions. The upstream name "stapp" can be referenced in proxy_pass directives.

### Step 4: Configure Reverse Proxy Location Block

Set up the location block to proxy requests to the upstream backend servers with appropriate headers.

```nginx
location / {
    proxy_pass http://stapp;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;

    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";

    proxy_connect_timeout 5s;
    proxy_read_timeout 60s;
}
```

This location block intercepts all requests (`/`) and forwards them to the upstream server pool. The `proxy_pass` directive sends requests to the "stapp" upstream group using round-robin distribution. The `proxy_set_header` directives preserve important client information: `Host` maintains the original hostname, `X-Real-IP` passes the client's actual IP address, `X-Forwarded-For` creates a chain of proxy IPs, and `X-Forwarded-Proto` indicates whether the original request was HTTP or HTTPS. The WebSocket support lines (`Upgrade` and `Connection`) enable WebSocket protocol upgrades. Timeout settings control connection establishment (5 seconds) and read operations (60 seconds), preventing hung connections.

### Step 5: Validate and Apply Configuration

Test the NGINX configuration for syntax errors, then restart the service to apply changes.

```sh
sudo nginx -t
sudo systemctl restart nginx
```

The `nginx -t` command performs a comprehensive configuration test, checking syntax, validating file paths, and ensuring all referenced upstream servers are properly defined. This test runs without affecting the running NGINX instance, preventing service disruption from configuration errors. Only after confirming the configuration is valid should you restart NGINX with `systemctl restart`. The restart command gracefully stops all worker processes and starts new ones with the updated configuration, enabling the load balancing functionality.

---

## Complete NGINX Load Balancer Configuration

Here's the full `/etc/nginx/nginx.conf` configuration with load balancing enabled:

```nginx
# For more information on configuration, see:
#   * Official English Documentation: http://nginx.org/en/docs/
#   * Official Russian Documentation: http://nginx.org/ru/docs/

user nginx;
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

# Load dynamic modules. See /usr/share/doc/nginx/README.dynamic.
include /usr/share/nginx/modules/*.conf;

events {
    worker_connections 1024;
}

http {
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile            on;
    tcp_nopush          on;
    tcp_nodelay         on;
    keepalive_timeout   65;
    types_hash_max_size 4096;

    include             /etc/nginx/mime.types;
    default_type        application/octet-stream;

    # Load modular configuration files from the /etc/nginx/conf.d directory.
    include /etc/nginx/conf.d/*.conf;

    # Define upstream backend server pool
    upstream stapp {
        server stapp01:5001;
        server stapp02:5001;
        server stapp03:5001;
    }

    server {
        listen       80;
        listen       [::]:80;
        server_name  _;

        # Load configuration files for the default server block.
        include /etc/nginx/default.d/*.conf;

        error_page 404 /404.html;
        location = /404.html {
        }

        error_page 500 502 503 504 /50x.html;
        location = /50x.html {
        }

        # Proxy all requests to upstream backend servers
        location / {
            proxy_pass http://stapp;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;

            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";

            proxy_connect_timeout 5s;
            proxy_read_timeout 60s;
        }
    }
}
```

---

## Key Concepts

### Load Balancing Fundamentals

**Purpose and Benefits**: Load balancing distributes incoming network traffic across multiple backend servers, preventing any single server from becoming overwhelmed. This improves application responsiveness, increases availability, enables horizontal scaling, and provides fault tolerance by automatically routing around failed servers.

**High Availability**: When one backend server fails, the load balancer automatically redirects traffic to healthy servers, ensuring continuous service availability. This eliminates single points of failure and increases overall system reliability.

**Scalability**: Load balancers enable horizontal scaling by making it easy to add or remove backend servers without changing client configuration. As traffic increases, simply add more servers to the upstream pool.

**Session Persistence**: Some applications require session stickiness, where a client always connects to the same backend server. This can be configured using IP hash or cookie-based session persistence.

### NGINX Load Balancing Algorithms

**Round Robin (Default)**: Distributes requests sequentially across all backend servers. Each server receives an equal number of requests. This is the default algorithm and works well when backend servers have similar capacity.

**Least Connections**: Routes requests to the server with the fewest active connections, useful when request processing times vary significantly. Enable with `least_conn;` in the upstream block.

**IP Hash**: Routes requests from the same client IP to the same backend server, providing session persistence. Enable with `ip_hash;` in the upstream block. This maintains session state for applications that store data in server memory.

**Weighted Load Balancing**: Assign different weights to servers with different capacities. For example, `server stapp01:5001 weight=3;` routes 3x more traffic to that server compared to servers with weight=1.

**Random**: Randomly selects a backend server for each request. Enable with `random;` in the upstream block. Useful for evenly distributed load when servers have equal capacity.

### Upstream Configuration Options

**Health Checks**: NGINX automatically marks servers as unavailable after failed connection attempts. Configure with `max_fails=3 fail_timeout=30s` to mark a server down after 3 failures within 30 seconds.

**Backup Servers**: Designate backup servers that only receive traffic when primary servers are unavailable. Use `server stapp04:5001 backup;` to create backup servers for disaster recovery.

**Server States**: Temporarily remove servers from rotation with `down` parameter or mark servers for maintenance. For example: `server stapp01:5001 down;` keeps the configuration but stops routing traffic.

**Keepalive Connections**: Reduce latency by maintaining persistent connections to backend servers. Add `keepalive 32;` to the upstream block to maintain up to 32 idle keepalive connections per worker process.

### Reverse Proxy Headers

**Host Header**: The `proxy_set_header Host $host;` directive preserves the original hostname from the client request, ensuring backend applications know which domain was requested. This is critical for applications hosting multiple sites.

**X-Real-IP**: Passes the actual client IP address to backend servers. Without this header, backends only see the load balancer's IP. Applications need this for logging, geolocation, and security features.

**X-Forwarded-For**: Creates a comma-separated list of all proxy IPs in the request chain. The `$proxy_add_x_forwarded_for` variable appends the client IP to any existing X-Forwarded-For header, maintaining the complete proxy chain.

**X-Forwarded-Proto**: Indicates whether the original client request used HTTP or HTTPS. Backend applications need this to generate correct absolute URLs and enforce security policies.

**Custom Headers**: Add application-specific headers as needed. For example, `proxy_set_header X-Request-ID $request_id;` can add unique request IDs for distributed tracing.

### WebSocket Support

**Protocol Upgrade**: WebSocket connections start as HTTP and then upgrade to the WebSocket protocol. The `proxy_http_version 1.1;` directive enables HTTP/1.1, which supports protocol upgrades.

**Upgrade Headers**: The `Upgrade` and `Connection` headers signal the protocol upgrade to backend servers. `$http_upgrade` and `"upgrade"` properly forward these headers.

**Connection Persistence**: WebSocket connections are long-lived. Increase `proxy_read_timeout` significantly (or set to 0 for unlimited) to prevent premature connection termination.

**Load Balancing WebSockets**: Use IP hash load balancing for WebSocket applications to ensure clients maintain connections to the same backend server throughout the session lifecycle.

### Timeout Configuration

**proxy_connect_timeout**: Maximum time (5 seconds in this config) to establish a connection to a backend server. If exceeded, NGINX tries the next server in the upstream pool.

**proxy_read_timeout**: Maximum time (60 seconds) between two successive read operations from the backend server. Prevents hung connections but should be increased for long-running requests.

**proxy_send_timeout**: Maximum time to send data to the backend server. Set this based on the size of uploads your application handles.

**Timeout Strategy**: Balance between failing fast (short timeouts) and accommodating slow operations (long timeouts). Set different timeouts for different location blocks if needed.

### Performance Optimization

**Connection Pooling**: NGINX reuses connections to backend servers through keepalive connections, significantly reducing TCP handshake overhead and improving response times.

**Buffering**: NGINX buffers responses from slow backends, freeing up backend connections quickly. Configure with `proxy_buffering`, `proxy_buffer_size`, and `proxy_buffers` directives.

**Caching**: Implement response caching with `proxy_cache` to reduce backend load and improve response times for cacheable content.

**Compression**: Enable gzip compression to reduce bandwidth usage. NGINX can compress responses before sending to clients.

### Monitoring and Debugging

**Access Logs**: The configured log format includes client IP, timestamp, request details, response status, and X-Forwarded-For chain. Monitor these logs to identify traffic patterns and issues.

**Error Logs**: Check `/var/log/nginx/error.log` for upstream connection failures, timeout errors, and configuration problems. Set `error_log` level to `warn`, `error`, or `debug`.

**Upstream Status**: Use the NGINX Plus status module or third-party modules to monitor backend server health, connection counts, and response times in real-time.

**Testing Load Distribution**: Use tools like `ab` (Apache Bench) or `wrk` to generate load and verify traffic is distributed evenly across backend servers. Check backend server logs to confirm.

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 15](day-15.md) | [Day 17 →](day-17.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
