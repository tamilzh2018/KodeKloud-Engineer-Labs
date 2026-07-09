# Day 30: Git Reset Hard

## Task Overview

Rewrite Git commit history by resetting to a specific commit and removing all subsequent commits. This operation is used to clean test repositories, undo experimental changes, or restore a repository to a known good state.

**Technical Specifications:**
- Repository: /usr/src/kodekloudrepos/ecommerce (storage server)
- Operation: Reset commit history to specific commit
- Target commit: "add data.txt file" (90b2925)
- Final state: Only initial commit and "add data.txt file" remain
- Remote sync: Force push required to update remote repository

**Scenario:**
The development team created multiple test commits (Test Commit1 through Test Commit10) for experimentation. These commits are no longer needed and should be removed from both the local repository and remote origin. The repository needs to be restored to only contain the initial commit and the "add data.txt file" commit, effectively erasing the test commit history.

**Warning:**
This is a destructive operation that permanently deletes commits. Use with extreme caution, especially on shared repositories. Always ensure you have backups or that the deleted commits are truly disposable.

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** Connect to storage server with root privileges

```sh
sudo -i
```

Switch to the root user account to gain full administrative privileges on the storage server. The `sudo -i` command starts a root shell session, providing unrestricted access to system resources and the ability to modify any repository. This is necessary because the repository is located in a system directory (/usr/src) that typically requires elevated permissions. Always use root access carefully and only when necessary for the specific task at hand.

**Step 2:** Navigate to the Git repository

```sh
cd /usr/src/kodekloudrepos/ecommerce
```

Change the current working directory to the ecommerce repository location. This repository contains the test commits that need to be removed. The /usr/src/kodekloudrepos directory is a common location for shared repositories on the storage server. Once in this directory, all subsequent Git commands will operate on this specific repository without needing to specify the repository path.

**Step 3:** Examine current commit history

```sh
git log --oneline
```

Display a condensed view of the entire commit history showing each commit on a single line with its abbreviated hash and commit message. The `--oneline` format makes it easy to see the full history at a glance without overwhelming detail. This command helps you identify the target commit (90b2925 "add data.txt file") and understand how many commits will be removed by the reset operation. You should see 12 commits total: the initial commit, the target commit, and 10 test commits.

Output example:
```
81e08fc (HEAD -> master, origin/master) Test Commit10
686cb01 Test Commit9
f0ff119 Test Commit8
a8404ed Test Commit7
a9fccf0 Test Commit6
2554746 Test Commit5
461c467 Test Commit4
287d981 Test Commit3
a63283d Test Commit2
5479bcb Test Commit1
90b2925 add data.txt file
848a423 initial commit
```

**Step 4:** Reset HEAD to target commit with hard reset

```sh
git reset --hard 90b2925
```

Perform a hard reset to the commit with hash 90b2925 ("add data.txt file"), permanently removing all commits that came after it. The `--hard` option makes this a destructive reset that discards all changes in three areas: (1) moves the HEAD pointer to the specified commit, (2) resets the staging area/index to match that commit, and (3) modifies the working directory to reflect the state at that commit. This effectively erases Test Commit1 through Test Commit10 from the repository's history, though they remain in the reflog for potential recovery. Replace the commit hash with the appropriate hash from your repository if it differs.

**Step 5:** Verify the local repository state

```sh
git status
```

Check the status of the working directory and staging area after the reset operation. This command reveals that your local branch is now "behind" the remote origin/master by 10 commits because the remote still contains the test commits you just removed locally. Git helpfully suggests using `git pull` to update your local branch, but that would re-introduce the deleted commits. The "nothing to commit, working tree clean" message confirms that the working directory matches the current HEAD commit (90b2925) with no uncommitted changes.

Output:
```
On branch master
Your branch is behind 'origin/master' by 10 commits, and can be fast-forwarded.
(use "git pull" to update your local branch)

nothing to commit, working tree clean
```

**Step 6:** Force push to update remote repository

```sh
git push --force
```

Push the local repository state to the remote origin, using the `--force` flag to override the remote's history with your local history. This is necessary because you're rewriting history that already exists on the remote. Without `--force`, Git would reject the push because your local branch appears to be behind the remote. Force pushing updates the remote master branch to point to commit 90b2925, effectively deleting the 10 test commits from the remote repository as well. This operation affects all team members who have access to the remote repository, which is why force pushes should be used cautiously and communicated to the team.

