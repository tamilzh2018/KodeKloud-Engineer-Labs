# Lab Information:

The xFusionCorp Industries deployment team needs the fraud-detection model code packaged as an installable Python distribution. A draft `pyproject.toml`exists at `/root/code/fraud-detection/`, but it does not build a wheel that meets the team's standard. Correct the file and produce a compliant package.

1. The project at `/root/code/fraud-detection/` already contains the source code under `src/fraud_detection/`. The Python files are complete—you do not need to modify any of them.
    
2. The corrected `pyproject.toml` must satisfy every one of the following:
    
    - it declares a `[build-system]` section with `requires = ["setuptools>=61.0", "wheel"]`and `build-backend = "setuptools.build_meta"`;
    - `name` is `fraud_detection` (the distribution name must match the module path under `src/`);
    - `version` is `0.1.0`;
    - `requires-python` is `>=3.10`;
    - `dependencies` is `["scikit-learn", "pandas", "numpy"]`.
3. Review the existing `pyproject.toml` and correct everything that does not match the requirements above.
    
4. Build the package from the project directory:
    

```
   cd /root/code/fraud-detection
   python3 -m build
```

5. The build must produce a wheel named `fraud_detection-0.1.0-*.whl` under `dist/`.

The `build` package is already installed. Use `python3` rather than `python`.

---

# Solution
🧭 Part 1: Lab Step-by-Step Guidelines

Original pyproject.toml

```shell
[project]
name = "fraud-detection"
version = "0.0.1"
description = "Fraud detection model for xFusionCorp Industries"
requires-python = ">=3.8"
dependencies = []

[tool.setuptools.packages.find]
where = ["src"]

```

Corrections:
- Added `[build-system]`
- Changed package name from `fraud-detection` → `fraud_detection`
- Updated version to `0.1.0`
- Updated Python requirement to `>=3.10`
- Added required dependencies
- Kept setuptools package discovery pointed at `src/`

Updated pyproject.toml

```shell
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "fraud_detection"
version = "0.1.0"
description = "Fraud detection model for xFusionCorp Industries"
requires-python = ">=3.10"
dependencies = ["scikit-learn", "pandas", "numpy"]

[tool.setuptools.packages.find]
where = ["src"]

```
# Create tests/test_predict.py
from fraud_detection import predict


def test_predict_fraudulent_transaction():
    assert predict([[150]]) == [1]


def test_predict_legitimate_transaction():
    assert predict([[100]]) == [0]


# Test and Build the package from the project directory

```shell
cd /root/code/fraud-detection
pytest
python3 -m build
```

Check for new wheel at dist/

🧠 Part 2: Simple Beginner-Friendly Explanation

**What is this lab about?**

This lab focuses on packaging a Python project into an installable distribution.

The goal is to:

configure the project correctly build a Python wheel package make the ML code installable on other systems

**What is pyproject.toml?**
pyproject.toml is the modern Python project configuration file.

It defines: project metadata dependencies build system configuration packaging settings

It replaces older files like: setup.py setup.cfg

in many modern Python projects. Understanding the [build-system] Section

The lab requires:

[build-system] requires = ["setuptools>=61.0", "wheel"] build-backend = "setuptools.build_meta"

This tells Python: which tools are needed to build the package which backend performs the build

Why setuptools and wheel Are Required Package Purpose setuptools Builds Python packages wheel Creates .whl files

Without these: package building may fail

Why the Package Name Matters The lab requires: name = "fraud_detection" This must match the module directory: src/fraud_detection/ Using a different name can break:

imports packaging installation

What requires-python Means Required setting: requires-python = ">=3.10" This means: the package only supports Python 3.10 or newer.

Why Dependencies Are Declared Required dependencies:

dependencies = [ "scikit-learn", "pandas", "numpy" ]

When someone installs the package: these libraries install automatically

What python3 -m build Does

Command: python3 -m build performs the packaging process.

It creates:

source distribution (.tar.gz) wheel distribution (.whl)

inside:

dist/

**What Is a Wheel File?**
A wheel (.whl) is a standard Python package format.

Example: fraud_detection-0.1.0-py3-none-any.whl

It allows fast installation using: pip install package.whl

Why python3 Must Be Used The lab explicitly requires:

python3 -m build

instead of:

python -m build

This guarantees the correct Python interpreter is used.

