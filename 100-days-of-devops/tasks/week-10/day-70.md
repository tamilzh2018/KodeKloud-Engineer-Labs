# Day 70: Configure Jenkins User Access

## Task Overview

Configure fine-grained user permissions in Jenkins using Project-based Matrix Authorization Strategy. Create a new user account and implement role-based access control with read-only permissions for the development team while maintaining full admin access.

**Technical Specifications:**
- Jenkins admin credentials: username `admin`, password `Adm!n321`
- New user: username `mark`, password `Rc5C9EyvbU`, full name `Mark`
- Authorization strategy: Project-based Matrix Authorization Strategy
- Global permissions: Admin (Administer), Mark (Overall Read), Anonymous (none)
- Job permissions: Mark (Read only for existing job)
- Required plugin: Matrix Authorization Strategy

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Access Jenkins and login

Click the "Jenkins" button in the top bar to open the Jenkins web interface. Login with username `admin` and password `Adm!n321`. You need administrator privileges to create users and configure security settings.

**Step 2:** Update required plugins (if needed)

Before configuring authorization, ensure all plugins are up to date. Navigate to Manage Jenkins > Plugins > Updates. If there are plugins listed for update, select them and click "Download now and install after restart". Check "Restart Jenkins when installation is complete and no jobs are running". Wait for Jenkins to restart and log back in. This step prevents compatibility issues with the Matrix Authorization Strategy plugin.

**Step 3:** Create the new user account

From the Jenkins dashboard, navigate to Manage Jenkins > Users (in the Security section). Click "Create User" in the left sidebar. Fill in the user details:
- **Username**: `mark`
- **Password**: `Rc5C9EyvbU`
- **Confirm password**: `Rc5C9EyvbU`
- **Full name**: `Mark`
- **E-mail address**: (can be left blank or set to mark@example.com)

Click "Create User". The new user account is now created but has no specific permissions yet - those will be configured through the authorization strategy.

**Step 4:** Install Matrix Authorization Strategy plugin

Navigate to Manage Jenkins > Plugins > Available plugins. In the search box, type "Matrix Authorization Strategy". Find the "Matrix Authorization Strategy Plugin" and check the box next to it. Click "Install" at the bottom. On the installation progress page, check "Restart Jenkins when installation is complete and no jobs are running". Wait for Jenkins to restart and log back in with admin credentials. This plugin enables fine-grained permission control at both global and per-project levels.

**Step 5:** Configure Project-based Matrix Authorization Strategy

Navigate to Manage Jenkins > Security (or Configure Global Security). Under the "Authorization" section, you'll see different authorization strategy options. Select "Project-based Matrix Authorization Strategy" from the radio button list. This strategy allows you to set global permissions and override them on a per-project basis, providing maximum flexibility for access control.

**Step 6:** Configure global permissions for admin user

In the matrix that appears, you'll see columns for different permission types (Overall, Credentials, Agent, Job, Run, View, SCM) and rows for users/groups. Look for the "admin" user row (it should already exist). Ensure the admin user has the "Administer" permission checked under the "Overall" column. This checkbox automatically grants all permissions. If the admin user isn't listed, click "Add user or group" and enter `admin`, then check the Administer box. This ensures you maintain full administrative access.

**Step 7:** Add read permissions for mark user

Click "Add user or group" button below the permission matrix. Enter `mark` in the field and click "OK". A new row for the mark user appears in the matrix. Under the "Overall" column, check only the "Read" permission checkbox for mark. Leave all other permissions unchecked. The "Overall Read" permission allows mark to view the Jenkins dashboard and see available jobs, but prevents any modifications or builds.

**Step 8:** Remove anonymous user permissions

Look for the "Anonymous" user row in the permission matrix. If it exists and has any permissions checked, uncheck all of them. Anonymous users are unauthenticated visitors to Jenkins - they should have no access in a secure installation. If the Anonymous row doesn't exist or already has no permissions, no action is needed. This prevents unauthorized access to Jenkins.

**Step 9:** Save global security configuration

After configuring the permission matrix, scroll to the bottom of the page and click "Save" (or "Apply" then "Save"). Jenkins will apply the new authorization strategy immediately. You'll be redirected back to the Jenkins dashboard. The global permissions are now set: admin has full control, mark has read-only access, and anonymous users have no access.

**Step 10:** Identify the existing job

From the Jenkins dashboard, you'll see a list of existing jobs. There should be a job visible (possibly named "HelloWorld" or another name). Note the exact job name as you'll need to configure project-based permissions for it in the next step.

**Step 11:** Configure project-based security for the job

