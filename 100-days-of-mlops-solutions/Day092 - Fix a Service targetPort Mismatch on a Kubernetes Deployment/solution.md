# Task
The xFusionCorp Industries ML platform team has deployed a Kubernetes Deployment of the fraud-detector model server. This deployment uses an nginx:alpine container listening on port 80. Please note that this task focuses on Kubernetes Service routing, rather than the model itself. Currently, the Deployment is operating with two replicas, and executing kubectl get deploy fraud-detector confirms that the status shows READY 2/2. However, any requests made to the Service at fraud-detector-svc:8080 result in a timeout. Your task is to diagnose the issue preventing the Service from routing traffic to its backing pods and to correct the manifest accordingly.


A kind cluster named mlops is pre-provisioned and kubectl is configured to reach it. The Deployment and Service manifests live at /root/code/k8s/deployment.yaml and /root/code/k8s/service.yaml, and both have already been applied — the fraud-detector Deployment reports READY 2/2, but requests to fraud-detector-svc:8080 time out. Inspect the Service and its endpoints to see why traffic never reaches the pods:

kubectl describe svc fraud-detector-svc

The end state must include:

Deployment fraud-detector is Available.
Service fraud-detector-svc exists; clients still dial it on 8080.
Endpoints/fraud-detector-svc routes to the port the container is actually listening on (80).
An in-cluster HTTP GET http://fraud-detector-svc:8080/ returns the nginx default page.
In a Kubernetes Service, port is what clients dial and targetPort is what kube-proxy forwards that traffic to on the backing pods. They can legitimately differ (e.g. external 8080 → internal 80), but targetPort must match a real listening port on the container.
# Solution

A Kubernetes Service gives a set of pods a stable virtual IP and routes traffic to them, using `port` (what clients dial) and `targetPort` (the container port kube-proxy forwards to). This task hands you a green Deployment whose Service silently routes nowhere, and you fix the `targetPort` mismatch so the Service reaches its backing pods.

> As an MLOps engineer, you make the model server reachable by fixing its Kubernetes Service wiring — you are not changing the model; the served container is an `nginx:alpine` stand-in for the model server.

#### Follow the steps below

##### 1. Read the cluster state.
From a VS Code terminal:
```
kubectl get deploy fraud-detector
kubectl get svc fraud-detector-svc
kubectl get endpoints fraud-detector-svc -o wide
```

The Deployment is `Available 2/2`. The Service exists. The Endpoints row shows addresses populated at port `8080`.

##### 2. Compare container port vs. Service targetPort.
```
kubectl get deploy fraud-detector -o jsonpath='{.spec.template.spec.containers[0].ports[0].containerPort}'
kubectl get svc fraud-detector-svc -o jsonpath='{.spec.ports[0].targetPort}'
```

`containerPort` reads `80`. `targetPort` reads `8080`. Mismatch — kube-proxy is forwarding to a port the container isn't listening on.

##### 3. Fix the Service manifest.
Open `/root/code/k8s/service.yaml` in the VS Code editor. Change:
```yaml
  ports:
    - port: 8080
      targetPort: 8080
      nodePort: 30092
```
to:
```yaml
  ports:
    - port: 8080
      targetPort: 80
      nodePort: 30092
```
Save.

##### 4. Re-apply.
```
kubectl apply -f /root/code/k8s/service.yaml
kubectl get endpoints fraud-detector-svc -o wide
```

Endpoints now list each pod IP with port `80`.

##### 5. End-to-end probe.
```
kubectl run probe --rm -i --restart=Never --image=busybox -- \
  wget -qO- http://fraud-detector-svc:8080/ | head -5
```

The nginx welcome page prints. The Service is now routing to the pods.

#### References

- Kubernetes — Service (`port` vs `targetPort`, selectors, Endpoints): https://kubernetes.io/docs/concepts/services-networking/service/
- Kubernetes — debugging Services (empty/mis-pointed Endpoints, in-cluster probing): https://kubernetes.io/docs/tasks/debug/debug-application/debug-service/
