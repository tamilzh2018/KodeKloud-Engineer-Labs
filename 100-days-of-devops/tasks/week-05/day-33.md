# Day 33: Git Merge Conflict Resolve

## Task Overview

Resolve merge conflicts when synchronizing local changes with remote repository updates. Conflicts occur when the same file sections are modified in both locations, requiring manual intervention to reconcile the differences.

**Technical Specifications:**
- Repository: story-blog (on storage server)
- User: max (developer with local changes)
- Conflict source: Remote has updates that conflict with local commits
- Resolution method: Rebase with manual conflict resolution
- File involved: story-index.txt (contains titles for 4 stories)
- Additional fix: Correct typo ("Mooose" → "Mouse" in "The Lion and the Mouse")

**Scenario:**
Max and Sarah have been collaborating on a story blog repository. Sarah has pushed updates to the remote repository while Max was working on his local changes. When Max attempts to push his commits, Git detects that the remote has diverged from his local state. Max needs to fetch the remote changes, rebase his commits on top of Sarah's updates, resolve any conflicts that arise, fix a typo in the content, and successfully push the integrated changes.

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** SSH into storage server as Max

```sh
ssh max@storage-server
# Password: Max_pass123
```

Establish an SSH connection to the storage server using Max's credentials. This server hosts the story-blog repository where both Max and Sarah have been working. SSH provides secure encrypted access to the remote server, allowing you to execute commands and manage the repository. Once connected, you'll be in Max's home directory where the repository is located.

**Step 2:** Navigate to the repository

```sh
cd ~/story-blog
```

Change to the story-blog repository directory in Max's home folder. This repository contains the collaborative work between Max and Sarah, including story files and the story-index.txt file that lists all story titles. All subsequent Git commands will operate within this repository's context.

**Step 3:** Check current repository status

```sh
git status
```

Display the current state of the working directory and staging area. This shows whether you have uncommitted changes, which branch you're on, and the relationship between your local branch and the remote tracking branch. Understanding the current state helps you plan the next steps for synchronization and conflict resolution.

**Step 4:** Fetch latest changes from remote

```sh
git fetch origin
```

Download all changes from the remote repository (origin) without modifying your local working directory or current branch. Fetching updates your local copy of remote branches (like origin/main) so you can see what changes exist remotely. This is a safe operation that doesn't affect your working files, allowing you to review remote changes before integrating them. After fetching, Git will display how many commits the remote is ahead of your local branch.

**Step 5:** View the divergence between local and remote

```sh
git log --oneline --graph --all --decorate
```

Visualize the commit history showing both your local commits and the fetched remote commits. The graph will reveal that your local branch and origin/main have diverged - they share a common ancestor but each has commits the other doesn't have. This visual representation helps you understand the scope of changes you'll need to integrate. You'll see Max's commits on one branch and Sarah's commits on another.

**Step 6:** Rebase local commits onto remote main

```sh
git rebase origin/main
```

Attempt to replay your local commits on top of the updated remote main branch. Git will start the rebase process, temporarily saving your commits, moving to the latest remote commit, then reapplying your changes one by one. If Git encounters conflicts (changes to the same lines in both versions), it will pause the rebase and report which files have conflicts. The rebase ensures your changes are based on the most recent remote state.

**Step 7:** Check for conflicts

```sh
git status
```

After the rebase pauses due to conflicts, check which files have conflicts. Git status will show files marked as "both modified" or with "unmerged paths," indicating they need manual resolution. The output will explicitly list the conflicted files and provide guidance on next steps. In this scenario, story-index.txt is likely to have conflicts since both Max and Sarah modified it.

**Step 8:** Open and examine conflicted file

```sh
cat story-index.txt
# or
vi story-index.txt
# or
nano story-index.txt
```

View the contents of the conflicted file to see the conflict markers. Git inserts special markers to show the conflicting sections:
- `<<<<<<< HEAD` marks the start of your local changes
- `=======` separates the two versions
- `>>>>>>> origin/main` marks the end of the remote changes

Between these markers, you'll see both versions of the conflicting content. You need to decide which changes to keep, or combine both versions appropriately.

**Step 9:** Resolve conflicts in the file

