# Task
The xFusionCorp Industries machine learning platform team requires that every fraud-detector release tag is reproducible from a single Gitea page. This includes the Docker image used in production, the metrics.json file that details the model's performance, and a permanent link to the commit that generated these artifacts. A tag-triggered release workflow has been established in the main branch at .gitea/workflows/release.yml. However, the two container-registry steps, labeled Build image and Push image to Gitea registry, remain incomplete and currently only contain TODO stubs that result in an exit 1, preventing any image from being shipped with a release. Your task is to implement the necessary functionality for these two steps, ensuring that the workflow successfully builds the Docker image and publishes it to Gitea's integrated container (package) registry. Following the completion of these steps, proceed to create the v0.1.0 release, allowing the tag to trigger the finalized workflow.


The Gitea UI is running on port 3000 (the Gitea button opens the login page). Admin credentials: gitea-admin / gitea2026. The repo is at http://localhost:3000/gitea-admin/fraud-detector and a working clone is at /root/code/fraud-detector (on main).

The release workflow (.gitea/workflows/release.yml) triggers on any v* tag push. Its build-and-publish job already logs in to localhost:3000 (Gitea's built-in container registry) using the pre-provisioned repository secret REGISTRY_TOKEN, resolves the image version from the git tag (steps.version.outputs.VERSION), and runs python3 -m src.train to emit artifacts/metrics.json and attach it to the release via akkuman/gitea-release-action@v1. The two steps in between — Build image and Push image to Gitea registry — are TODO stubs that currently exit 1. The surrounding steps set $REGISTRY, $IMAGE, and the resolved version (steps.version.outputs.VERSION) for the two steps to use.

Once the workflow is completed on main, publishing a v0.1.0 release (target main, any non-empty title) from the repo's Releases tab cuts the tag that triggers the run, which publishes the image and attaches the metrics file.

The end state must include:

GET /api/v1/repos/gitea-admin/fraud-detector/releases/tags/v0.1.0 returns a release whose tag_name is v0.1.0.
release.yml at the v0.1.0 tag runs docker build and docker push in the build-and-publish job (the image is published by CI, not by hand).
The tag's commit SHA reports combined status success on its checks.
The release's assets array contains an entry whose name resolves to metrics.json.
Gitea's packages API (GET /api/v1/packages/gitea-admin?type=container) lists a container package named fraud-detector with a version equal to v0.1.0 (or 0.1.0).
Tagging a release is the moment a commit becomes addressable by humans, not just by SHA. The workflow's job is to make sure the release carries everything downstream systems need—an image reference for the deployer, a metrics file for compliance, a signed tag for provenance—so the Releases page becomes the single source of truth for what's running in production.
# Solution

A release pipeline turns a git tag into a shipped artefact. In this task you author the build-and-push steps of a tag-triggered workflow so it builds the `fraud-detector` image and publishes it to Gitea's container registry, then cut the `v0.1.0` release so the tag fires the finished workflow and attaches its metrics to the release page.

> As an MLOps engineer, you make a release tag build and publish the production image automatically so every version is reproducible from one page — you are not writing the model; you are packaging and shipping it. The metrics attached to the release come from a synthetic training run.

#### Follow the steps below

##### 1. Confirm the starting state.
From a VS Code terminal:
```
cd /root/code/fraud-detector
ls
cat .gitea/workflows/release.yml
```
`main` carries `src/`, `tests/`, `Dockerfile`, and `.gitea/workflows/release.yml`. The workflow fires on any `v*` tag, but its **Build image** and **Push image to Gitea registry** steps are TODO stubs that `exit 1` — a release cut now would run a red workflow that publishes no image.

##### 2. Author the build + push steps.
Open `/root/code/fraud-detector/.gitea/workflows/release.yml` in the VS Code editor. Replace the two TODO steps so the job builds the image and pushes it to Gitea's container registry:
```yaml
      - name: Build image
        run: |
          docker build \
            -t "$REGISTRY/$IMAGE:${{ steps.version.outputs.VERSION }}" \
            .

      - name: Push image to Gitea registry
        run: docker push "$REGISTRY/$IMAGE:${{ steps.version.outputs.VERSION }}"
```
`$REGISTRY` (`localhost:3000`) and `$IMAGE` (`gitea-admin/fraud-detector`) come from the job's `env:` block; `steps.version.outputs.VERSION` is the tag name resolved by the earlier step (e.g. `v0.1.0`). The login step already authenticated to the registry with the `REGISTRY_TOKEN` secret, so the push is authorised. Save.

##### 3. Commit and push to `main`.
The tag you cut next captures the workflow file **as it exists at that commit**, so the finished steps must land on `main` first:
```
cd /root/code/fraud-detector
git add .gitea/workflows/release.yml
git commit -m "ci: build and push the release image to the Gitea registry"
git push
```

##### 4. Cut the `v0.1.0` release from the Gitea UI.
Click the **Gitea** button, log in with `gitea-admin` / `gitea2026`, open the `fraud-detector` repo, and click the **Releases** tab -> **New Release** (top right). Fill in:
- **Tag name:** `v0.1.0`
- **Target:** `main` (default)
- **Release title:** `Fraud detector v0.1.0` (any non-empty title)

Click **Publish Release**. Gitea creates the tag + the release in one step, which triggers the workflow.

##### 5. Watch the workflow fire.
Click the **Actions** tab in the repo header. A new run under the **Release** workflow is queued or in-progress. Click into it — the `build-and-publish` job now runs `docker build` and `docker push` (no longer `exit 1`), trains the model, and attaches `metrics.json`. Wait for it to finish green (about 1-3 minutes; most of the time is the first `pip install`).

##### 6. Verify from the Gitea UI.
- Return to **Releases** → click `v0.1.0`. A **Downloads** section at the bottom now lists `metrics.json`. Clicking it downloads the file.
- Open the profile avatar (top right) → **Packages** (or navigate to `http://localhost:3000/gitea-admin/-/packages`). A container package **fraud-detector** shows up with version `v0.1.0`. Clicking it reveals the full `docker pull` URL.

##### 7. Verify via Gitea's REST API.
From a VS Code terminal:
```
TOKEN=$(cat /root/.gitea/token)

curl -s -H "Authorization: token $TOKEN" \
  http://localhost:3000/api/v1/repos/gitea-admin/fraud-detector/releases/tags/v0.1.0 \
  | python3 -m json.tool | head -30

curl -s -H "Authorization: token $TOKEN" \
  'http://localhost:3000/api/v1/packages/gitea-admin?type=container' \
  | python3 -m json.tool
```
The first call shows the `v0.1.0` release with `assets[].name == "metrics.json"`. The second lists the container package with `name: "fraud-detector"`, `version: "v0.1.0"`.

##### 8. (Optional) Pull the image locally.
```
docker login localhost:3000 -u gitea-admin -p $(cat /root/.gitea/token)
docker pull localhost:3000/gitea-admin/fraud-detector:v0.1.0
docker run --rm -p 5000:5000 localhost:3000/gitea-admin/fraud-detector:v0.1.0 &
sleep 5
curl -s http://localhost:5000/health
```
`{"status":"ok"}` confirms the published image runs the same serve script the workflow built.

#### References

- Gitea Actions — workflow syntax (GitHub-Actions-compatible): https://docs.gitea.com/usage/actions/overview
- Gitea Container Registry — pushing and pulling OCI images: https://docs.gitea.com/usage/packages/container
- Releases — tagging a commit and attaching assets (concept, mirrored by Gitea's Releases UI): https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases
