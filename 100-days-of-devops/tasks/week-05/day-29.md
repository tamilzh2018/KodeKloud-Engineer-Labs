# Day 29: Git Pull Request

## Task Overview

Implement a collaborative code review workflow using Git pull requests. Pull requests provide a structured mechanism for proposing, reviewing, and merging code changes before they reach the main branch, ensuring code quality and team collaboration.

**Technical Specifications:**
- Repository: Pre-cloned on storage server
- Source branch: story/fox-and-grapes (developer's feature branch)
- Target branch: master (production-ready code)
- Review workflow: Require approval before merge
- Access control: Protect master branch from direct pushes

**Scenario:**
Max has completed a feature story about "The Fox and Grapes" on a dedicated feature branch. The changes need to be merged into master through a formal review process where Tom acts as the code reviewer. This workflow prevents unauthorized or unreviewed code from reaching production.

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Solution Steps

**Step 1:** SSH into the storage server and verify repository

```sh
ssh max@storage-server
# Password: Max_pass123
```

Establish an SSH connection to the storage server using Max's credentials. This server hosts the cloned Git repository where Max has already pushed his feature branch. SSH provides secure remote access to the server, encrypting both authentication credentials and subsequent commands. Once connected, you'll have access to Max's home directory where the repository is located.

**Step 2:** Navigate to repository and inspect commit history

```sh
cd ~/repository-name
git log --oneline --all --graph
```

Change to the cloned repository directory and display the complete commit history across all branches using a graphical representation. The `--all` flag shows commits from all branches (not just the current one), while `--graph` creates an ASCII visualization showing how branches diverge and merge. The `--oneline` format condenses each commit to a single line showing the short hash and commit message, making it easier to understand the repository's structure. You should see both Sarah's previous commits on master and Max's new commits on the story/fox-and-grapes branch.

**Step 3:** Verify current branch status and changes

```sh
git status
git branch -a
```

Check which branch you're currently on and view all available branches including remote-tracking branches. The `git status` command shows the working tree status, indicating if there are any uncommitted changes. The `git branch -a` command lists all local branches and remote-tracking branches (prefixed with remotes/origin/). You should see the story/fox-and-grapes branch listed, confirming that Max has successfully pushed his changes to the remote repository.

**Step 4:** Access Gitea web interface and authenticate as Max

Navigate to the Gitea UI (accessible via the platform's top bar button) and login with Max's credentials:
- Username: max
- Password: Max_pass123

Gitea is a lightweight self-hosted Git service that provides a web-based interface for Git repository management, similar to GitHub or GitLab. After logging in, you'll see Max's repositories and can access the collaboration features. The web interface allows you to perform Git operations through a graphical interface rather than command-line commands, making it more accessible for complex workflows like pull request management.

**Step 5:** Create a new pull request

In the Gitea interface:
1. Navigate to the repository
2. Click on "Pull Requests" tab
3. Click "New Pull Request" button
4. Configure PR settings:
   - **Source branch**: story/fox-and-grapes
   - **Target branch**: master
   - **Title**: Added fox-and-grapes story
   - **Description**: (Optional) Add context about the changes

Click "Create Pull Request" to submit

Create a pull request that proposes merging Max's feature branch into the master branch. The pull request serves as a formal proposal to integrate changes, providing a space for discussion, review, and approval before the merge occurs. The title should clearly describe what the PR accomplishes, while the description can provide additional context about implementation details, testing performed, or related issues. This creates a permanent record of why and how changes were introduced.

**Step 6:** Assign Tom as reviewer

In the newly created pull request:
1. Locate the "Reviewers" section on the right sidebar
2. Click on the reviewers field
3. Select "tom" from the list of available reviewers
4. The assignment is saved automatically

Assign Tom as the designated code reviewer for this pull request. Assigning reviewers ensures that specific team members are notified and responsible for reviewing the proposed changes. This creates accountability in the review process and ensures that changes are examined by qualified team members before integration. Tom will receive a notification that he has been assigned to review this pull request.

**Step 7:** Logout from Max's account

Click on the user profile icon (top right) and select "Sign Out" to logout from Max's account. This step is necessary to switch user contexts and simulate the reviewer's workflow. In real-world scenarios, different team members work from their own accounts, so this logout/login process demonstrates the collaborative nature of pull request workflows where one developer proposes changes and another reviews them.

**Step 8:** Login as Tom to review the pull request

Login to Gitea with Tom's credentials:
- Username: tom
- Password: Tom_pass123

Authenticate as Tom, who has been assigned to review Max's pull request. As a reviewer, Tom has the responsibility to examine the proposed changes, verify code quality, check for potential issues, and ensure the changes align with project standards. This role separation between author and reviewer is a fundamental practice in collaborative development, providing an additional quality gate before code reaches production.

**Step 9:** Review the pull request changes

As Tom, navigate to:
1. Click on "Pull Requests" tab
2. Open the PR titled "Added fox-and-grapes story"
3. Click on the "Files Changed" tab
4. Review the diff showing additions/deletions
5. Verify the story content and file changes

Examine the actual code changes proposed in the pull request. The "Files Changed" view displays a unified diff showing exactly what lines were added (green, prefixed with +), removed (red, prefixed with -), or modified. This allows the reviewer to understand the scope and nature of changes without needing to check out the branch locally. Review for code quality, correctness, adherence to coding standards, potential bugs, and whether the changes accomplish the stated goal.

**Step 10:** Approve and merge the pull request

In the pull request interface:
1. Scroll to the bottom of the PR page
2. Click "Approve" button to formally approve the changes
3. After approval, click "Merge Pull Request" button
4. Confirm the merge action
5. Optionally, delete the source branch after merge

Complete the review workflow by approving and merging the pull request. The approval indicates that Tom has reviewed the changes and found them acceptable for integration into master. The merge operation combines the story/fox-and-grapes branch into master, making Max's changes part of the main codebase. Deleting the source branch after merge is optional but keeps the repository clean by removing branches that have served their purpose. The merge creates a permanent record in the repository history showing when and by whom the changes were approved and integrated.

**Step 11:** Verify the merge in command line (optional)

```sh
# Login back as Max or access via terminal
git checkout master
git pull origin master
git log --oneline -5
```

Verify that the merge was successful by fetching the latest changes from the remote master branch. Switch to the master branch locally, pull the latest changes from the remote repository, and check the recent commit history. You should see Max's commits from the story/fox-and-grapes branch now present in the master branch history. This confirms that the pull request workflow successfully integrated the feature branch changes into the main production branch.

---

## Key Concepts

**Pull Request Workflow:**
- **Purpose**: Formal mechanism for proposing changes with mandatory review
- **Code Review**: Team collaboration to verify quality before integration
- **Discussion Platform**: Centralized space for feedback and iteration
- **Quality Gate**: Ensures only approved code reaches production branches
- **Audit Trail**: Permanent record of who changed what and why

**PR Components:**
- **Source Branch**: Contains proposed changes (story/fox-and-grapes)
- **Target Branch**: Destination for changes (master)
- **Title**: Concise summary of changes (50 characters or less)
- **Description**: Detailed explanation of what changed and why
- **Reviewers**: Team members assigned to examine changes
- **Status**: Open, approved, merged, or closed

**Review Process Benefits:**
- **Knowledge Sharing**: Multiple team members understand changes
- **Error Detection**: Catch bugs, logic errors, or security issues early
- **Code Quality**: Enforce standards, best practices, and consistency
- **Mentorship**: Senior developers guide junior team members
- **Documentation**: PR discussions document decision-making process

**Branch Protection:**
- **Direct Push Prevention**: Master branch cannot be modified directly
- **Required Reviews**: Enforce minimum number of approvals
- **Status Checks**: Require CI/CD tests to pass before merge
- **Linear History**: Maintain clean, understandable commit history

**Best Practices:**
- **Small, Focused PRs**: Keep changes reviewable (200-400 lines ideal)
- **Clear Descriptions**: Explain context, reasoning, and trade-offs
- **Tests Included**: Add or update tests for new functionality
- **Self-Review First**: Review your own changes before requesting review
- **Responsive Communication**: Address reviewer feedback promptly
- **Link Issues**: Reference related tickets or bug reports

**Common PR Patterns:**
- **Feature Branches**: Develop new features in isolation
- **Bug Fix Branches**: Address specific issues independently
- **Hotfix Branches**: Emergency production fixes
- **Release Branches**: Prepare versions for production deployment

---

## Validation

Test your solution using KodeKloud's automated validation.

**Verification Steps:**
1. Pull request created with correct title and branches
2. Tom successfully assigned as reviewer
3. Pull request approved by Tom
4. Changes successfully merged into master branch
5. Master branch now contains Max's story commits

---

[← Day 28](../week-04/day-28.md) | [Day 30 →](day-30.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
