# Task
The xFusionCorp Industries ML platform team operates a fraud-detection training process structured as a four-stage pipeline: preprocess, featurize, train, and evaluate. This pipeline is managed by a single Python script that consolidates the entire run into one MLflow execution. However, two critical issues need to be addressed.

First, the stage chain is incorrectly configured, resulting in two stages reading from the incorrect upstream source. As a consequence, the preprocess and featurize stages do not successfully transmit their outputs to the model, despite the pipeline indicating a successful run.

Second, the orchestrator currently fails to log the run; neither the pipeline's configuration nor its final metrics are recorded in MLflow.

Your task is to identify and rectify the miswiring in the stage chain and to enhance the orchestrator, ensuring that a single MLflow run accurately captures the parameters of the pipeline and its evaluation metrics.


The MLflow tracking server is already running on port 5000. The MLflow UI button at the top of the lab can be opened to confirm—the dashboard loads with an empty training-pipeline experiment.

The project layout under /root/code/fraud-detection/:

data/raw/train.csv – The same 200-row synthetic binary-classification dataset the rest of the Training section uses (imbalanced roughly 70 / 30).
configs/pipeline_config.yaml – Declares the data paths, model hyperparameters, output paths, and MLflow settings every stage consumes. Correct and must remain intact.
src/preprocess.py, src/featurize.py, src/train.py, src/evaluate.py – The four pipeline stages. preprocess.py drops negligible-amount rows (amount < 50) and duplicates before writing the processed CSV. The four stages are wired through the config's data: paths.
run_pipeline.py – The orchestrator that executes the four stages in order under a single MLflow run. The stage-execution loop and fail-fast handling are wired; two tracking steps (logging the config parameters and the final metrics) are marked TODO for you to complete.
Run the orchestrator once against the scaffold as-is—python run_pipeline.py—then inspect the row counts of the intermediate CSVs under data/ to see where the stage chain diverges (the pipeline reports success even though outputs do not flow through).

The end state must include:

The row count of data/features/features.csv equals the row count of data/processed/train_clean.csv and is strictly less than the 200-row raw CSV.
The training stage consumes the feature matrix — the engineered amount_log column produced by featurize is present in the training data (and in the persisted held-out set), not the pre-featurize processed data.
models/model.pkl and reports/evaluation.json are written and the report carries accuracy, f1, and roc_auc as numeric values.
Exactly one MLflow run exists in the training-pipeline experiment, carrying params.model_type, params.n_estimators, params.max_depth, and the three evaluation metrics.

# Solution

A multi-stage training **pipeline** chains independent steps — preprocess → featurize → train → evaluate — where each stage reads its **immediate predecessor's output**. The contract holds only if the wiring is right: every stage's *input* path must point at the *output* the previous stage wrote. When a stage reaches back to an earlier source, the chain silently breaks — work done upstream (here, dropping low-value rows in preprocess and engineering `amount_log` in featurize) never reaches the model, even though the pipeline still "runs" green. This task has **two** such broken links. Beyond the wiring, the **orchestrator** (`run_pipeline.py`) is what turns four independent scripts into one tracked experiment: an imperative Python runner that wraps the whole pipeline in a single MLflow run and records its parameters and metrics — the experiment-tracking layer a declarative pipeline definition alone does not provide. Two of its tracking steps are left for you to complete.

> As an MLOps engineer, you wire a multi-stage pipeline correctly and capture its end-to-end run in MLflow—you are not judging the model's predictive quality. The data is synthetic.

#### Follow the steps below

##### 1. Confirm the starting state.
Open the **MLflow UI** button at the top of the lab — the `training-pipeline` experiment is present and empty. From a VS Code terminal:
```
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:5000/
ls /root/code/fraud-detection/src/ /root/code/fraud-detection/run_pipeline.py /root/code/fraud-detection/configs/pipeline_config.yaml
```
A `200` confirms MLflow is reachable. The four stage scripts, the orchestrator, and the config are already staged.

