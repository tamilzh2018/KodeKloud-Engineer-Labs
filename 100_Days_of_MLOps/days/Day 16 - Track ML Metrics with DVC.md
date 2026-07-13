# Lab Information

After training a model, the xFusionCorp Industries ML team wants DVC to surface metrics through `dvc metrics show` and the DVC extension's METRICS view. The fraud-detection pipeline already trains a model and writes a `metrics.json`, but DVC does not recognise the file as a metric. Wire it in correctly.
  

1. A project exists at `/root/code/fraud-detection/` with a three-stage DVC pipeline (`process_data`, `split_data`, `train`). The `train` stage runs `src/models/train.py`, which writes the model to `models/model.pkl` and metrics to `metrics.json`. Do not modify the Python files.
    
2. The `train` stage in `dvc.yaml` must declare `metrics.json` as a DVC metric output, not as a regular file output. The metric must be declared with `cache: false` so the JSON lives in Git for diff history rather than in the DVC cache.
    
3. Re-run the pipeline with `dvc repro` so the metric registration takes effect.
    
4. After your changes, `dvc metrics show` must report the `accuracy` and `f1_score` values from `metrics.json`.
    

> The DVC extension's **METRICS** section under the DVC view will surface the same values directly in the editor once the metric is registered.

---

# Solution
✅ Part 1: Lab Step-by-Step Guidelines
dvc.yaml

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
    outs:
      - models/model.pkl
      - metrics.json

```

Updated dvc.yaml

Changes:

- move metrics.json from outs: -> metrics:
- declare cache: false under metrics

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
    outs:
      - models/model.pkl
    metrics:
      - metrics.json:
          cache: false

```

Navigate to project

```shell
cd /root/code/fraud-detection/
```

Re-run pipeline

```shell
dvc repro
```

Output

```shell
Running stage 'process_data':                                                       
> python src/data/process_data.py
Generating lock file 'dvc.lock'                                                     
Updating lock file 'dvc.lock'

Running stage 'split_data':                                                         
> python src/data/split_data.py
Updating lock file 'dvc.lock'                                                       

Running stage 'train':                                                              
> python src/models/train.py
Metrics: {'accuracy': 1.0, 'f1_score': 1.0}
Updating lock file 'dvc.lock'                                                       

To track the changes with git, run:

        git add models/.gitignore dvc.lock data/processed/.gitignore

To enable auto staging, run:

        dvc config core.autostage true
Use `dvc push` to send your updates to remote storage.
```

Run dvc metrics show

```shell
dvc metrics show
```

Output

```shell
Path          accuracy    f1_score
metrics.json  1.0         1.0
```

![Verify Screenshot](<../screenshots/Screenshot Day 16.png>)

# 🧠 Part 2: Simple Step-by-Step Explanation (Beginner Friendly)

**What is metrics.json?**
After training the model, the Python script creates a file called:

metrics.json

It contains information about how well the model performed.

For example:

{ "accuracy": 1.0, "f1_score": 1.0 }

These numbers help you evaluate the model.

**Why doesn't DVC recognize it automatically?**
DVC only knows about files that are declared in dvc.yaml.

Currently, DVC knows about:

input files (deps) output files (outs) parameters (params)

It doesn't know that metrics.json contains evaluation metrics.

**Why use metrics: instead of outs:?**
Regular outputs:

outs:

models/model.pkl
are treated as artifacts (files produced by the pipeline).

Metrics are different—they are values you want to compare between experiments.

So we use:

metrics:

metrics.json: cache: false
This tells DVC:

metrics.json contains evaluation metrics. Keep it in Git (cache: false) instead of storing it in the DVC cache. Allow commands like dvc metrics show and dvc metrics diff to read it.

**Why cache: false?**
Normally, DVC stores outputs in its cache.

For metrics, we want the JSON file to stay in the Git repository because:

it's small, it's easy to compare between commits, Git can track its history.

That's why the lab requires:

cache: false

**What does dvc metrics show do?**
After running:

dvc repro

you can execute:

dvc metrics show

Instead of opening metrics.json manually, DVC displays the important values in a table, for example:

Path accuracy f1_score metrics.json 1.0 1.0

**What is dvc metrics diff?**
As you experiment with different model parameters (such as n_estimators), the metrics may change.

Running:

dvc metrics diff

compares the metric values across Git commits, making it easy to see whether the new model performed better or worse.