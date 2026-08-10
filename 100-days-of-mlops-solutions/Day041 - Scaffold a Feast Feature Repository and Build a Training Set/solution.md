# Task
The xFusionCorp Industries ML platform team is adopting Feast as the feature store for their fraud-detection workflow. The first steps are to scaffold a working feature repository with the Feast CLI, apply the starter definitions to the local registry, build a point-in-time training set from the offline store, and confirm everything loads in the Feast UI. Your task is to initialise a feature repository under /root/code/, apply the registry, complete the pre-staged build_training_set.py so it generates a training set via get_historical_features, and verify the project in the Feast UI.


Feast is already installed in the lab image and the feast CLI is on PATH.

The target project layout:

/root/code/feature_repo/feature_repo/feature_store.yaml – The feast init scaffold config (provider, registry, online/offline stores).
/root/code/feature_repo/feature_repo/data/registry.db – Written by feast apply from the repo root.
/root/code/feature_repo/feature_repo/feature_definitions.py – The starter feature definitions Feast ships with the scaffold (a driver_hourly_stats feature view over data/driver_stats.parquet).
/root/code/build_training_set.py – Pre-staged. Reads (driver_id, event_timestamp) rows from the source and is meant to build a training set via get_historical_features; the retrieval call is left as a # TODO.
The end state must include:

The /root/code/feature_repo/feature_repo/ directory is populated with the feast init scaffold.
feature_store.yaml parses as valid YAML and carries the project, provider, and registry keys.
data/registry.db exists – feast apply completed without error.
build_training_set.py calls store.get_historical_features(entity_df=…, features=["driver_hourly_stats:conv_rate", "driver_hourly_stats:acc_rate", "driver_hourly_stats:avg_daily_trips"]).to_df(), and running it writes /root/code/training_set.parquet carrying those joined feature columns (a point-in-time training set).
The Feast UI button at the top of the lab opens a responsive dashboard that lists the scaffold's project.
feast ui is a long-running process; run it in a second VS Code terminal (or append & to the command) so the shell remains usable. The UI loads the registry at start-up—start the UI after feast apply has written registry.db.
# Solution

