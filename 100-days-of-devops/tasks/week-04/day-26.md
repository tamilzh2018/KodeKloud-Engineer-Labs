# Day 26: Git Manage Remotes

## Task Overview

The xFusionCorp development team made updates to the project maintained under `/opt/beta.git` (cloned at `/usr/src/kodekloudrepos/beta`). The DevOps team added new Git remotes on the Storage server in Stratos DC, requiring updates to the local repository's remote configuration. This exercise demonstrates remote repository management, a critical skill for distributed development workflows.

**Scenario Requirements:**
- Repository location: `/usr/src/kodekloudrepos/beta`
- Add new remote named `dev_beta` pointing to `/opt/xfusioncorp_beta.git`
- Copy `/tmp/index.html` to the repository
- Add and commit the file to the master branch
- Push the master branch to the new `dev_beta` remote

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Key Concepts

### Git Remotes Fundamentals

**What are Git Remotes?**
Remotes are references to remote repositories that allow you to collaborate with others. They're bookmarks for repository locations, whether on network servers, GitHub, GitLab, or even other directories on your local machine. Remotes enable pushing your changes and fetching updates from collaborators.

**Why Use Remotes?**
Remotes are essential for distributed development. They allow multiple developers to work on the same project from different locations, provide backup locations for your code, enable code review through pull requests, and facilitate continuous integration and deployment pipelines.

**Origin Remote:**
When you clone a repository, Git automatically creates a remote named 'origin' pointing to the source repository. This is just a convention - 'origin' is not special, it's simply the default name Git uses. You can rename it or create additional remotes with any name you choose.

### Remote Operations

**Adding Remotes:**
```bash
git remote add <name> <url>
```
Creates a new remote reference with the specified name pointing to the given URL. The URL can be HTTPS, SSH, or a local file path.

**Listing Remotes:**
```bash
git remote -v
```
The `-v` (verbose) flag shows all configured remotes with their fetch and push URLs. Without `-v`, only remote names are displayed.

**Removing Remotes:**
```bash
git remote remove <name>
```
Deletes the specified remote reference. This doesn't affect the remote repository itself, only your local configuration.

**Renaming Remotes:**
```bash
git remote rename <old-name> <new-name>
```
Changes the local name of a remote reference, useful for improving clarity or fixing typos.

**Inspecting Remotes:**
```bash
git remote show <name>
```
Displays detailed information about a remote, including tracked branches, push/pull URLs, and branch relationships.

### Remote URL Types

Git supports several protocols for accessing remote repositories:

**Local File Path:**
```bash
git remote add backup /opt/repository.git
```
References a repository on the local filesystem or network-mounted drive. Fast and simple, ideal for local development or backup scenarios.

**HTTPS Protocol:**
```bash
git remote add origin https://github.com/user/repo.git
```
User-friendly with credential caching, works through firewalls, commonly used for public repositories. Requires username/password or token authentication.

**SSH Protocol:**
```bash
git remote add origin git@github.com:user/repo.git
```
Secure authentication using SSH keys, no password prompts after key setup, preferred for private repositories and automated workflows.

**Git Protocol:**
```bash
git remote add origin git://server/repo.git
```
Fast but unencrypted, typically used for read-only access to public repositories. Rarely used in modern development.

### Pushing to Specific Remotes

**Basic Push:**
```bash
git push <remote> <branch>
```
Uploads commits from the specified local branch to the remote repository.

**Set Upstream:**
```bash
git push -u <remote> <branch>
```
The `-u` (or `--set-upstream`) flag establishes a tracking relationship, so future `git push` and `git pull` commands know which remote branch to use.

**Push All Branches:**
```bash
git push --all <remote>
```
Uploads all local branches to the remote repository at once.

**Force Push (Dangerous):**
```bash
git push --force <remote> <branch>
```
Overwrites remote history with your local history. Use with extreme caution as it can lose other developers' work.

### Multiple Remotes Use Cases

**Fork Workflow:**
- `origin`: Your fork
- `upstream`: Original repository
Allows you to fetch updates from the original while pushing to your fork.

**Deployment:**
- `origin`: Development server
- `production`: Production server
Enables pushing to different environments from the same repository.

**Backup:**
- `origin`: Primary repository
- `backup`: Backup location
Provides redundancy by pushing to multiple locations.

**Team Collaboration:**
- `origin`: Central repository
- `teammate`: Colleague's repository
Facilitates direct collaboration between team members.

---

## Solution Steps

### Step 1: Access the Storage Server

Log into the Storage server via SSH.

```bash
ssh user@storage-server
```

This establishes a secure connection to the Storage server in Stratos DC where the beta repository is located. The server hosts multiple repositories for the xFusionCorp development team.

### Step 2: Elevate Privileges

Switch to root user for necessary permissions.

```bash
sudo su
```

The `sudo su` command grants root access, ensuring you have the required permissions to access repositories, modify files, and configure Git remotes. This is necessary when repositories are owned by system accounts or have restricted permissions.

### Step 3: Navigate to Repository

Change to the beta repository directory.

```bash
cd /usr/src/kodekloudrepos/beta
```

This command makes the beta repository your current working directory. All subsequent Git commands will operate within this repository context. The path `/usr/src/kodekloudrepos/` is the standard location for development repositories in this environment.

### Step 4: Check Current Remotes

View existing remote configurations.

```bash
git remote -v
```

The `git remote -v` command lists all configured remotes with their URLs for both fetch (downloading) and push (uploading) operations. Before adding a new remote, it's good practice to review existing remotes to avoid naming conflicts and understand the current configuration.

