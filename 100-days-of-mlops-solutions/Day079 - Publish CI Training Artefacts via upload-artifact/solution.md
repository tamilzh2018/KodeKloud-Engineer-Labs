# Task
The xFusionCorp Industries ML platform team's Continuous Integration (CI) system currently trains the model and generates a confusion matrix in PNG format. However, these artifacts are discarded when the runner tears down the workspace, preventing reviewers on a Pull Request (PR) from accessing them. A teammate has submitted a PR titled Publish Training Artifacts from CI in the fraud-detector repository. Your task is to integrate actions/upload-artifact into the existing report job, ensuring that metrics.json and confusion_matrix.png are available as a downloadable zip file on the run page.


The Gitea UI is running on port 3000 (the Gitea button opens the login page). Admin credentials: gitea-admin / gitea2026. The repo lives at http://localhost:3000/gitea-admin/fraud-detector and a working clone is at /root/code/fraud-detector, already checked out on branch add-artifact-upload. The PR is pre-opened.

The current report job in .gitea/workflows/ci.yml already installs numpy scikit-learn joblib matplotlib, runs python3 -m src.train (writes artifacts/model.joblib and artifacts/metrics.json), runs python3 -m src.plot (writes artifacts/confusion_matrix.png), and ends with ls -la artifacts/ — but the produced files are discarded when the run finishes. The job needs a final step that uploads the artifacts/ directory as a named artefact (model-report) using actions/upload-artifact. Use @v3 — Gitea's runner rejects @v4.

The end state must include:

The report job contains a step that uses actions/upload-artifact@* with a non-empty path and the artefact name model-report.
The run-level artefact download at /gitea-admin/fraud-detector/actions/runs/<id>/artifacts/model-report returns a zip containing both metrics.json and confusion_matrix.png by basename.
The PR head commit's combined status is success.
Artefacts are CI's answer to the question 'what did that run actually produce?'. A green check-mark tells you the code compiled; an uploaded artefact tells you what shipped out the other end. For ML runs, this is where the metrics JSON, the confusion matrix plot, and the pickled model live before anyone promotes them to a registry.


# Solution

CI artefacts are the files a run produces and hands back for download after the workspace is torn down. In this task a `report` job already trains and renders a confusion matrix but throws the outputs away, so you wire in `actions/upload-artifact` to publish `metrics.json` and `confusion_matrix.png` as a named, downloadable artefact on the run page.

> As an MLOps engineer, you make CI publish the run's outputs so reviewers can download what shipped instead of trusting a green check — you are not tuning the model; you are persisting its artefacts. The metrics and plot come from a synthetic training run.

#### Follow the steps below

##### 1. Confirm the starting state.
From a VS Code terminal:
```
cd /root/code/fraud-detector
git log --oneline -3
cat .gitea/workflows/ci.yml
```
The branch is `add-artifact-upload`. The `report` job already runs `src.train` + `src.plot` but ends with `ls -la artifacts/` — the files are listed in the log, then thrown away with the workspace.

##### 2. Open the pre-existing PR.
Click the **Gitea** button at the top of the lab, log in with `gitea-admin` / `gitea2026`, open the `fraud-detector` repository, and click **Pull Requests -> Publish training artefacts from CI**. Open the **Checks** tab to see the current `report` run finishing without producing a downloadable artefact.

##### 3. Add the upload step.
Open `/root/code/fraud-detector/.gitea/workflows/ci.yml` in the VS Code editor. Append one step to the end of the `report` job's `steps:` list:
```yaml
      - name: Upload training artefacts
        uses: actions/upload-artifact@v3
        with:
          name: model-report
          path: artifacts/
```
Use `@v3`, not `@v4`. Gitea's Actions runner does not support the newer artifact backend that `upload-artifact@v4+` requires — v4 fails the step with `GHESNotSupportedError: ... upload-artifact@v4+ ... not currently supported on GHES`. Save.

##### 4. Commit and push.
```
git add .gitea/workflows/ci.yml
git commit -m "ci: upload metrics + confusion matrix as a run artefact"
git push
```

##### 5. Watch the artefact land on the run.
Return to the PR's **Checks** tab in the Gitea UI. A new run starts. When `report` finishes, click into it — the run page now has an **Artefacts** section at the bottom with one entry, `model-report`. Click it; Gitea serves a zip containing `metrics.json` and `confusion_matrix.png`.

##### 6. (Optional) Download the artefact from the terminal.
The normal way is the one-click download you just did — the **Artifacts** section on the run page. If you'd rather pull it from a script, note that Gitea 1.22.3 exposes artefacts only through that run-page web route (`/<owner>/<repo>/actions/runs/<id>/artifacts/<name>`), not a JSON REST API. Resolve the run id from the PR head commit's combined status, then download the named artefact:
```
TOKEN=$(cat /root/.gitea/token)
SHA=$(curl -s -H "Authorization: token $TOKEN" \
  'http://localhost:3000/api/v1/repos/gitea-admin/fraud-detector/pulls?state=all&sort=newest' \
  | python3 -c "import json, sys; print(next(p['head']['sha'] for p in json.load(sys.stdin) if p['head']['ref']=='add-artifact-upload'))")
RUN_ID=$(curl -s -H "Authorization: token $TOKEN" \
  "http://localhost:3000/api/v1/repos/gitea-admin/fraud-detector/commits/$SHA/status" \
  | python3 -c "
import json, re, sys
body = json.load(sys.stdin)
for s in body.get('statuses', []):
    m = re.search(r'/actions/runs/(\d+)', s.get('target_url') or '')
    if m:
        print(m.group(1))
        break
")
curl -sL -H "Authorization: token $TOKEN" -o /tmp/report.zip \
  "http://localhost:3000/gitea-admin/fraud-detector/actions/runs/$RUN_ID/artifacts/model-report"

unzip -l /tmp/report.zip
```
The zip contains `metrics.json` and `confusion_matrix.png`.

#### References

- Gitea Actions — workflow syntax (GitHub-Actions-compatible): https://docs.gitea.com/usage/actions/overview
- `actions/upload-artifact` — the action, its `name`/`path` inputs, and version notes: https://github.com/actions/upload-artifact
- Storing workflow data as artefacts — why runs publish outputs for later download: https://docs.github.com/en/actions/using-workflows/storing-workflow-data-as-artifacts