A **feature store** like Feast is the shared layer between feature engineering and model serving: it keeps feature *definitions* (entities, feature views, schemas) in a versioned **feature repository** + **registry**, so training and serving read the *same* features. `feast init` scaffolds a repo, `feast apply` registers its definitions, and `feast ui` serves a read-only dashboard. The store then serves features two ways: the **offline** path — `get_historical_features` — builds **training** data with a *point-in-time* join (each row sees a feature's value *as of* its event timestamp, so no future data leaks into training); the **online** path serves the latest values at inference (covered later). This task scaffolds the repo, builds a point-in-time training set from the offline store, and opens the UI.

> As an MLOps engineer, you scaffold a shared feature store so training and serving read the exact same feature values — you are not engineering new features; the data is synthetic.

#### Follow the steps below

##### 1. Confirm the starting state.
From a VS Code terminal, verify the Feast CLI is available and the target directory is empty:
```
feast version
ls /root/code/
```
The `feast version` output prints the installed Feast version. `/root/code/` exists but has no `feature_repo/` yet.

##### 2. Initialise the feature repository.
`feast init` scaffolds a complete starter project — `feature_store.yaml`, `feature_definitions.py`, a sample dataset, and a local SQLite-backed online store:
```
cd /root/code
feast init feature_repo
```

##### 3. Apply the starter definitions to the registry.
`feast apply` reads the example repo and writes the registry + schema files. The command runs from the inner `feature_repo/` directory where `feature_store.yaml` lives:
```
cd /root/code/feature_repo/feature_repo
feast apply
```

##### 4. Inspect the scaffold.
```
cat feature_store.yaml
ls data/
```
`feature_store.yaml` carries `project`, `provider`, `registry`, `online_store`, and `offline_store` keys. The `data/` directory now contains `registry.db` — the proof that `feast apply` completed.

##### 5. Build a point-in-time training set.
The store's offline path turns feature definitions into training data. Open `/root/code/build_training_set.py` — it reads `(driver_id, event_timestamp)` rows from the scaffold's source; complete the TODO to join the features as of each timestamp:
```python
training_df = store.get_historical_features(
    entity_df=entity_df,
    features=[
        "driver_hourly_stats:conv_rate",
        "driver_hourly_stats:acc_rate",
        "driver_hourly_stats:avg_daily_trips",
    ],
).to_df()
```
Run it (the `FeatureStore(repo_path=…)` inside points at the applied repo):
```
python3 /root/code/build_training_set.py
```
It writes `/root/code/training_set.parquet` — the entity rows now carry `conv_rate`, `acc_rate`, and `avg_daily_trips` joined *as of* each event timestamp. That point-in-time join is what keeps training honest (a row never sees a feature value from after its own timestamp).

##### 6. Start the Feast UI.
The Feast UI is a read-only dashboard over the registry. It must run from a feature_repo directory. Start it in the background so the terminal stays usable:
```
feast ui --host 0.0.0.0 --port 8888 &
```
Wait a few seconds for the server to bind port `8888`.

##### 7. Verify in the Feast UI.
Open the **Feast UI** button at the top of the lab. The dashboard lists the scaffold's project (`feature_repo`) with **Data Sources (3)**, **Entities (2)** — `driver` plus Feast's built-in `__dummy` entity (used by on-demand views) — **Features (12)**, **Feature Views (4)** (`driver_hourly_stats` and `driver_hourly_stats_fresh`, plus the on-demand `transformed_conv_rate` and `transformed_conv_rate_fresh`), and **Feature Services (3)** (`driver_activity_v1` through `driver_activity_v3`). The **Lineage** tab renders the source → entity → view → service graph. The UI loading cleanly confirms the registry is valid and Feast is wired end-to-end. (The entities show **Value Type** `INVALID` — this is cosmetic: the stock `feast init` definitions don't set an entity `value_type`, so Feast infers the type from the source. It doesn't affect the training-set build.)

#### References
- Feast quickstart (`feast init` / `feast apply` / `feast ui`): https://docs.feast.dev/getting-started/quickstart
- Feast concepts — feature repository, registry, feature store: https://docs.feast.dev/getting-started/concepts
- Feast CLI commands reference: https://docs.feast.dev/reference/feast-cli-commands
- Feast feature retrieval — `get_historical_features` (point-in-time training data): https://docs.feast.dev/getting-started/concepts/feature-retrieval

# What is feast in MLops
**Feast** is an **open-source feature store** used in MLOps.

In simple terms, Feast helps you **manage, store, and serve the input features that machine-learning models need**, consistently across training and production.

### Why do you need Feast?

Suppose you're building a fraud-detection model. Your model might use features like:

* `transaction_count_last_24h`
* `average_transaction_amount`
* `user_account_age`
* `number_of_failed_logins`

During **training**, you need historical values of these features.

During **prediction in production**, you need the **latest values** quickly.

Feast provides a common system for both:

```text
                 ┌──────────────────┐
                 │   Data Sources    │
                 │ DB / Data Lake    │
                 │ Kafka / BigQuery  │
                 └────────┬─────────┘
                          │
                          ▼
                    ┌───────────┐
                    │   Feast   │
                    │  Feature  │
                    │   Store   │
                    └─────┬─────┘
                          │
              ┌───────────┴───────────┐
              ▼                       ▼
       Offline Store            Online Store
       Historical data          Latest values
              │                       │
              ▼                       ▼
       Model Training          Real-time Prediction
```

### The two important parts

**1. Offline store**

Used primarily for **training**.

It contains historical feature values, allowing you to create training datasets such as:

```text
user_id | timestamp  | purchases_7d | avg_amount
--------------------------------------------------
101     | Jan 1      | 12            | 45.2
101     | Jan 2      | 15            | 47.8
102     | Jan 1      | 3             | 21.4
```

**2. Online store**

Used for **real-time inference**.

When your model receives `user_id=101`, Feast can retrieve the latest features quickly:

```text
user_id = 101

purchases_7d = 18
avg_amount   = 52.3
account_age  = 742 days
```

### Where Feast fits in MLOps

A typical MLOps pipeline might look like:

```text
Raw Data
   ↓
Data Processing
   ↓
Feature Engineering
   ↓
     ┌───────────────┐
     │     Feast     │
     └───────┬───────┘
             ↓
      Training Dataset
             ↓
       Model Training
             ↓
       Model Registry
             ↓
        Deployment
             ↓
      Production Model
             ↑
             │
       Feast Online Store
```

### The big problem Feast solves

One of the biggest problems in ML systems is **training-serving skew**.

For example, you train a model using:

```python
average_purchase_30_days
```

but your production application calculates that feature differently.

Your model may perform well in testing but poorly in production.

Feast gives you a centralized way to **define and serve features consistently**, reducing this kind of mismatch.

### Feast vs. a normal database

A feature store isn't simply a database.

A database answers:

> "How do I store and retrieve data?"

A feature store is designed around:

> "How do I create, manage, retrieve, and serve ML features consistently for training and inference?"

### In one sentence

**Feast = a feature store that helps ML teams manage and serve features for both historical model training and low-latency production inference.**

If you're learning MLOps, the concepts worth learning alongside Feast are **feature engineering → feature store → offline/online store → training-serving skew → model registry → model serving**.
