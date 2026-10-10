# Task
The xFusionCorp Industries ML platform team requires that pull requests for the fraud-detector repository automatically run linting and testing processes prior to the review stage. A local Gitea server is currently operational with the fraud-detector repository pre-pushed on the main branch. Additionally, a self-hosted Actions runner has been registered and is awaiting jobs. Your objective is to complete the integration of the CI workflow template, which is located at .gitea/workflows/ci.yml.template on the main branch, within a feature branch. Once completed, open a pull request, monitor the Checks tab for successful approvals, and subsequently merge the pull request into the main branch.


The Gitea UI is running on port 3000 (the Gitea button opens the login page). Admin credentials: gitea-admin / gitea2026. The repo is at http://localhost:3000/gitea-admin/fraud-detector, with a working clone at /root/code/fraud-detector (on main).

The scaffold under /root/code/fraud-detector/ lints clean and has passing tests: src/train.py (a deterministic synthetic training script), tests/test_train.py (three passing unit tests), pyproject.toml (Ruff + pytest config), and .gitea/workflows/ci.yml.template — a pre-written CI workflow with the on: triggers and lint + test job skeletons already wired, plus # TODO: markers on the two run: lines that need filling in. Ruff and pytest are both installed on the host. Gitea Actions only schedules *.yml / *.yaml files, so the .template suffix keeps the file inert until it is renamed to ci.yml.

The end state must include:

A workflow file .gitea/workflows/ci.yml on branch add-ci that parses as YAML and declares both a lint and a test job.
One pull request in the repo targeting main, with add-ci as its head branch.
That PR's head commit reports combined status success on GET /api/v1/repos/gitea-admin/fraud-detector/commits/{sha}/status.
The PR is merged into main (merged: true on the pulls API).
Gitea Actions uses the same YAML syntax as GitHub Actions, so the workflow you ship here is also the kind of file you would drop into any github.com repo. Real CI engineers rarely author these from scratch — they inherit a template and edit the two or three lines that are project-specific, which is exactly what the .template scaffold mirrors.

# Solution

Continuous integration means every change is checked automatically before it reaches the shared branch. In this task you finish a Gitea Actions workflow so that opening a pull request on the `fraud-detector` repo runs `ruff` and `pytest` as required checks, then you open the PR, watch both jobs go green, and merge it into `main`.

> As an MLOps engineer, you make lint and tests run automatically on every PR so broken code never reaches `main` — you are not writing the model; the tests guard the pipeline. The training script is deterministic synthetic code.

#### Follow the steps below

##### 1. Confirm the starting state.
From a VS Code terminal:
```
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:3000/
curl -s -H "Authorization: token $(cat /root/.gitea/token)" \
  http://localhost:3000/api/v1/repos/gitea-admin/fraud-detector \
  | python3 -m json.tool | head -15
ls /root/code/fraud-detector/.gitea/workflows/
```
Gitea answers `200`. The API returns the `fraud-detector` repo. The `.gitea/workflows/` directory already carries `ci.yml.template` — the pre-written workflow with two TODO `run:` lines.

##### 2. Cut a feature branch.
```
cd /root/code/fraud-detector
git checkout -b add-ci
```

##### 3. Rename the template and fill in the two TODO lines.
```
git mv .gitea/workflows/ci.yml.template .gitea/workflows/ci.yml
```
Open `/root/code/fraud-detector/.gitea/workflows/ci.yml` in the VS Code editor. Replace the two `run: # TODO: ...` placeholders:
- In the `lint` job, set the last step's `run:` to `ruff check src tests`.
- In the `test` job, set the last step's `run:` to `python3 -m pytest tests -v`.

Save.

##### 4. Commit and push.
```
git add .gitea/workflows/ci.yml
git commit -m "ci: add lint and test workflow"
git push -u origin add-ci
```
The push succeeds — the clone was pre-configured with a credential helper + a reader identity on startup, so there is no password prompt and the commit does not bail on "Author identity unknown".

##### 5. Open the pull request in the Gitea UI.
Click the **Gitea** button at the top of the lab and log in with `gitea-admin` / `gitea2026`.
- Click the `fraud-detector` repository on the dashboard.
- Click **Pull Requests -> New Pull Request**.
- Base branch: `main`. Compare branch: `add-ci`.
- Click **Create Pull Request**. Give it a title (e.g. `Add CI workflow`) and click **Create Pull Request** again.

##### 6. Watch the Checks tab.
Inside the PR, click the **Checks** tab (next to Conversation / Commits / Files changed). The `CI` workflow appears with two jobs — `lint` and `test`. Both start as yellow spinners, then turn into green check-marks as the runner finishes each job. The PR's overall status flips from yellow to green.

##### 7. Merge the PR.
Back on the **Conversation** tab, click **Merge Pull Request** (enabled once both checks are green) → **Create merge commit** → **Merge Pull Request**. Gitea merges the workflow onto `main` and re-runs the `push`-triggered CI on the merge commit.

##### 8. Verify via Gitea's REST API.
From a VS Code terminal:
```
TOKEN=$(cat /root/.gitea/token)
curl -s -H "Authorization: token $TOKEN" \
  'http://localhost:3000/api/v1/repos/gitea-admin/fraud-detector/pulls?state=all&sort=newest' \
  | python3 -c "
import json, sys
pr = json.load(sys.stdin)[0]
print('merged :', pr.get('merged'))
print('sha    :', pr['head']['sha'][:8])
"
SHA=$(curl -s -H "Authorization: token $TOKEN" \
  'http://localhost:3000/api/v1/repos/gitea-admin/fraud-detector/pulls?state=all&sort=newest' \
  | python3 -c "import json, sys; print(json.load(sys.stdin)[0]['head']['sha'])")
curl -s -H "Authorization: token $TOKEN" \
  "http://localhost:3000/api/v1/repos/gitea-admin/fraud-detector/commits/$SHA/status" \
  | python3 -c "import json, sys; d=json.load(sys.stdin); print('state:', d.get('state'))"
```
The first call prints `merged : True` and the PR's head SHA; the second prints `state: success`.

#### References

- Gitea Actions — workflow syntax (jobs, steps, `run:`) and PR triggers: https://docs.gitea.com/usage/actions/overview
- Ruff — the `ruff check` linter command: https://docs.astral.sh/ruff/linter/
- pytest — invoking the test run: https://docs.pytest.org/en/stable/how-to/usage.html
