# Task
The xFusionCorp Industries ML platform team has developed a comprehensive fraud-detection training pipeline that includes data validation, Optuna tuning across two model families, model selection against a release threshold, Model Registry registration with a release-lane alias, and a consolidated training report. All of these components are integrated behind a single make train-pipeline command. Currently, the pre-staged system does not function end-to-end, as each invocation of make train-pipeline reveals a wiring issue, and two stages contain unfinished TODO items. To prepare for the release checklist, you must address the necessary updates in the Makefile, src/select_model.py, src/register.py, and src/report.py. Your objective is to resolve the wiring issues and complete the two TODO blocks, ensuring that make train-pipeline executes successfully from start to finish, the MLflow Model Registry contains a fraud-detector version under the staging alias, and reports/training_report.json compiles all upstream artifacts.


The MLflow tracking server is already running on port 5000. The MLflow UI button at the top of the lab can be opened to confirm—the dashboard loads with an empty fraud-detection-tuning experiment.

The project layout under /root/code/fraud-detection/:

data/train.csv – The 200-row synthetic binary-classification dataset the rest of the Training section uses.
src/validate_data.py – Schema + null-check gate. Writes reports/validation_status.json. Correct.
src/tune.py – Runs 10 Optuna trials across RandomForest and GradientBoosting, each logged as an MLflow run tagged with model_type + params.{n_estimators,max_depth} + metrics.f1_score + the fitted model artefact. Correct.
src/select_model.py – Picks the winning run by the training metric and writes reports/selection.json. Has a wiring bug.
src/register.py – Registers the selected run's model as fraud-detector; the release-lane alias assignment is left as a # TODO.
src/report.py – Aggregates every upstream artefact into reports/training_report.json; the report assembly is left as a # TODO.
Makefile – train-pipeline target runs the five stages in order. Has a wiring bug.
The end state must include:

make train-pipeline completes without non-zero exit.
The fraud-detection-tuning MLflow experiment carries at least five trial runs, each with metrics.f1_score.
reports/selection.json, reports/validation_status.json, and reports/training_report.json are all present. The training report carries best_model, best_params, metrics, total_trials, and validation_status keys; validation_status is "ok" and total_trials is an integer ≥ 5.
The MLflow Model Registry (MLflow UI → Models) shows a fraud-detector registered model with at least one version. That version carries the staging alias and no production alias.
Run make train-pipeline once against the scaffold as-is — the first wiring bug surfaces immediately, and each re-run reveals the next. The two # TODO blocks (the registry alias and the report assembly) do not crash the pipeline; they are caught by the release checklist, so complete them before expecting a clean pass.
# Solution

This capstone wires the whole training lifecycle behind one `make train-pipeline` command: **validate** the data → **tune** across two model families (Optuna) → **select** the best run against a release threshold → **register** it in the Model Registry on a release-lane alias → **report** a consolidated summary. A pipeline like this fails in two ways: *wiring* bugs (a stage runs out of order, or reads a key another stage never wrote) that crash the run, and *unfinished stages* whose output is incomplete even when the run exits cleanly. Here you fix two wiring bugs (stage order, metric key) and complete two unfinished stages (the registry **alias** assignment and the **report** aggregation) so the system runs end to end and the release checklist passes.

> As an MLOps engineer, you integrate the section's skills into one end-to-end training system (validate → tune → select → register → report)—you are not judging model quality. The data is synthetic and `f1_score` is a plumbing token.

#### Follow the steps below

##### 1. Confirm the starting state.
Open the **MLflow UI** button at the top of the lab — the `fraud-detection-tuning` experiment is present and empty. From a VS Code terminal:
```
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:5000/
ls /root/code/fraud-detection/src/ /root/code/fraud-detection/Makefile
```
A `200` confirms MLflow is reachable. The five stage scripts and the `Makefile` are already staged under `/root/code/fraud-detection/`.

##### 2. Run the pipeline and fix the stage order.
```
cd /root/code/fraud-detection && make train-pipeline
```
`validate_data.py` succeeds, then `src/select_model.py` aborts: `[select] no runs in experiment 'fraud-detection-tuning' — the tune stage has not produced any candidates yet.` The recipe selects before it tunes. Open `Makefile` and swap the two lines so `tune.py` runs first:
```make
train-pipeline:
	python3 src/validate_data.py
	python3 src/tune.py
	python3 src/select_model.py
	python3 src/register.py
	python3 src/report.py
```

##### 3. Re-run and fix the selector's metric key.
```
make train-pipeline
```
`tune.py` now runs 10 Optuna trials (visible in the **MLflow UI** → `fraud-detection-tuning`), then `select_model.py` aborts with a pandas `KeyError: 'metrics.accuracy'`. The tuner logs `metrics.f1_score`, not `accuracy`. In `src/select_model.py`, change both the `order_by` argument and the column access:
```python
    runs = mlflow.search_runs(
        experiment_ids=[exp.experiment_id],
        order_by=["metrics.f1_score DESC"],
        max_results=200,
    )
    ...
    best = runs.iloc[0]
    score = float(best["metrics.f1_score"])
```
The pipeline now runs to completion — but two stages are still unfinished.

##### 4. Author the registry alias (TODO in `register.py`).
`register.py` registers the selected model but never puts it on a release lane. Complete the TODO so the just-registered version gets the `RELEASE_ALIAS` (`"staging"`) alias:
```python
    client.set_registered_model_alias(
        REGISTERED_MODEL_NAME, RELEASE_ALIAS, version.version,
    )
```

##### 5. Author the report aggregation (TODO in `report.py`).
`report.py` gathers each upstream artefact (`validation`, `selection`, `total_trials`, `best_params`, `best_metrics`) but ships an empty `report = {}`. Assemble the consolidated report:
```python
    report = {
        "best_model": selection.get("model_type", ""),
        "best_params": best_params,
        "metrics": best_metrics,
        "total_trials": total_trials,
        "validation_status": validation.get("status", ""),
    }
```
Save both files.

##### 6. Run the pipeline end to end and verify.
```
make train-pipeline
cat reports/training_report.json
```
The pipeline completes with no non-zero exit, and the report lists `best_model`, `best_params`, `metrics`, `total_trials ≥ 5`, and `validation_status = "ok"`. Confirm the registry:
```
python3 -c "from mlflow.tracking import MlflowClient; c = MlflowClient('http://localhost:5000'); print(dict(c.get_registered_model('fraud-detector').aliases))"
```
The output is `{'staging': '<version>'}` — a `fraud-detector` version on the `staging` lane, with no `production` alias. In the **MLflow UI** → **Models** → `fraud-detector`, the latest version shows the `staging` alias; its **Artifacts** list the `model/` directory logged by the tuner.

#### References
- GNU Make — targets, recipes, and the order of a rule's commands: https://www.gnu.org/software/make/manual/make.html
- MLflow Model Registry — registering versions and assigning aliases: https://mlflow.org/docs/latest/model-registry.html
- MLflow Python API (`search_runs`, `set_registered_model_alias`, `get_run`): https://mlflow.org/docs/latest/python_api/mlflow.html
