# 📝 To-Do App Deployment using Kubernetes (Minikube)

## 📌 Project Overview
This project demonstrates how to build and deploy a simple **To-Do web application** using:
- Docker 🐳
- Kubernetes ☸️ (Minikube)
- Namespace-based deployment

The application is a basic frontend app that allows users to add tasks dynamically.

---

## 🚀 Technologies Used
- HTML, JavaScript
- Docker
- Kubernetes (Minikube)
- kubectl (CLI tool)

---

## 📁 Project Structure
```
to-do/
│
├── index.html        # Frontend To-Do App
├── Dockerfile        # Docker image configuration
├── deployment.yaml   # Kubernetes Deployment
├── service.yaml      # Kubernetes Service
```
---

## ⚙️ Setup & Installation

### 1️⃣ Start Minikube
```
minikube start
```
### 2️⃣ Verify Cluster
```
kubectl get nodes
```

---

## 🐳 Build Docker Image

### Use Minikube Docker Environment
```eval $(minikube docker-env)```

### Build Image
```docker build -t todo-app . ```

📌 This builds the Docker image inside Minikube so Kubernetes can access it.

---

## 📂 Create Namespace
```kubectl create namespace todo-ns```

---

## 📦 Deploy Application

### Apply Deployment
```kubectl apply -f deployment.yaml```

### Check Pods
```kubectl get pods -n todo-ns```

---

## 🌐 Expose Application

### Apply Service
```kubectl apply -f service.yaml```

### Access Application
```minikube service todo-service -n todo-ns```

🎉 The application will open in your browser.

---

## ⚠️ Important Configuration

In deployment.yaml, include:
```imagePullPolicy: Never```

👉 This ensures Kubernetes uses the locally built Docker image instead of trying to pull from Docker Hub.

---

## 🧪 Challenges Faced & Solutions

1. ImagePullBackOff Error  
Reason: Kubernetes tried to pull the image from Docker Hub  
Solution: Added imagePullPolicy: Never and restarted pods  

2. Browser Cache Confusion  
Reason: Page still visible after stopping Minikube  
Solution: Checked using incognito mode  

---

## 🧠 Key Learnings

- Docker image creation  
- Kubernetes namespaces  
- Deployment & Service usage  
- Debugging using kubectl  
- Understanding pod lifecycle  
- Handling real-world errors  

---

## 🛑 Stopping the Application

Stop app:
kubectl delete deployment todo-deployment -n todo-ns
kubectl delete service todo-service -n todo-ns

Delete namespace:
kubectl delete namespace todo-ns

Stop Minikube:
minikube stop

---

## 🎯 Conclusion

This project demonstrates the complete workflow of deploying a containerized application using Kubernetes and Minikube, including debugging and real-world issue handling.

---

## 🙌 Author
Gayathri B
