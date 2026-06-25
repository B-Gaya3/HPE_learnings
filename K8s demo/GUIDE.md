# Why Kubernetes? — Hands-on Demo Guide

Two FastAPI microservices. Three ways to run them.
You will feel exactly why Kubernetes exists.

---

## Folder structure

```
k8s-demo/
├── service-a/
│   ├── main.py          ← Returns {"message": "Hello from A"}
│   ├── requirements.txt
│   └── Dockerfile
├── service-b/
│   ├── main.py          ← Calls service-a, returns combined response
│   ├── requirements.txt
│   └── Dockerfile
└── k8s/
    ├── service-a.yaml   ← K8s Deployment + Service for A
    └── service-b.yaml   ← K8s Deployment + Service for B
```

---

## PHASE 1 — Run manually (no Docker, no K8s)

### Step 1: Install dependencies

```bash
cd k8s-demo/service-a
pip install -r requirements.txt

cd ../service-b
pip install -r requirements.txt
```

### Step 2: Start service-a in Terminal 1

```bash
cd k8s-demo/service-a
uvicorn main:app --port 8001
```

### Step 3: Start service-b in Terminal 2

```bash
cd k8s-demo/service-b
uvicorn main:app --port 8002
```

### Step 4: Test it

```bash
# In Terminal 3:
curl http://localhost:8001/       # service-a responds directly
curl http://localhost:8002/       # service-b calls service-a and returns both
```

Expected response from service-b:
```json
{
  "message": "Hello from Service B!",
  "service": "B",
  "service_a_says": {
    "message": "Hello from Service A!",
    "service": "A"
  }
}
```

### ❌ Problems you face manually:

1. KILL service-a (Ctrl+C in Terminal 1). Now call service-b again:
   ```bash
   curl http://localhost:8002/
   ```
   → service-b returns an error. Nobody restarted service-a.
   With K8s: it would restart automatically in ~2 seconds.

2. Want to run 3 copies of service-a for more traffic?
   → You'd manually open 3 terminals and run on ports 8001, 8003, 8004.
   With K8s: change replicas: 2 to replicas: 3 in the YAML.

3. Service-b has service-a's IP hardcoded as "localhost:8001".
   If service-a moves to another machine → service-b breaks.
   With K8s: service-b uses the name "service-a" — K8s DNS handles it.

4. Machine restarts → everything is gone. You restart manually.
   With K8s: all pods come back automatically.

---

## PHASE 2 — Run with Docker (better, but still manual)

### Prerequisites: Install Docker Desktop
Download from: https://www.docker.com/products/docker-desktop/

### Step 1: Build images

```bash
cd k8s-demo/service-a
docker build -t k8s-demo/service-a:latest .

cd ../service-b
docker build -t k8s-demo/service-b:latest .
```

### Step 2: Create a shared network so containers can talk

```bash
docker network create demo-network
```

### Step 3: Run both containers

```bash
# Run service-a (name "service-a" becomes hostname on the network)
docker run -d \
  --name service-a \
  --network demo-network \
  -p 8001:8001 \
  k8s-demo/service-a:latest

# Run service-b — tells it where service-a lives via env variable
docker run -d \
  --name service-b \
  --network demo-network \
  -p 8002:8002 \
  -e SERVICE_A_URL=http://service-a:8001 \
  k8s-demo/service-b:latest
```

### Step 4: Test it

```bash
curl http://localhost:8002/
```

### ❌ Problems still remaining with Docker:

1. Kill service-a container:
   ```bash
   docker stop service-a && docker rm service-a
   curl http://localhost:8002/   # → error. Nobody restarted it.
   ```
   With K8s: pod restarts automatically.

2. Scale service-a to 3 copies:
   → You have to manually run 3 docker run commands with different names/ports,
     then set up a load balancer yourself.
   With K8s: kubectl scale deployment service-a --replicas=3

3. Rolling update (deploy new version without downtime):
   → Stop container → start new one → downtime during gap.
   With K8s: replaces pods one-by-one, zero downtime.

---

## PHASE 3 — Run with Kubernetes (Minikube)

### Prerequisites

1. Install Minikube: https://minikube.sigs.k8s.io/docs/start/
2. Install kubectl: https://kubernetes.io/docs/tasks/tools/
3. Start Minikube:
   ```bash
   minikube start
   ```

### Step 1: Point Docker to Minikube's registry

```bash
eval $(minikube docker-env)
```
(This makes your docker build commands go into Minikube, not your laptop)

### Step 2: Build images inside Minikube

```bash
cd k8s-demo/service-a
docker build -t k8s-demo/service-a:latest .

cd ../service-b
docker build -t k8s-demo/service-b:latest .
```

### Step 3: Deploy both services

```bash
cd k8s-demo/k8s
kubectl apply -f service-a.yaml
kubectl apply -f service-b.yaml
```

### Step 4: Verify pods are running

```bash
kubectl get pods
```
Expected output:
```
NAME                         READY   STATUS    RESTARTS   AGE
service-a-6d9b8f7c4-xk2lp   1/1     Running   0          30s
service-a-6d9b8f7c4-mn3qr   1/1     Running   0          30s   ← 2 replicas!
service-b-4f8c9d2b1-pq7yt   1/1     Running   0          28s
service-b-4f8c9d2b1-rs4wx   1/1     Running   0          28s
```

### Step 5: Test it

```bash
minikube service service-b --url
```
Copy the URL and open in browser, or:
```bash
curl $(minikube service service-b --url)
```

### ✅ Now experience K8s superpowers:

#### Auto-restart (self-healing):
```bash
# Find a service-a pod name
kubectl get pods

# Delete it — simulate a crash
kubectl delete pod service-a-6d9b8f7c4-xk2lp

# Watch K8s bring it back automatically (within seconds!)
kubectl get pods --watch
```

#### Scale up instantly:
```bash
kubectl scale deployment service-a --replicas=5
kubectl get pods   # 5 service-a pods running
```

#### Scale back down:
```bash
kubectl scale deployment service-a --replicas=1
```

#### Rolling update (zero downtime):
```bash
# Imagine you pushed a new version:
kubectl set image deployment/service-a service-a=k8s-demo/service-a:v2

# Watch it update pods one by one — no downtime
kubectl rollout status deployment/service-a
```

#### Service discovery (no hardcoded IPs):
```bash
# service-b finds service-a by NAME, not IP
# K8s DNS automatically resolves "service-a" → correct pod IP
kubectl exec -it <any-service-b-pod> -- curl http://service-a:8001/
```

### Cleanup:
```bash
kubectl delete -f k8s/service-a.yaml
kubectl delete -f k8s/service-b.yaml
minikube stop
```

---

## Summary: The 4 reasons your project needs Kubernetes

| Problem | Without K8s | With K8s |
|---|---|---|
| Service crashes | Stays dead until you restart it | Auto-restarts in ~2 seconds |
| More traffic | Manually open more terminals/containers | `replicas: 5` in YAML |
| Services finding each other | Hardcoded IPs that break | DNS name like "service-a" |
| New version deployment | Downtime during swap | Rolling update, zero downtime |

### Your interview answer:

> "We used Kubernetes because our project has 8+ services running together —
> Falco, Kafka, FastAPI services, OpenSearch, Grafana — and managing all of
> them manually is impossible. Kubernetes gives us automatic restart if a pod
> crashes, easy scaling, service discovery by name instead of hardcoded IPs,
> and rolling deployments. It also generates the audit logs that our entire
> security pipeline is built on — every kubectl command, every API call to
> the cluster gets logged by the kube-apiserver."
