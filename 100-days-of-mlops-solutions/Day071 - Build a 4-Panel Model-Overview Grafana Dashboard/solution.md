# Task
The xFusionCorp Industries ML platform team requires the enforcement of quality gates for the fraud-detection model in two key ways: first, by establishing an Evidently test suite that can be executed by any CI job against a production batch, and second, by integrating this suite with Grafana to ensure that on-call personnel are notified immediately if live accuracy declines. The monitoring stack is operational, and the test-suite scaffold is already established, including data loading, classification mapping, report execution, and publication to the Evidently UI.

Your task consists of two parts: (1) Complete the TODO block of the scaffold with the two specified threshold metrics, execute the test suite, and examine the results in the Evidently UI; (2) Create a Grafana alert rule that triggers when avg_over_time(prediction_accuracy[1m]) falls below 0.80.


Evidently test suite. /root/code/monitoring/tests/test_suite.py is pre-wired except for the gates themselves; a TODO block marks where two thresholded metrics must be appended to METRICS:

a missing-values gate that fails the suite when the batch carries 10 or more missing values.

an accuracy gate that fails the suite when batch accuracy is 0.80 or lower.

The batch it runs against is /root/code/monitoring/tests/current.csv (features + is_fraud target + the model's prediction column). The batch carries only a few missing values and its accuracy clears 0.80, so both gates should end up SUCCESS. A successful run writes test_results.json and publishes a snapshot to the Evidently workspace, viewable under the Evidently UI button (port 8000) in the fraud-detector quality gates project (Reports tab).

Grafana alert rule. The Grafana UI is running on port 3000. The Grafana button opens the login page. Admin credentials: admin / grafana2026. The Prometheus datasource is pre-provisioned. Metrics available:

prediction_accuracy – The gauge for this task. It drifts in a random walk around 0.85, so avg_over_time(prediction_accuracy[1m]) is the smoothed signal the alert should watch.
data_drift_score{column}, evidently_drift_share – Per-feature PSI and the drifted-columns share, computed by the Evidently drift scorer at /root/code/monitoring/drift/drift_scorer.py.
flask_http_request_total{version, endpoint, method}, model_inference_duration_seconds – The other signals from the shared metric-emitter.
The alert rule must fire when avg_over_time(prediction_accuracy[1m]) drops below 0.80.

The end state must include:

/root/code/monitoring/tests/test_results.json exists and carries at least two Evidently test entries—a missing-values gate and an accuracy gate—all with status SUCCESS.
The Evidently UI's project carries at least one published run (snapshot).
GET /api/v1/provisioning/alert-rules returns a non-empty array.
At least one rule's PromQL expression references prediction_accuracy.
That rule's threshold evaluator carries 0.80 as a numeric parameter.
The same 0.80 accuracy gate is enforced at two altitudes: the Evidently test suite fails a CI pipeline before a degraded model ships, and the Grafana alert rule pages on-call after live accuracy slips. Evidently's include_tests=True turns each metric into a pass/fail assertion—the same structure a pytest run gives you, but over data and model quality—and the Evidently UI is where a reviewer reads those verdicts without touching code.

# Solution

Individual panels answer one question each; an on-call engineer needs the whole model's health on one screen. This task composes a single **model-overview** dashboard from four panels spanning three visualization types (time-series, stat, bar gauge), pulling the serving and drift signals together so one glance tells you whether the model is healthy. The skill is dashboard composition and choosing the right visualization per signal.

> As an MLOps engineer, you build the one board the team opens during an incident — consolidating the signals that matter so triage is fast — you are not judging the model; the metrics are synthetic.

#### Follow the steps below

##### 1. Confirm the starting state.
From a VS Code terminal:
```
docker ps --format '{{.Names}}\t{{.Status}}'
curl -s -u admin:grafana2026 http://localhost:3000/api/datasources | python3 -m json.tool
curl -s 'http://localhost:9090/api/v1/query?query=data_drift_score' | python3 -m json.tool | head -30
cat /root/code/monitoring/drift/drift_scores.json
```
All three containers are running. The Prometheus datasource is pre-provisioned. The `data_drift_score` series carry one value per feature column — these are the PSI scores the **Evidently drift scorer** (`/root/code/monitoring/drift/drift_scorer.py`) recomputes every 15 seconds; `drift_scores.json` is the hand-off file the metric-emitter republishes from. Every ~minute the scorer also publishes a run to the Evidently workspace behind the **Evidently UI** button.

#
cd /root/code/monitoring
sed -n '1,240p' tests/test_suite.py
grep -nE 'METRICS|TODO|Test|Metric|missing|accuracy' tests/test_suite.py

If the scaffold is using Evidently's current test API, the intended gates are conceptually:
# Missing-values gate: fail when missing values >= 10
# Accuracy gate: fail when accuracy <= 0.80
your scaffold already tells you exactly what to add. The TODO block should become:

```
METRICS = [
    DatasetMissingValueCount(tests=[lt(10)]),
    Accuracy(tests=[gt(0.80)]),
]
```

 So your complete relevant section is:

```
# ----------------------------------------------------------------------
# TODO 1: Gate data quality -- fail the suite when the batch carries
#         10 or more missing values.
#
#         METRICS.append(DatasetMissingValueCount(tests=[lt(10)]))
#
# TODO 2: Gate model quality -- fail the suite when batch accuracy
#         is 0.80 or lower. Use `Accuracy` with `tests=[gt(0.80)]`,
#         appended the same way.
# ----------------------------------------------------------------------
METRICS = [
    DatasetMissingValueCount(tests=[lt(10)]),
    Accuracy(tests=[gt(0.80)]),
]
```

 ### Then execute it

 Save the file and run:

```
python3 /root/code/monitoring/tests/test_suite.py
```

 You should get output similar to:

```
Tests: 2/2 passed -> /root/code/monitoring/tests/test_results.json
  - DatasetMissingValueCount: SUCCESS
  - Accuracy: SUCCESS
Run published -- refresh the Evidently UI to inspect it.
```

 ### Verify the JSON

 Run:

```
python3 -m json.tool /root/code/monitoring/tests/test_results.json
```

 You should see two test entries with:

```
"status": "SUCCESS"
```

 ### Verify the Evidently UI

 Open the Evidently UI on port **8000**, then:

 1. Open **fraud-detector quality gates**.
2. Go to **Reports**.
3. Open the newly published run.
4. Confirm both:
   - `DatasetMissingValueCount` → **SUCCESS**
   - `Accuracy` → **SUCCESS**

 The important detail is that `lt(10)` means the suite passes only when missing values are **strictly below 10**, so 10 or more fails. Likewise, `gt(0.80)` means accuracy must be **strictly above 0.80**, so 0.80 or lower fails.

 After this, you can proceed to the Grafana rule using:

```
avg_over_time(prediction_accuracy[1m])
```

 with the condition **IS BELOW 0.80**.
##### 2. Log in to Grafana.
Click the **Grafana** button at the top of the lab. Enter:
- **Username:** `admin`
- **Password:** `grafana2026`
 ## 3. Create the Grafana alert rule

 In Grafana:

 1. Go to **Alerting**.
2. Select **Alert rules**.
3. Click **New alert rule**.
4. Give it a name such as:

```
Fraud detector prediction accuracy below 0.80
```

 5. Select the existing **Prometheus** datasource.
6. Use this PromQL query:

```
avg_over_time(prediction_accuracy[1m])
```

 7. Configure the alert condition so it fires when the query result is:

```
< 0.80
```

 The resulting rule should therefore represent:

```
avg_over_time(prediction_accuracy[1m]) < 0.80
```

 Don't accidentally use `<=` here: your requested Grafana condition is specifically **below** `0.80`.

---

 ## 4. Save the rule

 Click **Save rule and exit**.

 You should now see the rule under:

 **Alerting → Alert rules**

 Make sure its state/configuration shows the threshold of `0.80`.

---

 ## 5. Verify Grafana through its API

 From the monitoring host, run:

```
curl -u admin:grafana2026 \
  http://localhost:3000/api/v1/provisioning/alert-rules
```

 The response must be a non-empty JSON array.

 For easier inspection:

```
curl -s -u admin:grafana2026 \
  http://localhost:3000/api/v1/provisioning/alert-rules | python -m json.tool
```

 Search for the PromQL expression:

```
curl -s -u admin:grafana2026 \
  http://localhost:3000/api/v1/provisioning/alert-rules \
  | grep -i -C 3 'prediction_accuracy'
```

 You should find:

```
avg_over_time(prediction_accuracy[1m])
```

 and the rule's threshold/evaluator should contain the numeric value:

```
0.8
```

---

 ## 6. Final end-state checks

 Run these checks:

```
cd /root/code/monitoring

test -f tests/test_results.json && echo "PASS: test_results.json"

grep -q 'prediction_accuracy' <(curl -s -u admin:grafana2026 \
  http://localhost:3000/api/v1/provisioning/alert-rules) \
  && echo "PASS: Grafana rule references prediction_accuracy"
```

 Then inspect the Evidently JSON manually:

```
python -m json.tool tests/test_results.json
```

 You want the final state to be:

```
Evidently:
  missing-values gate  -> SUCCESS
  accuracy gate        -> SUCCESS
  published snapshot   -> YES

Grafana:
  alert rule           -> EXISTS
  PromQL               -> avg_over_time(prediction_accuracy[1m])
  threshold            -> 0.80
```

 The two layers intentionally use slightly different semantics: **Evidently blocks a bad batch at CI time when accuracy is ≤ 0.80**, while **Grafana alerts on live degradation when the smoothed one-minute accuracy drops below 0.80**.


##### 7. Open a new dashboard.
From the left navigation:
- Click **Dashboards** (four-squares icon).
- Click **New -> New dashboard** (top right).

##### 8. Panel 1 — Request rate (Time series).
- Click **Add visualization** on the empty canvas.
- Select **Prometheus** when Grafana asks which data source to use.
- In the **Code** tab, enter:
  ```
  sum(rate(flask_http_request_total[1m])) by (version)
  ```
- Click **Run queries**. Grafana plots a line per model version.
  What you'll see
  Prometheus will return one time series for each version, for example:

  version="v1"    4.2
  version="v2"    3.7
- Leave the **Visualization** as **Time series**.
- Right sidebar -> **Title:** `Request rate`.
- Click **Back to dashboard** (top left).

##### 9. Panel 2 — p95 inference latency (Time series).
- Click **Add -> Visualization**.
- Data source: **Prometheus**.
- **Code** tab:
  ```
  histogram_quantile(0.95, sum(rate(model_inference_duration_seconds_bucket[5m])) by (le))
  ```
- **Run queries**. The p95 line appears.
- Visualization: **Time series**.
- **Title:** `p95 inference latency (s)`.
- **Back to dashboard**.

##### 10. Panel 3 — Prediction accuracy (Stat).
- **Add -> Visualization**.
- Data source: **Prometheus**.
- **Code** tab:
  ```
  prediction_accuracy
  ```
- **Run queries**.
- On the right sidebar, change the **Visualization** from **Time series** to **Stat** — the panel collapses into a single-number readout.
- **Title:** `Prediction accuracy`.
- **Back to dashboard**.

##### 11. Panel 4 — Drift by column (Bar gauge).
- **Add -> Visualization**.
- Data source: **Prometheus**.
- **Code** tab:
  ```
  data_drift_score
  ```
- **Run queries** — three series appear, one per `column` label. Each value is the PSI Evidently computed for that feature against the reference window, so the bars move as the simulated production feed drifts.
- On the right sidebar, change the **Visualization** to **Bar gauge**. One horizontal bar per feature column renders.
- **Title:** `Drift by column`.
- **Back to dashboard**.

##### 12. Save the dashboard.
- Click the **Save dashboard** icon (disk, top-right).
- **Dashboard title:** `Model overview`.
- Click **Save**.

##### 13. Cross-check in the Evidently UI.
Click the **Evidently UI** button at the top of the lab (port `8000`):
- Click the `fraud-detector drift monitoring` project.
- The **Dashboard** tab (default) renders two pre-configured line charts — **Share of drifted columns** and **Per-column drift (PSI)** — one point per scoring run, accumulating every ~minute. This is Evidently's own monitoring dashboard over the exact same data your Grafana bar gauge shows live.
- The **Reports** tab lists the underlying runs; **View** any row → one card per feature renders, headed e.g. `Drift in column 'amount' — Data drift detected. Drift detection method: PSI. Drift score: 1.726`. Each card has two tabs: **Data Drift** (current mean ± std against the reference band) and **Data Distribution** (current-vs-reference histogram) — the raw evidence behind your Grafana bars.

##### 14. Verify via Grafana's API.
From a VS Code terminal:
```
DASH_UID=$(curl -s -u admin:grafana2026 'http://localhost:3000/api/search?type=dash-db' \
  | python3 -c "import json, sys; print(json.load(sys.stdin)[0]['uid'])")
curl -s -u admin:grafana2026 http://localhost:3000/api/dashboards/uid/$DASH_UID \
  | python3 -c "
import json, sys
d = json.load(sys.stdin)['dashboard']
for p in d['panels']:
    expr = (p['targets'][0].get('expr') if p.get('targets') else '-')
    print(f\"{p['type']:12s} | {p['title']:30s} | {expr}\")
"
```
The output lists four rows — one per panel — with distinct `type` values (at least three of `timeseries` / `stat` / `bargauge` / `gauge`) and the four metric names in the `expr` column.

#### References

- Grafana — build a dashboard and add panels: https://grafana.com/docs/grafana/latest/dashboards/build-dashboards/
- Grafana visualizations (Stat, Bar gauge, Time series): https://grafana.com/docs/grafana/latest/panels-visualizations/visualizations/
- PromQL `histogram_quantile` — the p95 latency panel: https://prometheus.io/docs/prometheus/latest/querying/functions/#histogram_quantile
