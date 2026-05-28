# Task Manager Application - Deployment Guide

## 📋 Summary of Changes

### 1. **Backend (app.py)**
- ✅ Added MySQL database integration for persistent storage
- ✅ Implemented CRUD operations:
  - **GET `/api/tasks`** - Retrieve all tasks
  - **POST `/api/tasks`** - Create new task
  - **PUT `/api/tasks/<id>`** - Update task (title/description)
  - **DELETE `/api/tasks/<id>`** - Delete task
  - **PATCH `/api/tasks/<id>/status`** - Toggle task status (pending/completed)
- ✅ Auto-initialization of database schema on startup

### 2. **Frontend (index.html)**
- ✅ Modern minimalist UI with gradient design
- ✅ Features implemented:
  - Add new tasks with keyboard support (Enter key)
  - Edit existing tasks via modal dialog
  - Delete tasks with confirmation
  - Mark tasks as completed with checkbox
  - Responsive design for mobile/desktop
  - Empty state message
  - Real-time task list updates

### 3. **Kubernetes Infrastructure**
Created new k8s manifests:
- **mysql-secret.yaml** - Credentials (user: taskuser, db: tasks_db)
- **mysql-pv.yaml** - 5Gi persistent volume
- **mysql-pvc.yaml** - Persistent volume claim
- **mysql-deployment.yaml** - MySQL 8.0 deployment with resource limits
- **mysql-service.yaml** - ClusterIP service for internal communication
- **deployment.yaml** (updated) - Task app with MySQL env vars and health checks

### 4. **CI/CD Pipeline (Jenkinsfile)**
- ✅ **GitHub Webhook Integration** - `githubPush()` trigger
- ✅ **Automated MySQL Deployment** - Before app deployment
- ✅ **Improved Deployment Process:**
  - Waits for MySQL readiness
  - Handles both fresh and update deployments
  - Rollout status verification
  - Service endpoint verification

## 🚀 Deployment Instructions

### Prerequisites
- Kubernetes cluster running
- Jenkins with:
  - Docker integration
  - kubectl configured with kubeconfig credential
  - Docker Hub credentials (`dockerhub-credential`)
  - Kubernetes config credential (`kubeconfig`)
- GitHub repository with webhook configured

### Step 1: Configure GitHub Webhook
1. Go to your GitHub repository → Settings → Webhooks
2. Click "Add webhook"
3. Payload URL: `http://<jenkins-url>/github-webhook/`
4. Content type: `application/json`
5. Events: "Push events"

### Step 2: Configure Jenkins Credentials
```bash
# Ensure these credentials exist in Jenkins:
# 1. kubeconfig - Kubernetes config file
# 2. dockerhub-credential - Docker Hub username/password
```

### Step 3: Create Kubernetes cluster directories
```bash
# On worker nodes, create storage directory
sudo mkdir -p /mnt/data/mysql
sudo chmod 777 /mnt/data/mysql
```

### Step 4: Trigger Pipeline
Push code to main branch → Jenkins automatically triggers pipeline

## 📊 Deployment Flow

```
GitHub Push Event
    ↓
Jenkins Pipeline Triggered
    ↓
├─ Clone Repository
├─ Build Docker Image
├─ Push to Docker Hub
├─ Deploy MySQL (Secret → PV → PVC → Deployment → Service)
├─ Deploy Task App (with rollout strategy)
└─ Verify Deployment (health checks)
```

## 🔧 Environment Variables

The task app requires these environment variables (provided by Secret):
```yaml
MYSQL_HOST: mysql-service
MYSQL_USER: taskuser
MYSQL_PASSWORD: taskpass123
MYSQL_DB: tasks_db
```

## 📝 Database Schema

```sql
CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

## 🎯 Verification Checklist

After deployment:
- [ ] MySQL pod is running: `kubectl get pods -l app=mysql`
- [ ] Task app pods are running: `kubectl get pods -l app=task-app`
- [ ] Services are created: `kubectl get svc`
- [ ] Access app at: `http://<node-ip>:32123`
- [ ] Can add tasks
- [ ] Can edit tasks
- [ ] Can delete tasks
- [ ] Tasks persist after pod restart

## 🛑 Troubleshooting

### MySQL connection failed
```bash
# Check MySQL pod logs
kubectl logs -l app=mysql

# Verify service is running
kubectl get svc mysql-service
```

### App pod not starting
```bash
# Check app pod logs
kubectl logs -l app=task-app

# Verify all secrets and ConfigMaps
kubectl get secrets
kubectl get configmap
```

### Storage issues
```bash
# Check PVC status
kubectl get pvc

# Check PV status
kubectl get pv
```

## 📚 API Documentation

### GET /api/tasks
Returns all tasks
```bash
curl http://localhost:5000/api/tasks
```

### POST /api/tasks
Create new task
```bash
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "Milk, eggs, bread"}'
```

### PUT /api/tasks/<id>
Update task
```bash
curl -X PUT http://localhost:5000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "New title", "description": "New description"}'
```

### DELETE /api/tasks/<id>
Delete task
```bash
curl -X DELETE http://localhost:5000/api/tasks/1
```

### PATCH /api/tasks/<id>/status
Update task status
```bash
curl -X PATCH http://localhost:5000/api/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'
```

## 🎨 UI Features

- **Gradient Background** - Purple/blue gradient for modern look
- **Task Cards** - Minimalist design with left border accent
- **Edit Modal** - Clean modal dialog for task updates
- **Status Toggle** - Checkbox to mark tasks complete
- **Responsive** - Mobile and desktop friendly
- **Empty State** - Helpful message when no tasks exist
- **Keyboard Support** - Press Enter to add tasks

Enjoy your automated task manager! 🚀