Click on the job name to enter the job view. From the left sidebar, click "Configure". Scroll down to find the "Enable project-based security" checkbox (this option appears because we selected Project-based Matrix Authorization Strategy). Check this box to enable project-level permission overrides. A permission matrix similar to the global one will appear.

**Step 12:** Set job-level permissions for mark user

In the project permission matrix, click "Add user or group" and enter `mark`. A new row appears for mark. Under the "Job" column, check only the "Read" permission checkbox. Leave all other permissions unchecked (Build, Cancel, Configure, Delete, Discover, Move, Workspace). The Read permission allows mark to view the job configuration and build history but prevents running builds or making changes. Ensure the admin user also appears in the matrix with full permissions (this may be inherited from global settings).

**Step 13:** Save job configuration

Scroll to the bottom of the job configuration page and click "Save". The project-based permissions are now applied to this specific job. Mark can now view this job but cannot trigger builds or modify its configuration.

**Step 14:** Verify permissions (optional)

To verify the configuration works correctly, you can test by logging out and logging back in as mark:
1. Click your username in the top-right corner and select "Log out"
2. Login with username `mark` and password `Rc5C9EyvbU`
3. You should see the Jenkins dashboard with read-only access
4. Clicking on the job shows its details but no "Build Now" or "Configure" options
5. Attempting to create a new job shows an error (no permission)

Log out and log back in as admin to continue with validation.

---

## Key Concepts

**Jenkins Authorization Strategies:**
- **Anyone can do anything**: No security, full access to all (development only)
- **Legacy mode**: Authenticated users have full access, unauthenticated have read
- **Logged-in users can do anything**: Requires login but all users are admins
- **Matrix-based security**: Global permission matrix for users and groups
- **Project-based Matrix Authorization**: Global + per-project permission matrices (most flexible)

**Permission Types in Jenkins:**
- **Overall**: Global Jenkins permissions (Administer, Read, RunScripts, etc.)
- **Credentials**: Permission to view, create, update, delete credentials
- **Agent**: Permissions for build agent management (Configure, Connect, Delete)
- **Job**: Job-specific permissions (Build, Cancel, Configure, Delete, Discover, Read)
- **Run**: Build execution permissions (Delete, Replay, Update)
- **View**: Dashboard view permissions (Configure, Create, Delete, Read)
- **SCM**: Source control permissions (Tag)

**Overall Permission Levels:**
- **Administer**: Full system control, can configure everything, grant permissions
- **Read**: View Jenkins dashboard, see available jobs and builds
- **SystemRead**: Read all configuration (more than Read, less than Administer)
- **RunScripts**: Execute arbitrary Groovy scripts in Script Console (dangerous)

**Job Permission Levels:**
- **Build**: Trigger job builds manually
- **Cancel**: Cancel running builds
- **Configure**: Modify job configuration
- **Delete**: Delete the job entirely
- **Discover**: See job exists even without Read permission
- **Read**: View job configuration, build history, console output
- **Move**: Move job to different folder
- **Workspace**: Access job workspace files

**Security Best Practices:**
- **Principle of Least Privilege**: Grant minimum permissions required for each role
- **Remove Anonymous Access**: Disable all permissions for unauthenticated users
- **Separate Admin Accounts**: Use dedicated admin accounts, not personal accounts
- **Audit Permissions**: Regularly review and audit user permissions
- **Group-based Permissions**: Use groups instead of individual users when possible
- **Enable CSRF Protection**: Protect against Cross-Site Request Forgery attacks
- **Use Authentication Plugins**: Integrate with LDAP, Active Directory, or OAuth

**Project-based Matrix vs Matrix-based Security:**
- **Matrix-based**: Only global permissions, same for all jobs
- **Project-based Matrix**: Global permissions + per-job overrides
- **Use Case**: Project-based allows developers to have build access to their projects only
- **Flexibility**: Project-based provides maximum control but requires more configuration
- **Inheritance**: Project permissions override global for that specific project

**Common Permission Patterns:**
- **Administrators**: Overall Administer (all permissions)
- **Developers**: Overall Read, Job Build/Read on their projects
- **Viewers/QA**: Overall Read, Job Read only
- **CI Service Accounts**: Job Build/Read, no Configure permissions
- **Contractors/Temporary**: Limited project access with expiration

**Troubleshooting Access Issues:**
- **Locked Out**: If you accidentally remove admin permissions, edit config.xml and restart
- **Permissions Not Applied**: Ensure you clicked Save after configuration changes
- **User Can't Login**: Check authentication realm configuration (Security Realm)
- **Missing Permissions**: Verify plugin is installed and Jenkins restarted
- **Matrix Plugin Missing**: Install "Matrix Authorization Strategy Plugin"

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 69](day-69.md) | [Day 71 →](../week-11/day-71.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
