# Day 34: Configure Git Hook

## Task Overview

Implement a Git server-side hook that automatically creates release tags based on the current date whenever changes are pushed to the master branch. Git hooks enable automation of repetitive tasks and enforcement of repository policies.

**Technical Specifications:**
- Repository: /opt/demo.git (bare repository on storage server)
- Working directory: /usr/src/kodekloudrepos/demo (cloned repository)
- Hook type: post-update (server-side hook)
- Automation: Create dated release tag on every push to master
- Tag format: release-YYYY-MM-DD (e.g., release-2023-06-15)
- Prerequisites: Merge feature branch into master before testing hook

**Scenario:**
The development team wants to automatically create release tags with the current date whenever code is pushed to the master branch. This ensures consistent versioning and provides a clear timeline of releases without manual tag creation. The post-update hook runs on the remote repository after successful push operations, making it ideal for this automation.

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Connect to storage server with root privileges

```sh
sudo -i
```

Elevate to root user to gain administrative access required for modifying Git repositories in system directories. The `sudo -i` command initiates a root login shell with full system privileges. This access is necessary because both the bare repository (/opt/demo.git) and working repository (/usr/src/kodekloudrepos/demo) are located in system-managed directories that require elevated permissions to modify.

**Step 2:** Navigate to the working repository

```sh
cd /usr/src/kodekloudrepos/demo
```

Change to the cloned working repository where you'll perform Git operations. This is a standard working repository (not bare) where you can view files, make commits, and push to the remote. The remote for this repository is the bare repository at /opt/demo.git. All development work happens in this directory before being pushed to the bare repository.

**Step 3:** Check current branch and available branches

```sh
git branch
```

List all local branches to see which branch you're currently on and what other branches exist. The output shows an asterisk (*) next to your current branch. You'll likely see both "master" and "feature" branches. This task requires merging the feature branch into master, so you need to identify your current position before proceeding.

**Step 4:** Switch to master branch

```sh
git switch master
# or alternatively:
# git checkout master
```

Change your current working branch to master. The `git switch` command (introduced in Git 2.23) is the modern way to change branches, though `git checkout` still works. Switching to master is necessary because you'll be merging the feature branch into it. Git updates your working directory to reflect the master branch's state after switching.

**Step 5:** Merge feature branch into master

```sh
git merge feature
```

