# Task:
The xFusionCorp Industries ML platform team requires the fraud-detector model to undergo retraining on a fixed schedule without manual intervention. A CronWorkflow scaffold is available at /root/code/argo/fraud-retraining.yaml, but it is incomplete; it currently lacks a schedules cron expression and the retraining step is only a placeholder. Your objective is to complete the CronWorkflow by adding the appropriate schedule and defining the retraining step. Once completed, apply the CronWorkflow to the argo namespace and verify in the Argo UI that it activates and initiates retraining runs as scheduled.


The scaffold is at /root/code/argo/fraud-retraining.yaml. It is NOT applied yet — the Argo UI's Cron Workflows page (port 5000) stays empty until the CronWorkflow is applied to the argo namespace.

Two TODO-marked pieces are missing from the YAML:

TODO 1 — schedule: the schedules: list with its cron expression is absent, so the cron has no cadence to fire on. It needs to fire frequently enough that a run appears within the grading window (a minute or so).
TODO 2 — retraining step: the step is only a stub. It should run a stand-in retraining command that exits 0 — an echo is enough, since this section teaches orchestration, not model quality.
With the CronWorkflow applied, the Cron Workflows page should show fraud-retraining active (no Suspended badge) with a nextScheduledTime ≤ 60 s out, and within one schedule tick a child Workflow should appear under it and run to Succeeded.

The end state must include:

GET /api/v1/cron-workflows/argo/fraud-retraining returns the cron with a non-empty schedules and spec.suspend not true.
At least one Workflow labelled workflows.argoproj.io/cron-workflow=fraud-retraining (the owner-label Argo adds to every cron-spawned run) reaches Succeeded. Tests poll up to 240 s.
A CronWorkflow is Argo's scheduled-run primitive: schedules is the cron cadence and workflowSpec is the Workflow it fires each tick. This is how retraining runs on autopilot—no human clicking Submit—with concurrencyPolicy: Forbid ensuring a slow run never overlaps the next tick.
# Solution

A `CronWorkflow` is Argo's scheduled-run primitive: `schedules` sets the cron cadence and `workflowSpec` is the `Workflow` it fires each tick, so retraining runs on autopilot. This task finishes a `fraud-retraining` CronWorkflow — adding the schedule and the retraining step — applies it, and confirms it spawns child runs on schedule.

> As an MLOps engineer, you schedule retraining to run on a cadence without anyone clicking Submit — the model logic is incidental; the retraining step is a synthetic stand-in.

#### Follow the steps below

##### 1. Read the scaffolded cron.
The startup staged an incomplete CronWorkflow on disk and did **not** apply it — the Argo UI's **Cron Workflows** page is empty. Open it in VS Code:
```
sed -n '1,40p' /root/code/argo/fraud-retraining.yaml
```
Two pieces are missing: `spec.schedules` (TODO 1) and the retraining container's `args` (TODO 2, a stub that `exit 1`s).

##### 2. Author TODO 1 — the schedule.
Add a `schedules:` list under `spec:` with a cron expression firing every minute (it sits alongside the `timezone` the scaffold already ships):
```yaml
spec:
  schedules:
    - "* * * * *"
  timezone: "Etc/UTC"
  ...
```
`schedules` is the CronWorkflow's cadence — the controller creates one Workflow per matching tick.

##### 3. Author TODO 2 — the retraining step.
Replace the stub `args` with a real (synthetic) retraining step:
```yaml
          args:
            - |
              echo "[retrain] $(date -u +%FT%TZ) refitting fraud-detector"
              sleep 2
              echo "[retrain] done"
```
Save.

##### 4. Apply the CronWorkflow.
```
kubectl apply -n argo -f /root/code/argo/fraud-retraining.yaml
```
Open the **Argo UI** → **Cron Workflows**. `fraud-retraining` now appears — active (no Suspended badge) with a `nextScheduledTime`. Within one tick, its **Workflows** panel shows a `fraud-retraining-<timestamp>` run going green.

##### 5. Verify via the REST API.
From a VS Code terminal:
```
# Cron is resumed:
curl -s http://localhost:5000/api/v1/cron-workflows/argo/fraud-retraining \
  | python3 -c "
import json, sys
b = json.load(sys.stdin)
print('suspend:', b.get('spec', {}).get('suspend'))
print('lastScheduledTime:', (b.get('status') or {}).get('lastScheduledTime'))
"

# Child Workflow(s) from this cron (using the owner-label):
curl -s 'http://localhost:5000/api/v1/workflows/argo?listOptions.labelSelector=workflows.argoproj.io%2Fcron-workflow%3Dfraud-retraining' \
  | python3 -c "
import json, sys
b = json.load(sys.stdin)
for w in b.get('items', []):
    print(w['metadata']['name'], (w.get('status') or {}).get('phase'))
"
```
The first call shows `suspend: None` (or `False`) and a non-empty `lastScheduledTime`. The second lists at least one child workflow spawned by the cron, reaching `Succeeded`.

#### References

- Argo Workflows — CronWorkflows (`schedules`, `concurrencyPolicy`, `workflowSpec`): https://argo-workflows.readthedocs.io/en/latest/cron-workflows/
