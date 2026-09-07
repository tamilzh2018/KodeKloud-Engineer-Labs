# Task 
The xFusionCorp Industries ML platform team has developed a fraud-detection model that is accessible via a FastAPI service. This service features an auto-generated Swagger UI available at /docs. In the draft app.py file located at /root/code/serving/, the pre-trained model is loaded and the /health endpoint is implemented. However, the PredictRequest schema and the POST /predict handler have not yet been completed.

Your task is to finalize the app.py file by defining the typed request model and implementing the /predict handler. Additionally, ensure the server operates on port 8085, and verify that it successfully scores transactions through the Swagger UI while rejecting any invalid input.


FastAPI + uvicorn are baked into the lab image. The FastAPI Swagger UI button opens /docs once the server is running on port 8085.

The project layout under /root/code/serving/:

model.pkl – Deterministic RandomForest trained at startup on the shared amount / hour / num_tx_past_day → is_fraud synthetic dataset.
train.csv – The 10-row source used to fit the model.
app.py – FastAPI app. /health, the root→/docs redirect, the response models, and GET /last-predictions are wired. Two things are left as TODOs to author:
TODO 1 – the PredictRequest model's three typed fields (amount, hour, num_tx_past_day), with types and range constraints that drive FastAPI's request validation + Swagger schema.
TODO 2 – the POST /predict handler body (which returns 501 until authored): build the feature row, score it with MODEL.predict(...), record it, and return PredictResponse.
The end state must include:

The Swagger UI at /docs is reachable (the FastAPI Swagger UI button loads it).
POST /predict with a valid payload returns {"is_fraud": 0} or {"is_fraud": 1} (HTTP 200).
Two distinct payloads return different is_fraud values – The handler reads the posted features.
POST /predict with an out-of-range field (e.g. hour: 25) returns HTTP 422 – The typed model rejects invalid input before the handler runs.
Suggested payloads: {"amount": 3200, "hour": 23, "num_tx_past_day": 5} (high-value, late-night—expected to flag fraud); {"amount": 25.5, "hour": 10, "num_tx_past_day": 1} (low-value, daytime—expected to pass).

# Solution

FastAPI serves a model over HTTP like Flask, but adds two things a production API wants: typed request validation and self-documenting endpoints. This task authors a Pydantic `PredictRequest` model with field constraints and the `POST /predict` handler, then serves it under uvicorn — so malformed input is rejected with an automatic `422` and the interactive Swagger UI at `/docs` documents the contract.

> As an MLOps engineer, you put a typed schema in front of a model so bad input is rejected at the edge, not deep in the scoring code — you are not tuning the model. The data is synthetic.

#### Follow the steps below

##### 1. Confirm the starting state.
From a VS Code terminal:
```
cd /root/code/serving
sed -n '33,80p' app.py
```
`PredictRequest` has no fields (`pass`) and the `POST /predict` handler is a `# TODO` that raises `501`. `/health`, the root→`/docs` redirect, and `/last-predictions` are already wired.

##### 2. Author the request model (TODO 1).
Open `/root/code/serving/app.py` in the VS Code editor. Replace the `pass` in `PredictRequest` with three typed, validated fields:
```python
class PredictRequest(BaseModel):
    amount: float = Field(..., description="Transaction value in USD.")
    hour: int = Field(..., ge=0, le=23, description="Hour of day (0-23).")
    num_tx_past_day: int = Field(..., ge=0, description="Transactions in the past 24 h.")
```
The `ge`/`le` constraints make FastAPI reject out-of-range input with HTTP `422` automatically, and they drive the Swagger schema.

##### 3. Author the predict handler (TODO 2).
Replace the `raise HTTPException(...)` stub with the scoring logic:
```python
@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest) -> PredictResponse:
    features = np.array([[req.amount, req.hour, req.num_tx_past_day]])
    is_fraud = int(MODEL.predict(features)[0])
    prediction_history.append({
        "amount": req.amount,
        "hour": req.hour,
        "num_tx_past_day": req.num_tx_past_day,
        "is_fraud": is_fraud,
    })
    return PredictResponse(is_fraud=is_fraud)
```
Save the file.

##### 4. Start the server.
```
cd /root/code/serving
uvicorn app:app --host 0.0.0.0 --port 8085 &
sleep 2
curl -s http://localhost:8085/health
```
Health returns `{"status":"ok"}`. Open the **FastAPI Swagger UI** button — the root redirects to `/docs` and `POST /predict` now shows the typed `amount`/`hour`/`num_tx_past_day` schema.

##### 5. Verify scoring from the Swagger UI.
Expand `POST /predict` → **Try it out**, submit a high-value late-night payload, and **Execute**:
```json
{"amount": 3200, "hour": 23, "num_tx_past_day": 5}
```
The response is `{"is_fraud": 1}`. Submit a low-value daytime payload — `{"amount": 25.5, "hour": 10, "num_tx_past_day": 1}` — and it returns `{"is_fraud": 0}`. The two distinct payloads score differently.

##### 6. Verify the typed validation.
Submit an out-of-range payload (or from the terminal):
```
curl -s -o /dev/null -w '%{http_code}\n' -X POST \
  -H 'Content-Type: application/json' \
  -d '{"amount": 100, "hour": 25, "num_tx_past_day": 1}' \
  http://localhost:8085/predict
```
The server answers `422` — `hour=25` violates the `le=23` constraint, so FastAPI rejects the request before the handler runs. The `/last-predictions` audit log records only the valid submissions.

#### References

- FastAPI request body — declaring a Pydantic model as the request schema: https://fastapi.tiangolo.com/tutorial/body/
- Pydantic numeric field constraints (`ge`/`le`) that drive `422` validation: https://fastapi.tiangolo.com/tutorial/path-params-numeric-validations/
- Running a FastAPI app with uvicorn: https://fastapi.tiangolo.com/deployment/manually/
