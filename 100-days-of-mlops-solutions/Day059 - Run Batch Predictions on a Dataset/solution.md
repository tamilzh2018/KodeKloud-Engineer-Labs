# Task 
The xFusionCorp Industries ML platform team processes the overnight batch of transactions using a fraud-detection model. This process is executed with a standalone script that reads from input.csv, applies the pre-trained RandomForest model to each row, and generates predictions.csv. A scaffold for the script, located at /root/code/serving/batch_predict.py, includes the paths for the model, input, and output; however, the scoring flow is currently marked as TODO.

Your objective is to implement the batch scoring process within the script. Specifically, you need to ensure that it reads input.csv, utilizes the pre-trained model to score each row, and outputs predictions.csv, which should include a column for integer prediction class labels. After implementing the flow, run the script.


The project layout under /root/code/serving/:

model.pkl – Deterministic RandomForest trained at startup on the shared amount / hour / num_tx_past_day → is_fraud synthetic dataset.
input.csv – The 10-row batch input: three feature columns, no label column.
batch_predict.py – The scorer scaffold. The MODEL_PATH / INPUT_CSV / OUTPUT_CSV constants are set; the scoring flow (load the model, read the input, add an integer prediction column via model.predict(...), write the output) is left as a TODO to author.
The end state must include:

/root/code/serving/predictions.csv exists.
The output carries the three input columns plus a prediction column.
Every value in prediction is 0 or 1 (integer class label), not a float probability.
The output row count matches the input row count.
# Solution

Batch (offline) scoring runs a whole file of records through a model on a schedule and writes the results to disk — no HTTP server, no per-request latency. This task authors that scorer: load the persisted model, read the input CSV, predict a class label for every row, and write a `predictions.csv`.

> As an MLOps engineer, you author scorers like this for scheduled jobs, and the detail that bites teams is method choice — `model.predict` emits the integer class labels (0/1) downstream systems store, while `model.predict_proba` emits floats that silently corrupt a column expected to hold labels. The data is synthetic.

#### Follow the steps below

##### 1. Confirm the starting state.
From a VS Code terminal:
```
cd /root/code/serving
cat batch_predict.py
head -3 input.csv
```
`model.pkl` and `input.csv` are staged. `batch_predict.py` sets the `MODEL_PATH` / `INPUT_CSV` / `OUTPUT_CSV` constants, but the scoring flow is a `# TODO` — running it as-is produces no `predictions.csv`.

##### 2. Author the batch scoring flow.
Open `/root/code/serving/batch_predict.py` in the VS Code editor. Below the path constants, add the flow:
```python
model = joblib.load(MODEL_PATH)

df = pd.read_csv(INPUT_CSV)
features = df[["amount", "hour", "num_tx_past_day"]]

df["prediction"] = model.predict(features)

df.to_csv(OUTPUT_CSV, index=False)
print(f"Wrote {len(df)} rows to {OUTPUT_CSV}")
```
Use `model.predict(...)` — it returns integer class labels (`0`/`1`). `model.predict_proba(...)` would return float probabilities, which is *not* the class-label shape downstream consumers expect.

Save the file.

##### 3. Run the scorer.
```
python3 batch_predict.py
head -3 predictions.csv
```
The script prints `Wrote 10 rows to /root/code/serving/predictions.csv`. The CSV carries the three input columns plus a `prediction` column.

##### 4. Verify the output shape.
```
python3 -c "
import pandas as pd
df = pd.read_csv('predictions.csv')
print(df['prediction'].value_counts())
print('dtype:', df['prediction'].dtype)
print('rows:', len(df))
"
```
The `prediction` column holds integer class labels (`0` and `1`), and the row count matches `input.csv` (10). Every overnight transaction now carries a fraud label ready for downstream consumers.

#### References

- scikit-learn `predict` vs `predict_proba` — class labels vs probabilities: https://scikit-learn.org/stable/glossary.html#term-predict
- pandas `read_csv` / `to_csv` — reading and writing the batch: https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html
- `joblib.load` — loading the persisted estimator: https://joblib.readthedocs.io/en/stable/generated/joblib.load.html
