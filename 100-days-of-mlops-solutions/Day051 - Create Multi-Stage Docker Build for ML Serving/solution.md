
# Task
The xFusionCorp Industries ML platform team has deployed a fraud-detection model as a Docker image. However, the current runtime image includes all packages required for the training phase and the training source itself, resulting in an unnecessarily large image. Your objective is to refactor the single-stage Dockerfile located at /root/code/ml-serve/ into a multi-stage build. This should comprise a builder stage that trains the model and generates model.pkl, followed by a runtime stage that installs only the dependencies necessary for serving and copies the trained model from the builder stage.


The Docker daemon is already running. docker version can be run in a VS Code terminal to confirm.

The project layout under /root/code/ml-serve/:

train_model.py – Fits a 10-tree RandomForest on the shared 10-row synthetic fraud set and writes /app/model.pkl via joblib.dump(...). Correct and must remain intact.
serve.py – Flask app loading the model and exposing POST /predict + GET /health on port 8080. Correct and must remain intact.
Dockerfile – A single-stage build that installs scikit-learn, pandas, numpy, joblib, and flask, runs the trainer at build time to bake the model in, and serves. The reader rewrites this file.
The end state must include:

The Dockerfile carries at least two FROM instructions; the first is given a name (e.g. AS builder) so a later stage can reference it.
The builder stage produces /app/model.pkl (the trained model).
The runtime stage contains /app/model.pkl (copied out of the builder stage) and serve.py.
The runtime stage's pip install line installs only the four packages serve.py needs: flask, joblib, numpy, scikit-learn.
docker images ml-serve:v1 lists the built image; docker run --rm -p 8090:8080 ml-serve:v1 exposes /health returning {"status": "ok"} on port 8090.
Multi-stage builds let you ship runtime images that carry only what the serving app needs — training dependencies and source files stay in the builder stage and are discarded. docker build -t ml-serve:v1 . can be re-run as each change lands; Docker re-uses cached layers when only runtime-stage lines change.

# Solution

A serving image should carry only what it needs to answer requests — not the training code, not the training-only dependencies. A **multi-stage build** splits the `Dockerfile` into a **builder** stage that trains the model and produces `model.pkl`, and a slim **runtime** stage that installs only the serving dependencies and copies the artifact out with `COPY --from=builder`. This task converts a working single-stage image into that two-stage form. The real reasoning is which dependency belongs where: `pandas` is used only by the trainer (builder-only), while `scikit-learn` is still needed at runtime to unpickle the model — so the runtime stage installs `flask`, `joblib`, `numpy`, `scikit-learn`, and the training source never ships.

> As an MLOps engineer, you slim the serving image down to its runtime closure so deployments are smaller and carry less attack surface — you are not changing what the model predicts. The model is trained on a small synthetic dataset.

#### Follow the steps below

##### 1. Confirm the starting state.
From a VS Code terminal:
```
cd /root/code/ml-serve
ls
cat Dockerfile
```
`train_model.py`, `serve.py`, and the single-stage `Dockerfile` are all staged. The current Dockerfile installs every package in one layer, bakes the trainer in, and runs the Flask server.

##### 2. Build the draft image and observe the bloat.
```
docker build -t ml-serve:v1 .
docker run --rm --entrypoint ls ml-serve:v1 /app
docker run --rm --entrypoint python3 ml-serve:v1 -c "import pandas; print(pandas.__version__)"
```
The runtime `/app/` directory contains `train_model.py` as well as `model.pkl`, and `pandas` imports cleanly — both are runtime-useless but baked into the shipped image.

##### 3. Inspect `Dockerfile`.
Open `/root/code/ml-serve/Dockerfile` in the VS Code editor. The current file has one `FROM python:3.11-slim`, one `pip install` that lumps every dependency together, and one layer that copies both Python files plus runs the trainer. The refactor splits this into a **builder** stage (trains + produces `model.pkl`) and a **runtime** stage (installs only serve deps + copies the trained model out of the builder).

##### 4. Rewrite the Dockerfile as a multi-stage build.
Replace the file contents with:
```dockerfile
# Builder stage — installs the full training stack and produces
# /app/model.pkl from the synthetic fraud dataset.
FROM python:3.11-slim AS builder

WORKDIR /app
RUN pip install --no-cache-dir scikit-learn pandas numpy joblib
COPY train_model.py /app/train_model.py
RUN python3 /app/train_model.py

# Runtime stage — installs only the serving dependencies, copies
# the trained model artefact out of the builder, and serves.
FROM python:3.11-slim AS runtime

WORKDIR /app
RUN pip install --no-cache-dir scikit-learn numpy joblib flask
COPY --from=builder /app/model.pkl /app/model.pkl
COPY serve.py /app/serve.py

EXPOSE 8080
CMD ["python3", "/app/serve.py"]
```
Save the file.

Why each piece matters:
- `AS builder` — names the first stage so the runtime can reference it.
- `COPY --from=builder /app/model.pkl /app/model.pkl` — pulls the trained artefact out of the discarded builder.
- The runtime `pip install` omits `pandas` — the serving code never uses it.
- `train_model.py` is copied only in the builder; the runtime stage never sees it.

##### 5. Re-build and verify.
```
docker build -t ml-serve:v1 .
docker run --rm --entrypoint ls ml-serve:v1 /app
```
`/app/` now lists only `model.pkl` + `serve.py`. The training source is gone.

##### 6. Confirm pandas is no longer in the runtime image.
```
docker run --rm --entrypoint python3 ml-serve:v1 \
  -c "import importlib.util; print(importlib.util.find_spec('pandas'))"
```
Output prints `None` — pandas was left behind in the builder.

##### 7. Smoke-test the serving endpoint.
Start the container mapped to a host port, query `/health`, then clean up:
```
docker run -d --rm --name ml-serve-smoke -p 8090:8080 ml-serve:v1
for i in $(seq 1 30); do curl -sf http://localhost:8090/health >/dev/null && break; sleep 0.5; done
curl -s http://localhost:8090/health
docker rm -f ml-serve-smoke
```
The `/health` call returns `{"status": "ok"}` — the multi-stage image serves correctly and ships only what it needs to.

#### References

- Multi-stage builds — the `AS <stage>` / `COPY --from=<stage>` pattern used here: https://docs.docker.com/build/building/multi-stage/
- Dockerfile reference — `FROM`, `COPY`, `RUN`, `CMD`, `EXPOSE`: https://docs.docker.com/reference/dockerfile/
