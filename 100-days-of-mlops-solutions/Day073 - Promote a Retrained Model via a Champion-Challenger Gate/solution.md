# Task
The xFusionCorp Industries ML platform team operates a drift-triggered retraining pipeline. When data drift exceeds the alert threshold, the pipeline automatically retrains the fraud-detection model and registers it as a new version of fraud-detector. Currently, there is an incumbent version 1 serving production traffic under the production alias, along with a newly retrained challenger version 2, which has not yet been promoted. It is essential to avoid promoting the retrained model to production without evaluation, as this could result in a subpar model reaching users. Your task is to implement the promotion gate in promote.py, ensuring that the challenger is only promoted to production if it surpasses the incumbent's performance on the designated evaluation metric. After completing this task, proceed to execute the promotion.


The MLflow tracking server is on port 5000; the MLflow UI button opens it. Under Models → fraud-detector you can see version 1 (alias production, f1_score 0.71) and version 2 (no alias yet, f1_score 0.82).

The project is at /root/code/monitoring/:

retrain_pipeline.py – the startup setup that registered v1 and v2. Correct; do not edit.
promote.py – the promotion-gate scaffold. Its f1_of(version) helper (reads a version's logged f1_score) is wired; the gate logic is a # TODO naming the MLflow client calls to use.
The gate must read the version the production alias currently points at (the champion) and its f1_score, read the challenger's f1_score (version 2), and re-point production at the challenger only if the challenger's is strictly greater—otherwise leave the alias unchanged.

The end state must include:

The production alias on fraud-detector resolves to version 2 (the challenger).
The version now serving production has a higher f1_score than the incumbent v1 — the gate promoted the better model, not a blind version bump.
MLflow 3.x replaced stage-based promotion (Staging/Production) with aliases — named pointers like production that decouple a label from a version, so downstream code loads models:/fraud-detector@production and promotion is just re-pointing the alias. A champion/challenger gate is the guardrail: never re-point production at a retrained model without first confirming it actually beats what is live.
# Solution

When monitoring detects drift and triggers a retrain, the retrained model is a *candidate*, not automatically the new production model — promoting it blindly can ship a regression. The **champion/challenger** pattern is the guardrail: compare the challenger's evaluation metric against the version currently serving (the champion, reached via the `production` alias) and re-point the alias **only** if the challenger wins. This task authors that gate in `promote.py` against MLflow 3.x's alias API — read the incumbent through its alias, read the challenger, compare `f1_score`, and promote on a strict improvement.

> As an MLOps engineer, you gate model promotion on a metric comparison against the model that is actually live — a retrain that monitoring triggered still has to *earn* production by beating the incumbent, not just by being newer. The metrics here are synthetic.

#### Follow the steps below

##### 1. Confirm the starting state.
From a VS Code terminal:
```
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:5000/
curl -s 'http://localhost:5000/api/2.0/mlflow/registered-models/alias?name=fraud-detector&alias=production' \
  | python3 -m json.tool
```
MLflow returns `200`, and the `production` alias currently resolves to **version 1** (the incumbent). The retrain registered **version 2** (the challenger), which carries no alias yet. Optionally open the **MLflow UI** button → **Models → fraud-detector** to see both versions.

##### 2. Read the scaffold.
```
cd /root/code/monitoring
cat promote.py
```
`promote.py` already wires an `f1_of(version)` helper that returns a version's logged `f1_score`. The gate itself (`main()`) is a `# TODO`.
# Temperoly edit retrain_pipeline.py once model registered then remove skops_trusted_types=["sklearn.tree._tree.Tree"],
nano retrain_pipeline.py
Find:

registered_model_name=REGISTERED_MODEL,
Change it to:

registered_model_name=REGISTERED_MODEL,
skops_trusted_types=["sklearn.tree._tree.Tree"],
Then rerun the setup
python3 retrain_pipeline.py
This time it should get past the UntrustedTypesFoundException and register both candidates.

You should ultimately see:

Registered fraud-detector (incumbent, f1=0.71)
Registered fraud-detector (challenger, f1=0.82)
Set production -> v1 (incumbent). Challenger v2 awaits the promotion gate.

##### 3. Author the promotion gate.
Open `/root/code/monitoring/promote.py` in the VS Code editor and replace the `# TODO` / `raise SystemExit(...)` in `main()` with the champion/challenger comparison:
```python
def main() -> None:
    champion = client.get_model_version_by_alias(MODEL, PROD_ALIAS)
    champion_f1 = f1_of(champion.version)
    challenger_f1 = f1_of(CHALLENGER_VERSION)

    print(f"champion v{champion.version} f1={champion_f1:.2f}  |  "
          f"challenger v{CHALLENGER_VERSION} f1={challenger_f1:.2f}")

    if challenger_f1 > champion_f1:
        client.set_registered_model_alias(MODEL, PROD_ALIAS, CHALLENGER_VERSION)
        print(f"PROMOTED: production -> v{CHALLENGER_VERSION}")
    else:
        print(f"REJECTED: challenger did not beat the incumbent; "
              f"production stays at v{champion.version}")
```
Save. The gate reads the *live* champion via the alias (not a hardcoded version), so it keeps working after future promotions.

##### 4. Run the gate.
```
python3 promote.py
```
It prints `champion v1 f1=0.71 | challenger v2 f1=0.82` and then `PROMOTED: production -> v2` — the challenger clears the bar, so the `production` alias is re-pointed.

##### 5. Verify the promotion.
```
curl -s 'http://localhost:5000/api/2.0/mlflow/registered-models/alias?name=fraud-detector&alias=production' \
  | python3 -m json.tool
```
The `production` alias now resolves to **version 2**. Downstream consumers loading `models:/fraud-detector@production` pick up the challenger with zero redeploy — and only because it beat the incumbent, not merely because it was newer.

#### References

- MLflow Model Registry — aliases (the MLflow 3.x replacement for stages): https://mlflow.org/docs/latest/ml/model-registry/
- `MlflowClient` — `get_model_version_by_alias` / `set_registered_model_alias`: https://mlflow.org/docs/latest/api_reference/python_api/mlflow.client.html
- Loading a model by alias — `models:/fraud-detector@production`: https://mlflow.org/docs/latest/ml/model-registry/#fetching-a-model-version-by-alias
