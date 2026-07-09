# Day 31: Git Stash

## Task Overview

Restore previously stashed work-in-progress changes from Git's stash stack. Stashing allows developers to temporarily save uncommitted changes, switch contexts, and later retrieve those changes when needed.

**Technical Specifications:**
- Repository: /usr/src/kodekloudrepos/ecommerce (storage server)
- Operation: Restore specific stash entry by identifier
- Target stash: stash@{1} (second most recent stash)
- Final action: Commit and push restored changes
- Stash preservation: Apply operation keeps stash in the stack

**Scenario:**
A developer previously stashed some work-in-progress changes while working on the ecommerce repository. Multiple stash entries exist in the stash stack, and the team now needs to restore the changes stored in stash@{1}, commit them to the repository, and push them to the remote origin. This demonstrates how Git stash serves as a temporary storage mechanism for incomplete work.

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Connect to storage server with root privileges

```sh
sudo -i
```

Switch to the root user account to gain administrative access to the storage server. The `sudo -i` command initiates a root login shell, providing full system privileges required to access and modify repositories in system directories like /usr/src. This elevated access is necessary because the repository location typically requires root permissions. Always exercise caution when operating with root privileges to avoid unintended system modifications.

**Step 2:** Navigate to the Git repository

```sh
cd /usr/src/kodekloudrepos/ecommerce
```

Change the current working directory to the ecommerce repository. This repository is located in the /usr/src/kodekloudrepos directory, which serves as a centralized location for shared repositories on the storage server. Once in this directory, all subsequent Git commands will operate within the context of this repository, allowing you to access its stash stack and commit history without specifying the repository path repeatedly.

**Step 3:** List all stashed changes

```sh
git stash list
```

Display all saved stash entries in chronological order (most recent first). Each stash entry is identified by a reference like stash@{0}, stash@{1}, etc., where the number indicates how far back in the stash stack it was created. The command also shows the branch where the stash was created and the commit message of the HEAD at that time. This helps you identify which stash contains the changes you need to restore.

Output example:
```
stash@{0}: WIP on master: 7fe985d initial commit
stash@{1}: WIP on master: 7fe985d initial commit
```

The "WIP" prefix stands for "Work In Progress," indicating these are uncommitted changes that were saved mid-development.

**Step 4:** Apply the specific stash entry

```sh
git stash apply stash@{1}
```

Restore the changes from stash@{1} (the second most recent stash) to your working directory without removing the stash from the stack. The `apply` command retrieves the saved changes and reapplies them to your current working tree, but unlike `pop`, it preserves the stash entry for potential future use. This is safer than `pop` because you can reapply the same stash multiple times or to different branches if needed. The stash@{1} identifier specifically targets the second-most-recent stash entry.

**Step 5:** Verify the restored changes

```sh
git status
```

Check the current state of the working directory to see what files were restored from the stash. The `git status` command will display the files that were modified, added, or deleted when the stash was applied. These changes are now in your working directory as unstaged modifications, ready to be staged and committed. Review the output to confirm that the expected files and changes have been successfully restored from the stash.

**Step 6:** Stage all restored changes

```sh
git add .
```

Add all modified and new files from the working directory to the staging area (also called the index). The `.` argument tells Git to stage everything in the current directory and its subdirectories. This prepares all the restored changes to be included in the next commit. Staging is the intermediate step between modifying files and permanently recording those modifications in the repository's history through a commit.

**Step 7:** Commit the restored changes

```sh
git commit -m "Restored stash files"
```

Create a new commit containing all staged changes with the commit message "Restored stash files". This permanently records the previously stashed changes in the repository's history. The commit message should be descriptive enough to explain what changes were included, though in this case, a simple message indicating the restoration of stashed work is sufficient. The commit creates a new snapshot in the repository timeline with a unique hash identifier.

**Step 8:** Push changes to remote repository

```sh
git push
```

Upload the new commit to the remote repository (origin), making the restored changes available to all team members who have access to the repository. The push operation updates the remote master branch to include your new commit. This synchronizes your local repository with the remote, ensuring that the work that was previously stashed and is now committed becomes part of the shared codebase. Other developers can now pull these changes to their local repositories.

**Step 9:** Optional - Clean up the stash (if no longer needed)

```sh
git stash drop stash@{1}
```

Remove the stash@{1} entry from the stash stack if you no longer need it. Since you've successfully applied, committed, and pushed the changes, the stash entry is now redundant. The `drop` command permanently deletes the specified stash, freeing up the stash stack. This is good housekeeping practice to keep your stash list clean and manageable. Note that you can only drop stashes if you're certain you won't need to reapply them.

**Step 10:** Optional - Verify stash list after cleanup

```sh
git stash list
```

