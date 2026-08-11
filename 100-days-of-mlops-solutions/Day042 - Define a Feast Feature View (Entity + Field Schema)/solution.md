# Task
The xFusionCorp Industries ML platform team keeps the fraud-detection feature definitions in a Feast repository at /root/code/fraud-detection/feature_repo/. A draft features.py exists there: the source, the entity, and the feature-view shell are scaffolded, but the entity's join key and the served feature schema are unfinished. Your task is to author the entity join key and the feature schema to match the source in data/transactions.parquet, apply the registry, and confirm the customer_transaction_features view in the Feast UI.


The Feast UI is already running on port 8888. The Feast UI button at the top of the lab can be opened to confirm—the dashboard loads the fraud_detection project with one entity and one feature view carrying the draft declarations.

The repository layout under /root/code/fraud-detection/feature_repo/:

feature_store.yaml – The Feast config (project fraud_detection, local provider, sqlite online store, file offline store). Correct and must remain intact.
data/transactions.parquet – A 200-row synthetic source keyed by customer_id; carries amount as Float32, hour + num_tx_past_day + is_fraud as Int64, and an event_timestamp column. Correct and must remain intact.
features.py – Declares the FileSource, the customer Entity (join key unfinished — uses a placeholder that is not in the source), and the customer_transaction_features FeatureView (schema unfinished — only amount is declared, at a placeholder type). Author the join key and the full served schema here.
data/registry.db – Written by feast apply at startup from the draft; must be re-applied after the edits so the registry reflects the authored declarations.
The end state must include:

The customer entity in the registry has join_keys = ["customer_id"].
The customer_transaction_features view declares all three served features with source-matching dtypes: amount Float32, hour Int64, num_tx_past_day Int64 (the is_fraud label is not served).
feast apply exits without error and the Feast UI reflects the authored entity and feature-view schema.
The Feast UI's Entities and Feature Views tabs surface the applied values directly—the current (draft) values are visible there so the required change is easy to eyeball against the task's end-state.
# Solution

In Feast, a feature repository is **defined in Python**. Three objects describe what the store serves: a **`FileSource`** points at the raw data; an **`Entity`** names the key that rows are looked up by (its `join_keys` must be a *real column* in the source); and a **`FeatureView`** binds an entity to a typed **schema** — one `Field(name, dtype)` per served feature, where each `dtype` must match the source column's type (a wrong dtype means silent coercion or lookup failures downstream). `feast apply` reads these definitions and writes them into the registry. This task authors the entity's join key and the feature view's schema so both line up with the source, then applies them.

> As an MLOps engineer, you declare feature definitions once so training and serving read the exact same values — you are not engineering new features; the data is synthetic.

#### Follow the steps below

##### 1. Confirm the starting state.
Open the **Feast UI** button at the top of the lab — the `fraud_detection` project is loaded with the `customer` entity (the **Entities** tab shows 2 — `customer` plus Feast's built-in `__dummy`) and one feature view (`customer_transaction_features`). From a VS Code terminal:
```
ls /root/code/fraud-detection/feature_repo/
cat /root/code/fraud-detection/feature_repo/data/transactions.parquet | head -c 0
```
The repository is fully scaffolded, the synthetic transactions parquet exists, and `feast apply` has already been run once against the draft `features.py`.

##### 2. Inspect the draft in the UI.
In the Feast UI:
- Open the **Entities** tab → click `customer`. The **Join keys** cell reads `id` — a placeholder; the source file is keyed by `customer_id`.
- Open the **Feature Views** tab → click `customer_transaction_features` → the **Schema** panel lists only `amount`, declared as `String`. The schema is unfinished: `hour` and `num_tx_past_day` aren't served yet, and `amount`'s type is wrong (the parquet writer emits it as `Float32`).

The module docstring in `features.py` records the source's columns and types — your spec for what to author.

##### 3. Open `features.py`.
Open `/root/code/fraud-detection/feature_repo/features.py` in the VS Code editor. Two `# TODO`s: the `Entity` join key, and the `FeatureView` schema.

##### 4. Author the join key.
Set the `Entity`'s `join_keys` to the source's key column (the `value_type=ValueType.INT64` is pre-set to match the source's `customer_id` type, so the entity registers with a real type rather than `INVALID`):
```python
customer = Entity(
    name="customer",
    join_keys=["customer_id"],
    value_type=ValueType.INT64,
    description="Customer identifier keyed by the transactions source.",
)
```

##### 5. Author the feature schema.
Declare all three served features, each typed to match its source column (correct `amount` to `Float32`, add `hour` and `num_tx_past_day` as `Int64`; do not serve the `is_fraud` label):
```python
customer_transaction_features = FeatureView(
    name="customer_transaction_features",
    entities=[customer],
    ttl=timedelta(days=365),
    schema=[
        Field(name="amount", dtype=Float32),
        Field(name="hour", dtype=Int64),
        Field(name="num_tx_past_day", dtype=Int64),
    ],
    source=transactions_source,
    online=True,
)
```
Save the file.

##### 6. Re-apply the registry.
`feast apply` diffs the current `features.py` against the applied registry and updates any changed declarations:
```
cd /root/code/fraud-detection/feature_repo && feast apply
```
The command prints the entity + feature view updates and exits without error.

##### 7. Verify in the Feast UI.
Refresh the **Feast UI** tab. The **Entities** tab now shows `customer` with **Join keys** `customer_id` and **Value Type** `INT64`, and the **Feature Views** tab shows the `customer_transaction_features` schema with `amount` (`Float32`), `hour` (`Int64`), and `num_tx_past_day` (`Int64`). The registry is consistent with the source. (Feast's built-in `__dummy` entity still shows `INVALID` — that one is internal and unset by design.)

#### References
- Feast concepts — Feature View (entity binding, schema, ttl, source): https://docs.feast.dev/getting-started/concepts/feature-view
- Feast concepts — Entity (join keys): https://docs.feast.dev/getting-started/concepts/entity
- Feast type system (`feast.types`, `Field` dtypes): https://docs.feast.dev/reference/type-system
