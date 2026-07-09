# Day 25: Git Branch Merge

## Task Overview

The Nautilus application development team has been working on the `/opt/demo.git` repository (cloned at `/usr/src/kodekloudrepos/demo`) and needs to integrate changes from a feature branch back into the master branch. This exercise demonstrates the complete workflow of branch creation, file modifications, committing changes, and merging branches while pushing to the remote repository.

**Scenario Requirements:**
- Repository location: `/usr/src/kodekloudrepos/demo`
- Create a new branch named `nautilus` from master
- Copy `/tmp/index.html` to the repository
- Commit the file in the nautilus branch
- Merge the nautilus branch back into master
- Push changes to origin for both branches

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Key Concepts

### Git Merge Fundamentals

**What is Git Merge?**
Merging is the process of integrating changes from one branch into another. It's how parallel lines of development are combined, allowing teams to bring feature work, bug fixes, or experimental changes into the main codebase. Git's merge capabilities enable true parallel development workflows.

**Why Merge?**
Merging allows developers to work independently on features without interfering with each other, then integrate their work when ready. It maintains a complete history of how code evolved and who contributed what changes.

### Merge Types and Strategies

**Fast-Forward Merge:**
When the target branch hasn't diverged from the source branch, Git simply moves the branch pointer forward. No merge commit is created because no actual merging is needed.

```
Before:     master: A---B
            nautilus:    C---D

After:      master: A---B---C---D
            nautilus:          ^
```

**Three-Way Merge:**
When both branches have diverged with new commits, Git creates a special merge commit with two parent commits, preserving the history of both branches.

```
Before:     master: A---B---E---F
            nautilus:    C---D

After:      master: A---B---E---F---M
                         \         /
            nautilus:     C---D---/
```

**Squash Merge:**
Combines all commits from the source branch into a single commit on the target branch. This creates a cleaner history but loses individual commit details.

```bash
git merge --squash nautilus
git commit -m "Feature: Add nautilus functionality"
```

**Rebase (Alternative to Merge):**
Replays commits from one branch onto another, creating a linear history without merge commits. We'll cover this in detail in a later exercise.

### Merge Workflow Process

The standard merge workflow follows these steps:

**1. Switch to Target Branch:**
Always merge into the branch that should receive the changes (usually master or main).

**2. Execute Merge:**
Use `git merge source-branch` to integrate changes from the source branch.

**3. Resolve Conflicts (if any):**
If the same lines were modified in both branches, manually resolve conflicts.

**4. Commit Merge:**
In case of three-way merge, Git creates a merge commit automatically (or prompts you to finalize it).

**5. Push Changes:**
Upload the merged changes to the remote repository to share with the team.

### Conflict Resolution

When Git cannot automatically merge changes, it creates conflict markers in affected files:

**Conflict Markers:**
```
<<<<<<< HEAD
Content from the current branch (master)
=======
Content from the merging branch (nautilus)
>>>>>>> nautilus
```

**Resolution Steps:**
1. Open files with conflicts
2. Review both versions of the changes
3. Edit the file to keep desired content
4. Remove conflict markers
5. Stage resolved files with `git add`
6. Complete merge with `git commit`

### Merge Best Practices

**Test Before Merging:**
Ensure your feature branch works correctly before merging. Run tests, check functionality, and verify no breaking changes.

**Keep Branches Updated:**
Regularly merge or rebase from master into your feature branch to minimize conflicts and stay current with team changes.

**Meaningful Merge Messages:**
Write descriptive merge commit messages explaining what functionality is being integrated and why.

**Delete Merged Branches:**
After successfully merging, delete feature branches to keep the repository clean and organized.

```bash
git branch -d nautilus  # Local branch
git push origin --delete nautilus  # Remote branch
```

---

## Solution Steps

### Step 1: Access the Storage Server

Connect to the Storage server via SSH.

```bash
ssh user@storage-server
```

This establishes a secure connection to the Storage server in the Stratos DC where the demo repository is hosted. The SSH protocol encrypts all communication between your machine and the server, ensuring secure access to the repository and development environment.

### Step 2: Elevate Privileges

Switch to root user for necessary permissions.

```bash
sudo su
```

The `sudo su` command elevates your privileges to root user. This ensures you have the necessary permissions to access the repository, modify files, and perform Git operations. Always use elevated privileges judiciously and only when required for specific tasks.

### Step 3: Navigate to Repository

Change to the repository directory.

```bash
cd /usr/src/kodekloudrepos/demo
```

This command changes your working directory to the demo repository. All subsequent Git commands will operate on this repository. The path `/usr/src/kodekloudrepos/` is the standard location for code repositories in this environment.

### Step 4: Verify Current Branch

Check which branch is currently active.

```bash
git branch
```

The `git branch` command displays all local branches, with the current branch marked by an asterisk (*). Before creating a new branch, verify you're on the master branch, as the new branch should be created from master according to the requirements.

Expected output:
```
* master
```

If you're not on master, switch to it with `git switch master` or `git checkout master`.

### Step 5: Create and Switch to New Branch

Create the nautilus branch and switch to it.

```bash
git checkout -b nautilus
```

This command performs two operations in one:
- **Creates** a new branch named `nautilus` pointing to the same commit as master
- **Switches** your working directory to the new branch

The `-b` flag indicates "create branch". After this command, you're on the nautilus branch, and any commits you make will be added to this branch while master remains unchanged. This isolation allows you to experiment and develop features without affecting the stable master branch.

Alternative modern syntax:
```bash
git switch -c nautilus
```

### Step 6: Copy File to Repository

