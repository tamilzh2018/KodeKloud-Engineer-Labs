# Day 24: Git Branch Create

## Task Overview

The Nautilus development team is actively working on the `/usr/src/kodekloudrepos/media` repository and has decided to implement new features. To maintain code stability and enable parallel development, they need to create a separate branch for these experimental changes. This exercise demonstrates fundamental Git branching operations essential for modern software development workflows.

**Scenario Requirements:**
- Repository location: `/usr/src/kodekloudrepos/media`
- Create a new branch named `xfusioncorp_media` from the master branch
- Do not modify any code in the repository
- Server: Storage server in Stratos DC

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Key Concepts

### Git Branching Fundamentals

**What are Git Branches?**
Branches in Git are lightweight, movable pointers to specific commits in your repository's history. They enable multiple parallel lines of development to coexist, allowing teams to work on features, bug fixes, and experiments simultaneously without interfering with each other's work or the stable codebase.

**Core Characteristics:**
- **Lightweight**: Branches are simply 40-character SHA-1 checksums pointing to commits, making them extremely fast to create and switch between
- **Isolation**: Changes made in one branch don't affect other branches until explicitly merged, providing safe experimentation spaces
- **Parallel Development**: Multiple team members can work on different features simultaneously without conflicts
- **Easy Context Switching**: Developers can quickly switch between different tasks by changing branches

### Branch Operations

Understanding the different commands for branch management is crucial:

**Create Branch Only:**
```bash
git branch feature-name
```
This command creates a new branch pointing to your current commit but doesn't switch to it. You remain on your current branch. Use this when you want to create a branch for later use.

**Create and Switch:**
```bash
git checkout -b feature-name
```
This combines branch creation and switching in a single command. The `-b` flag tells Git to create a new branch before checking it out. This is the most common way to start working on a new feature.

**Modern Switch Command:**
```bash
git switch -c feature-name
```
Git 2.23 introduced `git switch` as a clearer alternative to `git checkout` for branch operations. The `-c` flag creates a new branch, similar to `checkout -b`.

**List Branches:**
```bash
git branch           # List local branches
git branch -a        # List all branches (local + remote)
git branch -r        # List only remote branches
```

### Branching Strategies

Different teams adopt various branching strategies based on their workflow:

**Feature Branches:**
Each new feature gets its own branch created from the main development branch. Features are developed in isolation and merged back when complete. This is the foundation of most modern workflows.

