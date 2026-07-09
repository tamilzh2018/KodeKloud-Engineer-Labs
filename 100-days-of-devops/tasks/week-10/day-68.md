# Day 68: Set Up Jenkins Server

## Task Overview

Install and configure Jenkins CI/CD server on CentOS Stream 9. Set up the initial administrator account and complete the Jenkins web UI setup wizard.

**Technical Specifications:**
- Installation method: YUM package manager
- Operating System: CentOS Stream 9 (Fedora-based)
- Java version: OpenJDK 21 (required dependency)
- Admin username: `theadmin`
- Admin password: `Adm!n321`
- Admin full name: `John`
- Admin email: `john@jenkins.stratos.xfusioncorp.com`
- SSH credentials: root user with password `S3curePass`

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Connect to the Jenkins server via SSH

```bash
ssh root@jenkins
```

Establish an SSH connection to the Jenkins server using the root account. You'll be prompted for the password `S3curePass`. SSH provides secure encrypted remote access to the Linux server where Jenkins will be installed. Once connected, you'll have administrative privileges to install packages and configure services.

**Step 2:** Identify the operating system version

```shell
cat /etc/os-release
```

Display the operating system release information to determine the correct installation method. This command reads the `/etc/os-release` file which contains OS identification data. The output shows this is CentOS Stream 9, a Fedora-based distribution, which means we'll use DNF (the next-generation YUM package manager) and follow Fedora installation instructions.

**Expected output:**
```
NAME="CentOS Stream"
VERSION="9"
ID="centos"
ID_LIKE="rhel fedora"
VERSION_ID="9"
PLATFORM_ID="platform:el9"
PRETTY_NAME="CentOS Stream 9"
ANSI_COLOR="0;31"
LOGO="fedora-logo-icon"
CPE_NAME="cpe:/o:centos:centos:9"
HOME_URL="https://centos.org/"
BUG_REPORT_URL="https://issues.redhat.com/"
REDHAT_SUPPORT_PRODUCT="Red Hat Enterprise Linux 9"
REDHAT_SUPPORT_PRODUCT_VERSION="CentOS Stream"
```

The `ID_LIKE="rhel fedora"` line indicates this distribution is compatible with both RHEL and Fedora packages.

**Step 3:** Update system packages and install prerequisites

```sh
yum update -y
yum install -y wget
```

Update all existing system packages to their latest versions with `yum update -y` (the `-y` flag automatically answers "yes" to all prompts). Then install `wget`, a command-line utility for downloading files from the web, which we'll use to fetch the Jenkins repository configuration. Keeping the system updated ensures security patches are applied and reduces compatibility issues with new software installations.

**Step 4:** Install Jenkins and dependencies

```sh
sudo wget -O /etc/yum.repos.d/jenkins.repo \
    https://pkg.jenkins.io/redhat-stable/jenkins.repo
sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io-2023.key
sudo dnf upgrade -y
# Add required dependencies for the jenkins package
sudo dnf install fontconfig java-21-openjdk -y
sudo dnf install jenkins -y
sudo systemctl daemon-reload
```

This multi-step process installs Jenkins following the official documentation for Fedora-based systems:

1. **Add Jenkins Repository**: Download the Jenkins stable repository configuration file and save it to `/etc/yum.repos.d/` so the package manager knows where to find Jenkins packages.

2. **Import GPG Key**: Import Jenkins' GPG signing key to verify package authenticity and integrity during installation. This ensures you're installing legitimate Jenkins packages.

3. **Upgrade Packages**: Run `dnf upgrade` to refresh the package cache with the newly added Jenkins repository.

4. **Install Dependencies**: Install `fontconfig` (required for Jenkins UI rendering) and `java-21-openjdk` (Java Runtime Environment). Jenkins is a Java application and requires Java 21 to run.

5. **Install Jenkins**: Install the Jenkins package itself, which includes the Jenkins war file, service configuration, and default directories.

6. **Reload Systemd**: Reload the systemd daemon to recognize the new Jenkins service unit file installed by the package.

**Step 5:** Start and enable Jenkins service

```sh
sudo systemctl enable --now jenkins
```

