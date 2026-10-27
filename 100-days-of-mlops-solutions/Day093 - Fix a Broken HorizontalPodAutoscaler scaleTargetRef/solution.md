# Task
The xFusionCorp Industries ML platform team has autoscaled their fraud-server Deployment, which serves as a stand-in for the fraud-detector model using nginx:alpine. This task focuses on the configuration of the HorizontalPodAutoscaler (HPA), rather than the model itself. Currently, executing kubectl get hpa results in TARGETS <unknown>/70%, indicating that the HPA is unable to find a metric to measure, and as a consequence, it is not performing any scaling operations. Please investigate the issue and rectify the HPA manifest located at /root/code/k8s/hpa.yaml.


A kind cluster is pre-provisioned and kubectl is configured to reach it. metrics-server is installed and patched for kind's kubelet, the fraud-server Deployment is running with CPU requests and limits, and the HPA manifest at /root/code/k8s/hpa.yaml has already been applied — its TARGETS column currently reads <unknown>/70%. Inspect the HPA to see why it can't read a metric:

kubectl describe hpa fraud-server-hpa

The end state must include:

The fraud-server Deployment is Available with 2 or more replicas.
HPA fraud-server-hpa exists, and its scaleTargetRef points at a Deployment that exists in the cluster.
HPA.status.currentMetrics[].resource.current.averageUtilization (or averageValue) is populated — no longer <unknown> (tests poll up to 180 s).
An HPA is a reference plus a metric target — nothing works if the reference points at a resource that no longer exists. Silent break modes like this are why CI gates on kubectl apply --dry-run=server (which validates the scaleTargetRef against live resources) are a useful safety net in pipelines that rename workloads. 

# Solution

A HorizontalPodAutoscaler scales a workload's replica count up and down against a metric target, using a `scaleTargetRef` to name the Deployment it manages. This task hands you an HPA stuck at `<unknown>/70%` because its `scaleTargetRef` names a Deployment that doesn't exist, and you reconcile the reference so the HPA reads metrics and can scale.

> As an MLOps engineer, you make the model server scale under load by fixing its autoscaler wiring — you are not changing the model; the served container is an `nginx:alpine` stand-in for the model server.

#### Follow the steps below

##### 1. Confirm the broken state.
From a VS Code terminal:
```
kubectl get deploy
kubectl get hpa
kubectl describe hpa fraud-server-hpa | head -40
```
The Deployment is `fraud-server`. `kubectl get hpa` shows `TARGETS  <unknown>/70%`. Describe's Events section reads:
```
Warning  FailedGetScale  horizontal-pod-autoscaler
   ScaleTargetRef for kind=Deployment name=fraud-serving not found
```

##### 2. Diff the name.
```
kubectl get deploy fraud-server -o jsonpath='{.metadata.name}{"\n"}'
kubectl get hpa fraud-server-hpa -o jsonpath='{.spec.scaleTargetRef.name}{"\n"}'
```
First prints `fraud-server`, second prints `fraud-serving`. The HPA is one character off.

##### 3. Fix the HPA manifest.
Open `/root/code/k8s/hpa.yaml` in the VS Code editor. Change:
```yaml
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: fraud-serving
```
to:
```yaml
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: fraud-server
```
Save.

##### 4. Re-apply.
```
kubectl apply -f /root/code/k8s/hpa.yaml
```

##### 5. Wait for metrics to populate.
```
for i in 1 2 3 4 5 6 7 8; do
  kubectl get hpa fraud-server-hpa
  sleep 10
done
```
Within one or two iterations, `TARGETS` moves from `<unknown>/70%` to `0%/70%`.

Read `0%/70%` as **current / target**:
- **`70%`** is the target you set in the manifest (`averageUtilization: 70`) — the average pod CPU, expressed as a percentage of each pod's CPU *request* (here `50m`), at which the HPA would add replicas.
- **`0%`** is the current average CPU across the pods. The served container is an idle `nginx:alpine` stand-in handling no traffic, so it uses effectively none of its 50m request — hence `0%`.

`0%` (rather than a larger number) is exactly what to expect here — nothing is generating load. What matters is that the current value is a **real reading, not `<unknown>`**: that is the proof the HPA now resolves its `scaleTargetRef` and is reading pod CPU through metrics-server. Since 0% is below the 70% target, the HPA correctly holds at `minReplicas: 2` — it would only scale up if sustained CPU crossed 70%. Run `kubectl top pods` to confirm metrics-server is scraping pod CPU.

##### 6. Verify via status.
```
kubectl get hpa fraud-server-hpa -o json | python3 -c "
import json, sys
hpa = json.load(sys.stdin)
status = hpa.get('status', {})
for m in status.get('currentMetrics', []):
    r = m.get('resource', {})
    if r.get('name') == 'cpu':
        print('cpu current:', r.get('current'))
print('conditions:', [c.get('type') for c in status.get('conditions', [])])
"
```
`cpu current` prints a dict with `averageUtilization` set to `0` (near-zero for the idle stand-in) — the key point is that it is *present*, which is what the grader checks. `conditions` contains `AbleToScale: True` and `ScalingActive: True`.

#### References

- Kubernetes — HorizontalPodAutoscaler (`scaleTargetRef`, resource metrics): https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/
- Kubernetes — HPA walkthrough (metrics-server, `TARGETS`, scaling behaviour): https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/
