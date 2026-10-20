#Task
The xFusionCorp Industries ML platform team has submitted an initial training workflow to Argo — a three-step Directed Acyclic Graph (DAG), data-prep → train → evaluate, whose steps share a workspace volume. This workflow is triggered on every push; however, the current execution is marked red because one of the steps races ahead of its upstream dependency. Your task is to review the broken DAG displayed in the Argo UI, submit a corrected workflow using the YAML editor in the UI, and observe the new execution transition to a successful green Succeeded status.


The Argo UI button at the top of the lab opens the Workflows page on port 5000. The Workflows list holds the pre-submitted run (training-pipeline-<suffix>) in a Failed state. Open that run and click the red node to read its logs and the DAG graph — that is where the failure surfaces.

The workflow is a dag template of three tasks that each run in their own pod and share a workspace volume; the three tasks do not run in the order the pipeline needs. The same spec is staged at /root/code/pipelines/training-workflow.yaml.

After the corrected workflow is submitted through the UI's YAML editor, the DAG should run data-prep → train → evaluate in order, all three nodes turning green with the workflow phase Succeeded.

The end state must include:

At least two workflows in namespace argo (the original broken run plus the fixed resubmit).
The corrected workflow's main DAG gives the evaluate task dependencies: [train], so the three steps run in order rather than in parallel.
The most recent workflow's status.phase == Succeeded (tests wait up to 240 s).
An Argo dag template starts each task the moment its dependencies are satisfied, and a task with no dependencies runs immediately. Declaring the right dependencies is what turns independently-scheduled pods into an ordered pipeline — without them, a task races its inputs, which is a classic cause of a red DAG run.

# Solution

An Argo `dag` template runs each task in its own pod and starts a task as soon as its `dependencies` are satisfied — so a task with no dependencies runs immediately. This task diagnoses a failed `data-prep → train → evaluate` DAG whose `evaluate` task has no dependency on `train`, so it starts in parallel and fails before the model exists, then resubmits a corrected spec so the three steps run as an ordered chain. The tasks share a workflow volume so the model file passes down the chain.

> As an MLOps engineer, you make the ordering contract between pipeline steps explicit so a downstream step never runs before its inputs exist — you are not tuning the model; the steps run synthetic stand-ins.

#### Follow the steps below

##### 1. Inspect the red run and read the failing step's log.
Click the **Argo UI** button at the top of the lab. The Workflows list shows `training-pipeline-<suffix>` in state **Failed**. Click it.

On the graph, `data-prep` and `train` are green; `evaluate` is red. Click the red `evaluate` node, then **LOGS** — the log (container `main`) shows exactly why it failed:
```
[evaluate] checking model
[evaluate] ERROR: model.pkl not found
```
`evaluate` ran before `train` produced `/workdir/model.pkl`.

##### 2. Confirm the cause in the spec.
The pipeline is staged on disk at `/root/code/pipelines/training-workflow.yaml` (it is the same spec that was submitted). Open it in the VS Code editor and look at the `main` template's `dag.tasks`:
- `data-prep` — no dependencies, runs first.
- `train` — `dependencies: [data-prep]`.
- `evaluate` — **no `dependencies:` field**. That is the bug: the DAG starts it immediately, in parallel with `data-prep` and `train`.

##### 3. Add the missing dependency.
Give the `evaluate` task the ordering contract it is missing — add a `dependencies: [train]` line so it waits for `train` to finish (the same mechanism `train` uses to run after `data-prep`):
```yaml
          - name: evaluate
            template: evaluate
            dependencies: [train]
```
Save.

##### 4. Submit the corrected workflow via the Argo UI.
From the Workflows list, click **+ Submit New Workflow** (top-right). The in-browser YAML editor opens with a default template — replace its contents with the fixed `/root/code/pipelines/training-workflow.yaml` (copy from VS Code, paste into the editor). Click **+ Create**.

##### 5. Watch the fixed DAG complete.
The UI opens the new workflow's detail page. The DAG now runs `data-prep → train → evaluate` in order; each node turns green in turn. Final phase: `Succeeded`.

##### 6. Verify via the API.
From a VS Code terminal:
```
curl -s http://localhost:5000/api/v1/workflows/argo \
  | python3 -c "
import json, sys
body = json.load(sys.stdin)
for w in sorted(body.get('items', []),
                key=lambda x: x['metadata']['creationTimestamp']):
    phase = (w.get('status') or {}).get('phase')
    name = w['metadata']['name']
    print(f'{name:40s}  phase={phase}')
"
```
The output lists two workflows: the original `Failed` and the new `Succeeded`.

#### References

- Argo Workflows — DAG template and task `dependencies`: https://argo-workflows.readthedocs.io/en/latest/walk-through/dag/
- Argo Workflows — sharing data between steps with `volumeClaimTemplates`: https://argo-workflows.readthedocs.io/en/latest/walk-through/volumes/
