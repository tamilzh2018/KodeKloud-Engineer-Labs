# Day 28: Git Cherry Pick

## Task Overview

The Nautilus application development team is actively working on the `/opt/official.git` repository (cloned at `/usr/src/kodekloudrepos/official`). A developer working on the feature branch has created a commit that needs to be merged into the master branch immediately, even though the feature branch work is still in progress. This exercise demonstrates Git cherry-pick, a powerful technique for selectively applying specific commits from one branch to another without merging entire branches.

**Scenario Requirements:**
- Repository location: `/usr/src/kodekloudrepos/official`
- Two branches exist: master and feature
- Find the commit with message "Update info.txt" in the feature branch
- Cherry-pick only this specific commit into the master branch
- Push the changes to the remote repository

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Key Concepts

### Cherry-Pick Fundamentals

**What is Cherry-Pick?**
Cherry-pick is a Git operation that applies changes from a specific commit to your current branch. Unlike merge, which integrates an entire branch's history, cherry-pick allows you to select individual commits and apply them elsewhere. This creates a new commit with the same changes but a different commit hash.

**Why Use Cherry-Pick?**
Cherry-pick is invaluable when you need specific changes without merging entire branches. It enables selective integration, allowing you to choose exactly which commits to include in your branch while leaving others behind.

**How It Works:**
When you cherry-pick a commit, Git:
1. Identifies the changes introduced by that commit (the diff)
2. Applies those changes to your current branch
3. Creates a new commit with the same changes and message
4. The new commit has a different hash and parent

### Cherry-Pick Use Cases

**Bug Fixes:**
A critical bug fix committed to a development branch needs immediate deployment to production. Cherry-pick the fix commit to the production branch without merging unfinished features.

```bash
# Fix is in development branch, need it in production
git switch production
git cherry-pick abc123
```

**Feature Backporting:**
A new feature developed for version 2.0 is needed in version 1.5. Cherry-pick the feature commits to the maintenance branch without bringing in breaking changes.

**Selective Merging:**
When a feature branch contains multiple independent commits and you only need some of them, cherry-pick specific commits instead of merging everything.

**Release Management:**
Building a release branch by cherry-picking specific ready commits from various feature branches while excluding incomplete work.

**Hotfix Distribution:**
Applying the same hotfix to multiple release branches. Cherry-pick the fix once, then apply it to each branch that needs it.

### Cherry-Pick Operations

**Single Commit:**
```bash
git cherry-pick <commit-hash>
```
Applies changes from one commit to your current branch. This is the most common cherry-pick operation.

**Multiple Commits:**
```bash
git cherry-pick commit1 commit2 commit3
```
Applies several specific commits in sequence. Each becomes a separate commit on your current branch.

**Commit Range:**
```bash
git cherry-pick start-hash..end-hash
```
Applies all commits between start (exclusive) and end (inclusive). Use carefully as this can apply many commits.

**Cherry-Pick Without Committing:**
```bash
git cherry-pick --no-commit <commit-hash>
```
Applies changes to your working directory without creating a commit. Useful when combining multiple cherry-picks into one commit.

**Continue After Conflicts:**
```bash
git cherry-pick --continue
```
After resolving conflicts during a cherry-pick, this completes the operation.

**Abort Cherry-Pick:**
```bash
git cherry-pick --abort
```
Cancels an in-progress cherry-pick, returning to the state before the operation began.

### Cherry-Pick vs Merge

Understanding when to use each operation:

**Cherry-Pick:**
- Selective: Choose specific commits
- Creates new commits with different hashes
- No branch relationship created
- Useful for one-off commits
- Can duplicate commits across branches

**Merge:**
- Comprehensive: Integrates entire branch history
- Preserves original commits and hashes
- Creates branch relationship in history
- Standard workflow for feature integration
- Maintains clean branch topology

**When to Choose Cherry-Pick:**
- Need only specific commits, not entire branch
- Applying fixes across multiple branches
- Branch contains mixed stable and unstable commits
- Backporting features to older versions

**When to Choose Merge:**
- Integrating complete feature development
- Standard team workflow
- Want to preserve branch relationships
- Need complete history context

### Conflict Resolution

Cherry-picking can cause conflicts when the same code has changed differently:

