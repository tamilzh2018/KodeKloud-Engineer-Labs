# Task:
The xFusionCorp Industries ML platform team stages a materialisation script (materialize.sh) under /root/code/fraud-detection/feature_repo/ so the batch job that populates the Feast online store is always repeatable. The registry has already been applied against a correct features.py, but running the script writes zero rows into the online sqlite store. Your task is to correct materialize.sh so ./materialize.sh populates the online store, then author fetch_features.py to read the features back via store.get_online_features() and confirm a non-null amount for a known customer.


The Feast UI is already running on port 8888. The Feast UI button at the top of the lab can be opened to confirm—the dashboard loads the fraud_detection project, the customer entity, and the customer_transaction_features feature view. Materialisation status is not visible in the UI; the online store is inspected from the terminal.

The repository layout under /root/code/fraud-detection/feature_repo/:

feature_store.yaml – Local provider, sqlite online store at data/online_store.db. Correct.
features.py – Declares the customer entity (join_keys=["customer_id"]) and the customer_transaction_features view over the transactions source. Correct.
data/transactions.parquet – 200-row synthetic source, event timestamps from 2024-01-01 onward.
data/registry.db – Already written by feast apply at startup.
materialize.sh – Single-purpose shell script that calls feast materialize-incremental "$END_DATE".
fetch_features.py – Reads features back from the online store; the store.get_online_features(...) call is left as a # TODO.
The end state must include:

materialize.sh's end date is an ISO-8601 date on or after 2024-01-01, and data/online_store.db is populated (on-disk size comfortably larger than the bare sqlite header, ≥ 4 KB).
fetch_features.py calls store.get_online_features(features=["customer_transaction_features:amount", …], entity_rows=[{"customer_id": i}, …]) and writes online_features.json.
online_features.json carries at least one non-null amount value for a customer id present in the source.
feast materialize-incremental takes a single ISO-8601 end date and uses the feature view's TTL to pick the start watermark on the first run. Run ./materialize.sh and read its output — the summary line reports how many rows were written into the online store, which is where the zero shows up.

# Solution

**Materialisation** is how Feast moves feature values from the offline source into the **online store** — the low-latency key-value store that serving reads at inference time. `feast materialize-incremental <end_date>` writes every event between a start watermark (derived from the feature view's TTL on the first run) and `<end_date>`; pick an end date *before* the data exists and it writes zero rows. Materialising is only half the loop — the payoff is **reading features back** for a live entity via `store.get_online_features(...)`. This task fixes the materialisation window so the online store is populated, then reads a customer's features back to prove the round trip works.

> As an MLOps engineer, you move features into the online store so serving reads the exact same values training saw — you are not engineering new features; the data is synthetic.

#### Follow the steps below

##### 1. Confirm the starting state.
Open the **Feast UI** button at the top of the lab — the `fraud_detection` project shows the `customer` entity (`join_keys=["customer_id"]`, Value Type `INT64`; the **Entities** tab also lists Feast's built-in `__dummy`) and the `customer_transaction_features` view. The registry is correct; only the materialisation remains. From a VS Code terminal:
```
cd /root/code/fraud-detection/feature_repo
ls -l data/
cat materialize.sh
```
`data/registry.db` exists (written by startup). `data/online_store.db` is absent or barely past the sqlite header size. `materialize.sh` ships with `END_DATE="1970-12-31T00:00:00"`.

##### 2. Run the draft script and observe the empty online store.
```
./materialize.sh
ls -l data/online_store.db
```
The script prints `Materializing 1 feature views to 1970-12-31 00:00:00+00:00 …` and then a single line showing a reversed date window (`from <today> to 1970-12-31`) with no rows reported. `data/online_store.db` stays at the sqlite header size (~16 KB) because no events fall inside the window.

##### 3. Confirm the online store is empty via the Feast SDK.
```
python3 -c "
from feast import FeatureStore
fs = FeatureStore(repo_path='.')
resp = fs.get_online_features(
    features=['customer_transaction_features:amount'],
    entity_rows=[{'customer_id': i} for i in range(1, 11)],
).to_dict()
print(resp)
"
```
Every `amount` value comes back `None`.

##### 4. Fix the `END_DATE`.
Open `materialize.sh` in the VS Code editor. The source's event timestamps start at `2024-01-01`, so any end date on or after that picks up the full 200-row window. A safe choice that also tolerates later additions:
```bash
END_DATE="2025-12-31T23:59:59"
```
Save the file.

##### 5. Re-run materialisation.
```
./materialize.sh
ls -l data/online_store.db
```
The script now logs rows written per feature view and `online_store.db` grows well beyond 4 KB.

##### 6. Author the online fetch and run it.
Materialisation only pays off when something reads the features back. Open `fetch_features.py` and complete the TODO — call `store.get_online_features(...)` for the three features over customers 1–5, then `.to_dict()`:
```python
result = store.get_online_features(
    features=[
        "customer_transaction_features:amount",
        "customer_transaction_features:hour",
        "customer_transaction_features:num_tx_past_day",
    ],
    entity_rows=[{"customer_id": i} for i in range(1, 6)],
).to_dict()
```
Run it from the feature repo:
```
python3 fetch_features.py
```
It writes `online_features.json`; the `amount` list carries non-null values for the materialised customers. The fraud-detection online store is now serving ready-to-query features.

##### 7. Verify in the Feast UI.
Refresh the **Feast UI** tab. The registry view is unchanged (the UI is registry-only and does not surface materialisation rows), which confirms the fix did not alter the feature declarations.

#### References
- Feast `materialize-incremental` (CLI, end date + TTL watermark): https://docs.feast.dev/reference/feast-cli-commands
- Feast online store (low-latency serving store): https://docs.feast.dev/getting-started/components/online-store
- Feast feature retrieval — `get_online_features`: https://docs.feast.dev/getting-started/concepts/feature-retrieval
