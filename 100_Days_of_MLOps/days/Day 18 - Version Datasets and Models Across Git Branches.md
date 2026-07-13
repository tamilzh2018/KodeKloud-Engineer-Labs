# Lab Information
The xFusionCorp Industries ML team keeps different dataset and model versions on different Git branches so that the team can roll between versions cleanly. Tag the current state as `v1.0`, produce a `v2-improved`branch based on a newer dataset, and confirm that switching back restores the original data.


1. A project exists at `/root/code/fraud-detection/` with a working DVC pipeline and the baseline `data/raw/transactions.csv` already tracked.
    
2. An improved dataset has been pre-staged at `/root/code/fraud-detection/data/raw/transactions_v2.csv` and is visible in the file explorer. Do not delete this file.
    
3. On the main branch, tag the current state as `v1.0`.
    
4. Create a new branch named `v2-improved`. Replace the tracked dataset with the contents of the v2 file, re-track it with DVC, re-run the pipeline, and commit the changes.
    
5. Switch back to the main branch and use `dvc checkout`to restore the v1 dataset on disk. The restored content must match the hash recorded by the `v1.0` tag.
    

> The DVC extension's **DVC TRACKED** section in the EXPLORER panel will reflect the current branch's tracked state—it should show different dataset hashes on `main`and `v2-improved`.

---

# Solution
✅ Part 1: Lab Step-by-Step Guidelines
Navigate to working directory

```shell
cd /root/code/fraud-detection/
```

Tag current state (v1.0)

```shell
git tag v1.0
```

Create new branch (v2-improved)

```shell
git checkout -b v2-improved
```

Copy dataset

```shell
cp data/raw/transactions_v2.csv data/raw/transactions.csv
```

Re-track dataset with DVC

```shell
dvc add data/raw/transactions.csv
```

Output

```shell
100% Adding...|████████████████████████████████████████████|1/1 [00:00, 83.78file/s]
                                                                                    
To track the changes with git, run:

        git add data/raw/transactions.csv.dvc

To enable auto staging, run:

        dvc config core.autostage true
```

Commit changes

```shell
git add data/raw/transactions.csv.dvc
git commit -m "Update dataset to v2 and re-run pipeline"
```

Switch back to main branch

```shell
git checkout main
```

Restore dataset with DVC

```shell
dvc checkout
```

Output

```shell
Building workspace index                                  |7.00 [00:00,  877entry/s]
Comparing indexes                                        |8.00 [00:00, 3.50kentry/s]
Applying changes                                          |1.00 [00:00, 1.20kfile/s]
M       data/raw/transactions.csv
```
# 🧠 Part 2: Simple Step-by-Step Explanation (Beginner Friendly)

**Why do we create a Git tag?**
The command:

git tag v1.0

creates a permanent label for the current project state.

Think of it as taking a snapshot:

main │ ├── v1.0 ← Snapshot

You can always return to exactly this version later.

**Why create a new branch?**
Instead of changing the main branch directly, we create:

v2-improved

This allows us to safely experiment with a new dataset.

The structure becomes:

main │ └── v2-improved

**Why run dvc add again?**
The file name stays the same:

transactions.csv

but its contents change because you copied in the improved dataset.

DVC tracks file contents (using hashes), not just filenames.

Running:

dvc add data/raw/transactions.csv

updates the .dvc pointer to reference the new dataset version.

**Why rerun the pipeline?**
The dataset changed.

That means:

transactions.csv │ ▼ process_data ▼ split_data ▼ train ▼ model.pkl

Every downstream stage depends on the dataset, so DVC reruns the pipeline to produce a model trained on the new data.

**Why use dvc checkout?**
When you switch back to:

git checkout main

Git restores:

dvc.yaml .dvc files dvc.lock

However, Git does not restore the actual dataset or model, because DVC manages those files.

Running:

dvc checkout

reads the .dvc files and restores the correct versions of:

transactions.csv model.pkl

from the DVC cache.


