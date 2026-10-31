# Task
The xFusionCorp Industries MLOps team is standing up the serving path of their fraud-detector platform — the route a model takes from a training run to a live prediction endpoint. The backing stack is already running: a SeaweedFS object store (with a seeded training dataset) and an MLflow tracking server. Your task is to drive that path end to end: run the training script to produce a run, complete register.py so it registers the run as the fraud-detector model and assigns the production alias, then start the FastAPI inference server so it serves live predictions from the aliased model.


The MLflow UI and SeaweedFS Filer buttons at the top of the lab open those UIs. Pre-staged state:

SeaweedFS bucket data holds transactions.csv; the mlflow-artifacts bucket is empty until a run logs to it.
MLflow experiment fraud-detection does not exist yet and the Model Registry is empty.
Under /root/code/: train.py, serve.py, and config.yaml are reference scripts (no edits needed); register.py ships with its register + promote step as an unfinished TODO for you to complete. train.py reads the dataset from SeaweedFS and logs the run + artefacts to MLflow; the FastAPI server's background loader polls the registry for models:/fraud-detector@production and loads the model once the alias exists.
The end state must include:

MLflow experiment fraud-detection has at least one run; run artefacts are in the mlflow-artifacts SeaweedFS bucket.
A Registered Model named fraud-detector exists with the production alias assigned to the version sourced from the run, set in code by register.py.
POST http://localhost:8085/predict with {"features": [100.5, 12, 3]} returns {"prediction": 0} or {"prediction": 1} (tests poll up to 60 s).
This task builds the serving path of the platform: training logs a run + artefacts to MLflow (backed by SeaweedFS object storage), the registry production alias is the stable handle production code targets (models:/fraud-detector@production), and the serving process resolves that alias at load time — so promoting a new model later is an alias move, not a redeploy.
# Solution

**The platform.** xFusionCorp runs `fraud-detector` as a small production ML system: models are trained and served (logged to MLflow with artefacts in object storage, served from FastAPI behind the `production` registry alias); an automated loop retrains on drift and promotes by moving that alias; the server is deployed by GitOps; and the running service is observed with Prometheus + Grafana. **This task builds the serving path** — the route from a training run to a live endpoint.

You drive that path end to end: a training run logs a model + artefacts to MLflow (backed by SeaweedFS), you register the run and put the `production` alias on it (in code, via `register.py`) so the alias becomes the stable handle production targets, and a FastAPI server resolves `models:/fraud-detector@production` at load time and answers `/predict`.

> As an MLOps engineer, you wire training, registry, and serving into one path so a model goes from run to live endpoint with no manual copy steps — you are not judging model quality; the model and data are synthetic.

#### Follow the steps below

##### 1. Confirm the pre-staged environment.
From a VS Code terminal:
```
curl -s -o /dev/null -w 'mlflow=%{http_code}\n' http://localhost:5000/
curl -s -o /dev/null -w 'seaweed=%{http_code}\n' http://localhost:8333/status
```
MLflow and SeaweedFS answer `200`. The `fraud-detection` experiment does not exist yet, the Model Registry is empty, and nothing is listening on `:8085` — you produce all of that in the steps below.

##### 2. Train — produce the run and artefacts.
The reference `train.py` reads the dataset from the SeaweedFS `data` bucket, trains the model, and logs the run + artefacts to MLflow:
```
cd /root/code
python3 train.py
```
It prints the new run id. Click the **SeaweedFS Filer** button → `/buckets/mlflow-artifacts/` now holds a run's `model/` directory (`MLmodel` + `model.pkl` + `conda.yaml`).

##### 3. Register + promote — complete and run `register.py`.
`register.py` already looks up the latest run in `fraud-detection`; author the `TODO` so it registers that run as `fraud-detector` and moves the `production` alias onto the new version. Add these two lines where the `TODO` is:
```python
mv = mlflow.register_model(f"runs:/{run_id}/model", MODEL_NAME)
client.set_registered_model_alias(MODEL_NAME, ALIAS, mv.version)
print(f"[register] promoted {MODEL_NAME} v{mv.version} -> @{ALIAS}")
```
Then run it:
```
python3 /root/code/register.py
```
It prints `promoted fraud-detector v1 -> @production`. (You can confirm in the **MLflow UI → Models → fraud-detector** that Version 1 now carries the `@production` alias — but the registration and alias were both set in code, not by clicking.)

##### 4. Serve — start the inference server.
Start the FastAPI server in the background. It boots immediately; its background loader polls the registry for `models:/fraud-detector@production` and pulls the model from SeaweedFS once the alias resolves:
```
nohup python3 /root/code/serve.py > /tmp/serve.log 2>&1 &
```
Wait for the loader to pick the model up (`/health` flips from `loading` to `healthy`):
```
for i in 1 2 3 4 5 6; do
  curl -s http://localhost:8085/health
  echo
  sleep 3
done
```
`/health` transitions to `{"status":"healthy", "model_uri":"models:/fraud-detector@production"}`.

##### 5. Call `/predict`.
```
curl -s -X POST http://localhost:8085/predict \
  -H 'Content-Type: application/json' \
  -d '{"features": [100.5, 12, 3]}'
```
Response: `{"prediction": 0}` or `{"prediction": 1}`.

#### References

- MLflow — Model Registry (registering runs, model versions, and aliases like `models:/<name>@<alias>`): https://mlflow.org/docs/latest/ml/model-registry/
- FastAPI — first steps (the serving app pattern): https://fastapi.tiangolo.com/tutorial/first-steps/