Start the Jenkins service immediately and configure it to start automatically on system boot. The `enable` flag sets up the service to launch at boot time, while `--now` starts it immediately without requiring a separate `systemctl start jenkins` command. Jenkins will begin its initialization process, which includes creating the home directory at `/var/lib/jenkins`, generating the initial admin password, and starting the web server on port 8080 (default). If you encounter timeout issues during startup, you may need to increase the service timeout as mentioned in the [Jenkins systemd services documentation](https://www.jenkins.io/doc/book/system-administration/systemd-services/#starting-services).

**Step 6:** Retrieve the initial admin password

```sh
cat /var/lib/jenkins/secrets/initialAdminPassword
```

Display the automatically generated initial administrator password that Jenkins creates during first startup. This password is stored in a secure location readable only by root and the jenkins user. Copy this password as you'll need it to unlock Jenkins in the web UI setup wizard. The password is a random alphanumeric string that ensures secure initial access to the Jenkins installation.

**Step 7:** Access Jenkins web interface

Click the "Jenkins" button in the KodeKloud interface to open the Jenkins web UI in your browser. You'll be presented with the "Unlock Jenkins" screen. Paste the initial admin password you retrieved in the previous step and click "Continue". This security measure prevents unauthorized access to a freshly installed Jenkins server.

**Step 8:** Install suggested plugins

On the "Customize Jenkins" page, click "Install suggested plugins". Jenkins will automatically install a curated set of commonly used plugins including:
- Git plugin for source control integration
- Pipeline plugin for pipeline jobs
- Credentials plugin for managing secrets
- SSH Build Agents plugin for distributed builds
- Many other essential plugins

The installation process may take 2-5 minutes depending on internet speed. If any plugin fails to install, you can click "Retry" or continue without it (you can install missing plugins later). Wait for all plugins to complete installation before proceeding.

**Step 9:** Create the admin user account

After plugin installation completes, you'll see the "Create First Admin User" page. Fill in the required fields:
- **Username**: `theadmin`
- **Password**: `Adm!n321`
- **Confirm password**: `Adm!n321`
- **Full name**: `John`
- **E-mail address**: `john@jenkins.stratos.xfusioncorp.com`

Click "Save and Continue". This creates the permanent administrator account that will replace the temporary initial admin password. The username and email will be used to identify the user in build logs, notifications, and audit trails.

**Step 10:** Configure Jenkins URL and complete setup

On the "Instance Configuration" page, verify the Jenkins URL is correct (usually pre-populated with the server's address). Click "Save and Finish". Then click "Start using Jenkins" to complete the setup wizard. You'll be redirected to the Jenkins dashboard, indicating successful installation and configuration. Jenkins is now ready to create jobs, configure pipelines, and integrate with version control systems.

---

## Key Concepts

**Jenkins Architecture:**
- **Master/Controller**: Central server that manages build jobs, schedules, and coordinates agents
- **Web Interface**: User-friendly dashboard for configuration and monitoring (port 8080)
- **Build Executor**: Runs build jobs on the master or distributed agent nodes
- **Plugin System**: Modular architecture allowing extensibility with thousands of plugins

**Jenkins Components:**
- **Home Directory**: `/var/lib/jenkins` stores all Jenkins data, configurations, jobs, and builds
- **War File**: Java Web Application Archive containing Jenkins application code
- **Service**: Systemd service unit for starting/stopping Jenkins and managing lifecycle
- **Logs**: Located at `/var/log/jenkins/jenkins.log` for troubleshooting

**Initial Setup Process:**
- **Security**: Initial admin password ensures only authorized users can configure Jenkins
- **Plugin Installation**: Essential plugins provide core functionality for CI/CD workflows
- **Admin Account**: Primary administrator with full system access and configuration rights
- **Instance URL**: Used for webhook callbacks, email links, and API access

**Java Dependency:**
- **Java 21**: Latest LTS version required by modern Jenkins releases
- **JRE vs JDK**: Jenkins requires JRE (Java Runtime Environment), not full JDK
- **OpenJDK**: Open-source Java implementation, free alternative to Oracle JDK
- **Memory Requirements**: Jenkins recommends minimum 2GB RAM for master server

**Package Management:**
- **YUM/DNF**: Package managers for Red Hat-based distributions (DNF is YUM's successor)
- **RPM**: Red Hat Package Manager format used by Jenkins
- **Repository**: Remote package source configured in `/etc/yum.repos.d/`
- **GPG Verification**: Ensures package authenticity and prevents tampering

**Best Practices:**
- **Secure Admin Password**: Use strong passwords meeting complexity requirements
- **Regular Updates**: Keep Jenkins and plugins updated for security patches
- **Backup Configuration**: Regularly backup `/var/lib/jenkins` directory
- **HTTPS**: Configure SSL/TLS for production deployments to encrypt web traffic
- **Firewall**: Restrict port 8080 access to authorized networks only
- **Monitoring**: Track Jenkins logs, disk space, and system resources

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 67](day-67.md) | [Day 69 →](day-69.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