##### 2. Run the draft pipeline and observe the gaps.
```
cd /root/code/fraud-detection && python3 run_pipeline.py
```
All four stages complete and one run is written to the `training-pipeline` experiment. Compare the row counts each stage reports:
```
wc -l data/raw/train.csv data/processed/train_clean.csv data/features/features.csv
```
The raw CSV is 200 rows (+ header). The processed CSV is shorter — preprocess dropped the low-amount rows and duplicates. But the features CSV is still 200 rows — the preprocess stage's work never reached the feature matrix. And the held-out set the train stage writes lacks the `amount_log` column, so train trained on the pre-featurize data. Two links are broken. In the MLflow UI, the run also carries no parameters and no metrics — the orchestrator's tracking is unfinished.

##### 3. Diagnose the two broken links.
Each stage's input path must point at its immediate predecessor's output. Read the `input_path` / `features_path` assignments against the config's `data:` block:
- `src/featurize.py` reads `config["data"]["raw_path"]` — it bypasses preprocess. Its output row count should match the *preprocessed* count, so it must read `processed_path`.
- `src/train.py` reads `config["data"]["processed_path"]` — it bypasses featurize, so the model never sees the engineered `amount_log`. It must read `features_path`.

The config's `data:` block already exposes both keys; the fixes are confined to the stage scripts (the config must stay intact).

##### 4. Fix the featurize input source.
In `/root/code/fraud-detection/src/featurize.py`, change the `input_path` line so featurize reads the preprocess stage's output:
```python
input_path = config["data"]["processed_path"]
```

##### 5. Fix the train input source.
In `/root/code/fraud-detection/src/train.py`, change the `features_path` line so train reads the featurize stage's output:
```python
features_path = config["data"]["features_path"]
```
Save both files.

##### 6. Complete the orchestrator — TODO 1 (log the parameters).
Open `run_pipeline.py`. Inside the `with mlflow.start_run(...)` block, at TODO 1, log the config-driven hyperparameters onto the run:
```python
        mlflow.log_param("model_type", config["model"]["type"])
        mlflow.log_param("n_estimators", config["model"]["n_estimators"])
        mlflow.log_param("max_depth", config["model"]["max_depth"])
```

##### 7. Complete the orchestrator — TODO 2 (log the metrics).
At TODO 2, after the stage loop, read the evaluation report the last stage wrote and log every metric onto the same run:
```python
        with open(config["output"]["report_path"]) as f:
            metrics = json.load(f)
        for key, value in metrics.items():
            mlflow.log_metric(key, value)
```
Save the file.

##### 8. Re-run the pipeline.
```
cd /root/code/fraud-detection && python3 run_pipeline.py
wc -l data/processed/train_clean.csv data/features/features.csv
head -1 data/features/test_set.csv
```
The processed and features CSVs now report the same row count (both < 200), and the persisted `test_set.csv` header includes `amount_log` — confirming train consumed the feature matrix. The stage chain holds end to end.

##### 9. Verify the artefacts.
```
cat /root/code/fraud-detection/reports/evaluation.json
ls -l /root/code/fraud-detection/models/model.pkl
```
The JSON carries `accuracy`, `f1`, and `roc_auc` as numeric values. The pickled model exists.

##### 10. Verify in the MLflow UI.
Open the **MLflow UI** button → `training-pipeline` experiment. One run named `full-pipeline` is listed with `params.model_type`, `params.n_estimators`, and `params.max_depth`, plus `metrics.accuracy`, `metrics.f1`, and `metrics.roc_auc`. The **Artifacts** tab lists `model.pkl`.

#### References
- MLflow logging (`start_run` / `log_param` / `log_metric` — the orchestrator's end-to-end run): https://mlflow.org/docs/latest/python_api/mlflow.html
- scikit-learn — pipelines and chaining estimators (the stage-chain idea): https://scikit-learn.org/stable/modules/compose.html
- PyYAML — `yaml.safe_load` (how each stage reads its config paths): https://pyyaml.org/wiki/PyYAMLDocumentation
