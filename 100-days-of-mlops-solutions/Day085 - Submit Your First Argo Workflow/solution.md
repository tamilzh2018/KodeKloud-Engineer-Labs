# Task
The xFusionCorp Industries ML platform team has established a new Kubernetes cluster for pipeline orchestration. Argo Workflows v4.0.4 is currently operational in the argo namespace, with both the workflow-controller and argo-server Deployments marked as Available. Additionally, the Argo web UI is accessible via port-forwarding in the lab. Your task is to create your first Argo Workflow and submit it using the Argo UI's + Submit New Workflow form. This should be a single-step container that simulates a training step and achieves a status of Succeeded in the Workflows list.


The Argo UI button at the top of the lab opens the Workflows page on port 5000. The UI has no auth (quick-start install) and the Workflows list is empty on first open; new workflows are authored through its + Submit New Workflow form, whose in-browser YAML editor is the canonical authoring surface for this section.

The workflow to author is a kind: Workflow in namespace argo that declares a spec.entrypoint pointing at a template under spec.templates. That template runs a single container whose command/args stand in for a training step — an echo is fine, since this section teaches orchestration, not model quality. Once submitted, the single node should progress Pending → Running → Succeeded.

The end state must include:

GET http://localhost:5000/ returns 200 (Argo UI reachable).
workflow-controller and argo-server Deployments in namespace argo are Available.
At least one Workflow exists in namespace argo, and the most recent one is genuinely authored: it declares spec.entrypoint and a template whose container runs a command/args.
That most recent workflow reaches status.phase == Succeeded (tests wait up to 180 s for a terminal phase).
Argo's + Submit New Workflow flow is how every future lab in this section starts. The UI's YAML editor is the canonical authoring surface—not kubectl apply -f file.yaml from a terminal. Authoring the Workflow spec by hand here—entrypoint, templates, container—is the foundation every WorkflowTemplate, CronWorkflow, and parameterised pipeline in the coming labs builds on.

# Solution

Argo Workflows is a Kubernetes-native engine that runs each pipeline as a `Workflow` object — a graph of container steps the controller schedules, retries, and reports on. This task authors your first `Workflow` and submits it through the Argo UI's **+ Submit New Workflow** editor, watching a single stand-in training step run to `Succeeded`.

> As an MLOps engineer, you author a `Workflow` spec — `entrypoint`, `templates`, `container` — so a training step runs as an observable, retryable Kubernetes object; you are not tuning the model, the step is a synthetic `echo` stand-in.

#### Follow the steps below

##### 1. Confirm the starting state.
From a VS Code terminal:
```
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:5000/
kubectl -n argo get deploy
```
The Argo UI answers `200`. Both `workflow-controller` and `argo-server` deployments show `AVAILABLE 1/1`.

##### 2. Open the Argo UI.
Click the **Argo UI** button at the top of the lab. The **Workflows** page loads with an empty list.

##### 3. Author and submit your first Workflow.
- Click **+ Submit New Workflow** (top-right).
- The in-browser YAML editor opens with a default template that references an image the cluster's containerd no longer pulls. Replace the editor contents with a Workflow you author — a single container step on a current image running a stand-in training step:
  ```yaml
  apiVersion: argoproj.io/v1alpha1
  kind: Workflow
  metadata:
    generateName: train-hello-
    namespace: argo
  spec:
    entrypoint: train
    templates:
      - name: train
        container:
          image: alpine:3.20
          command: [echo]
          args: ["fraud-detector: training step complete"]
  ```
  The pieces to understand: `entrypoint` names which template runs first; `templates` is the list of steps; each `container` is a pod spec. `generateName` lets you submit repeatedly without name clashes.
- Click **+ Create**.

The UI navigates to the new workflow's detail page. One node on the DAG moves `Pending` → `Running` → `Succeeded` (green tick) in about 10 seconds.

##### 4. Inspect the pod log.
Click the green node. The right-hand drawer opens; click **Logs** → the `train` container prints:
```
fraud-detector: training step complete
```

##### 5. Verify via the API.
From a VS Code terminal:
```
curl -s http://localhost:5000/api/v1/workflows/argo \
  | python3 -c "
import json, sys
body = json.load(sys.stdin)
for w in body.get('items', []):
    meta = w.get('metadata', {})
    st = w.get('status', {}) or {}
    print(f\"{meta.get('name'):40s}  phase={st.get('phase')}\")
"
```
The output lists the new workflow with `phase=Succeeded`.

#### References

- Argo Workflows — core concepts (`Workflow`, `entrypoint`, `templates`, `container`): https://argo-workflows.readthedocs.io/en/latest/workflow-concepts/
- Argo Workflows — hello-world walk-through: https://argo-workflows.readthedocs.io/en/latest/walk-through/hello-world/
