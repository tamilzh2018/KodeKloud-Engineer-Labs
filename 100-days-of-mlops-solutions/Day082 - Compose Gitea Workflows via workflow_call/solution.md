# Task
The xFusionCorp Industries ML platform team is currently enhancing the fraud-detector continuous integration (CI) process. The existing main.yml file contains three similar inline jobs that have been duplicated, requiring the same changes to be implemented for each on every pull request (PR). A team member has already separated the lint, test, and report stages into distinct files located in the .gitea/workflows/ directory—each configured to declare on: workflow_call—and has opened a PR that modifies one job (lint) to call the reusable workflow. Your task is to complete this refactor by converting the two remaining inline jobs in main.yml into uses: calls, thereby enabling the main run to expand into three nested workflow_call executions.


The Gitea UI is on port 3000 (Gitea button). Admin credentials: gitea-admin / gitea2026. The repo is at http://localhost:3000/gitea-admin/fraud-detector and a working clone is at /root/code/fraud-detector, already checked out on branch add-reusable-workflows. The PR is pre-opened.

Four workflow files ship in .gitea/workflows/. lint.yml, test.yml, and report.yml are reusable callees, each triggered by on: workflow_call. main.yml is the caller: jobs.lint already calls ./.gitea/workflows/lint.yml via uses: (the example wiring), while jobs.test and jobs.report are still inline runs-on + steps jobs that duplicate logic already parked in the callee files. Those two inline job bodies need to become single uses: lines mirroring the lint job — a job cannot declare both uses: and steps:, so the inline blocks are removed entirely.

The end state must include:

lint.yml, test.yml, and report.yml each declare on: workflow_call on the PR head branch.
main.yml defines jobs lint, test, and report, each with a uses: key pointing at the matching ./.gitea/workflows/<name>.yml.
No job in main.yml mixes uses: with steps: (illegal in Actions YAML).
The PR head commit's combined status reaches success.
Reusable workflows turn a monolithic main.yml into a small graph of composable pieces. Each callee becomes the canonical definition for its concern (lint / test / report); any number of callers can consume it. When you later add a release.yml workflow for tagged pushes, it can reuse the same test.yml callee—no more copy-paste sync issues across files.
# Solution

Reusable workflows turn a monolithic pipeline into a small graph of composable pieces that callers invoke with `uses:`. In this task the `lint`, `test`, and `report` stages have been split into their own `workflow_call` files and one job is already re-wired, so you finish the refactor by converting the two remaining inline jobs in `main.yml` into `uses:` calls that fan out into nested runs.

> As an MLOps engineer, you refactor CI into reusable callee workflows so each concern is defined once and any caller can consume it — you are not changing the model; you are restructuring the pipeline. The jobs exercise synthetic training code.

#### Follow the steps below

##### 1. Confirm the starting state.
From a VS Code terminal:
```
cd /root/code/fraud-detector
git log --oneline -3
ls .gitea/workflows/
sed -n '1,50p' .gitea/workflows/main.yml
```
Four workflow files ship under `.gitea/workflows/`. `main.yml` already calls `lint.yml` via `uses:`; `test` and `report` are still inline.

##### 2. Open the pre-existing PR.
Click the **Gitea** button, log in with `gitea-admin` / `gitea2026`, open the `fraud-detector` repo, and click **Pull Requests -> Refactor main workflow to use workflow_call**. The **Checks** tab shows the first `Main` run — everything green, but the `test` and `report` jobs still have their full inline logic visible in the logs.

##### 3. Refactor the two remaining jobs.
Open `/root/code/fraud-detector/.gitea/workflows/main.yml` in the VS Code editor. Replace the `test:` and `report:` blocks with short `uses:` stanzas:
```yaml
name: Main

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  lint:
    uses: ./.gitea/workflows/lint.yml

  test:
    uses: ./.gitea/workflows/test.yml

  report:
    uses: ./.gitea/workflows/report.yml
```
Make sure the inline `runs-on:` and `steps:` blocks are fully removed — a job cannot declare both `uses:` and `steps:`.

Save.

##### 4. Commit and push.
```
git add .gitea/workflows/main.yml
git commit -m "ci: refactor main workflow to call reusable lint/test/report"
git push
```

##### 5. Watch the nested run in Gitea.
Return to the PR's **Checks** tab. The new run shows:
- A top-level `Main` workflow.
- Three nested rows — `Lint (reusable)`, `Test (reusable)`, `Report (reusable)` — each with its own collapsible log.
- Each callee is independently re-runnable from its nested row.

Open the repo's **Actions** tab; the Runs list now shows one `Main` run per push rather than four separate runs per push.

##### 6. Verify via Gitea's REST API.
From a VS Code terminal:
```
TOKEN=$(cat /root/.gitea/token)

# main.yml's jobs are now three pure `uses:` references.
SHA=$(curl -s -H "Authorization: token $TOKEN" \
  'http://localhost:3000/api/v1/repos/gitea-admin/fraud-detector/pulls?state=all&sort=newest' \
  | python3 -c "import json, sys; print(next(p['head']['sha'] for p in json.load(sys.stdin) if p['head']['ref']=='add-reusable-workflows'))")

curl -s -H "Authorization: token $TOKEN" \
  "http://localhost:3000/api/v1/repos/gitea-admin/fraud-detector/commits/$SHA/status" \
  | python3 -m json.tool | head -40

curl -s -H "Authorization: token $TOKEN" \
  'http://localhost:3000/api/v1/repos/gitea-admin/fraud-detector/contents/.gitea/workflows/main.yml?ref=add-reusable-workflows' \
  | python3 -c "
import json, sys, base64, yaml
doc = yaml.safe_load(base64.b64decode(json.load(sys.stdin)['content']))
for name, job in doc['jobs'].items():
    print(f\"{name:10s} uses -> {job.get('uses')}\")
"
```
The first call shows combined status `success`; the second lists three jobs, each pointing at its callee workflow.

#### References

- Gitea Actions — workflow syntax (GitHub-Actions-compatible): https://docs.gitea.com/usage/actions/overview
- Reusing workflows — `on: workflow_call` callees and `uses:` callers: https://docs.github.com/en/actions/using-workflows/reusing-workflows
