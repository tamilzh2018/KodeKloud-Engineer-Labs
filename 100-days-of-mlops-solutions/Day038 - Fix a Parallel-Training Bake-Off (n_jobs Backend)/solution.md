# Task
The xFusionCorp Industries ML platform team is conducting a parallel-training bake-off for the fraud-detection model. The same estimator is to be trained twice: once on a single worker and once across all available CPUs. The MLflow Compare view will be utilized to highlight any differences in wall time. A draft script is located at /root/code/fraud-detection/src/models/train_parallel.py. Currently, executing this script yields nearly identical wall times for both the 'serial' and 'parallel' runs, resulting in the Compare view being unable to differentiate between the two configurations. Your task is to modify the script to ensure that the second run executes in genuine parallel mode. Additionally, each training run must log the actual number of workers utilized, and the observed parallelization speedup must be recorded.


The MLflow tracking server is already running on port 5000. The MLflow UI button at the top of the lab can be opened to confirm—the dashboard loads with an empty parallel-training experiment.

The project layout under /root/code/fraud-detection/:

data/train.csv – A 5000-row synthetic binary-classification dataset (imbalanced roughly 70 / 30). Larger than the 200-row dataset used earlier in the section because the n_jobs speedup is only visible once there is enough work per tree.
src/models/train_parallel.py – The bake-off script. Data loading, MLflow experiment setup, wall-time measurement, metrics.training_time_seconds logging, and model persistence to models/model.pkl are already wired; the corrections are confined to this file.
Run the script once against the scaffold as-is—python src/models/train_parallel.py—and note that both runs report near-identical wall times.

The end state must include:

At least two training runs exist in the parallel-training experiment, with params.n_jobs taking the values 1 and -1.
Each training run carries metrics.training_time_seconds, recorded for both the single-worker (n_jobs = 1) and all-cores (n_jobs = -1) configurations.
A speedup-summary run logs a speedup metric equal to the serial wall time divided by the parallel wall time. (The exact magnitude depends on the container's core count and load; on a 2-CPU box the all-cores run is typically faster.)
A pickled model at /root/code/fraud-detection/models/model.pkl.

# Solution

Many scikit-learn estimators parallelise across CPU cores via the **`n_jobs`** argument: `n_jobs=1` trains on a single worker, `n_jobs=-1` fans the work (here, fitting 200 independent trees) across **every** available core. A bake-off makes the benefit visible by training the *same* estimator both ways and comparing wall times in MLflow's Compare view — but only if each run actually uses the configured worker count *and* logs the value it used (logging a hardcoded label hides which run was which). The payoff is best expressed as a **speedup** — serial time ÷ parallel time — so the team can see *how many times faster* the parallel run was. This task makes the parallel run real, logs the true `n_jobs`, and records that speedup.

> As an MLOps engineer, you parallelize training across CPU cores and track the speedup in MLflow—you are not judging model quality. The data is synthetic and the metric values carry no meaning.

#### Follow the steps below

##### 1. Confirm the starting state.
Open the **MLflow UI** button at the top of the lab — the `parallel-training` experiment is present and empty. From a VS Code terminal:
```
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:5000/
wc -l /root/code/fraud-detection/data/train.csv
```
A `200` confirms MLflow is reachable. The training CSV is ~5000 rows — large enough that the parallel speedup is measurable.

##### 2. Run the draft script and observe the gap.
```
python3 /root/code/fraud-detection/src/models/train_parallel.py
```
Two runs are logged — one named `serial`, one named `parallel` — and their `training_time_seconds` values print to the terminal. The two wall times are near-identical, and opening the **MLflow UI** → `parallel-training` experiment shows both runs carrying `params.n_jobs = all`. The Compare view cannot tell the two configurations apart.

##### 3. Inspect `train_parallel.py`.
Open `/root/code/fraud-detection/src/models/train_parallel.py` in the VS Code editor. Two things need attention.

- `N_JOBS_VALUES = [1, 1]` — both entries are `1`, so both runs execute single-threaded. The second entry must be `-1` so the parallel run fans out across every CPU.
- `mlflow.log_param("n_jobs", "all")` inside the loop is hardcoded. The `n_jobs` variable is already in scope from the loop header; logging it directly is enough.

##### 4. Fix the `n_jobs` list.
Change the second entry to `-1`:
```python
N_JOBS_VALUES = [1, -1]
```

##### 5. Fix the `log_param` call.
Log the actual loop variable, not the hardcoded string:
```python
            mlflow.log_param("n_jobs", n_jobs)
```

##### 6. Log the parallelization speedup (TODO at the end of the script).
The loop already records each run's wall time into `times` (keyed by `n_jobs`). After the loop, open one more run and log the speedup — how many times faster the parallel run was:
```python
    with mlflow.start_run(run_name="speedup-summary"):
        mlflow.log_metric("speedup", times[1] / times[-1])
```
Save the file.

##### 7. Re-run the script.
```
python3 /root/code/fraud-detection/src/models/train_parallel.py
```
The printed `training_time_seconds` for the parallel run is now measurably lower than the serial run's.

##### 8. Verify in the MLflow UI.
Open the **MLflow UI** button → `parallel-training` experiment. Select the latest `serial` and `parallel` runs and click **Compare** — `params.n_jobs` reads `1` and `-1` respectively, and each run carries its own `training_time_seconds`. The all-cores run is typically faster (the exact gain depends on the container's core count and load), and the `speedup-summary` run's `speedup` metric quantifies serial ÷ parallel wall time.

#### References
- scikit-learn — parallelism and the `n_jobs` argument: https://scikit-learn.org/stable/computing/parallelism.html
- `RandomForestClassifier` (`n_jobs` over tree fitting): https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html
- MLflow logging (`start_run` / `log_param` / `log_metric`): https://mlflow.org/docs/latest/python_api/mlflow.html
