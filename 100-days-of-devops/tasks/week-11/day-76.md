# Day 76: Jenkins Project Security

## Task Overview

Implement project-level access control in Jenkins by configuring granular permissions for individual users on specific jobs. This security model enables fine-grained authorization where different team members have different levels of access to the same Jenkins job.

**Technical Specifications:**
- Authorization strategy: Project-based Matrix Authorization
- Inheritance strategy: Inherit permissions from parent ACL
- Job: Existing "Packages" job
- Users: sam and rohan (existing users)
- Permissions: Different permission sets for each user

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Access Jenkins UI and log in

```
Username: admin
Password: Adm!n321
```

Open the Jenkins web interface and authenticate with administrator credentials. Admin access is required to install security plugins, configure global authorization strategies, and set up project-level permissions. The admin user will need to grant specific permissions to other users while maintaining full administrative control.

**Step 2:** Install Project-based Matrix Authorization plugin

Navigate to Manage Jenkins > Manage Plugins > Available tab

Search for and install:
- Matrix Authorization Strategy Plugin (includes Project-based Matrix Authorization)

Select "Restart Jenkins when installation is complete and no jobs are running"

The Matrix Authorization Strategy plugin enables fine-grained permission control at both global and project levels. Project-based Matrix Authorization allows each job to have its own permission matrix that can either inherit from global settings or override them. This plugin is essential for multi-team Jenkins environments where different users need different access levels to different projects. After installation, Jenkins restarts to load the security plugin.

**Step 3:** Configure global authorization strategy

Navigate to Manage Jenkins > Security (or Configure Global Security)

Under "Authorization" section:
- Select "Project-based Matrix Authorization Strategy"

In the permission matrix, configure admin user:
- User/group: admin
- Check ALL permissions (Administer, Read, Job permissions, etc.)

Click "Apply" then "Save"

The global authorization strategy defines the default permission model for Jenkins. Project-based Matrix Authorization Strategy enables both global and per-project permission matrices. It's critical to grant the admin user full permissions (all checkboxes) before saving - otherwise you could lock yourself out of Jenkins. The global matrix defines baseline permissions that all users get. Project-specific matrices can then add or restrict permissions for individual jobs.

**Step 4:** Verify existing users and job

Before configuring project security, verify:

Users exist:
- Navigate to Manage Jenkins > Manage Users
- Confirm users "sam" and "rohan" are listed

Job exists:
- Dashboard should show "Packages" job

If users or job don't exist, the task is invalid and you need to check lab setup.

Verification prevents configuration errors. The task assumes existing users (sam with password sam@pass12345, rohan with password rohan@pass12345) and an existing Packages job. If these don't exist, attempting to grant permissions will fail. Always verify prerequisites before configuring security - trying to grant permissions to non-existent users or jobs creates confusion and potential security issues.

**Step 5:** Configure project-based security for Packages job

Dashboard > Packages job > Configure

Scroll to the "Enable project-based security" section (near the bottom)

Check the box: "Enable project-based security"

Under "Inheritance Strategy":
- Select "Inherit permissions from parent ACL"

This enables job-level security for the Packages job while inheriting global permissions. The parent ACL (Access Control List) refers to the global authorization matrix you configured earlier. Inheritance means users with global permissions retain those permissions, plus any additional permissions granted at the project level. This strategy is most common - it allows global admins to always access jobs while granting additional project-specific permissions to team members.

**Step 6:** Grant permissions to user "sam"

In the project-based security matrix, click "Add user or group"

Enter username: sam

Grant the following permissions to sam (check these boxes):
- Job/Build: Allows triggering builds
- Job/Configure: Allows modifying job configuration
- Job/Read: Allows viewing job and build history

Leave other permissions unchecked for sam.

These permissions give sam the ability to view the job, modify its configuration, and trigger builds. Build permission is essential for developers who need to run jobs. Configure permission allows modifying job settings (build steps, parameters, schedules). Read permission is the baseline that allows viewing the job in the dashboard and accessing build history. This permission set is typical for developers who actively work with a job but don't need advanced permissions like workspace management or deletion.

**Step 7:** Grant permissions to user "rohan"

Click "Add user or group" again

Enter username: rohan

Grant the following permissions to rohan (check these boxes):
- Job/Build: Trigger builds
- Job/Cancel: Stop running builds
- Job/Configure: Modify job configuration
- Job/Read: View job and build history
- Job/Update: Update job description and settings
- Job/Tag: Create tags for builds

Leave other permissions (like Delete, Workspace) unchecked.

Rohan receives more extensive permissions than sam. Cancel permission allows stopping running builds (useful for release managers). Update permission enables modifying job metadata and settings beyond basic configuration. Tag permission allows creating meaningful labels for builds (e.g., "release-1.0", "tested", "production-ready"). This permission set is appropriate for senior developers, team leads, or release managers who need more control over the CI/CD pipeline.

**Step 8:** Save project security configuration

