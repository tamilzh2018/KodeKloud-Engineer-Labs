# Day 69: Install Jenkins Plugins

## Task Overview

Install Git and GitLab plugins in Jenkins to enable source code management integration for CI/CD pipelines. Learn the plugin management workflow including updating existing plugins and restarting Jenkins.

**Technical Specifications:**
- Jenkins admin credentials: username `admin`, password `Adm!n321`
- Required plugins: Git and GitLab
- Plugin management: Update Center and Available Plugins
- Post-installation: Jenkins service restart may be required

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Access Jenkins web interface

Click the "Jenkins" button in the top bar of the KodeKloud interface to open the Jenkins web UI in your browser. You'll be presented with the Jenkins login page where you need to authenticate before accessing the admin features.

**Step 2:** Login to Jenkins

Enter the admin credentials:
- **Username**: `admin`
- **Password**: `Adm!n321`

Click "Sign in" to access the Jenkins dashboard. These credentials were configured during the initial Jenkins setup. Once logged in, you'll have full administrative access to install plugins, create jobs, and configure system settings.

**Step 3:** Navigate to Plugin Manager

From the Jenkins dashboard, click on "Manage Jenkins" in the left sidebar. This opens the system administration page where you can configure global settings, manage plugins, and perform system maintenance. On the Manage Jenkins page, find and click on "Plugins" under the "System Configuration" section. This opens the Plugin Manager interface.

**Step 4:** Update existing plugins (recommended)

Before installing new plugins, it's best practice to update any existing plugins that have newer versions available. In the Plugin Manager, click on the "Updates" tab to see plugins with available updates. If there are plugins listed:
- Select the plugins you want to update (or check "Select all" to update everything)
- Scroll to the bottom and click "Download now and install after restart"
- Check the box "Restart Jenkins when installation is complete and no jobs are running"

This ensures plugin dependencies are current and reduces compatibility issues when installing new plugins. Wait for Jenkins to restart before proceeding. The Jenkins UI will show "Jenkins is getting ready to restart" and then the login page will reappear once the restart is complete.

**Step 5:** Navigate to Available Plugins

After Jenkins restarts and you log back in (if needed), return to Manage Jenkins > Plugins. Click on the "Available plugins" tab. This tab displays all plugins available from the Jenkins Update Center that aren't currently installed. The list contains thousands of plugins, so you'll need to use the search functionality.

**Step 6:** Search and select Git plugin

In the search box at the top of the Available Plugins page, type "Git". The list will filter to show Git-related plugins. Look for the plugin named simply "Git" (description: "This plugin integrates Git with Jenkins"). Check the checkbox next to the Git plugin to mark it for installation. This plugin provides fundamental Git SCM integration, allowing Jenkins to clone repositories, checkout branches, and trigger builds based on Git commits.

**Step 7:** Search and select GitLab plugin

Without clearing the search box, add " GitLab" to search for both plugins, or clear the search and type "GitLab". Find the "GitLab" plugin (description: "This plugin allows GitLab to trigger Jenkins builds and display their results"). Check the checkbox next to the GitLab plugin. This plugin enables advanced GitLab integration including webhook triggers, merge request builders, commit status updates, and GitLab authentication.

**Step 8:** Install the selected plugins

After selecting both Git and GitLab plugins, scroll to the bottom of the page and click the "Install" button (formerly "Download now and install after restart" in older Jenkins versions). Jenkins will begin downloading and installing the selected plugins along with any dependencies they require. You'll be redirected to a page showing installation progress for each plugin.

**Step 9:** Monitor plugin installation

On the installation progress page, you'll see each plugin being downloaded and installed. The status will show:
- **Pending**: Plugin queued for download
- **Installing**: Plugin being downloaded and extracted
- **Success**: Plugin installed successfully
- **Failure**: Plugin installation failed (rarely happens)

If any plugin fails, you can click "Retry" to attempt installation again. Failures are usually due to temporary network issues or Update Center connection problems. The installation typically takes 1-3 minutes depending on the number of dependencies.

**Step 10:** Restart Jenkins to activate plugins

