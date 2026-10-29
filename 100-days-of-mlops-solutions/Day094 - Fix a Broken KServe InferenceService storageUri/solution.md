# Task
The xFusionCorp Industries ML platform team has established KServe on their Kind cluster and deployed a fraud-detector InferenceService, which is backed by a PVC-mounted Scikit-learn model. However, the InferenceService is not reaching a Ready state, as the predictor pod remains in Pending. Please investigate the cause of this issue and rectify the manifest located at /root/code/k8s/inference-service.yaml to ensure that the InferenceService transitions to Ready. After making the necessary adjustments, confirm that the predictor can successfully serve a prediction.


KServe is installed on a kind cluster, and a fraud-detector InferenceService has been deployed — but it never reaches Ready and its predictor pod stays Pending. Inspect the predictor pod to see what is blocking it:

kubectl describe pod -l serving.kserve.io/inferenceservice=fraud-detector

The end state must include:

kubectl get isvc fraud-detector shows the InferenceService.
spec.predictor.model.storageUri references a PVC that exists in the namespace.
.status.conditions[?(@.type=="Ready")].status == True (tests poll up to 360 s).
A prediction request to the predictor's /v1/models/fraud-detector:predict returns a JSON predictions array.
KServe's pvc:// storage scheme mounts the named PVC into the predictor pod at /mnt/models and lets the runtime read model artefacts from there. The reference must name a PVC that exists in the InferenceService's namespace.
# Solution

KServe is a Kubernetes-native model-serving platform: an `InferenceService` declares where a model lives (`storageUri`) and which runtime serves it, and KServe reconciles the predictor pods for you. This task hands you an InferenceService stuck at `READY=False` because its `storageUri` points at a PVC that doesn't exist, and you fix the reference so the predictor mounts the model and serves a prediction.

> As an MLOps engineer, you get the serving stack to load and expose the model by fixing its KServe `storageUri` — you are not judging the model; the served artefact is a throwaway `DummyClassifier` standing in for a real one.

#### Follow the steps below

##### 1. Read the broken state.
From a VS Code terminal:
```
kubectl get pvc
kubectl get isvc --> lists KServe InferenceService custom resources in your current Kubernetes namespace
kubectl get pods -l serving.kserve.io/inferenceservice=fraud-detector
kubectl describe pod -l serving.kserve.io/inferenceservice=fraud-detector \
  | awk '/Events/,/$/' | tail -15
```

- The PVC `model-storage` is Bound.
- `kubectl get isvc` shows `fraud-detector` with `READY=False`.
- The predictor pod is `Pending`; its events contain:
  ```
  Warning  FailedMount  persistentvolumeclaim "models-storage" not found
  ```

##### 2. Compare the PVC name.
```
kubectl get pvc -o name
kubectl get isvc fraud-detector -o jsonpath='{.spec.predictor.model.storageUri}{"\n"}'
```
PVC is `model-storage`. storageUri is `pvc://models-storage/`. Typo — the extra `s`.

##### 3. Fix the InferenceService manifest.
Open `/root/code/k8s/inference-service.yaml` in the VS Code editor. Change:
```yaml
      storageUri: "pvc://models-storage/"
```
to:
```yaml
      storageUri: "pvc://model-storage/"
```
Save.

##### 4. Re-apply.
```
kubectl apply -f /root/code/k8s/inference-service.yaml
```

##### 5. Watch the InferenceService come up.
```
kubectl get isvc fraud-detector -w
```

Within 2-3 minutes the `READY` column flips to `True` and the `URL` column populates with `http://fraud-detector-default.example.com`. The predictor pod goes through `Init:0/1` (storage-initializer mounting the PVC) → `Running`. Press `Ctrl+C` to exit the watch.

##### 6. Confirm the predictor pod is serving.
```
kubectl get pods -l serving.kserve.io/inferenceservice=fraud-detector
kubectl get isvc fraud-detector \
  -o jsonpath='{.status.conditions[?(@.type=="Ready")].status}{"\n"}'
```
The predictor pod is `Running` with the storage-initializer init-container already complete, and the `Ready` condition is `True` — the sklearn runtime loaded `model.joblib` from the mounted PVC.

##### 7. Send a real inference request.
`Ready=True` means the model loaded — confirm it actually serves. Send a prediction to the predictor's v1 endpoint by exec-ing into the pod and hitting the KServe runtime directly on its own `localhost:8080` (the `DummyClassifier` was trained on 4 features):
```
POD=$(kubectl get pod -l serving.kserve.io/inferenceservice=fraud-detector -o name | head -1)
kubectl exec "$POD" -- python3 -c "
import urllib.request, json
d = json.dumps({'instances': [[0, 0, 0, 0]]}).encode()
req = urllib.request.Request(
    'http://localhost:8080/v1/models/fraud-detector:predict',
    data=d, headers={'Content-Type': 'application/json'})
print(urllib.request.urlopen(req).read().decode())
"
```
The response is a JSON `predictions` array, e.g. `{"predictions": [0]}` — the model server is answering requests end-to-end.

> Reach the runtime by exec-ing the pod, not with a host-side `kubectl port-forward svc/fraud-detector-predictor … + curl`: forwarding through the predictor Service can return `Unsupported method POST`, whereas the pod's own `localhost:8080` is where the KServe server actually listens.

#### References

- KServe — your first InferenceService (`spec.predictor.model`, `Ready`): https://kserve.github.io/website/latest/get_started/first_isvc/
- KServe — PVC storage (`pvc://<name>/` mounted at `/mnt/models`): https://kserve.github.io/website/latest/modelserving/storage/pvc/pvc/
- KServe — scikit-learn serving runtime and the predict protocol: https://kserve.github.io/website/latest/modelserving/v1beta1/sklearn/v2/