Expected output:
```
origin  /opt/beta.git (fetch)
origin  /opt/beta.git (push)
```

### Step 5: Verify Current Branch

Check which branch is active.

```bash
git branch
```

The `git branch` command shows all local branches with the current branch marked by an asterisk (*). You need to be on the master branch to commit and push changes as required. This verification step ensures you're working on the correct branch before making changes.

If not on master, switch to it:
```bash
git switch master
```

### Step 6: Add New Remote

Create a new remote reference named dev_beta.

```bash
git remote add dev_beta /opt/xfusioncorp_beta.git
```

This command adds a new remote called `dev_beta` pointing to the repository at `/opt/xfusioncorp_beta.git`. The remote name `dev_beta` is arbitrary - you can choose any name that's meaningful. This remote will be used to push changes to an alternate repository location, supporting scenarios like separate development and production repositories.

The command doesn't produce output but creates the remote reference in your local Git configuration.

### Step 7: Verify New Remote

Confirm the remote was added successfully.

```bash
git remote -v
```

Running `git remote -v` again displays the updated remote configuration. You should now see both `origin` and `dev_beta` remotes listed. Each remote shows separate URLs for fetch and push operations, though in this case they're the same.

Expected output:
```
dev_beta  /opt/xfusioncorp_beta.git (fetch)
dev_beta  /opt/xfusioncorp_beta.git (push)
origin    /opt/beta.git (fetch)
origin    /opt/beta.git (push)
```

### Step 8: Copy File to Repository

Copy the index.html file from /tmp to the repository.

```bash
cp /tmp/index.html .
```

The `cp` command copies `/tmp/index.html` to the current directory (`.`). This file represents a change that needs to be committed and pushed to the new remote. In real-world scenarios, this could be configuration updates, new features, or documentation.

Verify the copy:
```bash
ls -l index.html
```

### Step 9: Check Repository Status

View the current working directory state.

```bash
git status
```

The `git status` command shows which files are modified, staged, or untracked. After copying index.html, it appears as an untracked file. This status check is crucial for understanding what changes will be included in the commit and ensuring you're committing the intended files.

Expected output:
```
On branch master
Untracked files:
  (use "git add <file>..." to include in what will be committed)
        index.html

nothing added to commit but untracked files present (use "git add" to track)
```

### Step 10: Stage Changes

Add the new file to the staging area.

```bash
git add .
```

The `git add .` command stages all changes in the current directory for commit. The staging area (index) is an intermediate space where you prepare the next commit. Using `.` stages everything, but you could also stage specific files with `git add index.html` for more precise control.

### Step 11: Commit Changes

Create a commit with the staged changes.

```bash
git commit -m "added tmp file"
```

The `git commit` command creates a new snapshot (commit) in the repository history containing all staged changes. The `-m` flag allows you to specify the commit message inline. Good commit messages explain what changed and why, helping future developers (including yourself) understand the project's evolution.

The commit is now part of your local repository's master branch but hasn't been uploaded to any remote yet.

### Step 12: Verify Commit

Confirm the commit was created successfully.

```bash
git log --oneline -3
```

This displays the last 3 commits in abbreviated format. You should see your "added tmp file" commit at the top, along with its unique commit hash. This verification ensures the commit was created correctly before pushing to the remote.

### Step 13: Push to New Remote

Upload the master branch to the dev_beta remote.

```bash
git push dev_beta master
```

The `git push dev_beta master` command uploads your local master branch commits to the `dev_beta` remote repository. The syntax is `git push <remote> <branch>`. This makes your changes available in the dev_beta repository, separate from the origin remote.

Git will display progress information showing objects being compressed, written, and transferred. If this is the first push to this remote, Git creates the master branch on the remote repository.

### Step 14: Verify Push Success

Confirm the push completed successfully.

```bash
git log --oneline --all --decorate -5
```

This command shows the recent commit history with decorators indicating branch and remote positions. You should see `dev_beta/master` at the same position as your local `master`, confirming the push was successful.

---

## Additional Information

### Managing Multiple Remotes

When working with multiple remotes, you can push to different remotes based on your needs:

```bash
git push origin master      # Push to origin
git push dev_beta master    # Push to dev_beta
git push --all dev_beta     # Push all branches to dev_beta
```

### Fetching from Multiple Remotes

You can fetch updates from any configured remote:

```bash
git fetch origin           # Fetch from origin
git fetch dev_beta         # Fetch from dev_beta
git fetch --all            # Fetch from all remotes
```

### Setting Default Push Remote

Configure a branch to push to a specific remote by default:

```bash
git push -u dev_beta master
```

After setting upstream with `-u`, you can simply use `git push` without specifying the remote.

### Changing Remote URLs

If a remote's location changes, update the URL:

```bash
git remote set-url dev_beta /new/path/to/repository.git
```

### Remote Tracking Branches

Remote tracking branches are local references to the state of remote branches:

```bash
git branch -r              # List remote tracking branches
git branch -a              # List all branches (local + remote)
```

### Prune Stale Remote References

Remove references to deleted remote branches:

```bash
git remote prune dev_beta   # Prune specific remote
git fetch --prune           # Prune during fetch
```

---

## Validation

Test your solution using KodeKloud's automated validation system. The validator will check:
- New remote `dev_beta` is configured correctly
- Remote points to `/opt/xfusioncorp_beta.git`
- index.html file exists in the repository
- Changes were committed to the master branch
- Master branch was pushed to the dev_beta remote
- Repository state matches requirements

---

[← Day 25](day-25.md) | [Day 27 →](day-27.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
