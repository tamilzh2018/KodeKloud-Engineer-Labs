# Task
The xFusionCorp Industries ML platform team requires that all credentials necessary for the lab-ops service—including MLflow's admin password, SeaweedFS's access keys, and PostgreSQL passwords—be retrieved from HashiCorp Vault at service startup, rather than being hardcoded into a startup script. A development Vault is currently operational on port 8200, and its web UI can be accessed via the Vault button. Additionally, an MLflow boot wrapper on the host is polling Vault every 5 seconds for the secret/mlflow.admin_password. However, the wrapper can only initiate MLflow once this KV entry is available. Your task is to enable the KV v2 engine in Vault, create the secret, and observe the successful startup of MLflow on port 5000.


The Vault UI is on port 8200 (Vault button opens the login page). The dev-mode root token is pre-created and written to /root/code/vault-token; paste the file's contents into the Vault Token login field. (Production deployments would use userpass / AppRole / OIDC instead, but the root token is the shortest path for a dev server.)

The MLflow wrapper picks up the new KV entry within ~5 s and execs mlflow server on port 5000. The MLflow UI button then opens the live tracker.

The end state must include:

A KV v2 secrets engine is enabled at path secret/ — GET /v1/sys/mounts returns secret/ with type: kv and options.version: "2".
The secret at path secret/mlflow carries a non-empty admin_password key — GET /v1/secret/data/mlflow (with the root token) returns a JSON body whose data.data.admin_password is a non-empty string.
GET http://localhost:5000/ answers 200 – MLflow is running because the wrapper found the password.
Running services should not know their own secrets at image-build time. A Vault-first pattern lets you rotate a credential in Vault and restart the consumer to pick up the new value—no rebuild, no config patch, no secret in the commit history. This task's single-service wrapper is the minimum viable version of that pattern; a real deployment replaces the root token with an AppRole login and adds audit logging.

# Solution

Credentials scattered across scripts and `.env` files are a leak waiting to happen. **HashiCorp Vault** centralizes them in one audited, access-controlled store, and services fetch what they need at startup instead of carrying a baked-in copy. This task brings up Vault's KV secrets engine and stores the lab-ops service's credentials (MLflow's admin password among them) so a consumer can read them at runtime rather than have them hardcoded.

> As an MLOps engineer, you keep service credentials in an audited secrets store and have consumers fetch them at startup, instead of hardcoding them into scripts — there is no model work here.

#### Follow the steps below

##### 1. Confirm the starting state.
From a VS Code terminal:
```
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:8200/v1/sys/health?standbyok=true
cat /root/code/vault-token
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:5000/
tail -5 /var/log/mlflow-wrapper.log
```
Vault answers `200`. The root token file exists. MLflow is NOT reachable (connection refused) because the wrapper is still looping — the log shows repeated `polling ...` entries. This is expected: the KV entry does not exist yet.

##### 2. Log in to Vault.
Click the **Vault** button at the top of the lab. On the login page:
- **Method:** Token (default)
- **Token:** paste the value of `/root/code/vault-token` (from the terminal). Click **Sign In**.

##### 3. Enable the KV v2 secrets engine.
In the left navigation, click **Secrets** → **Enable new engine**:
- Pick **KV** → click **Next**.
- **Version:** `2`.
- **Path:** `secret`.
- Leave the rest at defaults. Click **Enable engine**.

The engine now appears on the Secrets Engines list with path `secret/` and type `kv / 2`.

##### 4. Create the secret.
Still on the `secret/` engine page:
- Click **Create secret**.
- **Path for this secret:** `mlflow`.
- **Secret data** row: key `admin_password`, value `mlflow-admin-2026`.
- Click **Save**.

##### 5. Watch MLflow come up.
Give the wrapper one poll cycle (~5 s) and then click the **MLflow UI** button, or from a VS Code terminal:
```
for i in {1..12}; do
  code=$(curl -s -o /dev/null -w '%{http_code}' http://localhost:5000/)
  echo "attempt $i: $code"
  [ "$code" = "200" ] && break
  sleep 3
done
tail -5 /var/log/mlflow-wrapper.log
```
The wrapper log's last line reads `Password present -- launching MLflow.` and MLflow's landing page returns `200`.

##### 6. Verify via the Vault REST API.
```
TOKEN=$(cat /root/code/vault-token)

curl -s -H "X-Vault-Token: $TOKEN" http://localhost:8200/v1/sys/mounts \
  | python3 -c "
import json, sys
body = json.load(sys.stdin)
mnt = body.get('secret/') or {}
print('type:   ', mnt.get('type'))
print('version:', (mnt.get('options') or {}).get('version'))
"

curl -s -H "X-Vault-Token: $TOKEN" http://localhost:8200/v1/secret/data/mlflow \
  | python3 -m json.tool
```
The first call prints `type: kv`, `version: 2`. The second shows a JSON body whose `data.data.admin_password` is the value you stored.

#### References

- KV v2 secrets engine (enabling the engine, secret versioning): https://developer.hashicorp.com/vault/docs/secrets/kv/kv-v2
- KV v2 HTTP API — the `secret/data/<path>` endpoint the wrapper polls: https://developer.hashicorp.com/vault/api-docs/secret/kv/kv-v2
- Vault dev server and the dev root token used here: https://developer.hashicorp.com/vault/docs/concepts/dev-server
