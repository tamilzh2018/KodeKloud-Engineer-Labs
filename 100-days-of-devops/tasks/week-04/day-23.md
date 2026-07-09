# Day 23: Fork a Repository

## Task Overview

A new developer named Jon has joined the Nautilus project team and needs to begin working on an existing project. Before making any changes, he must first create his own copy of the repository by forking it. This exercise demonstrates the fundamental workflow for contributing to projects using a fork-based collaboration model.

**Scenario Requirements:**
- Access the Gitea UI (Git hosting platform)
- Login with credentials: username `jon`, password `Jon_pass123`
- Fork the repository `sarah/story-blog` under the `jon` user account

**Lab:** [KodeKloud Engineer Platform](https://engineer.kodekloud.com/practice)

---

## Key Concepts

### Git Forking Fundamentals

**What is a Fork?**
A fork is a server-side copy of someone else's repository that you create under your own account. This copy is completely independent and allows you to experiment with changes without affecting the original project. Forking is the cornerstone of open-source collaboration and distributed development workflows.

**Core Characteristics:**
- **Personal Copy**: You own and have full control over your fork, including all branches and settings
- **Independence**: Changes in your fork don't affect the original repository until you explicitly propose them
- **Connection Maintained**: The fork retains a link to the original repository, enabling synchronization and contribution
- **Contribution Pathway**: Forks facilitate the pull request workflow, allowing you to propose changes back to the original project

### Fork vs Clone: Understanding the Difference

These two operations are often confused, but they serve different purposes:

**Fork (Server-side):**
- Creates a copy on the Git hosting platform (GitHub, GitLab, Gitea)
- Visible to others on the platform
- Enables pull request submissions to the original repository
- Maintains a relationship with the upstream (original) repository

**Clone (Local):**
- Creates a copy on your local machine
- Only visible to you
- Used for local development and testing
- Required step after forking to work on the code

**Typical Workflow:**
```
Fork (on server) → Clone (to local) → Modify → Push (to your fork) → Pull Request (to original)
```

### Collaboration Workflow with Forks

The fork-based workflow is the standard approach for contributing to projects you don't have direct write access to:

**Step 1 - Fork:**
Create your personal copy of the repository on the Git hosting platform. This gives you a space to experiment and develop features.

**Step 2 - Clone:**
Download your fork to your local development machine using `git clone`. This creates a working directory where you can edit files.

**Step 3 - Branch:**
Create a feature branch for your specific changes. This keeps your work organized and makes it easier to propose discrete changes.

**Step 4 - Commit:**
Make your changes and commit them with descriptive messages. Each commit should represent a logical unit of work.

**Step 5 - Push:**
Upload your commits to your fork on the Git hosting platform. This makes your changes visible to others.

**Step 6 - Pull Request:**
Propose your changes to the original repository through a pull request. The maintainers can review, discuss, and potentially merge your contributions.

### Gitea Platform Overview

**What is Gitea?**
Gitea is a lightweight, self-hosted Git service similar to GitHub or GitLab. It provides a web interface for repository management, collaboration features, and access control.

**Key Features:**
- **Web Interface**: User-friendly browser-based repository management
- **Self-hosted**: Run on your own infrastructure with full control over data
- **Lightweight**: Minimal resource requirements, suitable for small teams and personal servers
- **Collaboration Tools**: Issues, pull requests, wikis, and organization management
- **Git Operations**: All standard Git operations through both web UI and command line

**Why Use Gitea?**
Organizations choose Gitea for privacy, control, and cost-effectiveness. It's particularly popular for internal projects, educational environments, and teams that prefer self-hosted solutions over cloud-based platforms.

---

## Solution Steps

### Step 1: Access the Gitea Web Interface

Click on the Gitea UI button located on the top bar of your lab environment.

This button opens the Gitea web interface in your browser. Gitea serves as the Git hosting platform for this environment, similar to how GitHub or GitLab would be used in production environments. The web interface provides visual access to repositories, user management, and collaboration features.

### Step 2: Login to Gitea

Enter the login credentials for the new developer Jon.

```
Username: jon
Password: Jon_pass123
```

Authentication verifies your identity and grants access to repositories and features based on your user permissions. Once logged in, you'll see Jon's dashboard showing repositories, activity, and available actions. In a real-world scenario, these credentials would be securely managed and possibly integrated with enterprise authentication systems like LDAP or OAuth.

### Step 3: Locate the Target Repository

Navigate to the repository that needs to be forked: `sarah/story-blog`.

You can find this repository by:
- Looking in the right sidebar for repository listings
- Using the search functionality at the top of the page
- Navigating to Sarah's profile and viewing her repositories

The repository path `sarah/story-blog` indicates this repository is owned by user 'sarah' and named 'story-blog'. This naming convention (owner/repo-name) is standard across Git hosting platforms.

### Step 4: Fork the Repository

Click the "Fork" button located in the top-right corner of the repository page.

The fork button initiates the server-side copy operation. When you click it, Gitea will:
- Create a complete copy of the repository under your account (jon/story-blog)
- Copy all branches, tags, and commit history
- Establish a link to the original repository (sarah/story-blog)
- Configure the fork relationship for future pull requests

The process typically takes a few seconds, depending on the repository size. Once complete, you'll be redirected to your newly created fork.

### Step 5: Verify the Fork

Confirm that the fork was created successfully.

After forking, you should see:
- The repository URL shows `jon/story-blog` (your fork)
- A note indicating "forked from sarah/story-blog"
- All branches and files from the original repository
- Your username as the owner of this copy

You now have full control over this repository and can clone it to your local machine to begin making changes. The original repository (sarah/story-blog) remains unchanged and independent from your fork.

---

## Additional Information

### Working with Your Fork

Once you've forked a repository, typical next steps include:

**Clone Your Fork Locally:**
```bash
git clone https://gitea-server/jon/story-blog.git
cd story-blog
```

**Add Upstream Remote:**
To keep your fork synchronized with the original repository:
```bash
git remote add upstream https://gitea-server/sarah/story-blog.git
```

**Fetch Updates from Upstream:**
Regularly sync with the original repository to stay current:
```bash
git fetch upstream
git merge upstream/main
```

### Fork Management Best Practices

**Keep Forks Updated:**
Regularly sync your fork with the upstream repository to avoid merge conflicts and stay current with project changes.

**Organize with Branches:**
Create feature branches in your fork for different changes. Never commit directly to the main/master branch.

**Clean Pull Requests:**
Before submitting a pull request, ensure your fork is up-to-date with upstream and your changes are tested.

**Fork Permissions:**
Remember that while you control your fork, you cannot push changes directly to the original repository. All contributions must go through the pull request process.

### When to Fork vs Clone

**Fork When:**
- Contributing to projects you don't own
- Experimenting with major changes to someone else's code
- Creating a derivative project based on existing work
- Participating in open-source development

**Clone Only When:**
- Working on repositories you have direct access to
- Making temporary local copies for reference
- Working on your own projects
- You don't intend to contribute changes back

---

## Validation

Test your solution using KodeKloud's automated validation system. The validator will check:
- Fork exists under the correct user account (jon/story-blog)
- Fork maintains proper relationship to original repository (sarah/story-blog)
- All branches and commit history are present
- Fork is accessible and properly configured

---

[← Day 22](day-22.md) | [Day 24 →](day-24.md)

**Source:** [100 Days of DevOps](https://engineer.kodekloud.com/practice/100-days-of-devops)
