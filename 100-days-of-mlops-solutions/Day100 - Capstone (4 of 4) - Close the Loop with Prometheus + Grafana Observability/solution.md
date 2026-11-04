# Task
The xFusionCorp Industries MLOps team is closing the loop on the fraud-detector with a single observability pane: oncall needs to see request rate and latency at a glance, and be alerted when the service misbehaves. The service is already instrumented, Prometheus is already scraping it, and synthetic traffic is being generated in the background. Grafana was provisioned empty — no data source, no dashboards, no alerts. Your task is to wire Grafana to Prometheus, author a multi-panel fraud-monitor dashboard, and add an alert rule on the service.


The Grafana (port 3000, log in with admin / admin) and Prometheus (port 9090) buttons at the top of the lab open the relevant UIs. The pre-staged state:

The FastAPI app on :8085 exposes Prometheus metrics at /metrics: http_requests_total (request counter) and http_request_duration_seconds (latency histogram).
Prometheus on :9090 scrapes the app every 5 s as job fraud-detector.
A background traffic generator hits /predict and /health continuously, so non-zero samples are already flowing.
Grafana on :3000 has no data source, no dashboards, and no alert rules. It reaches Prometheus at http://prometheus:9090.
The end state must include:

Grafana has a data source of type prometheus pointed at http://prometheus:9090.
Grafana has a dashboard named fraud-monitor with at least two panels — one querying http_requests_total, one querying http_request_duration_seconds.
Grafana has at least one alert rule whose query references a service metric.
The Compose stack lives under /root/code/observability/ (app/, compose.yaml, prometheus.yml, scripts/) for transparency; nothing under that directory needs to be edited. Observability is two halves — a dashboard answers 'what is happening?' and an alert answers 'when should a human care?'.
# Solution

**The platform.** xFusionCorp runs `fraud-detector` as a small production ML system: models are trained and served behind the `production` registry alias, an automated loop retrains on drift, the server is deployed by GitOps, and the running service is observed with Prometheus + Grafana. **This task builds the observability pane** — the part that makes the running service visible and pageable.

You compose a single pane over an already-instrumented service: Prometheus scrapes the metrics, and you wire Grafana to it, author a multi-panel `fraud-monitor` dashboard, and add an alert rule. Observability is two halves — a dashboard answers 'what is happening?' and an alert answers 'when should a human care?' — and you build both.

> As an MLOps engineer, you turn raw request and latency metrics into a dashboard and an alert so oncall can see and be paged on service health — you are not measuring model accuracy; the traffic and metrics are synthetic.

#### Follow the steps below

##### 1. Confirm the stack is up.
From a VS Code terminal:
```
docker compose -f /root/code/observability/compose.yaml ps
curl -s -o /dev/null -w 'app=%{http_code}\n' http://localhost:8085/metrics
curl -s -o /dev/null -w 'prom=%{http_code}\n' http://localhost:9090/-/healthy
curl -s -o /dev/null -w 'grafana=%{http_code}\n' http://localhost:3000/login
```
All three containers (`fraud-app`, `prometheus`, `grafana`) report `Up`. All three curls return `200`. A background traffic generator is hitting `/predict` + `/health` continuously, so Prometheus already has non-zero samples on `http_requests_total`.

##### 2. Confirm Prometheus is scraping the app.
Click the **Prometheus** button at the top of the lab. Open **Status → Target health**. The `fraud-detector` target shows **State: UP** with a recent last-scrape time. From **Graph**, query `http_requests_total` and confirm the result table lists samples per HTTP method/handler.

##### 3. Add the Prometheus data source in Grafana.
Click the **Grafana** button. Log in with `admin` / `admin` (skip the password change prompt).

From the left sidebar, open **Connections → Data sources**. Click **+ Add new data source** (top right) and choose **Prometheus**.

Fill the form:
- **Name:** leave as `prometheus` (the default).
- **Prometheus server URL:** `http://prometheus:9090`. (This is the Docker Compose service hostname — Grafana reaches Prometheus over the compose network.)
- Scroll to the bottom, click **Save & test**. A green banner confirms `Successfully queried the Prometheus API`.

##### 4. Create the `fraud-monitor` dashboard with a request-rate panel.
From the left sidebar, open **Dashboards**, then click **New → New dashboard** (top right) and **Add visualization** on the empty canvas. Select the Prometheus data source just added.

In the visualization editor:
- **Query A → expression:** `sum(rate(http_requests_total[1m]))`.
- **Panel title** (right-hand options): `Request rate`.
- The preview renders a non-flat line immediately (the background traffic generator is producing samples). Click **Apply**.

##### 5. Add a second panel for latency.
Back on the dashboard, click **Add → Visualization** (top toolbar). In the editor:
- **Query A → expression:** `histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))`.
- **Panel title:** `p95 latency`.
- Click **Apply**.

Click **Save dashboard** (top-right) → **Dashboard name:** `fraud-monitor` → **Save**. The dashboard now shows two signals: request rate and p95 latency.

##### 6. Add an alert rule on the service.
From the left sidebar, open **Alerting → Alert rules**, then click **New alert rule** (top right).
- **1. Name:** `fraud-detector-traffic`.
- **2. Define query and alert condition:** pick the `prometheus` data source and enter **Query A:** `sum(rate(http_requests_total[1m]))`. Under **Alert condition**, leave `WHEN QUERY [A]`, set the operator to `IS BELOW` and the value to `0.01` (fires if the endpoint stops receiving traffic). Click **Preview alert rule condition** to confirm it evaluates. (This simplified condition folds the old Reduce + Threshold expressions into one row; toggle **Advanced options** only if you want the separate expression steps.)
- **3. Add folder and labels:** create or select a folder (e.g. `fraud`).
- **Set evaluation behavior:** create/select an evaluation group (e.g. `fraud`, every `1m`).
- Click **Save rule and exit**. Grafana's default notification policy handles routing; no contact-point setup is required for the rule to exist and evaluate.

##### 7. Verify from the terminal.
```
curl -s http://localhost:3000/api/datasources -u admin:admin \
  | python3 -c "import json,sys; print('datasources:', [(d['type'], d['url']) for d in json.load(sys.stdin)])"

curl -s 'http://localhost:3000/api/search?query=fraud-monitor&type=dash-db' -u admin:admin \
  | python3 -c "import json,sys; print('dashboards:', [h['title'] for h in json.load(sys.stdin)])"

curl -s http://localhost:3000/api/v1/provisioning/alert-rules -u admin:admin \
  | python3 -c "import json,sys; r=json.load(sys.stdin); print('alert rules:', [x.get('title') for x in r])"
```
The output shows a `prometheus` data source at `http://prometheus:9090`, a `fraud-monitor` dashboard, and at least one alert rule.

#### References

- Grafana — add a Prometheus data source: https://grafana.com/docs/grafana/latest/datasources/prometheus/
- Grafana — create a dashboard and add panels: https://grafana.com/docs/grafana/latest/dashboards/build-dashboards/
- Grafana — create a Grafana-managed alert rule: https://grafana.com/docs/grafana/latest/alerting/alerting-rules/create-grafana-managed-rule/
