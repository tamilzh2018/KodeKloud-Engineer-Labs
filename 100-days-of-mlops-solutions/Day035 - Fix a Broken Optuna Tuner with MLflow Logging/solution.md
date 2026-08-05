# Task 35
The xFusionCorp Industries ML platform team is currently tuning hyperparameters for fraud detection using Optuna and reviewing the comprehensive search results in the MLflow Compare view. A draft tuner is available at /root/code/fraud-detection/src/models/tune.py. However, the current optimization process is functioning incorrectly, causing no trials to be recorded on the tracking server. Your objective is to modify the tuner so that all 20 trials are visible in MLflow, and ensure that the saved best configuration corresponds to the candidate with the highest F1 score.


The MLflow tracking server is already running on port 5000. The MLflow UI button at the top of the lab can be opened to confirm—the dashboard loads with an empty hyperopt-tuning experiment.

The project layout under /root/code/fraud-detection/:

data/train.csv – A 200-row synthetic binary-classification dataset (imbalanced roughly 70 / 30).
src/models/tune.py – The Optuna tuner scaffold. Fold iteration, metric averaging, Optuna study creation, and YAML persistence are already wired; corrections are required.
configs/ – Where best_params.yaml is written after the search completes.
Run the tuner once against the scaffold as-is—python src/models/tune.py—and check the hyperopt-tuning experiment to confirm no trials land on the tracking server.

The end state must include:

At least 20 runs exist in the hyperopt-tuning experiment on MLflow. Every run carries params.n_estimators, params.max_depth, and metrics.f1_score.
A YAML file at /root/code/fraud-detection/configs/best_params.yaml with exactly two keys: n_estimators (integer in the range [50, 500]) and max_depth (integer in the range [3, 20]).
The saved best_params corresponds to the highest-F1 trial in the search space.
# Solution

**Optuna** automates hyperparameter search: you write an `objective(trial)` that samples candidate values (`trial.suggest_int(...)`), evaluates them, and returns a score; a **study** then runs the objective many times and remembers the best. Two things make a study trustworthy and inspectable. First, the **direction** must match the metric — F1 is better when *higher*, so the study must `maximize` (a `minimize` study would hand back the *worst* trial as `best_params`). Second, logging **each trial as its own MLflow run** turns the search into something you can open in the Compare view and reason about, rather than a single opaque "best" number. This task fixes the direction and adds the per-trial MLflow logging.

> As an MLOps engineer, you track a hyperparameter sweep as per-trial MLflow runs with the correct study direction—you are not reasoning about which hyperparameters make a better model. The data is synthetic.

#### Follow the steps below

##### 1. Confirm the starting state.
Open the **MLflow UI** button at the top of the lab — the `hyperopt-tuning` experiment is present and empty. From a VS Code terminal:
```
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:5000/
```
A `200` confirms the server is reachable.

##### 2. Run the draft tuner and observe the gaps.
```
python3 /root/code/fraud-detection/src/models/tune.py
```
The script completes 20 Optuna trials and writes `configs/best_params.yaml`. Now check the MLflow UI — the `hyperopt-tuning` experiment is still empty, so no evidence of the search is inspectable. The printed `best f1` is also suspiciously low, because the study picked the minimum-F1 trial.

##### 3. Inspect `tune.py`.
Open `/root/code/fraud-detection/src/models/tune.py` in the VS Code editor. Two things need attention.

- The `objective(trial, X, y)` function returns the mean F1 but does not open an MLflow run — nothing is ever logged. The docstring says "every trial must land in the MLflow `hyperopt-tuning` experiment as an independent run" and lists the required params + metric.
- The `optuna.create_study(direction="minimize", ...)` call is directed the wrong way for F1 — the metric should be maximised so `study.best_params` returns the highest-F1 trial.

##### 4. Add per-trial MLflow logging.
Inside `objective`, open a short `mlflow.start_run(...)` context block after the F1 score is computed. Log the two sampled hyperparameters as run parameters and the mean F1 as a metric keyed `f1_score`:
```python
    with mlflow.start_run(run_name=f"trial-{trial.number}"):
        mlflow.log_params({"n_estimators": n_estimators, "max_depth": max_depth})
        mlflow.log_metric("f1_score", score)

    return score
```

##### 5. Fix the study direction.
Change the Optuna study creation to maximise:
```python
study = optuna.create_study(direction="maximize", study_name=EXPERIMENT_NAME)
```
Save the file.

##### 6. Re-run the tuner.
```
python3 /root/code/fraud-detection/src/models/tune.py
cat /root/code/fraud-detection/configs/best_params.yaml
```
The printed `best f1` is now high, and `best_params.yaml` carries the maximising combination.

##### 7. Verify in the MLflow UI.
Open the **MLflow UI** button → `hyperopt-tuning` experiment. The run list shows 20 trial runs named `trial-0` through `trial-19`, each with `params.n_estimators`, `params.max_depth`, and `metrics.f1_score`. Select every run in the list and click **Compare** — the parallel-coordinates plot surfaces the shape of the search, and the top-F1 point matches the combination saved to `best_params.yaml`.

#### References
- Optuna — first optimization (`objective`, `suggest_int`, `study.optimize`): https://optuna.readthedocs.io/en/stable/tutorial/10_key_features/001_first.html
- `optuna.create_study` (the `direction` argument): https://optuna.readthedocs.io/en/stable/reference/generated/optuna.create_study.html
- MLflow logging (`start_run` / `log_params` / `log_metric`): https://mlflow.org/docs/latest/python_api/mlflow.html
