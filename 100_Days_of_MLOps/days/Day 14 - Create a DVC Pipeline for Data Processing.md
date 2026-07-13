# Lab Information

The xFusionCorp Industries ML team uses DVC pipelines to keep data processing reproducible. A draft `dvc.yaml` exists in the fraud-detection project, but `dvc repro` does not complete the full pipeline. Correct the pipeline definition so it runs cleanly end to end.
  

1. A project exists at `/root/code/fraud-detection/` with DVC initialised. Python scripts are at `src/data/process_data.py` and `src/data/split_data.py`; raw input is at `data/raw/transactions.csv`. Do not modify the Python files or the input data.
    
2. The corrected pipeline must declare two stages with the following behaviour:
    
    - `process_data` – Depends on `data/raw/transactions.csv` and `src/data/process_data.py`; produces `data/processed/clean_transactions.csv`.
    - `split_data` – Depends on `data/processed/clean_transactions.csv` and `src/data/split_data.py`; produces `data/processed/train.csv` and `data/processed/test.csv`.
3. Review the existing `dvc.yaml` and correct everything that prevents `dvc repro` from completing.
    
4. After your changes, `dvc repro` must run end to end and `dvc status` must report no stale stages.
    

> Once the pipeline is valid, the DVC extension's **PIPELINES**section under the DVC view will list both stages and visualise the dependency graph between them.

---

# Solution
✅ Part 1: Lab Step-by-Step Guidelines
Original file (/root/code/fraud-detection/dvc.yaml)

```yaml
stages:
  process_data:
    cmd: python src/data/process.py
    deps:
      - data/raw/transactions.csv
      - src/data/process_data.py
    outs:
      - data/processed/clean.csv

  split_data:
    cmd: python src/data/split_data.py
    deps:
      - src/data/split_data.py
    outs:
      - data/processed/train.csv
      - data/processed/test.csv

```

Corrections:

- fixed file name on process_data cmd line
- fixed file name on process_data outs line
- added depended file on split_data

Updated file (/root/code/fraud-detection/dvc.yaml)

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
      - src/data/split_data.py
      - data/processed/clean_transactions.csv
    outs:
      - data/processed/train.csv
      - data/processed/test.csv

```

Navigate to dvc repo

```shell
cd /root/code/fraud-detection/
```

Execute dvc repro

```shell
dvc repro
```

Output

![DVC repro Screenshot](<../screenshots/Screenshot Day 14.png>)

Check dvc status

```shell
dvc status
```

Output

```shell
Data and pipelines are up to date.
```
# 🧠 Part 2: Simple Step-by-Step Explanation (Beginner Friendly)

**What is a DVC Pipeline?**
A DVC pipeline defines a sequence of steps for processing data. Each step is called a stage.

Instead of manually running scripts one by one, DVC knows:

which script to run what input files it needs what output files it creates which stage depends on another

This makes the workflow reproducible.

**Why do we create two stages?**
The project has two separate tasks:

Stage 1: Process the raw data

Input:

data/raw/transactions.csv

Script:

src/data/process_data.py

Output:

data/processed/clean_transactions.csv

This stage cleans or prepares the raw dataset.

Stage 2: Split the processed data

Input:

data/processed/clean_transactions.csv

Script:

src/data/split_data.py

Outputs:

data/processed/train.csv data/processed/test.csv

This stage creates the training and testing datasets.

How are the stages connected?
The output of the first stage becomes the input of the second stage:

transactions.csv │ ▼ process_data │ ▼ clean_transactions.csv │ ▼ split_data ├──────────┐ ▼ ▼ train.csv test.csv

This dependency allows DVC to automatically execute the stages in the correct order.

**What does dvc repro do?**
The command:

dvc repro

checks the pipeline and runs any stages that need to be executed.

In this lab:

process_data runs first because it depends on the raw dataset. After clean_transactions.csv is created, split_data runs because its dependency is now available.

You don't need to run the Python scripts manually—DVC handles the execution order.

**What is dvc.lock?**
After a successful pipeline run, DVC creates:

dvc.lock

This file records:

the exact command used the dependencies the output files checksums (hashes) of inputs and outputs

It ensures that the pipeline can be reproduced exactly in the future.