**Handling Conflicts:**
1. Git pauses the cherry-pick and marks conflicts
2. Edit conflicted files to resolve issues
3. Stage resolved files with `git add`
4. Continue with `git cherry-pick --continue`

**Conflict Markers:**
```
<<<<<<< HEAD
Current branch content
=======
Cherry-picked content
>>>>>>> abc123 (commit message)
```

**Abort if Needed:**
If conflicts are too complex or you cherry-picked the wrong commit, abort the operation and reconsider your approach.

### Preserving Author Information

Cherry-pick automatically preserves the original author and commit message. The new commit shows:
- **Author**: Original commit author
- **Committer**: Person who performed the cherry-pick
- **Message**: Original commit message (can be edited with `-e` flag)

---

## Solution Steps

### Step 1: Access the Storage Server

Log into the Storage server via SSH.

```bash
ssh user@storage-server
```

This establishes a secure connection to the Storage server in Stratos DC where the official repository is located. The server hosts repositories for the Nautilus application development team.

### Step 2: Elevate Privileges

Switch to root user for necessary permissions.

```bash
sudo su
```

The `sudo su` command grants root access, ensuring you have permissions to access the repository and perform Git operations. In production, use service accounts with appropriate permissions.

### Step 3: Navigate to Repository

Change to the official repository directory.

```bash
cd /usr/src/kodekloudrepos/official
```

This makes the official repository your current working directory. All subsequent Git commands will operate within this repository context.

### Step 4: Check Available Branches

List all branches in the repository.

```bash
git branch
```

The `git branch` command shows all local branches. You should see both 'master' and 'feature' branches as mentioned in the requirements. The current branch is marked with an asterisk (*).

Expected output:
```
  feature
* master
```
or
```
* feature
  master
```

### Step 5: Switch to Feature Branch

Navigate to the feature branch to find the commit.

```bash
git switch feature
```

The `git switch feature` command changes your current branch to the feature branch. This allows you to view the commit history and identify the specific commit that needs to be cherry-picked.

Alternative command:
```bash
git checkout feature
```

### Step 6: View Feature Branch History

Examine commits in the feature branch.

```bash
git log --oneline
```

The `git log --oneline` command displays the commit history in condensed format, showing commit hashes and messages. Scan through the output to find the commit with message "Update info.txt". Note its commit hash (the short alphanumeric string at the beginning of the line).

Example output:
```
e8f9g1h Update info.txt
d7e8f9g Add new feature component
c6d7e8f Work in progress
b5c6d7e Initial feature setup
```

In this example, the commit hash is `e8f9g1h`.

### Step 7: Copy the Commit Hash

Note or copy the commit hash for the "Update info.txt" commit.

```bash
git log --grep="Update info.txt" --oneline
```

This command specifically searches for commits with "Update info.txt" in the message, making it easier to identify the exact commit. The grep filter ensures you find the right commit even in a long history.

Copy the commit hash from the output. You'll need it for the cherry-pick operation.

### Step 8: View Commit Details

Inspect the commit to understand what changes will be applied.

```bash
git show e8f9g1h
```

Replace `e8f9g1h` with your actual commit hash. This command displays:
- Commit metadata (author, date, message)
- Complete diff showing all changes
- Files modified in the commit

Reviewing the commit ensures you're cherry-picking the correct changes.

### Step 9: Switch to Master Branch

Return to the master branch where the commit will be applied.

```bash
git switch master
```

The `git switch master` command changes your current branch to master. Cherry-pick applies commits to the current branch, so you must be on master to add the commit there.

After switching, you're ready to perform the cherry-pick operation.

### Step 10: Verify Master Status

Confirm master is clean before cherry-picking.

```bash
git status
```

The `git status` command verifies there are no uncommitted changes or conflicts. A clean working directory prevents complications during the cherry-pick operation.

Expected output:
```
On branch master
nothing to commit, working tree clean
```

### Step 11: Cherry-Pick the Commit

Apply the specific commit from feature to master.

```bash
git cherry-pick e8f9g1h
```

Replace `e8f9g1h` with your actual commit hash. This command:
- Applies the changes from the specified commit
- Creates a new commit on master with the same changes
- Preserves the original commit message and author
- Assigns a new commit hash

