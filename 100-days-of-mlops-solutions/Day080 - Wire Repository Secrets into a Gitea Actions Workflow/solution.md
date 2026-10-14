# Task
The xFusionCorp Industries ML platform team requires that every pull request (PR) in the fraud-detector repository logs a training run to MLflow and registers the resulting model version. However, they prefer not to include the tracking URL or an API token in plaintext within the workflow file. Gitea and a local MLflow 3.x server are currently operational, and a teammate has initiated a PR titled Register trained model on every push. Currently, the first run fails because the register job is attempting to access MLFLOW_TRACKING_URI and MLFLOW_TOKEN from the environment, but these variables are not populated. Your task is to provision these two values as repository secrets and integrate them into the workflow to ensure the run succeeds.


The Gitea UI is on port 3000 (Gitea button); admin credentials gitea-admin / gitea2026. The MLflow UI is on port 5000 (MLflow UI button). The repo is at http://localhost:3000/gitea-admin/fraud-detector and a working clone is at /root/code/fraud-detector, already checked out on branch add-registry-push. The PR is pre-opened.

The shipped .gitea/workflows/ci.yml declares a register job that runs python3 -m src.register. src/register.py reads MLFLOW_TRACKING_URI and MLFLOW_TOKEN from os.environ and exits non-zero if either is missing, so on the first run the job fails with that error. Two pieces are needed: the repository secrets MLFLOW_TRACKING_URI (value http://localhost:5000) and MLFLOW_TOKEN (any non-empty string, e.g. fraud-detector-ci-token — the lab's MLflow does not enforce auth, but the script refuses to run without the value so a missing secret surfaces as a clear failure), created under the repo's Settings → Actions → Secrets; and the workflow wiring that exports each secret into the register job's environment under the same name.

The end state must include:

GET /api/v1/repos/gitea-admin/fraud-detector/actions/secrets lists both MLFLOW_TRACKING_URI and MLFLOW_TOKEN.
The register job in the workflow references each secret via ${{ secrets.<NAME> }} inside an env: block (job-level or step-level).
The PR head commit's combined status is success.
MLflow's registered-model endpoint reports fraud-detector with at least one version.
Repository secrets are the CI version of an environment-specific config file. The YAML stays identical between dev, staging, and prod; only the secret values change. This is also the pattern you extend when you add a PyPI token, an S3 access key, or a Kubernetes kubeconfig to a workflow—never paste the value into the committed file.
# Solution

Repository secrets keep credentials out of the committed workflow file — the YAML stays identical across environments and only the secret values change. In this task a `register` job fails because its MLflow tracking URL and token are unset, so you provision both as repo secrets and wire them into the workflow's `env` block so the run registers the model and goes green.

> As an MLOps engineer, you feed credentials into CI through secrets instead of pasting them into the workflow file, and let the pipeline register the model automatically — you are not building the model; you are wiring how CI talks to the registry. The registered model comes from a synthetic training run.

#### Follow the steps below

##### 1. Confirm the starting state.
From a VS Code terminal:
```
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:3000/
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:5000/
cat /root/code/fraud-detector/.gitea/workflows/ci.yml | grep -A5 register:
```
Gitea and MLflow both answer `200`. The `register` job has no `env:` block — the Python step will exit because `MLFLOW_TRACKING_URI` is missing.

##### 2. Open the pre-existing PR and confirm the red run.
Click the **Gitea** button, log in with `gitea-admin` / `gitea2026`, open the `fraud-detector` repo, and click **Pull Requests -> Register trained model on every push**. The **Checks** tab shows the `register` job red; the log reads `MLFLOW_TRACKING_URI is not set`.

##### 3. Add the two repository secrets.
Still in Gitea, open the `fraud-detector` repo page (not your user profile). In the repo's own top navigation bar, click **Settings** (far right, next to Activity / Wiki). The URL should end with `/gitea-admin/fraud-detector/settings` — **not** `/user/settings`.

> **Important:** Gitea has two separate "Settings" pages — one under your user avatar (personal settings) and one on each repo (repo settings). Secrets created under the user profile are scoped to your user and will not show up on the repo's secrets API.

Inside the repo's Settings page:
- In the left navigation, expand **Actions** and click **Secrets**.
- Click **Add Secret**:
  - **Name:** `MLFLOW_TRACKING_URI`
  - **Value:** `http://localhost:5000`
  - Click **Add secret**.
- Click **Add secret** again:
  - **Name:** `MLFLOW_TOKEN`
  - **Value:** `fraud-detector-ci-token` (the lab's MLflow does not enforce auth, but the script refuses to run without the value so a missing secret surfaces as a clear failure).
  - Click **Add secret**.

The secrets list now shows two entries.

##### 4. Wire the secrets into the workflow.
Open `/root/code/fraud-detector/.gitea/workflows/ci.yml` in the VS Code editor. Add a job-level `env:` block to the `register` job:
```yaml
  register:
    runs-on: ubuntu-latest
    env:
      MLFLOW_TRACKING_URI: ${{ secrets.MLFLOW_TRACKING_URI }}
      MLFLOW_TOKEN:        ${{ secrets.MLFLOW_TOKEN }}
    steps:
      - uses: actions/checkout@v4
      - name: Install registration deps
        run: pip install --break-system-packages mlflow numpy scikit-learn joblib pandas
      - name: Train and register
        run: python3 -m src.register
```
Save.

##### 5. Commit and push.
```
cd /root/code/fraud-detector
git add .gitea/workflows/ci.yml
git commit -m "ci: wire MLflow secrets into the register job"
git push
```

##### 6. Watch the new run.
Return to the PR's **Checks** tab in the Gitea UI. A new run kicks off; `register` goes green.

##### 7. Verify via Gitea + MLflow REST APIs.
From a VS Code terminal:
```
TOKEN=$(cat /root/.gitea/token)

curl -s -H "Authorization: token $TOKEN" \
  http://localhost:3000/api/v1/repos/gitea-admin/fraud-detector/actions/secrets \
  | python3 -m json.tool

curl -s http://localhost:5000/api/2.0/mlflow/registered-models/get?name=fraud-detector \
  | python3 -m json.tool | head -30
```
The secrets endpoint lists `MLFLOW_TRACKING_URI` and `MLFLOW_TOKEN` (names only — values are opaque). The MLflow endpoint shows `fraud-detector` with one or more versions.

#### References

- Gitea Actions — secrets (repo-level secrets and the `${{ secrets.* }}` syntax): https://docs.gitea.com/usage/actions/secrets
- Using secrets in workflows (GitHub-Actions-compatible reference): https://docs.github.com/en/actions/security-for-github-actions/security-guides/using-secrets-in-github-actions
- MLflow Model Registry — registered models and versions: https://mlflow.org/docs/latest/ml/model-registry/
