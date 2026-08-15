# Task
The xFusionCorp Industries ML platform team requires data-schema contracts for every batch that feeds the fraud-detector model. It is essential to identify malformed rows upstream of the training process, rather than three hours later in production. A Great Expectations project has already been initialized at /root/code/dataquality/gx/, featuring a pandas data source that reads from data/transactions.csv, an empty fraud_schema suite, and a default checkpoint configured to publish results to Data Docs with each run. Your task is to populate the suite with four expectations and execute the checkpoint to ensure that Data Docs reflects a green status for these expectations.


The platform's data contract for a transactions batch is:

Schema — every batch must carry exactly these columns: amount, hour, num_tx_past_day, is_fraud.
amount — a transaction amount; it is never negative.
hour — the hour-of-day the transaction occurred.
is_fraud — a binary label.
/root/code/dataquality/author_expectations.py carries four numbered TODOs, each naming the Great Expectations class that encodes one contract rule (imports for great_expectations as gx and great_expectations.expectations as ge are already in place):

TODO 1: ExpectTableColumnsToMatchSet — the required column set.
TODO 2: ExpectColumnValuesToBeBetween on amount.
TODO 3: ExpectColumnValuesToBeBetween on hour.
TODO 4: ExpectColumnValuesToBeInSet on is_fraud.
Running the script persists the suite to disk (gx/expectations/fraud_schema.json) and executes the default checkpoint, which validates transactions.csv against the suite and refreshes the Data Docs site. Data Docs is available from the Data Docs button at the top of the lab (port 8081), where each fraud_schema run renders with a green or red pill per expectation.

The end state must include:

gx/expectations/fraud_schema.json has all four expectations by type (expect_table_columns_to_match_set, two expect_column_values_to_be_between entries – One per column — and expect_column_values_to_be_in_set).
Each expectation's kwargs encode the data contract above.
The most recent validation JSON under gx/uncommitted/validations/ has success: true.
The Data Docs index page served on :8081 references fraud_schema.
Great Expectations treats data quality as code—expectation suites are versioned artefacts in the same repo as the model that consumes the data, run by the same CI that runs pytest. A run's result JSON is machine-readable (a downstream CI-gate lab consumes it), and Data Docs is the human-readable rendering of the same content. This task lays the ground for both.

# Solution

**Great Expectations** turns data quality into code. You declare **expectations** — assertions about a dataset's shape and values (which columns exist, numeric ranges, allowed value sets) — collected in an **expectation suite**, and run them through a **checkpoint** that validates a batch and renders the outcome as **Data Docs**, a browsable HTML report. The suite is a versioned *data contract*: the same assertions guard training data today and production batches later. This task authors the four expectations that encode the fraud-detector's contract and runs the checkpoint so Data Docs shows every expectation green.

> As an MLOps engineer, you author declarative data-validation expectations—a data contract enforced in code—you are not doing exploratory analysis or judging the dataset scientifically. The data is synthetic.

#### Follow the steps below

##### 1. Confirm the starting state.
From a VS Code terminal:
```
ls /root/code/dataquality/gx/expectations/
cat /root/code/dataquality/gx/expectations/fraud_schema.json | python3 -m json.tool
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8081/
```
The suite JSON exists but its `expectations` array is empty. Data Docs answers `200`.

##### 2. Populate the expectations.
Open `/root/code/dataquality/author_expectations.py` in the VS Code editor. Translate each data-contract rule into the keyword arguments of the class named in its TODO:

- **Schema** → `ExpectTableColumnsToMatchSet(column_set=[the four columns])`.
- **`amount` never negative** → `ExpectColumnValuesToBeBetween(column="amount", min_value=0)` (a lower bound of 0, no upper bound).
- **`hour` is an hour-of-day** → `ExpectColumnValuesToBeBetween(column="hour", min_value=0, max_value=23)` (the 0–23 hour range).
- **`is_fraud` is binary** → `ExpectColumnValuesToBeInSet(column="is_fraud", value_set=[0, 1])` (its only two label values).

Replace the `# (expectations go here)` line with the four `suite.add_expectation(...)` calls:

```python
    suite.add_expectation(
        ge.ExpectTableColumnsToMatchSet(
            column_set=["amount", "hour", "num_tx_past_day", "is_fraud"],
        )
    )
    suite.add_expectation(
        ge.ExpectColumnValuesToBeBetween(column="amount", min_value=0)
    )
    suite.add_expectation(
        ge.ExpectColumnValuesToBeBetween(
            column="hour", min_value=0, max_value=23,
        )
    )
    suite.add_expectation(
        ge.ExpectColumnValuesToBeInSet(column="is_fraud", value_set=[0, 1])
    )
```

Save.

##### 3. Run the authoring script.
```
python3 /root/code/dataquality/author_expectations.py
```

Expected output:
```
Persisted 4 expectations to `fraud_schema`
Checkpoint `default` result: success=True
```

##### 4. Inspect Data Docs.
Click the **Data Docs** button at the top of the lab. The landing page lists:
- **Expectation Suites**: `fraud_schema` → click to see the four expectations.
- **Validation Results**: the most recent run → click to see the per-expectation pass table.

Every pill reads green (`Success: True`).

##### 5. Verify from the terminal.
```
cat /root/code/dataquality/gx/expectations/fraud_schema.json \
  | python3 -c "
import json, sys
body = json.load(sys.stdin)
for e in body.get('expectations', []):
    print(e.get('type'), e.get('kwargs'))
"

ls -t /root/code/dataquality/gx/uncommitted/validations/**/*.json | head -1 \
  | xargs -I{} python3 -c "
import json
d = json.load(open('{}'))
print('success:', d['success'], '  statistics:', d.get('statistics'))
"
```
The first call prints four expectation lines, each with the kwargs matching the data contract. The second prints `success: True` and a statistics block showing `evaluated_expectations == successful_expectations == 4`.

#### References

- Expectation Gallery — browse every expectation and its keyword arguments: https://greatexpectations.io/expectations/
- `ExpectTableColumnsToMatchSet` (schema / required columns): https://greatexpectations.io/expectations/expect_table_columns_to_match_set
- `ExpectColumnValuesToBeBetween` (numeric range guards): https://greatexpectations.io/expectations/expect_column_values_to_be_between
- `ExpectColumnValuesToBeInSet` (allowed-value / categorical guards): https://greatexpectations.io/expectations/expect_column_values_to_be_in_set
