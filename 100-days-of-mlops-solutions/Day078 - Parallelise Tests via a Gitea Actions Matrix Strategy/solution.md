
# Task
The xFusionCorp Industries ML platform team has three distinct test suites within the fraud-detector repository: unit tests (test_train.py), data quality tests (test_data_quality.py), and model contract tests (test_model_contract.py). Currently, the continuous integration (CI) pipeline executes all three suites serially within a single test job. As the test suites expand, this configuration is becoming a significant bottleneck for every pull request (PR). A teammate has submitted a PR titled Convert test job to matrix strategy. Your task is to modify the workflow to enable the test job to utilize a Gitea Actions matrix, allowing each test suite to run in its own parallel job.


The Gitea UI is running on port 3000 (the Gitea button opens the login page). Admin credentials: gitea-admin / gitea2026. The repo lives at http://localhost:3000/gitea-admin/fraud-detector and a working clone is at /root/code/fraud-detector, already checked out on branch add-test-matrix. The PR is pre-opened.

The current .gitea/workflows/ci.yml declares a test job that runs all suites serially on a single runner, alongside a lint job. Three test files live under tests/: test_train.py, test_data_quality.py, test_model_contract.py. The goal is to fan the test job out over a strategy.matrix so each suite runs in its own parallel cell, while the lint job stays unchanged.

The end state must include:

The test job in the workflow declares strategy.matrix whose list dimension contains train, data_quality, and model_contract.
Every matrix value maps to an existing tests/test_<value>.py file on the add-test-matrix branch.
The latest run on the PR head commit reports combined status success, with at least three test status entries (one per matrix cell).
A matrix strategy is the CI equivalent of a loop variable: one job definition, many parameterised executions. The classical case is a Python-version matrix (3.10 / 3.11 / 3.12), but any axis works—test suites, feature flags, target platforms. The point is to express 'run this N times with N variants' once instead of copying the job body.
# Solution

A matrix strategy lets one CI job definition fan out into many parallel executions, one per variant. In this task you rewrite a serial `test` job so it runs each of the three test suites in its own parallel Gitea Actions job, then push and watch the matrix cells expand on the Checks tab.

> As an MLOps engineer, you fan the test job out across suites so they run in parallel instead of blocking each PR serially — you are not authoring the model; you are shaping how its checks execute. The suites run over synthetic data.

#### Follow the steps below

##### 1. Confirm the starting state.
From a VS Code terminal:
```
cd /root/code/fraud-detector
git log --oneline -3
ls tests/
cat .gitea/workflows/ci.yml
```
The branch is `add-test-matrix`. Three test files ship under `tests/` (`test_train.py`, `test_data_quality.py`, `test_model_contract.py`). The workflow declares a single `test` job running `pytest tests -v` serially.

##### 2. Open the pre-existing PR.
Click the **Gitea** button at the top of the lab, log in with `gitea-admin` / `gitea2026`, open the `fraud-detector` repository, and click **Pull Requests -> Convert test job to matrix strategy**. The **Checks** tab shows the first run with one `test` job containing all three suites.

##### 3. Rewrite the `test` job as a matrix.
Open `/root/code/fraud-detector/.gitea/workflows/ci.yml` in the VS Code editor. Replace the `test:` block with:
```yaml
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        suite: [train, data_quality, model_contract]
    steps:
      - uses: actions/checkout@v4
      - name: Install pytest + runtime deps
        run: pip install --break-system-packages pytest pandas numpy scikit-learn joblib
      - name: Run ${{ matrix.suite }} suite
        run: python3 -m pytest tests/test_${{ matrix.suite }}.py -v
```
Keep the `lint` job unchanged. Save.

##### 4. Commit and push.
```
git add .gitea/workflows/ci.yml
git commit -m "ci: fan test job out over matrix suites"
git push
```

##### 5. Watch the matrix expand on the Runs UI.
Return to the PR's **Checks** tab. The new run shows:
- `lint` — one job (unchanged).
- `test (train)`, `test (data_quality)`, `test (model_contract)` — three parallel jobs spawned from the matrix.

Click **Actions** in the repo header for the runs list, then click into the latest run to see all four jobs as lanes. Each matrix cell has its own log.

##### 6. Verify via Gitea's REST API.
From a VS Code terminal:
```
TOKEN=$(cat /root/.gitea/token)
SHA=$(curl -s -H "Authorization: token $TOKEN" \
  'http://localhost:3000/api/v1/repos/gitea-admin/fraud-detector/pulls?state=all&sort=newest' \
  | python3 -c "import json, sys; print(next(p['head']['sha'] for p in json.load(sys.stdin) if p['head']['ref']=='add-test-matrix'))")
curl -s -H "Authorization: token $TOKEN" \
  "http://localhost:3000/api/v1/repos/gitea-admin/fraud-detector/commits/$SHA/status" \
  | python3 -c "
import json, sys
body = json.load(sys.stdin)
print('overall:', body['state'])
for s in body.get('statuses', []):
    print(f\"  - {s['context']:40s} {s['status']}\")
"
```
The output shows `overall: success` and four per-job entries — one `lint` plus three `test (*)` cells — all `success`.

#### References

- Gitea Actions — workflow syntax (GitHub-Actions-compatible): https://docs.gitea.com/usage/actions/overview
- Matrix strategy — fanning one job out over variants (`strategy.matrix`, `${{ matrix.* }}`): https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/running-variations-of-jobs-in-a-workflow
