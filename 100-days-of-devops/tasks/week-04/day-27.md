# Day 27: Git Revert Some Changes

## Task Overview

The Nautilus application development team was working on the `/usr/src/kodekloudrepos/demo` repository when they encountered an issue with recent commits. They've asked the DevOps team to revert the repository HEAD to the previous commit. This exercise demonstrates how to safely undo changes in a shared repository using Git revert, which preserves history and avoids disrupting team collaboration.

**Scenario Requirements:**
- Repository location: `/usr/src/kodekloudrepos/demo`
- Revert the latest commit (HEAD) to the previous commit
- The previous commit should have the message "add data.txt file"
- Use "revert demo" (lowercase) as the commit message for the revert
- Push changes to the remote repository

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Key Concepts

### Git Revert vs Reset

Understanding the difference between revert and reset is crucial for safe repository management:

**Git Revert (Safe):**
Creates a new commit that undoes changes from a previous commit. The original commit remains in history, and the revert operation itself is recorded. This is the preferred method for undoing changes in shared repositories because it doesn't rewrite history.

**Git Reset (Dangerous):**
Moves the branch pointer to a different commit, potentially discarding commits. This rewrites history and can cause problems for other developers who have based work on the discarded commits. Use only for local, unpushed changes.

**Key Differences:**
- **History**: Revert preserves all history; reset can erase it
- **Collaboration**: Revert is safe for shared branches; reset breaks collaboration
- **Traceability**: Revert shows what was undone and why; reset hides the undo
- **Recovery**: Reverted changes can be re-applied; reset changes may be lost forever

### When to Use Revert

**Public/Shared Repositories:**
Always use revert when undoing changes that have been pushed to remote repositories that others access. This maintains a clean, traceable history without disrupting other developers' work.

**Production Branches:**
Revert is essential for production or main branches where history integrity is critical for auditing, compliance, and understanding system evolution.

**Team Collaboration:**
When multiple developers work on the same branch, revert ensures everyone can synchronize changes without conflicts caused by rewritten history.

**Audit Requirements:**
In environments with strict change tracking requirements, revert maintains complete records of what changed, when, and why.

### Revert Operations

**Revert Latest Commit:**
```bash
git revert HEAD
```
Creates a new commit that undoes the most recent commit. Git opens an editor for you to write a commit message describing the revert.

**Revert Specific Commit:**
```bash
git revert <commit-hash>
```
Undoes changes from any commit in history. This creates a new commit that applies the inverse of the specified commit's changes.

**Revert Multiple Commits:**
```bash
git revert HEAD~3..HEAD
```
Reverts a range of commits. Each reverted commit creates its own revert commit, maintaining detailed history.

**Revert Without Committing:**
```bash
git revert --no-commit <commit-hash>
```
Stages the revert changes without creating a commit immediately. Useful when reverting multiple commits and you want a single revert commit.

**Abort Revert:**
```bash
git revert --abort
```
Cancels an in-progress revert operation, returning the repository to its state before the revert began.

### Commit Messages for Reverts

Good revert commit messages should explain:

**What is Being Reverted:**
Reference the original commit hash and message: "Revert 'Add user authentication feature' (commit abc123)"

**Why It's Being Reverted:**
Explain the reason: "Reverting due to security vulnerability discovered in authentication logic"

**Impact:**
Describe what functionality is being rolled back and any user-facing changes.

**Next Steps:**
Indicate plans for re-introducing the feature or alternative approaches.

### Handling Revert Conflicts

When reverting causes conflicts (the code has changed since the commit being reverted):

**Conflict Resolution:**
1. Git marks conflicted files with conflict markers
2. Edit files to resolve conflicts manually
3. Stage resolved files with `git add`
4. Complete the revert with `git revert --continue`

**Abort if Needed:**
If conflicts are too complex, abort the revert and consider alternative approaches like creating a fix in a new commit.

---

## Solution Steps

### Step 1: Access the Storage Server

Log into the Storage server via SSH.

```bash
ssh user@storage-server
```

This establishes a secure connection to the Storage server in Stratos DC where the demo repository is hosted. The server contains the repository that needs the revert operation.

### Step 2: Elevate Privileges

Switch to root user for necessary permissions.

```bash
sudo su
```

The `sudo su` command grants root privileges, ensuring you have the necessary permissions to access the repository and perform Git operations. In production environments, use service accounts with appropriate permissions instead of root.

### Step 3: Navigate to Repository

Change to the demo repository directory.

```bash
cd /usr/src/kodekloudrepos/demo
```

This command makes the demo repository your current working directory. All subsequent Git commands will operate on this repository. The path `/usr/src/kodekloudrepos/` is the standard location for development repositories in this environment.

### Step 4: Check Repository Status

Verify the repository is in a clean state.

```bash
git status
```

The `git status` command shows if there are uncommitted changes, untracked files, or other issues. Before performing a revert, ensure the working directory is clean to avoid complications. If there are uncommitted changes, stash them with `git stash` or commit them first.

Expected output:
```
On branch master
nothing to commit, working tree clean
```

### Step 5: View Commit History

Examine the commit log to understand what will be reverted.

```bash
git log --oneline
```

The `git log --oneline` command displays the commit history in a condensed format, showing commit hashes and messages. This helps you verify which commit is HEAD (the most recent) and confirm that the previous commit has the message "add data.txt file" as specified in the requirements.

