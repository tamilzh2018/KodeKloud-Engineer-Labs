Prompt

The xFusionCorp Industries ML team is adopting DVC so that datasets and model files are versioned separately from code. Initialise DVC inside the existing Git repository at `/root/code/fraud-detection/` and record the initialisation in Git.

1. A Git repository already exists at `/root/code/fraud-detection/` with an initial commit.
    
2. Initialise DVC inside that repository so that the standard `.dvc/` control directory and `.dvcignore` file are created alongside the existing Git working tree.
    
3. Stage every file that DVC produces during initialisation, and record them in a new Git commit with the message `Initialize DVC`.
    

> Once initialisation is complete, the **DVC** extension will detect the new `.dvc/` directory and surface the **DVC TRACKED** section in the EXPLORER panel together with a `DVC` indicator in the bottom status bar.

---

Solution

Navigate to the correct directory

```shell
cd /root/code/fraud-detection/
```

Check Git status

```shell
git status
```

Output looks good

```shell
On branch master
nothing to commit, working tree clean
```

Check DVC exists

```shell
dvc --version
```

Verified DVC is installed

```shell
3.67.1
```

Initialize DVC 

```shell
dvc init
```

Initialization completed successfully

```shell
Initialized DVC repository.

You can now commit the changes to git.
```

Check Git to see what has changed

```shell
git status
```

Stage new files

```shell
git add .dvc .dvcignore
```

New files have been staged and are ready to commit

```shell
git commit -m "Initialize DVC"
```

Verify the commit

```shell
git log --oneline -n 2
```

Confirm clean working tree

```shell
git status
```

Success

```shell
On branch master
nothing to commit, working tree clean
```
🧠 Part 2: Simple Step-by-Step Explanation (Beginner Friendly)

**What is DVC?**
DVC (Data Version Control) is a tool used in Machine Learning projects to track:

Datasets Models Large files

without storing them directly in Git.

Think of it like:

Git -> tracks code DVC -> tracks data and models

**Why are we running dvc init?**
The repository already exists as a Git project.

When we run:

dvc init

DVC adds its own management files:

.dvc/ .dvcignore

These files tell DVC how to manage datasets and model artifacts.

What does .dvc/ contain?
Example:

.dvc/ ├── config ├── .gitignore └── tmp/

These files store DVC configuration information.

Why do we commit the DVC files?
The lab specifically says:

Record the initialization in Git.

This means the new DVC files must be saved in Git history.

So we:

git add .dvc .dvcignore git commit -m "Initialize DVC"

This creates a permanent record that DVC was enabled in the project.