**Git Flow:**
A comprehensive branching model with distinct branch types:
- **master/main**: Production-ready code
- **develop**: Integration branch for features
- **feature/***: Individual feature branches
- **release/***: Release preparation branches
- **hotfix/***: Emergency production fixes

**GitHub Flow:**
A simplified workflow with just two branch types:
- **main**: Always deployable production branch
- **feature branches**: Short-lived branches for specific changes

**Trunk-Based Development:**
Developers work on very short-lived branches (hours to days) or directly on the main branch with feature flags controlling feature visibility.

### Branch Naming Best Practices

**Descriptive Names:**
Use clear, meaningful names that describe the purpose: `feature/user-authentication`, `bugfix/login-error`, `hotfix/security-patch`

**Consistency:**
Adopt a team-wide naming convention: `type/description` (e.g., `feature/`, `bugfix/`, `hotfix/`)

**Lowercase and Hyphens:**
Use lowercase letters and hyphens for readability: `add-payment-gateway` rather than `AddPaymentGateway`

**Avoid Special Characters:**
Stick to alphanumeric characters and hyphens to prevent issues with various tools and systems.

---

## Solution Steps

### Step 1: Access the Storage Server

Log into the Storage server where the repository is located.

```bash
ssh user@storage-server
```

This command establishes a secure shell connection to the Storage server in the Stratos DC. The Storage server hosts the development repositories for the Nautilus project. Ensure you have the correct credentials and network access to connect to this server.

### Step 2: Elevate Privileges

Switch to the root user to ensure proper access permissions.

```bash
sudo su
```

The `sudo su` command elevates your privileges to root user. This is necessary because the repository directory may have specific ownership and permission requirements. In production environments, you would typically use a service account with appropriate permissions rather than root access. The command prompts for your password to verify authorization.

### Step 3: Navigate to the Repository

Change to the repository directory where branching operations will be performed.

```bash
cd /usr/src/kodekloudrepos/media
```

This changes your working directory to the media repository. The path `/usr/src/kodekloudrepos/` is a standard location for storing Git repositories in this environment. Before performing any Git operations, you must be inside the repository directory. The `cd` command makes this the active directory for all subsequent commands.

### Step 4: Check Current Branch

Verify which branch is currently active before creating a new branch.

```bash
git branch
```

The `git branch` command lists all local branches in the repository. The current branch is indicated with an asterisk (*) and may be highlighted in color. This verification step is important because new branches are created from the currently active branch. If you're not on the master branch, you'll need to switch to it first to ensure the new branch is based on master as required.

Example output:
```
* master
  development
  staging
```

### Step 5: Switch to Master Branch (If Needed)

If you're not on the master branch, switch to it before creating the new branch.

```bash
git switch master
```

The `git switch` command changes your current branch to master. This modern Git command (introduced in Git 2.23) is more intuitive than the older `git checkout` command for branch switching. It updates your working directory to match the master branch's state and moves the HEAD pointer to reference master. This ensures that the new branch will be created from the correct starting point.

Alternative command:
```bash
git checkout master
```

### Step 6: Create and Switch to New Branch

Create the new branch and immediately switch to it in a single operation.

```bash
git checkout -b xfusioncorp_media
```

This command performs two operations atomically:
1. Creates a new branch named `xfusioncorp_media` pointing to the same commit as master
2. Switches your working directory to this new branch

The `-b` flag stands for "branch" and tells Git to create a new branch before checking it out. This is the most efficient way to start working on a new branch. After this command, any new commits you make will be added to the `xfusioncorp_media` branch, leaving the master branch unchanged.

Modern alternative:
```bash
git switch -c xfusioncorp_media
```

### Step 7: Verify Branch Creation

Confirm that the new branch was created and is currently active.

```bash
git branch
```

Running `git branch` again shows the updated branch list. You should now see `xfusioncorp_media` in the list with an asterisk (*) indicating it's the current branch. This verification ensures the branch was created successfully and is ready for development work.

Expected output:
```
  master
* xfusioncorp_media
```

### Step 8: Check Branch Relationship

Verify that the new branch points to the same commit as master.

```bash
git log --oneline --graph --all --decorate -5
```

This command displays a visual representation of the commit history showing:
- `--oneline`: Condensed commit information (hash and message)
- `--graph`: ASCII graph showing branch relationships
- `--all`: Show all branches
- `--decorate`: Show branch and tag names
- `-5`: Limit to last 5 commits

You should see both `master` and `xfusioncorp_media` pointing to the same commit, confirming they share the same history up to this point.

---

## Additional Information

### Understanding Branch Pointers

When you create a branch, Git doesn't copy files or create duplicate history. Instead, it creates a 41-byte file containing:
- 40 characters: SHA-1 hash of the commit it points to
- 1 character: Newline

This makes branch creation instantaneous, regardless of repository size.

### The HEAD Pointer

`HEAD` is a special pointer that indicates which branch you're currently on. When you switch branches, HEAD moves to point to the new branch. When you create a commit, the current branch (referenced by HEAD) moves forward to the new commit.

### Branch Workflow Best Practices

**Keep Branches Short-lived:**
Merge feature branches quickly to avoid large, difficult merges. Aim for branches that live hours to days, not weeks or months.

**Regular Updates:**
Frequently sync your feature branch with the main branch to incorporate changes and reduce merge conflicts:
```bash
git switch xfusioncorp_media
git merge master
```

**Single Purpose:**
Each branch should address a single feature, bug, or task. This makes code review easier and reduces the scope of potential issues.

**Clean History:**
Before merging, consider cleaning up your branch's commit history with interactive rebase to create a logical, readable history.

### Deleting Branches

After merging a feature branch, delete it to keep your repository clean:

```bash
git branch -d xfusioncorp_media    # Safe delete (only if merged)
git branch -D xfusioncorp_media    # Force delete (even if unmerged)
```

### Remote Branch Tracking

When you're ready to share your branch with others, push it to the remote repository:

```bash
git push -u origin xfusioncorp_media
```

The `-u` flag sets up tracking, so future `git push` and `git pull` commands know which remote branch to use.

---

## Validation

Test your solution using KodeKloud's automated validation system. The validator will check:
- New branch `xfusioncorp_media` exists in the repository
- Branch was created from the master branch
- Branch contains the same commit history as master
- No code modifications were made to the repository
- Branch is properly configured and accessible

---

[← Day 23](day-23.md) | [Day 25 →](day-25.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