**Step 7:** Verify the updated commit history

```sh
git log --oneline
```

Display the commit history again to confirm that only the desired commits remain. You should now see only two commits: "848a423 initial commit" and "90b2925 add data.txt file". The 10 test commits have been successfully removed from both the local repository and the remote origin. This verification step ensures that the reset and force push operations completed successfully and the repository is in the expected clean state.

**Step 8:** Optional - Confirm remote synchronization

```sh
git fetch origin
git log --oneline origin/master
```

Fetch the latest state from the remote repository and display the remote master branch's commit history to verify that the remote matches your local state. Both commands should show the same two commits, confirming that the force push successfully updated the remote repository. This double-check ensures that the remote repository reflects the cleaned history and that all team members who pull from origin/master will receive the updated (shortened) history.

---

## Key Concepts

**Git Reset Types:**
- **Soft Reset** (`--soft`): Moves HEAD to target commit, preserves staging area and working directory. Committed changes become staged changes. Use when you want to recommit with different message or combine commits.
- **Mixed Reset** (`--mixed`, default): Moves HEAD to target commit, resets staging area, keeps working directory. Committed changes become unstaged changes. Use when you want to unstage files and recommit selectively.
- **Hard Reset** (`--hard`): Resets HEAD, staging area, and working directory to target commit. All changes after target commit are discarded. Use when you want to completely abandon changes.
- **Keep Reset** (`--keep`): Similar to hard but preserves uncommitted changes if they don't conflict. Use when resetting but want to keep work in progress.

**Reset Scope:**
- **Commit-level**: Moves branch pointer to different commit (`git reset <commit>`)
- **File-level**: Unstages specific files (`git reset <file>`)
- **HEAD Movement**: Changes where the current branch points
- **Branch Pointer**: Only affects current branch, not other branches

**Dangers of Hard Reset:**
- **Permanent Data Loss**: Commits are removed from history (recoverable via reflog for ~90 days)
- **Shared Repository Risk**: Never reset commits that have been pushed to shared repositories unless coordinated
- **Team Disruption**: Force pushes can break other developers' local repositories
- **Merge Conflicts**: Team members may face conflicts when pulling after force push
- **Lost Work**: Uncommitted changes in working directory are permanently deleted

**Force Push Implications:**
- **Rewriting History**: Changes commit hashes on remote repository
- **Team Coordination**: All team members must be notified and may need to reset their local branches
- **Protection Bypass**: Overrides remote branch protection (if permissions allow)
- **Deployment Risk**: Can affect deployed applications if they reference specific commits
- **Alternative**: Use `--force-with-lease` to prevent overwriting others' work

**Safe Alternatives to Hard Reset:**
- **Git Revert**: Creates new commits that undo previous commits (preserves history)
  ```sh
  git revert <commit-hash>
  ```
- **Create Branch**: Make a backup branch before resetting
  ```sh
  git branch backup-branch
  git reset --hard <commit>
  ```
- **Git Reflog**: View and recover from reset operations
  ```sh
  git reflog
  git reset --hard HEAD@{2}
  ```
- **Stash Changes**: Save work in progress before resetting
  ```sh
  git stash push -m "backup before reset"
  git reset --hard <commit>
  ```

**Recovery Options:**
- **Reflog**: Git maintains a log of all HEAD movements for ~90 days
  ```sh
  git reflog  # Find previous HEAD position
  git reset --hard HEAD@{n}  # Restore to that position
  ```
- **ORIG_HEAD**: Git stores previous HEAD position in ORIG_HEAD
  ```sh
  git reset --hard ORIG_HEAD
  ```
- **Garbage Collection**: Unreachable commits are eventually deleted by `git gc`
- **Time Limit**: Lost commits can be recovered until garbage collection runs

**When to Use Hard Reset:**
- **Test Repositories**: Cleaning up experimental changes
- **Local Development**: Undoing local commits not yet pushed
- **Coordination**: With team agreement to reset shared history
- **Mistakes**: Correcting accidental commits (before pushing)
- **Fresh Start**: Returning to a known good state

---

## Validation

Test your solution using KodeKloud's automated validation.

**Verification Checklist:**
1. Only two commits remain in repository history
2. Commits are: "initial commit" and "add data.txt file"
3. All 10 test commits have been removed
4. Remote repository matches local repository state
5. No uncommitted changes in working directory

---

[← Day 29](day-29.md) | [Day 31 →](day-31.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