Edit the file to resolve conflicts by:
1. Removing the conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`)
2. Keeping or combining the desired content from both versions
3. Ensuring all 4 story titles are present in story-index.txt
4. Fixing the typo: change "The Lion and the Mooose" to "The Lion and the Mouse"

Example resolution:
```
# Before (with conflict markers):
<<<<<<< HEAD
The Fox and the Grapes
The Lion and the Mooose
=======
The Crow and the Pitcher
The Tortoise and the Hare
>>>>>>> origin/main

# After (resolved and corrected):
The Fox and the Grapes
The Lion and the Mouse
The Crow and the Pitcher
The Tortoise and the Hare
```

Manually edit the file to create the final desired content. Remove all conflict markers and ensure the result is valid, complete, and correct. The resolved file should contain meaningful content that integrates both sets of changes appropriately. Save the file after making your edits.

**Step 10:** Stage the resolved file

```sh
git add story-index.txt
# or to add all resolved files:
git add .
```

Mark the conflict as resolved by staging the edited file. The `git add` command tells Git that you've finished resolving conflicts in the specified file and it's ready to be included in the rebased commit. Staging is the signal to Git that the file no longer has conflicts and should be incorporated into the commit being replayed during the rebase.

**Step 11:** Continue the rebase process

```sh
git rebase --continue
```

Instruct Git to continue the rebase process now that conflicts are resolved. Git will complete the rebase by finalizing the current commit and continuing to replay any remaining commits from your local branch. If there are more commits to replay and any of them have conflicts, Git will pause again for resolution. The `--continue` flag moves the rebase forward after each conflict resolution.

**Step 12:** Handle additional conflicts if they occur (conditional)

If more conflicts arise from subsequent commits:
```sh
# Repeat the conflict resolution process:
git status           # Check which files have conflicts
# Edit conflicted files
git add <files>      # Stage resolved files
git rebase --continue # Continue to next commit
```

Some rebases require multiple rounds of conflict resolution if several commits modify the same areas. Patiently work through each conflict, ensuring each resolution is correct before continuing. If the rebase becomes too complex, you can abort with `git rebase --abort` to return to the pre-rebase state and try a different approach (like merge instead of rebase).

**Step 13:** Verify the final state

```sh
git status
git log --oneline -5
cat story-index.txt
```

Confirm that the rebase completed successfully, your working directory is clean, and the story-index.txt file contains all 4 story titles with the typo corrected. The git status should show a clean working tree with your branch ahead of origin/main by the number of commits you had locally. The log should show your commits now based on Sarah's latest commit.

**Step 14:** Push the integrated changes

```sh
git push
```

Upload your rebased commits to the remote repository. Since your commits are now based on the latest remote state and include the conflict resolutions, Git will accept the push without issues. The push updates the remote repository with both Sarah's and Max's changes integrated together. Other team members can now pull these combined changes.

**Step 15:** Verify via Gitea UI (optional)

1. Access the Gitea UI (click button on top bar)
2. Login as max (password: Max_pass123) or sarah (password: Sarah_pass123)
3. Navigate to the story-blog repository
4. View the story-index.txt file to confirm all 4 titles are present
5. Verify the typo is corrected ("Mouse" not "Mooose")

Use the web interface to visually confirm that your changes were successfully pushed and appear correctly in the remote repository. This provides a user-friendly way to verify the final result without command-line inspection. The web UI can help you review the commit history, file contents, and ensure the integration was successful.

---

## Key Concepts

**Merge Conflicts:**
- **Definition**: Occur when Git cannot automatically reconcile differences between two versions
- **Common Causes**: Same lines modified differently, file renamed in one branch and modified in another, file deleted in one branch and modified in another
- **Detection**: Git identifies conflicts during merge, rebase, or cherry-pick operations
- **Resolution Required**: Developer must manually decide which changes to keep

**Conflict Markers:**
Git inserts special markers to delineate conflicting sections:
```
<<<<<<< HEAD (or current branch name)
Your changes here
=======
Their changes here (remote or other branch)
>>>>>>> branch-name or commit-hash
```

- **HEAD Section**: Changes from your current branch (local changes)
- **Separator (=======)**: Divides the two conflicting versions
- **Remote Section**: Changes from the branch being merged/rebased
- **Resolution**: Remove markers and keep/combine desired content

**Conflict Resolution Process:**
1. **Identify**: Git pauses operation and marks conflicted files
2. **Examine**: Open files and review conflicting sections
3. **Decide**: Choose which changes to keep or how to combine them
4. **Edit**: Modify file to desired final state, removing conflict markers
5. **Stage**: Use `git add` to mark conflicts as resolved
6. **Continue**: Resume operation with `git rebase --continue` or commit merge
7. **Test**: Verify the resolution works correctly (run tests, review functionality)

**Types of Conflicts:**
- **Content Conflicts**: Same lines modified differently (most common)
- **Delete/Modify Conflicts**: File deleted in one branch, modified in another
- **Rename Conflicts**: File renamed differently in both branches
- **Tree Conflicts**: Changes to directory structure conflict
- **Binary Conflicts**: Binary files modified in both branches (can't auto-merge)

**Rebase vs Merge for Conflict Resolution:**
- **Rebase** (as in this task):
  - Replays commits one by one on new base
  - May require resolving same conflict multiple times (once per commit)
  - Creates linear history
  - Command: `git rebase origin/main`

- **Merge**:
  - Combines branches in single merge commit
  - Resolve all conflicts once
  - Preserves branching history
  - Command: `git merge origin/main`

**Conflict Prevention Strategies:**
- **Frequent Pulls**: Regularly sync with remote to minimize divergence
- **Small Commits**: Smaller changes reduce conflict probability
- **Communication**: Coordinate with team on who's working on which files
- **Feature Branches**: Isolate work to minimize overlapping changes
- **Code Review**: Pull requests catch potential conflicts early
- **Modular Code**: Well-organized code reduces likelihood of editing same areas

**Tools for Conflict Resolution:**
- **Command Line**: Direct editing of files with text editor
- **Git GUI Clients**: Visual tools like GitKraken, SourceTree show conflicts graphically
- **IDE Integration**: VS Code, IntelliJ have built-in merge conflict tools
- **Merge Tools**: Configure external tools like meld, kdiff3
  ```sh
  git config --global merge.tool meld
  git mergetool
  ```

**Common Resolution Scenarios:**
- **Keep Mine**: Discard remote changes, keep your version
- **Keep Theirs**: Discard your changes, accept remote version
- **Combine Both**: Integrate both sets of changes logically
- **Rewrite Entirely**: Create new content that supersedes both versions

**Conflict Resolution Best Practices:**
- **Understand Context**: Know what each change was trying to accomplish
- **Preserve Intent**: Ensure resolution fulfills goals of both change sets
- **Test Thoroughly**: Verify functionality after resolution
- **Communicate**: Discuss complex conflicts with team members
- **Document**: Comment on why specific resolution approach was chosen
- **Review**: Have another team member review conflict resolutions

**Aborting Operations:**
If conflicts become too complex to resolve:
```sh
# Abort rebase and return to pre-rebase state
git rebase --abort

