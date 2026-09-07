# Task:
The xFusionCorp Industries ML platform team deploys Flask-based inference APIs as Docker images, incorporating Docker-native HEALTHCHECK instructions. This allows operators to easily verify the serving status of the process by running docker inspect --format='{{.State.Health.Status}}'. However, the draft Dockerfile located at /root/code/ml-health/ currently does not meet these standards; executing docker inspect --format='{{.State.Health.Status}}' ml-health-api returns unhealthy, and docker inspect --format '{{.Config.ExposedPorts}}' ml-health:v1 shows no exposed ports. Your task is to rectify the HEALTHCHECK target and include the missing EXPOSE declaration.


The Docker daemon is already running. docker version can be run in a VS Code terminal to confirm. With the current image built and run as ml-health-api, docker inspect --format='{{.State.Health.Status}}' ml-health-api reports unhealthy and docker inspect --format '{{.Config.ExposedPorts}}' ml-health:v1 shows no exposed ports.

The project layout under /root/code/ml-health/:

app.py – Flask API serving GET /health (returns {"status": "ok"} / 200) and POST /predict (returns a rule-based fraud flag) on port 8085. Correct.
Dockerfile – python:3.11-slim, installs flask, copies app.py, carries a HEALTHCHECK + CMD. The corrected image is built as ml-health:v1 and run as a container named ml-health-api with host port 8085 published.
The end state must include:

docker inspect --format '{{.Config.ExposedPorts}}' ml-health:v1 reports map[8085/tcp:{}].
After docker run, docker inspect --format='{{.State.Health.Status}}' ml-health-api reads healthy within ~15 seconds.
curl http://localhost:8085/health returns {"status": "ok"} with HTTP 200.
HEALTHCHECK reruns its CMD every --interval seconds and flips the state to unhealthy after --retries consecutive failures. EXPOSE does not change networking (that is done by -p)—it writes image metadata so docker inspect and downstream orchestrators know which port the image intends to serve on.
# Solution

Operators and orchestrators need to know whether a serving container is actually answering requests, not just whether the process is alive. A Docker **`HEALTHCHECK`** gives them that — it reruns a probe on an interval and flips the container's state to `unhealthy` after enough consecutive failures, readable via `docker inspect`. This task fixes a broken inference-API `Dockerfile`: the `HEALTHCHECK` probes a path the Flask app doesn't serve (so the container reports `unhealthy`), and the `EXPOSE` declaration is missing. Note what `EXPOSE` does and doesn't do — it writes image metadata that documents the intended port (surfaced in `docker inspect` and to orchestrators); it does **not** publish the port, which is what `-p` does at `docker run`.

> As an MLOps engineer, you make a serving container honestly report its own health and document its port so orchestrators can route to it — you are not touching the model. The `/predict` endpoint returns a rule-based stand-in.

#### Follow the steps below

##### 1. Confirm the starting state.
From a VS Code terminal:
```
cd /root/code/ml-health
cat Dockerfile
grep -E "@app\.route" app.py
```
The HEALTHCHECK probe targets `/healthz`; the Flask app serves `/health` (no trailing `z`). The Dockerfile has no `EXPOSE` declaration.

##### 2. Run the draft build and observe the failure.
```
docker build -t ml-health:v1 .
docker run -d --rm --name ml-health-api -p 8085:8085 ml-health:v1
sleep 12
docker inspect --format='{{.State.Health.Status}}' ml-health-api
```
The status reads `unhealthy`. Docker's probe hits `/healthz`, which the Flask app does not serve, so `urllib.request.urlopen(...)` raises `HTTPError: 404`, the probe's exit code is non-zero, and three consecutive failures flip the state to unhealthy. Clean up:
```
docker rm -f ml-health-api
```

##### 3. Inspect the exposed-ports metadata.
```
docker inspect --format='{{.Config.ExposedPorts}}' ml-health:v1
```
The output is `map[]` (empty). The container serves on 8085 when started with `-p 8085:8085`, but the image's metadata carries no exposed-port record — downstream orchestrators that read image metadata (not compose-file port mappings) cannot tell which port the image intends to bind.

##### 4. Fix the HEALTHCHECK endpoint.
Open `/root/code/ml-health/Dockerfile` in the VS Code editor. Change the HEALTHCHECK probe so the URL matches the Flask app's path:
```dockerfile
HEALTHCHECK --interval=5s --timeout=3s --start-period=3s --retries=3 \
  CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:8085/health')" || exit 1
```

##### 5. Add the EXPOSE instruction.
Append an `EXPOSE` line declaring the Flask server's port:
```dockerfile
EXPOSE 8085
```
Save the file.

##### 6. Rebuild and verify `ExposedPorts`.
```
docker build -t ml-health:v1 .
docker inspect --format='{{.Config.ExposedPorts}}' ml-health:v1
```
Output now reads `map[8085/tcp:{}]` — the image's metadata carries the port the app serves on.

##### 7. Start the container and poll for `healthy`.
```
docker run -d --rm --name ml-health-api -p 8085:8085 ml-health:v1
for i in $(seq 1 30); do
  status=$(docker inspect --format='{{.State.Health.Status}}' ml-health-api 2>/dev/null)
  echo "attempt $i: $status"
  [ "$status" = "healthy" ] && break
  sleep 1
done
```
Within the `start-period` + a few `--interval` cycles the status flips to `healthy`.

##### 8. Confirm the endpoint from the host.
```
curl -s http://localhost:8085/health
```
Output: `{"status":"ok"}`. Clean up:
```
docker rm -f ml-health-api
```

#### References

- `HEALTHCHECK` instruction — probe interval/timeout/retries and how the health state flips: https://docs.docker.com/reference/dockerfile/#healthcheck
- `EXPOSE` instruction — documenting the container's listening port in image metadata: https://docs.docker.com/reference/dockerfile/#expose
