# Day 21: Setup Git Repository on Server

## Task Overview

Set up a centralized Git repository on a storage server for team collaboration and version control. Install Git and create a bare repository that developers can clone, push to, and pull from.

**Git Repository Setup:**
- Install Git version control system
- Create bare repository for collaboration
- Configure repository location
- Prepare for team development workflows

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

### Step 1: Update System and Install Git

Update package repositories and install the Git version control system.

```sh
sudo yum update -y
sudo yum install -y git
```

The first command updates all installed packages and refreshes the YUM repository metadata to ensure you're installing the latest available version. The `-y` flag automatically confirms all prompts, streamlining the installation process. The second command installs Git, a distributed version control system designed for tracking changes in source code during software development. Git provides branching, merging, and distributed workflows that enable collaborative development. After installation, the `git` command becomes available for version control operations.

### Step 2: Create Bare Git Repository

Initialize a bare Git repository at the specified location on the storage server.

```sh
sudo git init --bare /opt/demo.git
```

This command creates a bare Git repository at `/opt/demo.git`. The `--bare` flag creates a repository without a working directory, containing only Git's internal data structures and version history. The `sudo` prefix is necessary because `/opt/` typically requires root permissions for creating directories. Bare repositories are the standard for central repositories that multiple developers push to and pull from, as they don't have a working tree where files could be edited, which would conflict with incoming pushes.

### Step 3: Verify Repository Creation

Confirm the bare repository was created successfully and examine its structure.

```sh
ls -la /opt/demo.git
```

This command lists all files and directories in the newly created repository, including hidden files (the `-a` flag). A properly initialized bare repository contains directories like `hooks/`, `info/`, `objects/`, `refs/`, and files like `config`, `HEAD`, and `description`. This structure represents Git's internal database and configuration. Verifying the repository structure ensures initialization completed successfully before developers begin using it.

---

## Key Concepts

### Git Version Control System

**Distributed Architecture**: Unlike centralized version control systems (SVN, CVS), Git is fully distributed. Every developer has a complete copy of the repository including full history, enabling work offline and providing redundancy.

**Version History**: Git tracks every change to every file through commits, which are snapshots of your project at specific points in time. Each commit references its parent commit(s), forming a directed acyclic graph (DAG) of history.

**Branching and Merging**: Git's lightweight branching model makes creating, switching, and merging branches fast and easy. Branches enable parallel development of features, bug fixes, and experiments without affecting the main codebase.

**Collaboration**: Git facilitates team collaboration through push/pull workflows, allowing multiple developers to work on the same project simultaneously while Git manages merging changes.

### Bare vs Working Repositories

