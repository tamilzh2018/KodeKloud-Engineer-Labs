# Day 11: Install and Setup Tomcat Server

## Task Overview

The Nautilus application development team recently finished the beta version of one of their Java-based applications, which they are planning to deploy on one of the app servers in Stratos DC. After an internal team meeting, they have decided to use the Tomcat application server.

**Objectives:**
1. Install Tomcat server on App Server 1
2. Configure it to run on port 8086
3. Deploy a ROOT.war file from the jump host at location `/tmp`
4. Ensure the webpage works directly on base URL: `curl http://stapp01:8086`

**Requirements:**
- Tomcat installation and configuration
- Custom port configuration
- WAR file deployment
- Service management and firewall rules
- Operational validation

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

### Step 1: Install Java Development Kit (JDK)

Install OpenJDK 8, which is required to run Tomcat.

```bash
sudo yum install java-1.8.0-openjdk-devel -y
```

**Explanation:** This command installs the Java 8 OpenJDK Development Kit using yum, the package manager for RHEL/CentOS systems. Tomcat requires a Java Runtime Environment (JRE) or JDK to execute Java servlets and JSP pages. The `-devel` package includes development tools and headers needed for compiling Java applications. The `-y` flag automatically answers "yes" to installation prompts, enabling unattended installation. OpenJDK 8 provides long-term stability and compatibility with most Java enterprise applications.

**Verify Java installation:**
```bash
java -version
```

**Expected output:**
```bash
openjdk version "1.8.0_362"
OpenJDK Runtime Environment (build 1.8.0_362-b09)
OpenJDK 64-Bit Server VM (build 25.362-b09, mixed mode)
```

### Step 2: Create Tomcat System User

Create a dedicated system user for running Tomcat with security best practices.

```bash
sudo groupadd tomcat
sudo useradd -M -U -d /opt/tomcat -s /bin/nologin -g tomcat tomcat
```

**Explanation:** These commands create a dedicated system account for running the Tomcat service, following the principle of least privilege.

**First command** creates a system group named `tomcat` that will own Tomcat files and processes.