Display the updated stash list to confirm that stash@{1} has been removed (if you ran the drop command). The remaining stashes will be renumbered automatically, so what was previously stash@{0} remains stash@{0}. This verification step ensures that your stash management operations completed successfully and your stash stack is in the expected state.

---

## Key Concepts

**Git Stash Purpose:**
- **Temporary Storage**: Save uncommitted changes without creating a commit
- **Context Switching**: Clean working directory to switch branches or pull updates
- **Emergency Fixes**: Quickly switch to fix urgent issues without losing current work
- **Experimentation**: Try different approaches without committing intermediate states
- **Work Preservation**: Prevent loss of work when needing to reset or checkout

**Stash Stack Structure:**
- **LIFO Order**: Last In, First Out (most recent stash is stash@{0})
- **Multiple Entries**: Unlimited stashes can be saved
- **Automatic Indexing**: Stashes are numbered sequentially from {0}
- **Branch Association**: Each stash remembers which branch it was created on
- **Commit Reference**: Stashes record the HEAD commit at creation time

**Stash Operations:**
- **Save**: `git stash` or `git stash push -m "description"` - Create new stash
- **List**: `git stash list` - Display all saved stashes
- **Apply**: `git stash apply stash@{n}` - Restore stash without removing it
- **Pop**: `git stash pop` - Apply most recent stash and remove from stack
- **Drop**: `git stash drop stash@{n}` - Delete specific stash entry
- **Clear**: `git stash clear` - Remove all stashes
- **Show**: `git stash show -p stash@{n}` - View stash contents as diff

**Apply vs Pop:**
- **Apply**: Restores changes but keeps stash in the stack (safer, can reapply)
- **Pop**: Restores changes and removes stash from stack (cleaner, one-time use)
- **Use Apply When**: You might need to reapply the same stash to multiple branches
- **Use Pop When**: You're certain you only need the stash once

**Advanced Stashing:**
- **Include Untracked Files**: `git stash -u` or `git stash --include-untracked`
  ```sh
  git stash push -u -m "Including new files"
  ```
- **Include Ignored Files**: `git stash -a` or `git stash --all`
  ```sh
  git stash push -a -m "Including ignored files"
  ```
- **Partial Stashing**: `git stash -p` or `git stash --patch` (interactive)
  ```sh
  git stash push -p -m "Selected changes only"
  ```
- **Stash Specific Files**: Stash only particular files
  ```sh
  git stash push -m "Config changes" config.json settings.yaml
  ```

**Creating Branches from Stash:**
- **Purpose**: Apply stash to new branch to avoid conflicts
- **Command**: `git stash branch branch-name stash@{n}`
- **Behavior**: Creates branch from commit where stash was created, applies stash, drops stash
- **Use Case**: When stash conflicts with current branch state
  ```sh
  git stash branch feature-from-stash stash@{1}
  ```

**Stash Workflow Best Practices:**
- **Descriptive Messages**: Always use meaningful stash messages
  ```sh
  git stash push -m "Half-finished user authentication feature"
  ```
- **Regular Cleanup**: Drop applied stashes to keep list manageable
- **Verify Before Drop**: Use `git stash show -p` to review before dropping
- **Prefer Commits**: For long-term work, commit to feature branches instead of stashing
- **Communication**: Inform team about important stashed work on shared machines

**Stash Inspection:**
- **View Stash Contents**: See what's in a stash without applying
  ```sh
  git stash show -p stash@{1}
  ```
- **Summary View**: Quick overview of changed files
  ```sh
  git stash show stash@{1}
  ```
- **Full Diff**: Detailed line-by-line changes
  ```sh
  git diff stash@{1}
  ```

**Conflict Resolution:**
- **Conflicts During Apply**: If stash conflicts with current state, resolve manually
- **Conflict Markers**: Same as merge conflicts (<<<<<<, ======, >>>>>>)
- **Resolution Process**:
  1. Apply stash (conflicts marked in files)
  2. Edit files to resolve conflicts
  3. Stage resolved files with `git add`
  4. Continue with commit (don't need `git stash continue`)

**Common Stash Scenarios:**
- **Quick Branch Switch**: Stash current work, switch branches, return and pop
- **Pull Latest Changes**: Stash uncommitted work, pull updates, reapply stash
- **Test Hypothesis**: Stash current approach, try alternative, compare results
- **Code Review Context**: Stash work to test someone's PR, return to your work

---

## Validation

Test your solution using KodeKloud's automated validation.

**Verification Checklist:**
1. Stash@{1} changes successfully applied to working directory
2. All restored files committed with message "Restored stash files"
3. Commit successfully pushed to remote origin/master
4. Working directory is clean with no uncommitted changes
5. Remote repository contains the restored changes

---

[← Day 30](day-30.md) | [Day 32 →](day-32.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
