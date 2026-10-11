# Task
The xFusionCorp Industries ML platform team requires data-schema tests to be executed as a continuous integration (CI) gate for every pull request, ensuring that poor training data is detected before it affects the model. A team member has submitted a pull request titled Add data-quality CI gate in the fraud-detector repository; however, the newly added data-quality job has failed on its initial execution. Your objective is to examine the failed run log in Gitea Actions, determine the cause of the job failure, rectify the workflow, and push your changes so that the pull request is successful.


The Gitea UI is running on port 3000 (the Gitea button opens the login page). Admin credentials: gitea-admin / gitea2026. The repo lives at http://localhost:3000/gitea-admin/fraud-detector and a working clone is at /root/code/fraud-detector, already checked out on branch add-data-validation.

The pre-opened PR's workflow at .gitea/workflows/ci.yml declares three jobs: lint, test (both green), and data-quality (meant to run the data-schema tests, currently red). Open the failed data-quality run from the PR's Checks tab to read its log.

The end state must include:

The data-quality job is still declared in the workflow (do not delete the job itself).
The data-quality job's pytest step references a .py file that exists on the add-data-validation branch.
After the latest push, the PR's head commit's combined status reaches success (all three jobs green).
The point of a red CI run is not just the red pill in the PR—it is the log underneath it. A workflow can look fine by static inspection and still fail at runtime.
# Solution

A CI gate is a job that must pass before a pull request can merge. In this task a data-quality gate is already wired into the workflow but its first run is red, so you read the failed run log in Gitea Actions, find why the job broke, fix the workflow, and push until the PR goes green.

> As an MLOps engineer, you gate merges on a data-quality check so bad training data can't ship — you are not judging model accuracy; you are keeping the pipeline honest. The data is synthetic.

#### Follow the steps below

##### 1. Read the red run log.
Click the **Gitea** button at the top of the lab and log in with `gitea-admin` / `gitea2026`.
- Open the `fraud-detector` repository.
- Click **Pull Requests** and open `Add data-quality CI gate`.
- Click the **Checks** tab.
- Find the red `data-quality` job and click into it.

The `Run data-quality tests` step ends with something like:

```
ERROR: file or directory not found: tests/test_data_validation.py
```

The workflow is pointing pytest at a filename that does not exist on the branch.

##### 2. Confirm the real filename on disk.
From a VS Code terminal:
```
cd /root/code/fraud-detector
git status
ls tests/
```
The file is `tests/test_data_quality.py`. The workflow YAML typed `test_data_validation.py` — classic half-done rename.

##### 3. Fix the workflow YAML.
Open `/root/code/fraud-detector/.gitea/workflows/ci.yml` in the VS Code editor. Locate the `data-quality` job's `Run data-quality tests` step:
```yaml
      - name: Run data-quality tests
        run: python3 -m pytest tests/test_data_validation.py -v
```
Change the pytest target to match the file on disk:
```yaml
      - name: Run data-quality tests
        run: python3 -m pytest tests/test_data_quality.py -v
```
Save.

##### 4. Commit and push.
```
git add .gitea/workflows/ci.yml
git commit -m "fix(ci): point data-quality job at the real test file"
git push
```

##### 5. Watch the new run go green.
Return to the PR's **Checks** tab in the Gitea UI. A new CI run starts on the new commit. The `data-quality` job runs to completion; all three jobs finish as green check-marks. The PR's overall status badge turns green.

##### 6. Verify via Gitea's REST API.
From a VS Code terminal:
```
TOKEN=$(cat /root/.gitea/token)
SHA=$(curl -s -H "Authorization: token $TOKEN" \
  'http://localhost:3000/api/v1/repos/gitea-admin/fraud-detector/pulls?state=all&sort=newest' \
  | python3 -c "import json, sys; print(next(p['head']['sha'] for p in json.load(sys.stdin) if p['head']['ref']=='add-data-validation'))")
curl -s -H "Authorization: token $TOKEN" \
  "http://localhost:3000/api/v1/repos/gitea-admin/fraud-detector/commits/$SHA/status" \
  | python3 -m json.tool
```
The `state` field reads `"success"` and every entry in `statuses[]` is `"success"`.

#### References

- Gitea Actions — reading a failed run's logs and workflow syntax: https://docs.gitea.com/usage/actions/overview
- pytest — selecting a test file to run: https://docs.pytest.org/en/stable/how-to/usage.html