If successful, you'll see output indicating files changed and the new commit created. If there are conflicts, Git will pause and allow you to resolve them before continuing.

### Step 12: Verify Cherry-Pick Success

Confirm the commit was applied to master.

```bash
git log --oneline -3
```

This displays the last 3 commits on master. You should see the "Update info.txt" commit at the top (or near the top), now part of master's history. The commit hash will be different from the original in the feature branch.

Expected output:
```
a1b2c3d (HEAD -> master) Update info.txt
z9y8x7w Previous master commit
...
```

### Step 13: Compare with Feature Branch

Verify the changes match the original commit.

```bash
git diff feature HEAD -- info.txt
```

This command compares the info.txt file between the feature branch and current HEAD (master). If the cherry-pick worked correctly, the differences should be minimal or only show other unrelated changes that exist between the branches.

### Step 14: Check Repository State

Ensure everything is in order before pushing.

```bash
git status
ls -la
```

The `git status` command should show a clean working tree. The `ls -la` command lists all files, allowing you to verify that info.txt exists and any other expected files are present.

### Step 15: Push Changes to Remote

Upload the cherry-picked commit to the remote repository.

```bash
git push
```

The `git push` command uploads your local master branch (now including the cherry-picked commit) to the remote repository. This makes the changes available to all team members and updates the central repository.

If master is configured to track origin/master, simply `git push` works. Otherwise, use `git push origin master` explicitly.

### Step 16: Verify Push Success

Confirm the push completed successfully.

```bash
git log --oneline --decorate -3
```

This displays recent commits with branch decorations. You should see that both your local master and origin/master point to the same commit, confirming the push was successful.

Expected output:
```
a1b2c3d (HEAD -> master, origin/master) Update info.txt
z9y8x7w Previous master commit
```

---

## Additional Information

### Advanced Cherry-Pick Options

**Edit Commit Message:**
```bash
git cherry-pick -e <commit-hash>
```
Opens an editor to modify the commit message during cherry-pick.

**Add Sign-Off:**
```bash
git cherry-pick -s <commit-hash>
```
Adds a "Signed-off-by" line with your name, useful for tracking who applied the commit.

**Cherry-Pick Without Committing:**
```bash
git cherry-pick -n <commit-hash>
```
Applies changes without creating a commit, allowing you to modify before committing.

### Cherry-Pick Best Practices

**Document Why:**
When cherry-picking, consider adding a note in the commit message explaining why this commit was cherry-picked rather than merged normally.

**Avoid Duplicates:**
Cherry-picking creates duplicate commits. Be cautious about later merging branches that contain both the original and cherry-picked commits.

**Test Thoroughly:**
Always test cherry-picked code. Even if the commit worked in one branch, context differences might cause issues in another.

**Coordinate with Team:**
Inform team members when cherry-picking to avoid confusion about commit history and duplicated changes.

### Handling Cherry-Pick Conflicts

When cherry-pick encounters conflicts:

**Resolve Conflicts:**
1. Edit conflicted files manually
2. Remove conflict markers
3. Test the resolved code
4. Stage files with `git add`
5. Continue with `git cherry-pick --continue`

**Abort if Necessary:**
```bash
git cherry-pick --abort
```
Returns to the state before cherry-pick began.

### Cherry-Picking Multiple Commits

**Sequential Commits:**
```bash
git cherry-pick abc123 def456 ghi789
```
Applies multiple commits in order.

**Commit Range:**
```bash
git cherry-pick abc123^..def456
```
Applies all commits from abc123 (inclusive) to def456 (inclusive).

### Referencing Commits

Besides commit hashes, you can reference commits using:

**Relative References:**
```bash
git cherry-pick feature~2  # Two commits before feature tip
git cherry-pick feature^   # First parent of feature tip
```

**Branch Names:**
```bash
git cherry-pick feature  # Cherry-pick the tip of feature branch
```

---

## Validation

Test your solution using KodeKloud's automated validation system. The validator will check:
- "Update info.txt" commit exists on master branch
- Changes from the feature branch commit were applied correctly
- Master branch was pushed to the remote repository
- Repository is in a clean, working state
- Commit author information is preserved
- No merge conflicts remain

---

[← Day 27](day-27.md) | [Day 29 →](../week-05/day-29.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