**Working Repository**: A standard Git repository initialized with `git init` contains both the `.git` directory (Git's database) and a working tree (checked-out files you can edit). This is what developers use on their local machines for development.

**Bare Repository**: Created with `git init --bare`, these repositories contain only Git's internal data (equivalent to the `.git` directory) without a working tree. Attempting to edit files in a bare repository would fail because there's no working directory.

**Use Cases**: Bare repositories serve as central hubs for collaboration. Developers clone from the bare repository, work in their local working repositories, and push changes back to the bare repository. Non-bare repositories are for development work where files need to be edited.

**Naming Convention**: Bare repositories typically have a `.git` suffix (e.g., `demo.git`) to clearly indicate they're bare repositories, while working repositories don't have this suffix.

### Central Repository Setup

**Location**: Central repositories are typically stored on servers in directories like `/opt/`, `/var/git/`, or `/srv/git/`. These locations are accessible to all team members and backed up regularly.

**Permissions**: Set appropriate ownership and permissions to control who can push to the repository. Use `chown -R git:git /opt/demo.git` to make it owned by a dedicated git user, and `chmod -R 770` to restrict access to the git group.

**Access Methods**: Developers can access central repositories via SSH (most common and secure), HTTPS (simpler but less secure without additional configuration), or the Git protocol (read-only, rarely used for production).

**Shared Repository**: For shared hosting, set the `core.sharedRepository` configuration to allow multiple users to push: `git config core.sharedRepository group`.

### Git Workflows

**Centralized Workflow**: Similar to SVN, developers clone from a central repository, commit locally, and push to the central repo. Simple but doesn't leverage Git's distributed nature fully.

**Feature Branch Workflow**: Developers create dedicated branches for each feature or bug fix. When complete, they merge or rebase into the main branch. This isolates work and enables code review through pull requests.

**Gitflow Workflow**: Structured workflow with specific branch types: `main` (production), `develop` (integration), `feature/*`, `release/*`, and `hotfix/*`. Provides clear release management but can be complex for small teams.

**Fork and Pull Request**: Common in open source, developers fork the repository, make changes in their fork, and submit pull requests to the original repository. Maintainers review and merge changes.

### Repository Structure

**Object Database**: The `objects/` directory contains all repository content (commits, trees, blobs) stored as compressed objects referenced by SHA-1 hashes. Git uses content-addressable storage for integrity and deduplication.

**References**: The `refs/` directory contains pointers to commit objects. `refs/heads/` has branches (e.g., `refs/heads/main`), `refs/tags/` has tags, and `refs/remotes/` has remote-tracking branches.

**HEAD**: The `HEAD` file points to the current branch reference. In a bare repository, it typically points to `refs/heads/main` or `refs/heads/master`, indicating the default branch for new clones.

**Configuration**: The `config` file contains repository-specific Git configuration, including remote definitions, branch tracking information, and user settings that override global configuration.

**Hooks**: The `hooks/` directory contains scripts that Git executes at specific points in its workflow (pre-commit, post-receive, etc.). These enable automation like running tests, enforcing commit message formats, or triggering deployments.

### Cloning and Remote Operations

**Cloning**: Developers clone the central repository with `git clone ssh://server/opt/demo.git`, which creates a local working repository. The bare repository becomes the remote named "origin" in their local clone.

**Pushing Changes**: After committing locally, developers push changes to the central repository with `git push origin branch-name`. Git transfers only new commits and objects, making pushes efficient even for large repositories.

**Pulling Changes**: Developers update their local repository with changes from the central repo using `git pull origin branch-name`, which fetches and merges remote changes into the current branch.

**Fetch vs Pull**: `git fetch` downloads objects and refs from the remote without merging, allowing you to review changes before integrating. `git pull` is effectively `git fetch` followed by `git merge`.

### Git Installation

**Package Managers**: On RHEL/CentOS, use `yum install git`. On Debian/Ubuntu, use `apt install git`. On macOS, use `brew install git` or install Xcode command-line tools.

**Version Considerations**: Different Git versions have different features and behavior. Check your version with `git --version`. Modern features like `git switch` and `git restore` require Git 2.23+.

**Configuration**: After installation, configure user identity with `git config --global user.name "Your Name"` and `git config --global user.email "you@example.com"`. These settings identify commit authors.

**Additional Tools**: Consider installing related tools like `gitk` (graphical commit viewer), `git-gui` (graphical commit tool), and `tig` (text-mode interface for Git).

### SSH Access Configuration

**SSH Keys**: Developers generate SSH key pairs with `ssh-keygen` and add their public key to the server's `~/.ssh/authorized_keys` file for the git user. This enables passwordless authentication.

**Restricted Shell**: For security, consider restricting the git user to git-shell, a limited shell that only allows Git commands. Set it as the git user's shell in `/etc/passwd` or with `usermod -s $(which git-shell) git`.

**SSH Configuration**: Developers can simplify SSH access by adding entries to `~/.ssh/config`:
```
Host git-server
    HostName server.example.com
    User git
    IdentityFile ~/.ssh/id_rsa_git
```

**Port Forwarding**: If using non-standard SSH ports, specify in the clone URL: `git clone ssh://git@server:2222/opt/demo.git` or configure in SSH config.

### Repository Permissions

**User/Group Setup**: Create a dedicated `git` user and group for repository management. Add authorized developers to the git group, allowing controlled access to repositories.

**File Permissions**: Set repository directories to 770 (rwxrwx---) and files to 660 (rw-rw----) to allow group read/write while preventing other users from accessing repositories.

**umask Configuration**: Set appropriate umask (e.g., 0002) for the git user to ensure newly created objects have correct group permissions.

**SELinux Contexts**: On SELinux-enabled systems, set appropriate contexts for Git directories if they're not in standard locations. Use `semanage fcontext` and `restorecon` to configure contexts.

### Git Hooks for Automation

**Server-Side Hooks**: Bare repositories support hooks like `pre-receive` (validate pushes), `update` (called once per branch), and `post-receive` (trigger actions after successful push).

**Deployment Automation**: Use post-receive hooks to automatically deploy code after successful pushes. Example: checkout code to a web directory, run build scripts, restart services.

**Validation Hooks**: Pre-receive hooks can enforce policies like commit message format, branch naming conventions, or code quality checks, rejecting pushes that don't meet standards.

**Notification Hooks**: Post-receive hooks can send notifications (email, Slack, webhooks) when code is pushed, keeping teams informed of repository activity.

### Backup and Maintenance

**Repository Backups**: Back up Git repositories by copying the entire directory or using `git bundle` to create portable repository snapshots. Bare repositories are easy to back up as they're single directories.

**Garbage Collection**: Git automatically runs garbage collection (`git gc`) to compress objects and clean up unnecessary files. On busy repositories, schedule periodic maintenance with `git gc --aggressive`.

**Repack Objects**: Large repositories benefit from repacking objects with `git repack -a -d` to optimize storage and improve performance by creating larger, more efficient pack files.

**Prune Unreachable Objects**: Use `git prune` to remove objects no longer reachable from any reference. This is automatically done by garbage collection but can be run manually for immediate cleanup.

### Advanced Repository Management

**Multiple Remotes**: Repositories can have multiple remotes. Developers might have `origin` (central repo) and `backup` (backup server): `git remote add backup ssh://backup-server/opt/demo.git`.

**Mirroring**: Create exact copies of repositories with `git clone --mirror`, which copies all refs (branches, tags) and configuration. Useful for creating backup mirrors or transitioning hosting providers.

**Submodules**: Include other Git repositories as subdirectories within a repository using submodules. Useful for managing dependencies or splitting large projects into manageable components.

**Git LFS**: For repositories with large files (binaries, media), use Git Large File Storage to store large files outside the main repository, keeping the repository small and performant.

---

## Validation

Test your solution using KodeKloud's automated validation.

---

[← Day 20](day-20.md) | [Day 22 →](../week-04/day-22.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