Copy the index.html file from /tmp to the repository.

```bash
cp /tmp/index.html .
```

The `cp` command copies the file from `/tmp/index.html` to the current directory (represented by `.`). This file represents a change or new feature that needs to be added to the repository. In real-world scenarios, this might be a new configuration file, updated documentation, or any project asset.

After copying, verify the file exists:
```bash
ls -l index.html
```

### Step 7: Check Repository Status

View the current state of the working directory.

```bash
git status
```

The `git status` command shows which files have changed, which are staged for commit, and which are untracked. After copying index.html, you should see it listed as an untracked file. This status check helps you understand what changes will be included in the next commit.

Expected output:
```
On branch nautilus
Untracked files:
  (use "git add <file>..." to include in what will be committed)
        index.html
```

### Step 8: Stage Changes

Add the new file to the staging area.

```bash
git add .
```

The `git add .` command stages all changes in the current directory for the next commit. The staging area (also called the index) is an intermediate area where you prepare commits. The `.` represents the current directory, so this stages all modified, new, and deleted files.

For more targeted staging:
```bash
git add index.html  # Stage specific file
git add *.html      # Stage all HTML files
```

### Step 9: Commit Changes

Create a commit with the staged changes.

```bash
git commit -m "added tmp file"
```

The `git commit` command creates a new commit (snapshot) containing all staged changes. The `-m` flag allows you to specify the commit message inline. Each commit represents a logical unit of work and should have a descriptive message explaining what changed and why.

The commit is now part of the nautilus branch's history. The master branch remains unchanged at this point.

### Step 10: Verify Commit

Check that the commit was created successfully.

```bash
git log --oneline -3
```

This displays the last 3 commits in condensed format, showing commit hash and message. You should see your "added tmp file" commit at the top of the nautilus branch.

### Step 11: Switch to Master Branch

Return to the master branch to prepare for merging.

```bash
git switch master
```

The `git switch master` command changes your current branch back to master. This is necessary because you merge into the current branch. To integrate nautilus changes into master, you must be on master when executing the merge command.

After switching, your working directory updates to reflect master's state. The index.html file won't be visible because it only exists in the nautilus branch (until we merge).

Alternative command:
```bash
git checkout master
```

### Step 12: Merge Nautilus Branch

Integrate changes from nautilus into master.

```bash
git merge nautilus
```

The `git merge nautilus` command brings all commits from the nautilus branch into master. Git analyzes the commit history of both branches and determines the appropriate merge strategy:

- **Fast-forward**: If master hasn't changed since nautilus was created, Git simply moves master's pointer forward
- **Three-way merge**: If both branches have new commits, Git creates a merge commit

In this scenario, master likely hasn't changed, so Git will perform a fast-forward merge. After merging, master contains all commits from nautilus, including the index.html file.

### Step 13: Verify Merge

Confirm the merge was successful.

```bash
git log --oneline --graph -5
```

This visualizes the commit history, showing how branches merged. The `--graph` option displays an ASCII graph illustrating branch relationships. You should see the nautilus commits now part of master's history.

Additionally, verify the file exists:
```bash
ls -l index.html
```

### Step 14: Push Changes to Remote

Upload local changes to the remote repository.

```bash
git push
```

The `git push` command uploads your local master branch commits to the remote repository (origin). This makes your changes available to other team members and updates the central repository. Since master is typically configured to track origin/master, `git push` without arguments works correctly.

For explicit syntax:
```bash
git push origin master
```

### Step 15: Push Nautilus Branch (Optional)

If you need to share the nautilus branch, push it as well.

```bash
git push -u origin nautilus
```

This command pushes the nautilus branch to the remote repository and sets up tracking with `-u` (upstream). This is useful if other team members need to review or continue work on the nautilus branch before it's merged.

---

## Additional Information

### Understanding Merge Commits

When Git creates a merge commit (in three-way merges), it has special characteristics:
- **Two Parent Commits**: Links to both branches being merged
- **Merge Message**: Automatically generated or custom message
- **Historical Record**: Preserves the fact that development happened in parallel

### Fast-Forward vs No-Fast-Forward

By default, Git uses fast-forward merges when possible. You can force a merge commit:

```bash
git merge --no-ff nautilus
```

This creates a merge commit even when fast-forward is possible, making it explicit in history that a feature was developed on a separate branch.

### Aborting a Merge

If you start a merge but encounter issues, you can abort:

```bash
git merge --abort
```

This returns the repository to the state before the merge began, useful when conflicts are too complex to resolve immediately.

### Checking Merge Status

During a merge with conflicts, check what's merged and what's pending:

```bash
git status  # Shows files with conflicts
git diff    # Shows conflicting changes
git log --merge  # Shows commits causing conflicts
```

### Branch Cleanup After Merge

After successfully merging and pushing, clean up branches:

```bash
# Delete local branch
git branch -d nautilus

# Delete remote branch
git push origin --delete nautilus

# Prune deleted remote branches
git fetch --prune
```

### Merge Tools

For complex conflicts, use visual merge tools:

```bash
git mergetool
```

This launches a configured merge tool (like Meld, KDiff3, or VS Code) providing a graphical interface for conflict resolution.

---

## Validation

Test your solution using KodeKloud's automated validation system. The validator will check:
- nautilus branch was created from master
- index.html file exists in the repository
- Changes were committed to the nautilus branch
- nautilus branch was successfully merged into master
- Changes were pushed to the remote repository
- Merge was performed correctly without data loss

---

[← Day 24](day-24.md) | [Day 26 →](day-26.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