Click "Apply" then "Save"

After saving, the Packages job now has project-specific permissions. Sam can view, configure, and build the job. Rohan can do all that plus cancel builds, update settings, and tag builds. The admin user retains full access through global permissions. Test the configuration by logging in as sam and rohan to verify each user can access the job according to their granted permissions.

**Step 9:** Test permissions as user "sam"

Log out of admin account

Log in with sam credentials:
- Username: sam
- Password: sam@pass12345

Navigate to Packages job:
- Should be visible in dashboard (Read permission)
- Click "Configure" - should be allowed (Configure permission)
- Click "Build Now" - should be allowed (Build permission)
- Try to delete the job - should be denied (no Delete permission)

Log out

Testing validates the permission matrix works correctly. Sam should be able to perform only the actions granted (build, configure, read). Attempting unauthorized actions (like deletion) should show "Access Denied" or hide the option entirely. This verification ensures security is working as intended and prevents privilege escalation vulnerabilities.

**Step 10:** Test permissions as user "rohan"

Log in with rohan credentials:
- Username: rohan
- Password: rohan@pass12345

Navigate to Packages job:
- Should be visible (Read permission)
- Click "Configure" - allowed (Configure permission)
- Start a build, then click build number > "Cancel Build" - allowed (Cancel permission)
- Click on a completed build > "Keep this build forever" - allowed (Update/Tag permission)
- Try to delete the job - should be denied (no Delete permission)

Log out and log back in as admin

Rohan's extended permissions should all work correctly. Cancel permission allows stopping long-running builds. The "Keep this build forever" option uses Update permission to prevent automatic build cleanup. Tag functionality might appear in plugins that support build tagging. Like sam, rohan cannot delete the job because that permission wasn't granted. This demonstrates fine-grained access control working properly.

**Step 11:** Verify permission inheritance

The inheritance strategy "Inherit permissions from parent ACL" means:
- Admin user (configured globally) has full access to Packages job
- Sam gets global permissions + project-specific permissions (build, configure, read)
- Rohan gets global permissions + project-specific permissions (build, cancel, configure, read, update, tag)

Without project-based security, all users would have the same permissions defined globally. With inheritance, the global permissions serve as a baseline, and project permissions add to that baseline. If you selected "Do not inherit" instead, only explicitly granted permissions would apply (more restrictive). Inheritance is usually preferred for its flexibility.

---

## Key Concepts

**Project-Level Security:**
- Granular Control: Set different permissions for different users on the same job
- Inheritance: Optionally inherit global permissions as baseline, add project-specific permissions
- Override: Can override global permissions for specific projects (restrict or expand access)
- Team Isolation: Separate team access to different projects without affecting other teams

**Permission Matrix:**
- Users and Groups: Assign permissions to individual users or LDAP/Active Directory groups
- Permission Types: Build, Configure, Read, Update, Tag, Cancel, Delete, Workspace, Credentials, etc.
- Inheritance Strategy: Control how permissions flow from global to project level
- Explicit Permissions: Clearly defined permissions prevent ambiguity and security holes

**Security Strategies:**
- Role-based Access Control (RBAC): Define roles (developer, tester, admin) with specific permissions
- Least Privilege Principle: Grant only the minimum permissions required to perform job functions
- Regular Reviews: Audit permissions periodically as team members change roles or leave
- Documentation: Document who has what permissions and why (for compliance and onboarding)

**Common Permissions:**
- Read: View job configuration, builds, and console output (baseline permission for visibility)
- Build: Trigger job execution manually or via API (for developers running tests/builds)
- Configure: Modify job settings, build steps, parameters (for job owners and maintainers)
- Cancel: Stop running builds (for release managers handling deployment issues)
- Update: Modify job metadata, description, and build settings (for configuration management)
- Tag: Create labels for builds to mark releases, milestones, or tested versions
- Delete: Remove jobs entirely (should be restricted to admins only)
- Workspace: View and manage job workspace files (for debugging build issues)

**Security Best Practices:**
- Minimal Admin Access: Limit admin privileges to essential personnel only
- Group-based Permissions: Use LDAP/AD groups instead of individual users for easier management
- Audit Logs: Enable audit logging to track permission changes and access patterns
- Two-Factor Authentication: Require 2FA for admin accounts and sensitive job access
- Regular Cleanup: Remove permissions for users who change roles or leave the organization

---

## Validation

Test your solution using KodeKloud's automated validation.

Verify:
1. Project-based Matrix Authorization Strategy is enabled globally
2. Admin user has full permissions in global matrix
3. Packages job has "Enable project-based security" enabled
4. Inheritance strategy is "Inherit permissions from parent ACL"
5. User sam has permissions: Build, Configure, Read
6. User rohan has permissions: Build, Cancel, Configure, Read, Update, Tag
7. Login as sam and verify limited access
8. Login as rohan and verify extended access

---

[← Day 75](day-75.md) | [Day 77 →](day-77.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