**Second command** creates the tomcat user with specific security-focused options:
- `-M`: No home directory creation (system account doesn't need a personal home)
- `-U`: Create a user private group matching the username (though we override with `-g`)
- `-d /opt/tomcat`: Set home directory to Tomcat installation location (used for file ownership context)
- `-s /bin/nologin`: Disable interactive shell login (prevents direct login as this account)
- `-g tomcat`: Assign primary group as tomcat

This configuration ensures Tomcat runs with minimal privileges, cannot be used for interactive login, and isolates file ownership from regular user accounts—critical security practices for internet-facing services.

### Step 3: Create Tomcat Installation Directory

Prepare the directory structure for Tomcat installation.

```bash
sudo mkdir -p /opt/tomcat
```

**Explanation:** The `mkdir -p` command creates the `/opt/tomcat` directory where Tomcat will be installed. The `/opt` directory is the standard Linux location for optional or third-party software not managed by the system package manager. The `-p` flag creates parent directories if needed and doesn't error if the directory exists, making the command idempotent (safe to run multiple times). This location provides a clean separation from system directories and simplifies permission management.

### Step 4: Download and Extract Tomcat

Download the Tomcat 9.0.80 binary distribution and extract it.

```bash
wget https://archive.apache.org/dist/tomcat/tomcat-9/v9.0.80/bin/apache-tomcat-9.0.80.tar.gz
sudo tar -xf apache-tomcat-9.0.80.tar.gz -C /opt/tomcat --strip-components=1
```

**Explanation:**

**First command** uses `wget` to download the Tomcat binary distribution from Apache's official archive. The URL points to Tomcat 9.0.80, a stable release providing modern Servlet and JSP API support. Wget is a non-interactive downloader ideal for scripts and remote systems without graphical interfaces.

**Second command** extracts the tarball with specific options:
- `tar -xf`: Extract files from the archive (`-x` extract, `-f` specify file)
- `-C /opt/tomcat`: Change to target directory before extraction
- `--strip-components=1`: Remove the first directory level (apache-tomcat-9.0.80), extracting contents directly into /opt/tomcat rather than /opt/tomcat/apache-tomcat-9.0.80. This creates a cleaner directory structure.

After extraction, /opt/tomcat contains bin/, conf/, lib/, webapps/, and other Tomcat directories.

**Alternative: Specify exact version based on task requirements:**
Check the task description for the required Tomcat version, as it may vary. The Apache archive maintains older versions for compatibility.

### Step 5: Set Correct File Ownership

Configure ownership of Tomcat files to the tomcat user.

```bash
sudo chown -R tomcat:tomcat /opt/tomcat
```

**Explanation:** This command recursively (`-R`) changes ownership of the entire Tomcat installation directory and all its contents to the tomcat user and tomcat group. Proper ownership is essential because:
- Tomcat process runs as the tomcat user and needs read access to configuration and library files
- Write access is needed for logs, temporary files, and deployed applications
- Correct ownership prevents permission errors during startup and operation
- Security best practice: prevents other users from modifying Tomcat files

The `user:group` format (`tomcat:tomcat`) sets both user and group ownership in a single command.

### Step 6: Create Tomcat Systemd Service

Create a systemd service unit for managing Tomcat as a system service.

```bash
sudo vi /etc/systemd/system/tomcat.service
```

**Service configuration:**
```ini
[Unit]
Description=Apache Tomcat Web Application Container
After=network.target

[Service]
Type=forking
User=tomcat
Group=tomcat
Environment="JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-1.8.0.362.b09-4.el9.x86_64"
Environment="CATALINA_PID=/opt/tomcat/temp/tomcat.pid"
Environment="CATALINA_HOME=/opt/tomcat"
Environment="CATALINA_BASE=/opt/tomcat"
ExecStart=/opt/tomcat/bin/startup.sh
ExecStop=/opt/tomcat/bin/shutdown.sh
RestartSec=10
Restart=always

[Install]
WantedBy=multi-user.target
```

**Explanation:** This systemd service unit file defines how the system should manage the Tomcat service.

**[Unit] Section** - Service metadata and dependencies:
- `Description`: Human-readable service description shown in service listings
- `After=network.target`: Ensures network is available before starting Tomcat (critical for web servers)

**[Service] Section** - Service execution configuration:
- `Type=forking`: Indicates Tomcat's startup script forks a child process and exits (daemon mode)
- `User=tomcat` / `Group=tomcat`: Run service as the tomcat user for security
- `Environment` variables configure Tomcat runtime:
  - `JAVA_HOME`: Path to JDK installation (verify with `ls /usr/lib/jvm/` and adjust to match your system)
  - `CATALINA_PID`: Location for process ID file
  - `CATALINA_HOME`: Tomcat installation directory
  - `CATALINA_BASE`: Tomcat base directory (same as HOME for single instance)
- `ExecStart`: Command to start Tomcat
- `ExecStop`: Command to stop Tomcat gracefully
- `RestartSec=10`: Wait 10 seconds before restart attempts
- `Restart=always`: Automatically restart on failure (high availability)

**[Install] Section** - Installation configuration:
- `WantedBy=multi-user.target`: Enable service when system reaches multi-user mode (normal operation)

**Important:** Verify JAVA_HOME path matches your system. Find it with:
```bash
ls /usr/lib/jvm/
```
Update the Environment line with your actual Java path.

### Step 7: Enable and Start Tomcat Service

Configure Tomcat to start on boot and start it immediately.

```bash
sudo systemctl daemon-reload
sudo systemctl enable tomcat
sudo systemctl start tomcat
```

**Explanation:**

**First command** (`daemon-reload`) instructs systemd to reload its configuration, scanning for new or modified service unit files. This is necessary after creating or editing the tomcat.service file so systemd recognizes the new service.

**Second command** (`enable`) creates symbolic links in systemd's target directories, configuring Tomcat to start automatically when the system boots. Enabling doesn't start the service immediately—it only configures boot behavior.

**Third command** (`start`) launches the Tomcat service immediately. Systemd executes the ExecStart command defined in the service unit, and Tomcat begins accepting connections.

**Verify service status:**
```bash
sudo systemctl status tomcat
```

You should see "active (running)" indicating successful startup.

### Step 8: Configure Firewall Rules (Optional)

If firewall is active, allow traffic on Tomcat's port.

```bash
sudo firewall-cmd --permanent --zone=public --add-port=8080/tcp
sudo firewall-cmd --reload
```

**Explanation:** These commands configure firewalld (the default firewall on RHEL/CentOS) to allow incoming TCP connections on port 8080.

**First command** adds a permanent firewall rule:
- `--permanent`: Save rule to persist across reboots (without this, rules are lost on restart)
- `--zone=public`: Apply to the public zone (default zone for public-facing interfaces)
- `--add-port=8080/tcp`: Allow TCP traffic on port 8080

**Second command** (`reload`) applies the permanent rules immediately without restarting the firewall or dropping existing connections.

**Note:** In containerized environments or systems without firewalld active, this step may not be necessary. Verify with `sudo firewall-cmd --state`. If you later change to port 8086, update this rule accordingly.

### Step 9: Verify Default Tomcat Installation

Test that Tomcat is accessible on the default port 8080.

```bash
curl http://stapp01:8080
```

**Explanation:** This command makes an HTTP request to Tomcat's default port 8080. You should receive HTML content from Tomcat's default welcome page, confirming the service is running and accessible. If this fails, check:
- Service status: `sudo systemctl status tomcat`
- Logs: `sudo tail -f /opt/tomcat/logs/catalina.out`
- Port listening: `sudo netstat -tlnup | grep 8080`
- Firewall: `sudo firewall-cmd --list-all`

### Step 10: Configure Custom Port

Modify Tomcat's server configuration to use port 8086 instead of 8080.

```bash
sudo vi /opt/tomcat/conf/server.xml
```

**Find the Connector element and change the port:**
```xml
<Connector port="8086" protocol="HTTP/1.1"
           connectionTimeout="20000"
           redirectPort="8443"
           maxParameterCount="1000"
           />
```

**Explanation:** The server.xml file is Tomcat's main configuration file, defining connectors, engines, hosts, and contexts. The `<Connector>` element defines how Tomcat listens for incoming requests.

**Key attributes:**
- `port="8086"`: Changed from default 8080 to meet task requirements
- `protocol="HTTP/1.1"`: Use HTTP/1.1 protocol for communication
- `connectionTimeout="20000"`: Drop connections idle for more than 20 seconds (20000 milliseconds)
- `redirectPort="8443"`: Redirect SSL/TLS requests to port 8443
- `maxParameterCount="1000"`: Limit query parameters to prevent denial-of-service attacks

After editing, save the file. Tomcat must be restarted to apply configuration changes.

**Update firewall if necessary:**
```bash
sudo firewall-cmd --permanent --zone=public --add-port=8086/tcp
sudo firewall-cmd --reload
```

### Step 11: Prepare for Application Deployment

Backup the default ROOT application and prepare for new deployment.

```bash
cd /opt/tomcat/webapps
sudo mv ROOT ROOT.bak
```

**Explanation:** Tomcat's `webapps` directory contains deployed applications. The `ROOT` directory contains the default Tomcat welcome application served at the context root (`/`). These commands:

**First command** navigates to the webapps directory where applications are deployed.

**Second command** renames the existing ROOT directory to ROOT.bak (backup), preventing conflicts with the new application. Tomcat automatically deploys applications based on directory or WAR file names—`ROOT` (or ROOT.war) deploys to the base URL, while other names create context paths (e.g., `myapp.war` deploys to `/myapp`).

Moving rather than deleting preserves the original in case you need to rollback or reference default configurations.

### Step 12: Copy WAR File from Jump Host

Transfer the application WAR file from the jump host to the app server.

**From the jump host, run:**
```bash
scp /tmp/ROOT.war tony@stapp01:/home/tony/
```

**Explanation:** This command uses SCP (Secure Copy Protocol) to transfer the ROOT.war file from the jump host to App Server 1. The syntax `source user@host:destination` copies the local file `/tmp/ROOT.war` to the remote user tony's home directory on stapp01. SCP encrypts the transfer over SSH, ensuring secure transmission. The file lands in the user's home directory first because we typically don't have direct write access to system directories like `/opt/tomcat/webapps`.

**Alternative:** If SSH is already configured between hosts, you could run this from the app server using rsync or wget if the file is hosted on an HTTP server.

### Step 13: Deploy the Application

Extract the WAR file into the ROOT directory for deployment.

**On the app server:**
```bash
sudo unzip /home/tony/ROOT.war -d /opt/tomcat/webapps/ROOT
```

**Explanation:** This command extracts the WAR (Web Application Archive) file into the ROOT directory, deploying the application at the base context (`/`).

**Command breakdown:**
- `unzip`: Extract ZIP/WAR archive (WAR files are JAR files, which are ZIP files)
- `/home/tony/ROOT.war`: Source WAR file location
- `-d /opt/tomcat/webapps/ROOT`: Destination directory (`-d` specifies extraction target)

Tomcat can auto-deploy WAR files—simply copying ROOT.war to webapps/ would trigger automatic extraction. However, manual extraction provides explicit control and immediate verification. After extraction, the ROOT directory contains servlets, JSPs, static files (HTML, CSS, JS), WEB-INF configuration, and library JARs.

**Set correct ownership:**
```bash
sudo chown -R tomcat:tomcat /opt/tomcat/webapps/ROOT
```

This ensures Tomcat can read and execute the application files.

### Step 14: Restart Tomcat Service

Apply all configuration changes and redeploy the application.

```bash
sudo systemctl restart tomcat
```

**Explanation:** The restart command stops and starts the Tomcat service, forcing it to:
- Reload server.xml with the new port configuration
- Rediscover applications in the webapps directory
- Deploy the new ROOT application
- Release the old port (8080) and bind to the new port (8086)

The restart takes several seconds as Tomcat:
1. Gracefully shuts down (finishing active requests)
2. Unloads existing applications
3. Starts the JVM and loads Tomcat libraries
4. Parses configuration files
5. Deploys applications from webapps/
6. Opens listening sockets on configured ports

**Monitor restart progress:**
```bash
sudo tail -f /opt/tomcat/logs/catalina.out
```

Watch for "Server startup in [XXX] milliseconds" indicating successful restart.

### Step 15: Verify Application Deployment

Test that the application is accessible on the custom port.

**From the app server:**
```bash
curl http://localhost:8086
```

**From the jump host:**
```bash
curl http://stapp01:8086
```

**Expected response (example):**
```html
<!DOCTYPE html>
<html>
    <head>
        <title>SampleWebApp</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body>
        <h2>Welcome to xFusionCorp Industries!</h2>
        <br>
    </body>
</html>
```

**Explanation:** These curl commands make HTTP requests to verify the application is deployed and responding correctly.

**First test** from localhost confirms Tomcat is listening and serving content. If this fails, the issue is with Tomcat configuration or the application itself.

**Second test** from the jump host confirms network connectivity and firewall rules allow external access. If localhost works but remote access fails, check firewall rules and network configuration.

Successful response with the expected HTML content confirms:
- Tomcat is running on port 8086
- The ROOT application deployed correctly
- The application is accessible from the base URL without a context path
- Network connectivity and firewall rules are properly configured

### Step 16: Troubleshooting (If Issues Occur)

If the application doesn't load, check common issues:

**Check Tomcat service status:**
```bash
sudo systemctl status tomcat
```

**View Tomcat logs:**
```bash
sudo tail -100 /opt/tomcat/logs/catalina.out
sudo tail -100 /opt/tomcat/logs/localhost.$(date +%Y-%m-%d).log
```

**Verify port binding:**
```bash
sudo netstat -tlnup | grep 8086
```

**Check file permissions:**
```bash
ls -la /opt/tomcat/webapps/ROOT
```

**Verify Java version:**
```bash
java -version
echo $JAVA_HOME
```

---

## Understanding Apache Tomcat

### Tomcat Fundamentals

**What is Apache Tomcat?**
Apache Tomcat is an open-source implementation of the Jakarta Servlet, Jakarta Server Pages, and other Jakarta EE specifications. It provides a "pure Java" HTTP web server environment for running Java code. Tomcat is widely used for hosting Java web applications, RESTful APIs, and microservices.

**Core Components:**
- **Catalina**: The servlet container (core Tomcat engine) that implements servlet and JSP specifications
- **Coyote**: HTTP connector that handles incoming HTTP requests and sends responses
- **Jasper**: JSP engine that compiles JSP pages into Java servlets
- **Cluster**: Provides session replication and load balancing for high availability
- **Web Application Manager**: Deploy, undeploy, start, and stop web applications

**Architecture:**
Tomcat uses a hierarchical architecture: Server → Service → Engine → Host → Context. Each level provides configuration and isolation boundaries for applications.

### Port Configuration

**Default Ports:**
- **8080**: HTTP connector (main application port)
- **8443**: HTTPS connector (SSL/TLS encrypted connections)
- **8005**: Shutdown port (receives shutdown command)
- **8009**: AJP connector (for integration with Apache HTTP Server)

**Port Selection Considerations:**
- Ports below 1024 require root privileges (avoid running Tomcat as root)
- Choose ports not conflicting with other services
- Document port assignments for operational awareness
- Consider port ranges for multiple Tomcat instances (8080, 8081, 8082...)

### Java Application Deployment

**WAR Files (Web Application Archive):**
WAR files are ZIP archives containing a complete Java web application:
- Servlets and JSP files
- HTML, CSS, JavaScript, and images
- WEB-INF/web.xml (deployment descriptor)
- WEB-INF/classes/ (compiled Java classes)
- WEB-INF/lib/ (JAR dependencies)

**Deployment Methods:**

**1. Automatic Deployment (Default):**
Copy WAR file to `webapps/` directory. Tomcat automatically detects, extracts, and deploys the application. Convenient but provides less control over deployment timing.

**2. Manual Deployment:**
Extract WAR file into a directory within `webapps/`. Provides explicit control and immediate file inspection. Useful for troubleshooting or custom deployment processes.

**3. Manager Application:**
Use Tomcat's web-based Manager application for GUI deployment, start/stop, and management. Requires authentication configuration.

**4. Ant/Maven Deployment:**
Build tools can deploy directly to Tomcat using deployment plugins. Ideal for CI/CD pipelines.

**Context Path:**
The application URL path is determined by the WAR filename or directory name:
- `ROOT.war` or `ROOT/` → http://server:8080/
- `myapp.war` or `myapp/` → http://server:8080/myapp
- `api-v2.war` or `api-v2/` → http://server:8080/api-v2

### Directory Structure

**Key Tomcat Directories:**

**/bin** - Executable scripts:
- `startup.sh` / `startup.bat`: Start Tomcat
- `shutdown.sh` / `shutdown.bat`: Stop Tomcat
- `catalina.sh`: Main control script with advanced options
- `version.sh`: Display Tomcat version information

**/conf** - Configuration files:
- `server.xml`: Main Tomcat configuration (connectors, engine, hosts)
- `web.xml`: Default servlet and MIME type definitions
- `tomcat-users.xml`: User authentication for manager apps
- `catalina.properties`: System properties and classpath configuration
- `context.xml`: Default context configuration for all applications

**/lib** - Shared Java libraries:
Contains JAR files available to all web applications. Includes Tomcat core libraries, servlet API, and shared dependencies.

**/logs** - Log files:
- `catalina.out`: Standard output and error (main log)
- `catalina.YYYY-MM-DD.log`: Daily Catalina logs
- `localhost.YYYY-MM-DD.log`: Host-specific logs
- `manager.YYYY-MM-DD.log`: Manager application logs
- `host-manager.YYYY-MM-DD.log`: Host manager logs

**/webapps** - Deployed applications:
Default deployment directory. Each subdirectory or WAR file represents a deployed application.

**/work** - Temporary files:
Compiled JSP pages and temporary working directories. Tomcat automatically manages this directory.

**/temp** - Temporary files:
JVM and application temporary storage. Can be cleaned safely when Tomcat is stopped.

### Configuration Files

**server.xml - Main Configuration:**
Defines Tomcat's structure: Servers, Services, Connectors, Engines, Hosts, and Contexts. Modifications require Tomcat restart.

**Key elements:**
- `<Server>`: Top-level element, represents entire Tomcat instance
- `<Service>`: Groups connectors with an engine
- `<Connector>`: Defines how Tomcat receives requests (HTTP, HTTPS, AJP)
- `<Engine>`: Request processing engine
- `<Host>`: Virtual host configuration
- `<Context>`: Individual application configuration

**web.xml - Application Descriptor:**
Defines servlet mappings, filters, listeners, security constraints, and session configuration. Application-specific web.xml files override default settings.

**tomcat-users.xml - User Authentication:**
Defines users, passwords, and roles for Tomcat manager applications. Secure this file with restrictive permissions (600).

**context.xml - Application Context:**
Configures resources, data sources, session managers, and other application-level settings. Can be global (/conf/context.xml) or application-specific (META-INF/context.xml in WAR).

### Security Best Practices

**1. Dedicated User Account:**
Run Tomcat as a non-root user with minimal privileges. This limits damage if Tomcat is compromised. Never run Tomcat as root in production.

**2. File Permissions:**
Restrict access to Tomcat files:
- Configuration files (conf/): 600 or 640 (readable only by tomcat user)
- Executables (bin/): 700 or 750
- Webapps: 755 for directories, 644 for files
- Logs: 640 (readable by tomcat and monitoring tools)

**3. Remove Default Applications:**
Delete or secure default applications in production:
- `docs/`: Documentation application (information disclosure)
- `examples/`: Sample applications (security vulnerabilities)
- `manager/` and `host-manager/`: Management interfaces (secure with strong auth or remove)

**4. Disable Directory Listing:**
In web.xml, ensure directory listing is disabled to prevent exposing file structures:
```xml
<init-param>
    <param-name>listings</param-name>
    <param-value>false</param-value>
</init-param>
```

**5. Enable SSL/TLS:**
Configure HTTPS connector with valid certificates for encrypted communication:
```xml
<Connector port="8443" protocol="HTTP/1.1" SSLEnabled="true"
           maxThreads="150" scheme="https" secure="true"
           keystoreFile="/path/to/keystore" keystorePass="password"
           clientAuth="false" sslProtocol="TLS"/>
```

**6. Update Regularly:**
Apply security patches and updates promptly. Monitor Apache Tomcat security advisories.

**7. Limit Access:**
Use firewalls and network segmentation to restrict who can access Tomcat. Implement authentication and authorization for sensitive applications.

---

## Key Concepts

### Why Use Tomcat?

**Lightweight:** Compared to full Java EE application servers (WildFly, WebLogic), Tomcat has a smaller footprint, faster startup, and lower resource consumption—ideal for microservices and containerized deployments.

**Standards Compliance:** Implements Jakarta EE specifications, ensuring portability of Java web applications across different servlet containers.

**Production Ready:** Proven stability and scalability in high-traffic environments. Used by organizations ranging from startups to enterprises.

**Open Source:** Free to use, with active community support, extensive documentation, and regular updates.

**Flexible:** Suitable for diverse use cases—from simple web applications to complex RESTful APIs and microservices architectures.

### Common Use Cases

**Web Application Hosting:** Serve dynamic Java web applications with servlets, JSPs, and modern frameworks (Spring MVC, JSF, Struts).

**RESTful API Backends:** Host REST APIs built with frameworks like Spring Boot, Jersey, or RESTEasy. Lightweight and efficient for API services.

**Microservices:** Deploy containerized microservices with embedded Tomcat (common with Spring Boot), enabling cloud-native architectures.

**Development and Testing:** Local development server for Java developers, providing rapid iteration and testing capabilities.

### Tomcat vs. Other Solutions

**Tomcat vs. Full Java EE Servers (WildFly, WebLogic, WebSphere):**
- Tomcat: Servlet container only, lighter, faster, focused on web tier
- Full Java EE: Complete enterprise stack (EJB, JMS, JTA), heavier, more features

**Tomcat vs. Jetty:**
- Both lightweight servlet containers
- Jetty: More embeddable, used in applications and tools
- Tomcat: More widely adopted, better documentation and community support

**Tomcat vs. Nginx/Apache HTTP Server:**
- Tomcat: Java application server, executes Java code
- Nginx/Apache: Static content servers, reverse proxies
- Often used together: Nginx/Apache as reverse proxy, Tomcat as backend

---

## Validation

Test your solution using KodeKloud's automated validation system. The validation checks:
- Java JDK is installed
- Tomcat user and group exist
- Tomcat service is running
- Tomcat is accessible on port 8086
- Application deploys successfully at base URL
- Application returns expected content

---

[← Day 10](day-10.md) | [Day 12 →](day-12.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
