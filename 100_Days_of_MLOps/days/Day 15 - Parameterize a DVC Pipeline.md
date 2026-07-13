# Lab Information

The xFusionCorp Industries ML team manages model hyperparameters through `params.yaml` so experiments can vary without code changes. The fraud-detection project's `train` stage already wires `params.yaml` for `n_estimators`, but `dvc repro`currently fails. Correct the parameter wiring and demonstrate that DVC re-runs the train stage when the parameter changes.
  

1. A project exists at `/root/code/fraud-detection/` with a three-stage DVC pipeline (`process_data`, `split_data`, `train`) and a `params.yaml` already in place. Do not modify the Python files.
    
2. The `train` stage in `dvc.yaml` references the `n_estimators` parameter. Every name listed under `params:` must resolve to a key in `params.yaml`.
    
3. Review `params.yaml`, correct whatever prevents `dvc repro` from completing, and run the full pipeline.
    
4. Demonstrate that DVC tracks parameter changes by updating `n_estimators` to a different value (for example `200`). Run `dvc repro` again—only the `train`stage should re-execute, the new value must be recorded in `dvc.lock`, and `models/model.pkl` must be regenerated.
    

> The DVC extension's **PARAMS** section under the DVC view will surface the values from `params.yaml` directly in the editor.

---

# Solution
✅ Part 1: Lab Step-by-Step Guidelines
Original (dvc.yaml)

```yaml
stages:
  process_data:
    cmd: python src/data/process_data.py
    deps:
      - data/raw/transactions.csv
      - src/data/process_data.py
    outs:
      - data/processed/clean_transactions.csv

  split_data:
    cmd: python src/data/split_data.py
    deps:
      - data/processed/clean_transactions.csv
      - src/data/split_data.py
    outs:
      - data/processed/train.csv
      - data/processed/test.csv

  train:
    cmd: python src/models/train.py
    deps:
      - data/processed/train.csv
      - src/models/train.py
    params:
      - n_estimators
    outs:
      - models/model.pkl

```

Original (params.yaml)

```yaml
n_estimator: 100

```

Updated (params.yaml)

- n_estimator -> n_estimators
- 100 -> 200

```yaml
n_estimators: 200

```

Navigate to working directory

```shell
cd fraud-detection/
```

Execute dvc repro

```shell
dvc repro
```

Output

```shell
Running stage 'process_data':                                                       
> python src/data/process_data.py
Processed 15 rows
Generating lock file 'dvc.lock'                                                     
Updating lock file 'dvc.lock'

Running stage 'split_data':                                                         
> python src/data/split_data.py
Train: 12 rows, Test: 3 rows
Updating lock file 'dvc.lock'                                                       

Running stage 'train':                                                              
> python src/models/train.py
Trained RandomForestClassifier with n_estimators=200
Updating lock file 'dvc.lock'                                                       

To track the changes with git, run:

        git add models/.gitignore data/processed/.gitignore dvc.lock

To enable auto staging, run:

        dvc config core.autostage true
Use `dvc push` to send your updates to remote storage.
```
# 🧠 Part 2: Simple Step-by-Step Explanation (Beginner Friendly)

**What is params.yaml?**
Instead of hardcoding values like:

n_estimators = 100

the project stores them in a separate file:

n_estimators: 100

The training script reads this value automatically.

This makes it easy to try different settings without changing the Python code.

**Why isn't changing params.yaml enough?**
Even though train.py reads params.yaml, DVC doesn't automatically know that the train stage depends on it.

If the params: section is missing from dvc.yaml, DVC thinks:

"Nothing important changed."

So running:

dvc repro

may skip the training stage.

**What does the params: section do?**
Adding:

params:

n_estimators
tells DVC:

"The train stage depends on the value of n_estimators."

Now, whenever n_estimators changes, DVC knows the model needs to be retrained.

**What happens after changing the parameter?**
Initially:

n_estimators: 100

After editing:

n_estimators: 200

When you run:

dvc repro

DVC compares the tracked parameter values and notices that n_estimators has changed.

Since only the training configuration changed:

✅ train runs again. ✅ process_data is skipped. ✅ split_data is skipped.

This saves time by only rerunning the stage that is affected.

**What is dvc.lock?**
After each successful run, DVC records the parameter value used.

Example:

params: params.yaml: n_estimators: 200

This allows anyone to reproduce the exact experiment later using the same parameter values.

**What does dvc params diff do?**
The command:

dvc params diff

shows how parameter values changed between Git commits.

For example:

Path Param Old New params.yaml n_estimators 100 200

This is useful for comparing different experiments and understanding what changed between model versions.