# Task
The xFusionCorp Industries ML platform team requires a reusable training pipeline that promotes a model to the registry only when it passes a configurable quality gate. This pipeline should utilize the same WorkflowTemplate with differing min_score values for each run. Currently, a train-and-maybe-register WorkflowTemplate is available on disk; however, it is not yet functional. The evaluate step computes a synthetic score of 0.75 but does not publish it, and the register step lacks a quality gate, causing it to execute unconditionally. Your task is to complete the template by publishing the score as an output parameter and implementing a when: expression to gate the register step, ensuring that it compares the score to min_score. Once you have applied these changes, submit the workflow twice from the Argo UI to demonstrate the functionality of the gate: first with a threshold that prevents register from executing, and then with a threshold that allows it to execute.


The scaffolded template is at /root/code/argo/train-and-maybe-register.yaml. It is NOT applied yet — the Argo UI's Workflow Templates list (port 5000) stays empty until the template is applied to the argo namespace as a cluster resource.

Two TODO-marked pieces are missing from the YAML:

TODO 1 — evaluate template: the script writes a synthetic score to /tmp/score.txt, but the template does not yet expose that value to the rest of the workflow as an output parameter.
TODO 2 — register step in main: the register step currently runs unconditionally, rather than only when the score clears the min_score threshold.
With the template applied and appearing in the UI, submitting it twice demonstrates the gate: a run with min_score above the evaluate score (e.g. 0.99) reaches Succeeded with the register node Skipped (the when: evaluated false), while a run with min_score below the score (e.g. 0.5) has register Succeeded.

The end state must include:

GET /api/v1/workflow-templates/argo/train-and-maybe-register returns the template, whose evaluate template emits a score output parameter and whose register step carries a when: gate referencing both the evaluate score and min_score.
At least two workflows exist whose spec.workflowTemplateRef.name == train-and-maybe-register.
One with min_score > 0.75 has its register node Skipped/Omitted; another with min_score <= 0.75 has register Succeeded.
This is the canonical CI/CT gate: every commit runs train + evaluate, but only commits that clear the configurable threshold promote the model. Passing the score between steps as an output parameter—and gating promotion with when:—is what lets one template serve dev (min_score=0.5), staging (0.75), and prod (0.9) without a single rewrite.
# Solution

A `WorkflowTemplate` is a reusable pipeline definition that can be parameterised per run, letting one template serve dev, staging, and prod by only changing an argument. This task finishes a `train-and-maybe-register` template — publishing the evaluate score as an output parameter and gating the `register` step with a `when:` expression — then submits it twice to prove the gate both skips and fires.

> As an MLOps engineer, you pass a score between steps as an output parameter and gate model promotion with a configurable `when:` threshold so the same template serves every environment — you are not tuning the model; the evaluate score is a synthetic constant.

#### Follow the steps below

##### 1. Read the scaffolded template.
The startup staged an incomplete template on disk and did **not** apply it — the Argo UI's **Workflow Templates** list is empty. Open it in VS Code:
```
sed -n '1,60p' /root/code/argo/train-and-maybe-register.yaml
```
Two pieces are missing: the `evaluate` template does not publish its score (TODO 1), and the `register` step has no `when:` gate (TODO 2).

#### 2.Corrected train-and-maybe-register.yaml
Update /root/code/argo/train-and-maybe-register.yaml to the following. The two important changes are marked with comments.

apiVersion: argoproj.io/v1alpha1
kind: WorkflowTemplate
metadata:
  name: train-and-maybe-register
  namespace: argo
spec:
  entrypoint: main
  arguments:
    parameters:
      - name: min_score
        value: "0.80"
  templates:
    - name: main
      steps:
        - - name: train
            template: train
        - - name: evaluate
            template: evaluate
        - - name: register
            template: register
            when: "{{steps.evaluate.outputs.parameters.score}} >= {{workflow.parameters.min_score}}"

    - name: train
      container:
        image: alpine:3.19
        command: [sh, -c]
        args: ["echo '[train] fitting model' && sleep 2"]

    - name: evaluate
      script:
        image: alpine:3.19
        command: [sh]
        source: |
          echo "0.75" > /tmp/score.txt
          echo "[evaluate] score=0.75"
      outputs:
        parameters:
          - name: score
            valueFrom:
              path: /tmp/score.txt

    - name: register
      container:
        image: alpine:3.19
        command: [sh, -c]
        args: ["echo '[register] promoting model to registry'"]

##### 3. Apply the template.
WorkflowTemplates are cluster resources — apply the finished file, then confirm it in the UI:
```
kubectl apply -n argo -f /root/code/argo/train-and-maybe-register.yaml
```
Click the **Argo UI** button → left nav **Workflow Templates** → `train-and-maybe-register` now appears. Click it.

##### 4. Submission 1 — `min_score` above the evaluate score.
On the template detail page, click **+ Submit** (top-right). The dialog opens with `min_score: 0.80` prefilled.
- Change `min_score` to `0.99` (above the `0.75` score).
- Click **+ Submit**.

The `main` steps render `train → evaluate → register`. `train` and `evaluate` go green; `register` stays dashed grey (**Skipped**) — the `when:` is false. Workflow phase: `Succeeded`.

##### 5. Submission 2 — `min_score` below the evaluate score.
Back on **Workflow Templates → `train-and-maybe-register`**, click **+ Submit** again.
- Change `min_score` to `0.5` (below the `0.75` score).
- Click **+ Submit**.

This run's `register` node is green — the `when:` is true. Workflow phase: `Succeeded`.

##### 6. Verify via the REST API.
From a VS Code terminal:
```
curl -s http://localhost:5000/api/v1/workflows/argo \
  | python3 -c "
import json, sys
body = json.load(sys.stdin)
for w in body.get('items', []):
    spec = w.get('spec', {})
    ref = spec.get('workflowTemplateRef', {})
    if ref.get('name') != 'train-and-maybe-register':
        continue
    args = spec.get('arguments', {}).get('parameters', [])
    ms = next((p['value'] for p in args if p['name'] == 'min_score'), '?')
    # Find the register node phase.
    reg_phase = '?'
    for n in (w.get('status') or {}).get('nodes', {}).values():
        nm = n.get('displayName') or n.get('name') or ''
        if nm.endswith('.register') or nm == 'register':
            reg_phase = n.get('phase'); break
    print(f\"min_score={ms:4s}  register.phase={reg_phase}\")
"
```
The output shows two lines — one with `min_score=0.99 register.phase=Skipped` (or `Omitted`) and one with `min_score=0.5 register.phase=Succeeded`.

#### References

- Argo Workflows — output parameters (`valueFrom.path`, `steps.X.outputs.parameters.Y`): https://argo-workflows.readthedocs.io/en/latest/walk-through/output-parameters/
- Argo Workflows — conditionals (`when:` with the `asFloat(...)` expr syntax): https://argo-workflows.readthedocs.io/en/latest/walk-through/conditionals/
- Argo Workflows — WorkflowTemplates and submitting from them: https://argo-workflows.readthedocs.io/en/latest/workflow-templates/
