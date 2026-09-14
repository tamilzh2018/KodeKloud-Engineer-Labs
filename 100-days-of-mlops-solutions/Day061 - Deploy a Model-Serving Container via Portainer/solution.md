# Task:
The xFusionCorp Industries ML platform team utilizes Portainer to manage every model-serving container. This operational layer allows for image inspection, container deployment, and runtime log management from a single web console. The fraud-detector:v1 image has been successfully built, and Portainer is currently accessible on port 9090.

Your task is to deploy the serving container named fraud-api using the Portainer UI. You are required to bind-mount the pre-staged /root/code/serving/ directory to ensure the container can locate app.py and model.pkl. Additionally, you must publish the host port 8085 and verify that the endpoints /health and /predict respond correctly on the host.


Portainer is already running on port 9090. The Portainer UI button at the top of the lab opens the login page. Admin credentials: username admin, password xFusionCorp2026! (pre-initialised at startup). The deploy is driven entirely from Portainer's Add container form in the local environment.

The project layout under /root/code/serving/:

app.py – FastAPI app loading /app/model.pkl and exposing /health + POST /predict. Correct.
Dockerfile – python:3.11-slim + fastapi + uvicorn + joblib + sklearn, EXPOSE 8085, CMD ["uvicorn", "app:app", ...]. Correct.
model.pkl – RandomForest trained at startup.
The image fraud-detector:v1 has already been built from the Dockerfile. The container is expected to bind-mount /root/code/serving/ → /app so the same image picks up new app.py or model.pkl versions on restart, and to publish host port 8085 → container 8085.

The end state must include:

Portainer is reachable on port 9090.
docker inspect fraud-api reports the container as running, using image fraud-detector:v1, with the bind-mount /root/code/serving → /app.
curl http://localhost:8085/health returns {"status":"ok"} with HTTP 200.
curl -X POST http://localhost:8085/predict -H 'Content-Type: application/json' -d '{"amount":3200,"hour":23,"num_tx_past_day":5}' returns a JSON body with an is_fraud field of 0 or 1.
Portainer's Add container form collects every field the equivalent docker run command would—name, image, port mapping, volume mount, env vars, restart policy—and runs the deploy through the mounted /var/run/docker.sock. The host path entered in the Volumes tab must match the lab's host filesystem exactly (/root/code/serving).

# Solution

Not every deployment happens from a terminal — ops teams often manage containers through a web console. Portainer is one such console. This task deploys a pre-built model-serving image as a running container through the Portainer UI: setting the container name, image, published port, and a bind-mount, then confirming the API serves `/health` and `/predict`.

> As an MLOps engineer, you should be able to stand up and inspect a serving container from a management UI, not only the CLI — Portainer's Add-container form collects exactly what a `docker run` would. The model and data are synthetic.

#### Follow the steps below

##### 1. Confirm the starting state.
From a VS Code terminal:
```
docker images fraud-detector:v1
docker ps --filter name=portainer
curl -s -o /dev/null -w '%{http_code}\n' http://localhost:9090/
ls /root/code/serving/
```
The image exists, the `portainer` container is running on host port 9090, the Portainer HTTP surface answers, and `/root/code/serving/` carries `app.py`, `Dockerfile`, and `model.pkl`.

##### 2. Open Portainer and log in.
Click the **Portainer UI** button at the top of the lab. On the login page, enter:
- **Username:** `admin`
- **Password:** `xFusionCorp2026!`

On first login Portainer shows the **Quick Setup** environment wizard ("Welcome to Portainer"). Click **Get Started** — this selects the **local** Docker environment (the one Portainer is running in), and the left sidebar re-renders with the environment-scoped sections (Dashboard, Containers, Images, Networks, Volumes, Events…).

> If you instead land on the **Home** page, click the **local** environment card to enter it. If the sidebar shows only the Administration sections (Users, Teams, Roles, Environments, Registries, Logs…), click the **Portainer.io** logo at the top-left to return to **Home**, then open **local** from there — clicking the `local` entry under **Administration → Environments** opens its config-edit page, not its dashboard.

##### 3. Start a new container.
In the environment's left sidebar, click **Containers**, then the **+ Add container** button (top-right of the container list). At the top of the **Create container** form:
- **Name:** `fraud-api`
- **Image configuration → Registry:** leave it on `Docker Hub (anonymous)`.
- **Image configuration → Image:** `fraud-detector:v1`. Portainer uses the local daemon image when the tag matches (the greyed `docker.io` prefix is cosmetic).
- **Always pull the image:** off.

##### 4. Publish the host port.
Stay in the **main form** — the **Network ports configuration** section sits just below *Image configuration* and above *Access control*. Click **+ Map additional port**; a row with two inputs appears. Set both:
- **host:** `8085`
- **container:** `8085`

> Do **not** use the **Network** tab inside *Advanced container settings* lower down — that tab is for network mode / hostname / DNS (its `Hostname` field is not a port). Port publishing is only done here, in the main-form **Network ports configuration** section.

##### 5. Bind-mount the serving directory.
Scroll to **Advanced container settings** (the tabbed panel below the **Deploy the container** button) and open the **Volumes** tab, then click **+ map additional volume**. In the row that appears:
- **container** (path inside the container): `/app`
- Click the **Bind** toggle (not **Volume**).
- In the **host** field that then appears, enter `/root/code/serving`.
- Leave it **Writable** (not Read-only).

##### 6. Deploy.
Leave **Access control** at its default (**Administrators**), then click **Deploy the container**. Portainer sends the equivalent `docker run` through the mounted daemon socket, and the page reloads on the container list with `fraud-api` running.

##### 7. Verify from the terminal.
```
docker ps --filter name=fraud-api
curl -s http://localhost:8085/health
curl -s -X POST -H 'Content-Type: application/json' \
  -d '{"amount":3200,"hour":23,"num_tx_past_day":5}' \
  http://localhost:8085/predict
```
The container is listed, `/health` returns `{"status":"ok"}`, and the predict call returns a JSON body with an integer `is_fraud` flag.

##### 8. Inspect the container in Portainer.
Back in the Portainer UI, click the `fraud-api` row under **Containers** and then the **Inspect** tab. The JSON panel shows the port binding (`8085/tcp → 0.0.0.0:8085`), the bind-mount (`/root/code/serving` → `/app`), and the image (`fraud-detector:v1`). (Optional: the **Logs** and **Stats** tabs stream over WebSockets and may not render through the lab's port proxy — the Inspect panel above is the reliable view; the container is confirmed serving by the `curl` checks in the previous step regardless.)

#### References

- Portainer — creating and deploying a container (the Add-container form fields): https://docs.portainer.io/user/docker/containers/add
- Portainer — managing containers (inspect, logs, stats): https://docs.portainer.io/user/docker/containers