Integrate all commits from the feature branch into the master branch. Git performs the merge by combining the commit histories and creating either a fast-forward merge (if master hasn't diverged) or a merge commit (if both branches have unique commits). This merge prepares the master branch with the latest development work, which you'll push to test the post-update hook. The merge should complete without conflicts in the lab environment.

**Step 6:** Create post-update hook from sample

```sh
cp /opt/demo.git/hooks/post-update.sample /opt/demo.git/hooks/post-update
```

Copy the sample post-update hook template to create an active post-update hook. Git repositories include sample hooks (with .sample extension) that serve as templates but aren't executed. Removing the .sample extension activates the hook. The /opt/demo.git/hooks directory is where server-side hooks reside for the bare repository. This hook will execute after successful push operations to this repository.

**Step 7:** Make the hook executable

```sh
chmod +x /opt/demo.git/hooks/post-update
```

Add execute permissions to the post-update hook script. Git only runs hooks that have executable permissions set. The `chmod +x` command grants execute permission to the file owner, group, and others. Without this step, Git would ignore the hook file even though it exists. Executable permission is a security feature ensuring hooks run intentionally.

**Step 8:** Edit the post-update hook to add tagging logic

```sh
vi /opt/demo.git/hooks/post-update
# or use nano:
# nano /opt/demo.git/hooks/post-update
```

Open the post-update hook file in a text editor to add your custom automation logic. You'll need to add shell script code that creates a dated release tag. Vi/Vim or nano are common command-line text editors available on Linux systems. The hook file is a shell script that Git executes, so you can use any valid bash commands.

**Step 9:** Add tag creation logic to the hook

Add the following lines to the post-update hook file (append or replace existing content):

```bash
#!/bin/sh
#
# An example hook script to prepare a packed repository for use over
# dumb transports.
#
# To enable this hook, rename this file to "post-update".

# Get current date in YYYY-MM-DD format
day=$(date +"%Y-%m-%d")

# Construct tag name
TAG="release-$day"

# Create annotated tag with current date
git tag -a $TAG -m "Released at: $day"

# Execute the default post-update actions
exec git update-server-info
```

Add custom shell script code to create a dated release tag after every push. The `date` command formats the current date as YYYY-MM-DD. The TAG variable constructs the tag name by prefixing "release-" to the date. The `git tag -a` command creates an annotated tag (which stores metadata like tagger name, date, and message) rather than a lightweight tag. The `-m` flag specifies the tag message. The final `exec` line runs the default post-update behavior (update-server-info) which is needed for dumb HTTP transport.

**Step 10:** Save and exit the editor

For vi/vim:
- Press `Esc` to ensure you're in command mode
- Type `:wq` and press Enter (write and quit)

For nano:
- Press `Ctrl+O` to write (save)
- Press Enter to confirm filename
- Press `Ctrl+X` to exit

Save your changes to the post-update hook file and exit the text editor. The hook is now configured and will execute whenever a push operation completes on the /opt/demo.git repository. The automation will create a new release tag with today's date each time you push to the repository.

**Step 11:** Push the merged master branch to trigger the hook

```sh
git push
# or be explicit:
# git push origin master
```

Push the merged master branch to the remote repository (/opt/demo.git). This operation uploads your local commits and triggers the post-update hook on the server side. Since you merged the feature branch into master, this push will include those changes. The post-update hook executes after the push completes successfully, automatically creating a release tag with today's date. You should see output indicating the hook ran.

**Step 12:** Fetch tags from remote repository

```sh
git fetch --tags
```

Download all tags from the remote repository to your local repository. Tags are not automatically fetched during a normal `git pull`, so you need to explicitly request them with the `--tags` flag. This command retrieves the release tag that the post-update hook just created on the remote repository. Fetching tags allows you to verify that the hook executed successfully.

**Step 13:** List all tags to verify hook execution

```sh
git tag
# or for more details:
# git tag -l -n
```

Display all tags in the repository to confirm the release tag was created. You should see a tag named "release-YYYY-MM-DD" where YYYY-MM-DD is today's date. This verifies that the post-update hook executed successfully and created the tag as expected. The tag serves as a snapshot marker for this release, which can be referenced later for deployments, rollbacks, or historical reference.

**Step 14:** Optional - View tag details

```sh
git show release-2023-06-15
# Replace with actual date
```

Display detailed information about the specific release tag, including the tag message, tagger information, and the commit it points to. This command shows that the tag is properly annotated with the message "Released at: YYYY-MM-DD". Viewing tag details confirms the hook created a complete, properly formatted tag rather than just a lightweight reference.

**Step 15:** Optional - Test hook with another push

Make a trivial change and push again to verify the hook runs consistently:

```sh
echo "# Test" >> README.md
git add README.md
git commit -m "Test hook functionality"
git push
git fetch --tags
git tag
```

Create a test commit and push to verify the hook executes on subsequent pushes. Note that if you test on the same day, the tag creation might fail because the tag "release-YYYY-MM-DD" already exists. In production, the hook script could be enhanced to handle duplicate tag names by adding timestamps or version numbers. This test demonstrates that the hook is persistently active for all push operations.

---

## Key Concepts

**Git Hooks:**
- **Definition**: Scripts that Git executes automatically before or after specific events
- **Purpose**: Automate tasks, enforce policies, trigger workflows, integrate with external systems
- **Types**: Client-side (run on local machine) and server-side (run on remote repository)
- **Implementation**: Shell scripts (or any executable) in .git/hooks directory
- **Naming**: Hook name matches Git event (pre-commit, post-update, etc.)

**Hook Types:**

**Client-Side Hooks** (run on developer's machine):
- **pre-commit**: Runs before commit is created (validate code, run linters)
- **prepare-commit-msg**: Runs before commit message editor opens (auto-generate message template)
- **commit-msg**: Runs after commit message is entered (validate message format)
- **post-commit**: Runs after commit is created (send notifications, update logs)
- **pre-rebase**: Runs before rebase operation (prevent rebasing protected branches)
- **post-merge**: Runs after merge completes (update dependencies, run migrations)
- **pre-push**: Runs before push to remote (run tests, check for large files)

**Server-Side Hooks** (run on remote repository):
- **pre-receive**: Runs before accepting push (enforce policies, validate commits)
- **update**: Runs for each branch being updated (branch-specific policies)
- **post-receive**: Runs after push is accepted (trigger deployments, send notifications)
- **post-update**: Runs after all references are updated (update server info, create tags)

**Hook Implementation:**
- **Location**: `.git/hooks/` directory (local repos) or `hooks/` (bare repos)
- **Executable Requirement**: Must have execute permission (`chmod +x`)
- **Language**: Any executable (bash, Python, Ruby, etc.)
- **Exit Codes**: Non-zero exit code prevents operation (pre-hooks only)
- **Standard Output**: Hook output appears in user's terminal

**Post-Update Hook:**
- **Trigger**: After all references (branches, tags) are updated from push
- **Use Cases**: Update cached repo info, create tags, trigger CI/CD, send notifications
- **Server-Side**: Runs on remote repository, not client
- **Parameters**: Receives list of updated refs as arguments
- **Default Behavior**: Runs `git update-server-info` for dumb HTTP transport

**Git Tagging:**
- **Purpose**: Mark specific commits as important (releases, milestones)
- **Lightweight Tags**: Simple pointer to commit (just a reference)
  ```sh
  git tag v1.0.0
  ```
- **Annotated Tags**: Full objects with metadata (tagger, date, message)
  ```sh
  git tag -a v1.0.0 -m "Release version 1.0.0"
  ```
- **Recommended**: Use annotated tags for releases (more information)
- **Listing**: `git tag` or `git tag -l "v1.*"` (pattern matching)
- **Pushing**: Tags aren't automatically pushed; use `git push --tags`

**Common Hook Use Cases:**
- **Code Quality**: Run linters, formatters, tests before commit/push
- **Policy Enforcement**: Require commit message format, prevent large files
- **Security**: Scan for secrets, credentials, sensitive data
- **Documentation**: Auto-generate docs, update changelogs
- **Deployment**: Trigger CI/CD pipelines, deploy to staging/production
- **Notifications**: Send emails, Slack messages, create tickets
- **Versioning**: Auto-create tags, update version numbers

**Hook Development Best Practices:**
- **Exit Codes**: Return 0 for success, non-zero to abort operation (pre-hooks)
- **Output Messages**: Provide clear feedback about why hook failed
- **Performance**: Keep hooks fast to avoid slowing down Git operations
- **Testing**: Test hooks thoroughly before deployment
- **Documentation**: Document what hooks do and why they exist
- **Error Handling**: Handle edge cases gracefully

**Example Pre-Commit Hook (Code Formatting):**
```bash
#!/bin/sh
# Run code formatter before commit

echo "Running code formatter..."
npm run format

if [ $? -ne 0 ]; then
    echo "Code formatting failed. Please fix errors."
    exit 1
fi

git add -u  # Re-add formatted files
exit 0
```

**Example Pre-Push Hook (Run Tests):**
```bash
#!/bin/sh
# Run test suite before push

echo "Running test suite..."
npm test

if [ $? -ne 0 ]; then
    echo "Tests failed. Fix tests before pushing."
    exit 1
fi

exit 0
```

**Server-Side Hook Considerations:**
- **Centralized Control**: Enforced for all users pushing to repository
- **Cannot Be Bypassed**: Unlike client-side hooks which can be skipped
- **Bare Repository**: Server hooks live in bare repo's hooks/ directory
- **Git Hosting**: GitHub/GitLab provide webhook alternatives (not true Git hooks)
- **Execution Context**: Runs with server user's permissions and environment

**Distributing Hooks:**
- **Challenge**: Hooks aren't tracked in Git (in .gitignore by default)
- **Solution 1**: Store hooks in tracked directory, symlink to .git/hooks
- **Solution 2**: Use scripts to install hooks from template
- **Solution 3**: Use tools like Husky (Node.js) or pre-commit framework (Python)

**Debugging Hooks:**
- **Add Logging**: Write to file to see hook execution
  ```bash
  echo "Hook ran at $(date)" >> /tmp/hook.log
  ```
- **Check Permissions**: Verify hook has execute permission
- **Test Manually**: Run hook script directly to test logic
- **View Output**: Hook output appears in Git command output

**Advanced Hook Features:**
- **Access Commit Data**: Read commit message, changed files, author info
- **Environment Variables**: Git provides variables like GIT_DIR, GIT_AUTHOR_NAME
- **Arguments**: Some hooks receive arguments (refs, commits, etc.)
- **Chaining**: Call multiple scripts from one hook
- **Conditional Logic**: Run different actions based on branch, files changed, etc.

---

## Validation

Test your solution using KodeKloud's automated validation.

**Verification Checklist:**
1. Feature branch successfully merged into master
2. Post-update hook exists at /opt/demo.git/hooks/post-update
3. Hook has executable permissions
4. Hook contains tag creation logic
5. Release tag created with today's date format (release-YYYY-MM-DD)
6. Tag visible in repository via `git tag` command
7. Changes successfully pushed to remote repository

---

[← Day 33](day-33.md) | [Day 35 →](day-35.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
