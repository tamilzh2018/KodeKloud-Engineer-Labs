# Task
The xFusionCorp Industries ML platform team has deployed the fraud-detection model using BentoML. The model is registered in BentoML's local store and is served over HTTP with the command bentoml serve, which automatically generates a Swagger UI at the server's root. Within the scaffold located at /root/code/serving/service.py, the modern @bentoml.service class API is utilized. This script loads the pre-registered fraud_detector:latest model from the store and defines the APIs, although the POST /predict handler remains unimplemented. Your objective is to implement the /predict handler to score a transaction using the loaded model. Additionally, you need to start the server on port 3000 and verify that it returns predictions.


The fraud_detector model is registered in BentoML's local store. The BentoML server is NOT pre-started — the BentoML UI button opens the Swagger surface once the server is running on port 3000.

The project layout under /root/code/serving/:

service.py – BentoML service (@bentoml.service class FraudService). The model-store load (bentoml.models.BentoModel + bentoml.sklearn.load_model in __init__) and the last_predictions API are wired. The predict handler body is left as a TODO — it returns an error until authored. The handler takes the amount/hour/num_tx_past_day parameters and returns {"is_fraud": <int>}.
train.csv – The 10-row source used at startup to train and register the model with bentoml.sklearn.save_model("fraud_detector", model).
The end state must include:

bentoml models list lists fraud_detector in the store.
curl http://localhost:3000/ returns HTTP 200 – The Swagger UI is reachable once the server is running.
POST /predict with a valid payload returns {"is_fraud": 0} or {"is_fraud": 1}.
Two distinct payloads return different is_fraud values – The handler scores the posted features.
Suggested payloads: {"amount": 3200, "hour": 23, "num_tx_past_day": 5} (high-value, late-night—expected to flag fraud); {"amount": 25.5, "hour": 10, "num_tx_past_day": 1} (low-value, daytime).

# Solution

Flask and FastAPI make you wire the server yourself; BentoML is a framework built for model serving — it keeps a model store and turns a service class into a runnable, packageable API. This task registers the trained model in the store and authors a `@bentoml.service` class with a typed `@bentoml.api` predict method, then serves it with `bentoml serve`.

> As an MLOps engineer, you reach for a serving framework like BentoML so packaging, versioning, and the API surface are standardized instead of hand-rolled per project — you are not changing the model. The data is synthetic.

#### Follow the steps below

##### 1. Confirm the starting state.
From a VS Code terminal:
```
cd /root/code/serving
bentoml models list
cat service.py
```
`fraud_detector` is registered in the BentoML store. `service.py` uses the modern `@bentoml.service` class API: the model is declared with `bentoml.models.BentoModel(...)` and loaded in `__init__`; the `last_predictions` API is wired; the `predict` handler is a `# TODO` that returns an error.

##### 2. Author the predict handler.
Open `/root/code/serving/service.py` in the VS Code editor. Replace the `return {"error": ...}` stub with the scoring logic:
```python
    @bentoml.api
    def predict(
        self, amount: float, hour: int, num_tx_past_day: int
    ) -> Dict[str, Any]:
        features = np.array([[amount, hour, num_tx_past_day]])
        is_fraud = int(self.model.predict(features)[0])
        self._history.append({
            "amount": amount,
            "hour": hour,
            "num_tx_past_day": num_tx_past_day,
            "is_fraud": is_fraud,
        })
        return {"is_fraud": is_fraud}
```
The `@bentoml.api` method's typed parameters (`amount`/`hour`/`num_tx_past_day`) become the JSON request body and drive the Swagger schema. Save the file.

##### 3. Start the server.
```
cd /root/code/serving
bentoml serve service:FraudService --host 0.0.0.0 --port 3000 &
sleep 5
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:3000/
```
Once it prints `200`, open the **BentoML UI** button — the Swagger surface loads with `predict` and `last_predictions`.

##### 4. Verify scoring from the Swagger UI.
Expand `POST /predict` → **Try it out**, submit a high-value late-night payload, and **Execute**:
```json
{"amount": 3200, "hour": 23, "num_tx_past_day": 5}
```
The response is `{"is_fraud": 1}`. Submit a low-value daytime payload — `{"amount": 25.5, "hour": 10, "num_tx_past_day": 1}` — and it returns `{"is_fraud": 0}`. The two distinct payloads score differently.

##### 5. Cross-check the audit log.
```
curl -s -X POST -H 'Content-Type: application/json' -d '{}' \
  http://localhost:3000/last_predictions | python3 -m json.tool
```
Every prediction the handler recorded appears in the `predictions` array with its inputs and `is_fraud` label.

#### References

- BentoML services — the `@bentoml.service` class API and `@bentoml.api` methods: https://docs.bentoml.com/en/latest/build-with-bentoml/services.html
- Loading and managing models from the store: https://docs.bentoml.com/en/latest/build-with-bentoml/model-loading-and-management.html
- `bentoml serve` — running the HTTP server: https://docs.bentoml.com/en/latest/reference/cli.html
