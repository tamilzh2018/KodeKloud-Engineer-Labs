# Day 32: Git Rebase

## Task Overview

Rebase a feature branch onto the master branch to incorporate recent changes without creating a merge commit. Rebasing creates a linear history by replaying feature branch commits on top of the master branch's latest state.

**Technical Specifications:**
- Repository: /usr/src/kodekloudrepos/games (storage server)
- Source branch: feature (developer's working branch)
- Base branch: master (has new commits since feature branched off)
- Operation: Rebase feature branch onto master
- History goal: Linear commit history without merge commits
- Remote sync: Force push required after rebase

**Scenario:**
A developer has been working on the feature branch while other team members have pushed updates to the master branch. The feature branch needs to incorporate those master branch changes to stay current, but the team wants to maintain a clean, linear commit history without merge commits. Rebasing allows the feature branch to be updated with master's changes while preserving a straight-line history that's easier to read and understand.

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Connect to storage server with root privileges

```sh
sudo -i
```

Elevate to root user to access system directories and repositories. The `sudo -i` command creates a root login shell with full administrative privileges, which is required to access repositories stored in system-managed directories like /usr/src. Root access provides unrestricted permissions to read and modify repository contents. Always verify the repository location and operations before executing commands with root privileges to prevent unintended changes.

**Step 2:** Navigate to the games repository

```sh
cd /usr/src/kodekloudrepos/games
```

Change to the games repository directory where the feature branch exists. This repository contains both the master branch (with recent updates) and the feature branch (with in-progress development work). The /usr/src/kodekloudrepos path is a centralized location for shared repositories on the storage server. All subsequent Git commands will operate within this repository's context.

**Step 3:** Verify current branch

```sh
git branch
```

Display all local branches and identify which branch is currently active (marked with an asterisk). This command shows you whether you're on the feature branch or need to switch to it. The output lists all local branches, with the current branch highlighted. You should see both "master" and "feature" branches listed. If you're not on the feature branch, you'll need to switch to it before rebasing.

Example output:
```
* feature
  master
```

The asterisk (*) indicates you're currently on the feature branch, which is where you need to be to perform the rebase operation.

**Step 4:** Optional - View diverged history before rebase

```sh
git log --oneline --graph --all --decorate
```

Visualize the current state of both branches to understand how they've diverged. The `--graph` flag creates an ASCII diagram showing branch relationships, `--all` displays commits from all branches, and `--decorate` shows branch and tag names. This helps you see which commits exist on master that aren't in feature, and vice versa. Understanding the divergence helps you anticipate potential conflicts during the rebase operation.

**Step 5:** Rebase feature branch onto master

```sh
git rebase master
```

Replay all commits from the feature branch on top of the master branch's current HEAD. Git first identifies the common ancestor commit where feature branched off from master, then temporarily removes all feature branch commits, fast-forwards to master's HEAD, and finally reapplies each feature commit one by one. This creates a linear history as if the feature branch was created from the current master instead of an older version. If conflicts occur, Git pauses the rebase and allows you to resolve them before continuing.

**Step 6:** Handle conflicts if they occur (conditional step)

If the rebase encounters conflicts:

```sh
# Git will pause and show conflicting files
git status  # View conflicted files

# Edit each conflicted file to resolve conflicts
# Look for conflict markers: <<<<<<<, =======, >>>>>>>

# After resolving conflicts in each file:
git add <resolved-file>

# Continue the rebase
git rebase --continue

# Or abort if needed:
# git rebase --abort
```

Resolve any conflicts that arise when Git attempts to reapply feature branch commits on top of master. Conflicts occur when the same lines were modified in both branches. Edit each conflicted file, remove the conflict markers, choose or combine the desired changes, then stage the resolved files and continue the rebase. Each commit may have conflicts, so this process might repeat multiple times. The `--abort` option allows you to cancel the rebase and return to the pre-rebase state if issues arise.

**Step 7:** Verify the rebased history

```sh
git log --oneline --graph
```

Examine the commit history to confirm that the rebase created a linear history. You should see feature branch commits appearing sequentially after master branch commits, with no merge commits. The graph should show a straight line rather than branching and merging. This linear history makes it easier to understand the project's evolution and use tools like `git bisect` for debugging.

**Step 8:** Force push the rebased feature branch

```sh
git push --force --set-upstream origin feature
```

Push the rebased feature branch to the remote repository, using `--force` to overwrite the remote branch's history. The `--set-upstream` flag (or `-u`) establishes a tracking relationship between your local feature branch and origin/feature, allowing simpler push/pull commands in the future. Force pushing is necessary because rebasing rewrites commit history, changing commit hashes even though the code changes remain the same. The remote repository's old feature branch history is replaced with the new linear history.

**Step 9:** Verify remote branch status

```sh
git status
```

Check that your local branch is now in sync with the remote origin/feature. The status should indicate that your branch is up to date with 'origin/feature' with no commits ahead or behind. This confirms that the force push successfully updated the remote repository with your rebased commits. A clean status with no uncommitted changes indicates the rebase and push completed successfully.

**Step 10:** Optional - Inform team members about the force push

Since force pushing rewrites history, communicate with team members who might have checked out the feature branch. They'll need to reset their local feature branches:

```sh
# Team members should run:
git checkout feature
git fetch origin
git reset --hard origin/feature
```

Coordinate with collaborators who have local copies of the feature branch. Force pushing creates a new history that conflicts with their local copies, so they must reset their branches to match the new remote state. Without this coordination, team members might try to merge the old and new histories, creating duplicate commits and confusion. Clear communication about rebasing activities is essential for team workflows.

---

## Key Concepts

**Rebase vs Merge:**
- **Rebase**: Moves commits to new base, creates linear history, rewrites commit hashes
- **Merge**: Combines branches with merge commit, preserves branching history, keeps original hashes
- **Linear History**: Rebase produces clean, straight-line history easier to follow
- **Preserved Context**: Merge maintains information about when branches diverged and converged
- **Use Rebase For**: Feature branches, keeping history clean, local changes
- **Use Merge For**: Integrating feature branches, preserving collaboration context, public branches

**How Rebase Works:**
1. **Find Common Ancestor**: Identify where branches diverged
2. **Store Commits**: Temporarily save all commits made on current branch since divergence
3. **Reset to Base**: Move branch pointer to target base commit
4. **Replay Commits**: Reapply saved commits one by one on the new base
5. **New Hashes**: Each replayed commit gets a new hash (different parent)

**Rebase Benefits:**
- **Clean History**: Linear timeline without merge commit clutter
- **Easier Review**: Clear sequence of changes for code review
- **Simpler Bisect**: `git bisect` works better with linear history
- **Professional Appearance**: Demonstrates understanding of Git best practices
- **Clearer Changelog**: Straightforward commit progression

**Rebase Risks:**
- **History Rewriting**: Changes commit hashes, incompatible with existing clones
- **Golden Rule**: Never rebase commits that have been pushed to public/shared branches
- **Team Disruption**: Force push requires coordination with collaborators
- **Conflict Multiplication**: May need to resolve same conflict for multiple commits
- **Lost Merge Context**: Can't see when branches diverged or converged

**Force Push Considerations:**
- **When Required**: After any operation that rewrites history (rebase, amend, reset)
- **Team Impact**: Affects anyone who has fetched the old branch state
- **Branch Protection**: May be blocked by repository settings on main branches
- **Safer Alternative**: `git push --force-with-lease` fails if remote has unexpected changes
  ```sh
  git push --force-with-lease origin feature
  ```
- **Communication**: Always notify team before force pushing shared branches

**Interactive Rebase:**
Interactive rebase (`-i` flag) provides powerful history editing capabilities:

```sh
git rebase -i HEAD~5  # Rebase last 5 commits
git rebase -i master  # Rebase all commits since diverging from master
```

**Interactive Commands:**
- **pick**: Keep commit as-is (default)
- **reword**: Change commit message without changing code
- **edit**: Pause to amend commit (modify code or message)
- **squash**: Combine with previous commit, keep both messages
- **fixup**: Combine with previous commit, discard this message
- **drop**: Remove commit entirely
- **reorder**: Move commits by reordering lines

Example interactive rebase session:
```
pick a1b2c3d Add user authentication
squash d4e5f6g Fix authentication bug
reword g7h8i9j Add user profile page
drop j1k2l3m Debug logging (remove)
```

**Rebase Workflow Best Practices:**
- **Rebase Before Merge**: Update feature branch with master before creating pull request
- **Small Commits**: Easier to resolve conflicts during rebase
- **Frequent Rebasing**: Regularly rebase to avoid large divergence
- **Local Only**: Only rebase commits that haven't been pushed
- **Backup Branch**: Create safety branch before risky rebase
  ```sh
  git branch backup-feature
  git rebase master
  ```

**Handling Rebase Conflicts:**
- **One Commit at a Time**: Resolve conflicts for each replayed commit
- **Context Understanding**: Know what the commit was trying to accomplish
- **Test After Resolve**: Ensure code works after conflict resolution
- **Skip Empty Commits**: If conflict resolution makes commit unnecessary:
  ```sh
  git rebase --skip
  ```
- **Abort if Needed**: Return to pre-rebase state if too complex:
  ```sh
  git rebase --abort
  ```

**Common Rebase Scenarios:**
- **Feature Development**: Keep feature branch updated with master
  ```sh
  git checkout feature
  git rebase master
  ```
- **Clean Up Before PR**: Squash fixup commits before submitting pull request
  ```sh
  git rebase -i HEAD~10
  ```
- **Reorder Commits**: Organize commits logically before merging
- **Remove Sensitive Data**: Drop commits containing secrets (also need filter-branch)

**Alternatives to Rebase:**
- **Merge Commits**: Use when history context matters
  ```sh
  git checkout feature
  git merge master
  ```
- **Fast-Forward Merge**: Possible when no divergence exists
- **Squash Merge**: Combine all feature commits into one on master
  ```sh
  git merge --squash feature
  ```

**Rebase Safety Tips:**
- **Check Remote**: `git fetch` before rebasing to know remote state
- **Clean Working Directory**: Commit or stash changes before rebasing
- **Test Afterward**: Run tests to ensure rebase didn't break functionality
- **Incremental Rebase**: Rebase onto intermediate commits if full rebase too complex
- **Reflog Recovery**: Use `git reflog` to recover if rebase goes wrong
  ```sh
  git reflog
  git reset --hard HEAD@{n}  # Before rebase
  ```

---

## Validation

Test your solution using KodeKloud's automated validation.

**Verification Checklist:**
1. Feature branch contains all commits from master
2. Feature branch commits appear after master commits (linear history)
3. No merge commits exist in the history
4. Remote origin/feature reflects rebased state
5. Working directory is clean with no conflicts

---

[← Day 31](day-31.md) | [Day 33 →](day-33.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