After all plugins show "Success" status, you need to restart Jenkins for the plugins to become fully active. At the bottom of the installation page, check the box that says "Restart Jenkins when installation is complete and no jobs are running". Jenkins will automatically restart once all installations finish and no builds are running.

Alternatively, if that option isn't available, you can manually restart by:
- Going to Manage Jenkins > Prepare for Shutdown
- Waiting for any running jobs to complete
- Manually restarting: `sudo systemctl restart jenkins` via SSH

**Step 11:** Verify plugin installation

After Jenkins restarts and you log back in, navigate to Manage Jenkins > Plugins and click on the "Installed plugins" tab. Use the search box to filter for "Git" and "GitLab". You should see both plugins listed with their version numbers, indicating successful installation. The plugins are now active and ready to use in Jenkins jobs and pipelines.

**Step 12:** Test Git plugin functionality (optional)

To verify the Git plugin is working, you can create a test job:
1. Click "New Item" from the dashboard
2. Enter a name, select "Freestyle project", click OK
3. Under "Source Code Management", you should now see "Git" as an option
4. The presence of the Git option confirms the plugin is installed and functional

---

## Key Concepts

**Jenkins Plugin System:**
- **Extensibility**: Plugins extend Jenkins functionality without modifying core code
- **Update Center**: Central repository hosting thousands of community-developed plugins
- **Dependencies**: Plugins can depend on other plugins, automatically installed together
- **Compatibility**: Plugin versions must be compatible with Jenkins version
- **Isolation**: Plugins run in isolation and can be enabled/disabled independently

**Plugin Categories:**
- **SCM Plugins**: Source control integration (Git, GitLab, GitHub, Bitbucket, SVN)
- **Build Tools**: Maven, Gradle, Ant, NPM integration
- **Authentication**: LDAP, Active Directory, OAuth, SAML
- **Notifications**: Email, Slack, Teams, webhooks
- **Pipeline**: Pipeline syntax, shared libraries, declarative pipeline
- **Cloud**: AWS, Azure, GCP, Docker, Kubernetes integration

**Git Plugin Features:**
- **Repository Cloning**: Clone Git repositories as build step
- **Branch Building**: Build specific branches, tags, or commits
- **Credentials**: Secure storage of Git credentials (SSH keys, tokens)
- **Webhooks**: Trigger builds on push events
- **Submodules**: Support for Git submodules and subtrees
- **Multiple Repositories**: Checkout multiple repos in single job

**GitLab Plugin Features:**
- **Webhook Integration**: GitLab webhooks trigger Jenkins builds automatically
- **Merge Request Builds**: Automatically build and test merge requests
- **Commit Status**: Report build results back to GitLab
- **GitLab Authentication**: Use GitLab accounts for Jenkins login
- **Multi-branch Pipeline**: Discover and build GitLab branches automatically
- **Tag Triggers**: Build on Git tag creation

**Plugin Update Best Practices:**
- **Update Before Install**: Update existing plugins before installing new ones
- **Check Compatibility**: Verify plugin works with your Jenkins version
- **Test in Staging**: Test plugin updates in non-production environment first
- **Read Changelogs**: Review plugin changelogs for breaking changes
- **Backup First**: Backup Jenkins home directory before major plugin updates

**Troubleshooting Plugin Installation:**
- **Network Issues**: Check internet connectivity and proxy settings
- **Update Center URL**: Verify Update Center is accessible
- **Disk Space**: Ensure sufficient disk space in `/var/lib/jenkins`
- **Java Errors**: Check Jenkins logs for Java compatibility issues
- **Version Conflicts**: Update Jenkins if plugins require newer version
- **Retry Failed Installations**: Temporary failures can often be resolved by retrying

**Common Issues and Solutions:**
- **Plugins Not Appearing**: Update plugin cache by clicking "Check now" in Update Center
- **Restart Not Happening**: Manually restart Jenkins service if automatic restart fails
- **Timeout Errors**: Increase Jenkins startup timeout or retry installation
- **Dependency Failures**: Install required plugins manually if auto-resolution fails
- **Restart Required Multiple Times**: Some plugins need multiple restarts to fully initialize

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 68](day-68.md) | [Day 70 →](day-70.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