# Abort merge and return to pre-merge state
git merge --abort
```

Use abort commands to safely return to the state before the conflict-causing operation, allowing you to try a different approach or seek help.

**Viewing Conflict Details:**
```sh
# Show which files have conflicts
git status

# Show detailed diff including conflict markers
git diff

# Show changes from both sides
git show :1:filename  # Common ancestor version
git show :2:filename  # Your version (HEAD)
git show :3:filename  # Their version (remote)

# List files with conflicts
git diff --name-only --diff-filter=U
```

**After Resolution Verification:**
- **Compile/Build**: Ensure code compiles without errors
- **Run Tests**: Execute test suite to catch logical errors
- **Manual Testing**: Test affected functionality manually
- **Peer Review**: Have teammate review resolution if complex
- **Documentation**: Update comments or docs if resolution changed behavior

**Advanced Conflict Scenarios:**
- **Recursive Conflicts**: When conflict resolution itself causes new conflicts
- **Multiple Commits**: Rebase may pause for conflicts on several commits
- **Cherry-pick Conflicts**: Applying single commit that conflicts with current state
- **Submodule Conflicts**: Conflicts in Git submodule references

---

## Validation

Test your solution using KodeKloud's automated validation.

**Verification Checklist:**
1. All 4 story titles present in story-index.txt
2. Typo corrected: "The Lion and the Mouse" (not "Mooose")
3. Local and remote repositories synchronized
4. No merge conflicts remaining
5. Working directory is clean
6. Changes successfully pushed to origin/main

---

[← Day 32](day-32.md) | [Day 34 →](day-34.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
