# Lab Information:
A colleague has started a new ML project at `/root/code/fraud-detection/`, but the layout does not match the xFusionCorp Industries standard. Bring the project in line with the team's conventions.

  

1. Inspect the existing project at `/root/code/fraud-detection/`.
    
2. The final layout must match the tree below exactly:
    

```
fraud-detection/
├── data/
│   ├── raw/
│   └── processed/
├── models/
├── notebooks/
├── src/
│   ├── data/
│   ├── features/
│   ├── models/
│   └── utils/
├── tests/
├── configs/
├── requirements.txt
└── README.md
```

3. Every subdirectory under `src/` must contain an `__init__.py` file so that Python recognises it as a package.
    
4. `requirements.txt` must list the following dependencies, one per line: `scikit-learn`, `pandas`, `numpy`, and `mlflow`. The canonical PyPI name for the scikit-learn package is `scikit-learn`.
    
5. `README.md` must begin with the heading `# fraud-detection`.
    
6. Review the existing project and correct everything that does not match the requirements above.

---

# Solution
🧭 Part 1: Lab Step-by-Step Guidelines

Added folders as required for structure

```shell
fraud-detection/
├── data/
│   ├── raw/ # added
│   └── processed/ # added
│
├── tests/ # added
└── configs/ # added
```

Corrected directory names

```shell
├── src/
│   ├── features/ # added s
│   └── utils/ # added s
```

Corrected requirements.txt contents

```shell
scikit-learn # corrected name
pandas
numpy
mlflow # added
```

Corrected README.md first line

```shell
# fraud-detection
```

Ensured add subdirectories under src/ include file

```shell
__init__.py found under all subdirectories
```

🧠 Part 2: Simple Beginner-Friendly Explanation

This lab focuses on organising a machine learning project according to the xFusionCorp Industries standard structure.

The goal is to:

standardise project layout improve maintainability make collaboration easier for developers and data scientists

You must inspect the existing project and correct anything that does not match the required structure.

**Understanding the Required Project Structure**

The final project must look exactly like this:

fraud-detection/ ├── data/ │ ├── raw/ │ └── processed/ ├── models/ ├── notebooks/ ├── src/ │ ├── data/ │ ├── features/ │ ├── models/ │ └── utils/ ├── tests/ ├── configs/ ├── requirements.txt └── README.md

Each folder has a specific purpose in an ML workflow.

Purpose of Each Directory

data/ Stores datasets used in the project.

data/raw/ Contains original unmodified data.

Example: transactions.csv

data/processed/ Contains cleaned or transformed datasets used for training.

Example: clean_transactions.csv

models/ Stores trained machine learning models.

Example: fraud_model.pkl

notebooks/ Contains Jupyter notebooks for experimentation and analysis.

Example: eda.ipynb

src/ Contains the main Python source code for the application. This keeps project logic organised and modular.

Why init.py Files Are Required Every subdirectory under src/ must contain: init.py

This tells Python: “Treat this directory as a Python package.”

Without these files: imports may fail modules may not be recognised correctly

Example: from src.models.train import train_model

Purpose of src/ Subdirectories

Directory Purpose src/data Data loading and preprocessing src/features Feature engineering logic src/models Training and prediction code src/utils Helper functions and utilities

Why requirements.txt Matters The lab requires the following dependencies:

scikit-learn pandas numpy mlflow

This file helps developers install all required Python packages consistently.

**Important note:**

the correct PyPI package name is scikit-learn not sklearn

Why README.md Matters The README file provides project documentation.

The lab specifically requires it to begin with:

# fraud-detection
This acts as the project title and ensures naming consistency.

Why Exact Naming Is Important Lab validators check: exact folder names exact file names exact dependency names

Even small differences such as: feature instead of features util instead of utils

# Fraud instead of # fraud-detection
can cause the lab to fail.