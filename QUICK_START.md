# Quick Start Guide - Task Manager App

## 🚀 Setup dalam 5 menit

### 1. Worker Node Setup (Satu kali saja)
```bash
# SSH ke setiap worker node
ssh root@<worker-ip>

# Create MySQL storage directory
mkdir -p /mnt/data/mysql
chmod 777 /mnt/data/mysql
```

### 2. Jenkins Setup (Satu kali saja)
```bash
# Di Jenkins UI: Manage Jenkins → Manage Credentials → Global credentials

# Buat credential: kubeconfig
Credentials → Add → Secret file
ID: kubeconfig
File: Upload ~/.kube/config dari master node

# Buat credential: dockerhub-credential
Credentials → Add → Username with password
Username: <docker_hub_username>
Password: <docker_hub_token>
ID: dockerhub-credential
```

### 3. GitHub Webhook Setup (Satu kali saja)
```
Repository → Settings → Webhooks → Add webhook
Payload URL: http://<JENKINS_URL>/github-webhook/
Content type: application/json
Events: Push events
Click: Add webhook
```

### 4. First Deployment
```bash
# Jika sudah setup di atas, cukup push ke main:
git push origin main

# Jenkins akan otomatis build dan deploy
# Check status di: http://<jenkins-ip>:8080
```

## 📊 Status Commands

```bash
# Check MySQL
kubectl get pods -l app=mysql
kubectl logs -l app=mysql

# Check Task App
kubectl get pods -l app=task-app
kubectl logs -l app=task-app

# Check Services
kubectl get svc

# Get NodePort
kubectl get svc python-app-service -o jsonpath='{.spec.ports[0].nodePort}'
```

## 🎯 Access Application
```
http://<node-ip>:32123
```

## 🧪 Quick Test
```bash
# Add task
curl -X POST http://<node-ip>:32123/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Task"}'

# Get tasks
curl http://<node-ip>:32123/api/tasks

# Delete task
curl -X DELETE http://<node-ip>:32123/api/tasks/1
```

## 🛠️ If Something Goes Wrong

```bash
# Restart MySQL
kubectl delete pod -l app=mysql

# Restart App
kubectl delete pod -l app=task-app

# View recent Jenkins builds
Jenkins UI → ci_cd job → Build History

# View Jenkinsfile logs
Jenkins UI → Recent Build → Console Output
```

---

**Selamat! Anda siap untuk automated CI/CD! 🎉**