Example output:
```
a1b2c3d (HEAD -> master) Test commit to revert
e4f5g6h add data.txt file
i7j8k9l initial commit
```

The commit at the top is HEAD and will be reverted. The commit below it ("add data.txt file") is where HEAD will effectively point after the revert.

### Step 6: Verify Previous Commit

Confirm the commit message of the target state.

```bash
git log --oneline -2
```

This shows the last 2 commits, allowing you to verify that the previous commit (the one that will become the new effective state) has the message "add data.txt file". This confirmation ensures you're reverting to the correct state as required.

### Step 7: Perform the Revert

Revert the latest commit with a specified commit message.

```bash
git revert HEAD -m "revert demo"
```

This command performs the revert operation:
- `git revert HEAD`: Reverts the most recent commit
- `-m "revert demo"`: Specifies the commit message for the revert commit

The `-m` flag (or `--message`) allows you to specify the commit message inline, avoiding the interactive editor. Git creates a new commit that undoes all changes from HEAD, effectively returning the repository to the state of the previous commit while maintaining full history.

**What Happens:**
1. Git calculates the inverse of HEAD's changes
2. Applies those inverse changes to create a new commit
3. The new commit has "revert demo" as its message
4. HEAD now points to this new revert commit
5. The repository state matches the previous commit, but with three commits in history instead of two

### Step 8: Verify the Revert

Confirm the revert commit was created successfully.

```bash
git log --oneline -3
```

This displays the last 3 commits. You should now see:
1. Your new revert commit with message "revert demo" at the top
2. The original commit that was reverted
3. The "add data.txt file" commit

Expected output:
```
m9n8o7p (HEAD -> master) revert demo
a1b2c3d Test commit to revert
e4f5g6h add data.txt file
```

### Step 9: Check Repository State

Verify the working directory matches the expected state.

```bash
git status
ls -la
```

The `git status` command should show a clean working tree. The `ls -la` command lists all files, allowing you to verify that the repository contents match what existed after the "add data.txt file" commit. Any files added in the reverted commit should no longer be present in the working directory.

### Step 10: Compare with Previous Commit

Confirm the repository state matches the target commit.

```bash
git diff HEAD HEAD~2
```

This command compares the current state (HEAD) with the commit two steps back (HEAD~2, which is the "add data.txt file" commit). The output should be empty or minimal, confirming that reverting HEAD effectively restored the repository to the state of HEAD~2.

### Step 11: Push Changes to Remote

Upload the revert commit to the remote repository.

```bash
git push
```

The `git push` command uploads your local commits (including the revert commit) to the remote repository. This makes the revert available to all team members and updates the central repository. Since revert creates a new commit rather than rewriting history, the push succeeds without requiring `--force`, maintaining safe collaboration practices.

### Step 12: Verify Push Success

Confirm the push completed successfully.

```bash
git log --oneline --decorate -3
```

This displays the recent commit history with branch decorations. You should see that both your local master and origin/master (the remote) point to the same commit (your revert commit), confirming the push was successful.

Expected output:
```
m9n8o7p (HEAD -> master, origin/master) revert demo
a1b2c3d Test commit to revert
e4f5g6h add data.txt file
```

---

## Additional Information

### Revert vs Reset: Detailed Comparison

**Revert:**
- Safe for shared repositories
- Preserves complete history
- Creates new commits
- No force push required
- Team-friendly

**Reset:**
- Only for local changes
- Can erase history
- Moves branch pointer
- May require force push
- Can break team collaboration

### Complex Revert Scenarios

**Reverting Merge Commits:**
Merge commits have two parents, requiring special handling:
```bash
git revert -m 1 <merge-commit-hash>
```
The `-m 1` specifies which parent to consider the mainline.

**Reverting Multiple Commits:**
To revert several commits without individual revert commits:
```bash
git revert --no-commit HEAD~3..HEAD
git commit -m "Revert last 3 commits"
```

**Reverting Old Commits:**
Reverting commits from deep in history may cause conflicts if subsequent commits modified the same code. Resolve conflicts as they arise during the revert process.

### When Reset is Appropriate

Reset is safe in these limited scenarios:

**Uncommitted Changes:**
```bash
git reset --hard HEAD  # Discard all uncommitted changes
```

**Local Commits Not Pushed:**
```bash
git reset --hard HEAD~3  # Remove last 3 local commits
```

**Private Branches:**
On branches only you use, reset can simplify history before sharing.

### Reverting a Revert

If you need to re-apply changes that were reverted:

```bash
git revert <revert-commit-hash>
```

This creates a new commit that undoes the revert, effectively re-applying the original changes.

### Best Practices for Reverting

**Test First:**
If possible, test the revert in a local branch before applying to master.

**Communicate:**
Inform team members when reverting shared commits so they're aware of the changes.

**Document Thoroughly:**
Write detailed revert commit messages explaining what and why.

**Review Impact:**
Consider dependencies and features that might be affected by the revert.

**Plan Forward:**
If reverting a feature, have a plan for re-introducing it properly.

---

## Validation

Test your solution using KodeKloud's automated validation system. The validator will check:
- Revert commit was created with message "revert demo"
- Latest commit is a revert of the previous HEAD
- Repository state matches the "add data.txt file" commit
- Changes were pushed to the remote repository
- History is preserved (no commits were deleted)
- Repository is in a clean, working state

---

[← Day 26](day-26.md) | [Day 28 →](day-28.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
