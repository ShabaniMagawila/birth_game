# Coolify Deployment Guide - Multi-Service Setup

## Overview
This guide explains how to deploy your application as separate services in Coolify:
1. **Database Service** - PostgreSQL
2. **Backend Service** - FastAPI (depends on Database)
3. **Frontend Service** - Flask (depends on Backend)

All services will be part of the same Coolify project and communicate via internal networking.

---

## Prerequisites
- Coolify instance running and accessible
- Docker installed on your Coolify server
- Git repository with this project (optional but recommended)

---

## Part 1: Deploy PostgreSQL Database

### Step 1: Create a New Service in Coolify

1. Go to your Coolify dashboard
2. Click **Projects** → **Create New Project** (if not already created)
3. Name your project: `coolify-app` (or your preferred name)
4. Click **Create**

### Step 2: Add PostgreSQL Database Service

1. In your project, click **Add Service**
2. Select **Database** → **PostgreSQL**
3. Configure the following:
   - **Service Name**: `coolify-db`
   - **Database Name**: `coolify_db`
   - **Username**: `postgres`
   - **Password**: `0000` (change this in production!)
   - **Port**: `5432` (default, can use internal port only)
4. Click **Deploy**

### Step 3: Initialize Database Schema

After PostgreSQL is deployed:

1. In the Coolify dashboard, find your `coolify-db` service
2. Click on it → **Logs** to verify it's running
3. Execute the initialization script:
   - Option A: Use Coolify's database shell/exec feature
   - Option B: Use your local psql client:
     ```bash
     psql -h <coolify-server-ip> -U postgres -d coolify_db -f database/init.sql
     ```

### Database Connection Details (for next services)
- **Internal Host**: `coolify-db` (when connecting from other Coolify services)
- **External Host**: `<your-coolify-server-ip>`
- **Port**: `5432`
- **Database**: `coolify_db`
- **User**: `postgres`
- **Password**: `0000`

---

## Part 2: Deploy Backend Service (FastAPI)

### Step 1: Create Coolify Configuration

Create a file in your backend folder for Coolify-specific settings:

**File**: `backend/coolify.dockerfile` (optional, or use existing Dockerfile)

The existing `backend/Dockerfile` should work fine with these settings.

### Step 2: Add Backend Service to Coolify

1. In your Coolify project, click **Add Service**
2. Select **Docker** (for custom Docker-based services)
3. Configure the following:

#### Basic Settings:
- **Service Name**: `coolify-backend`
- **Port**: `8000`
- **Public Port**: `8001` (or leave empty if using reverse proxy)

#### Docker Configuration:
- **Dockerfile Path**: `backend/Dockerfile` (relative to project root)
- **Build Context**: `backend/` (or root if building from git)

#### Environment Variables:
```
DB_HOST=coolify-db
DB_PORT=5432
DB_USERNAME=postgres
DB_PASSWORD=<your-database-password>
DB_DATABASE=coolify_db
PYTHON_ENV=production
```

**Note:** Replace `<your-database-password>` with the actual password from your database service.

#### Advanced (if using Git):
- **Git Repository**: Your GitHub repo URL
- **Git Branch**: `main` (or your default branch)
- **Build Strategy**: `Docker` with Dockerfile

4. Click **Deploy**

### Step 3: Verify Backend Deployment

1. Wait for the build and deployment to complete
2. Check **Logs** tab to verify the FastAPI server started
3. Test the API:
   ```bash
  curl http://<coolify-server-ip>:8001/docs
   ```

---

## Part 3: Deploy Frontend Service (Flask)

### Step 1: Add Frontend Service to Coolify

1. In your Coolify project, click **Add Service**
2. Select **Docker** (for custom Docker-based services)
3. Configure the following:

#### Basic Settings:
- **Service Name**: `coolify-frontend`
- **Port**: `5000`
- **Public Port**: `5000` (or leave empty if using reverse proxy)

#### Docker Configuration:
- **Dockerfile Path**: `frontend/Dockerfile`
- **Build Context**: `frontend/` (or root if building from git)

#### Environment Variables:
```
API_URL=http://coolify-backend:8000
SECRET_KEY=your-secret-key-change-in-production
FLASK_ENV=production
```

#### Advanced (if using Git):
- **Git Repository**: Your GitHub repo URL
- **Git Branch**: `main`
- **Build Strategy**: `Docker` with Dockerfile

4. Click **Deploy**

### Step 2: Verify Frontend Deployment

1. Wait for the build and deployment to complete
2. Check **Logs** tab
3. Access the application:
   ```
   http://<coolify-server-ip>:5000
   ```

---

## Networking & Communication

### Internal Service Communication (within Coolify)
When services are deployed in the same Coolify project, they can communicate using service names:

- **Backend connects to Database**: `coolify-db:5432`
- **Frontend connects to Backend**: `coolify-backend:8000`

### External Access
- **Frontend**: `http://<your-coolify-server-ip>:5000`
- **Backend API**: `http://<your-coolify-server-ip>:8001`
- **Backend Docs**: `http://<your-coolify-server-ip>:8001/docs`

---

## Environment Variables Reference

### Database Service (PostgreSQL)
```
POSTGRES_DB=coolify_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<your-generated-password>
```

**Important:** Use a strong password generated by Coolify, not `0000`!

### Backend Service (FastAPI)
```
DB_HOST=coolify-db
DB_PORT=5432
DB_USERNAME=postgres
DB_PASSWORD=<same-as-database-password>
DB_DATABASE=coolify_db
PYTHON_ENV=production
```

**Important:** The backend password must exactly match your database password!

### Frontend Service (Flask)
```
API_URL=http://coolify-backend:8000
SECRET_KEY=your-secret-key-change-in-production
FLASK_ENV=production
```

---

## Troubleshooting

### Backend Can't Connect to Database
- **Error**: `connection refused` or `host not found`
- **Solution**: 
  - Verify database service is running (check Logs)
  - Ensure DATABASE_URL environment variable uses `coolify-db` (internal hostname)
  - Check that backend service depends on database service

### Frontend Can't Connect to Backend
- **Error**: `connection refused` or API calls fail
- **Solution**:
  - Verify backend is running and healthy
  - Ensure API_URL environment variable is `http://coolify-backend:8000`
  - Check Flask app logs for details

### Service Crashes After Deployment
- **Solution**: Check service Logs tab for Python errors
  - For backend: Check uvicorn startup
  - For frontend: Check Flask app startup
  - Verify all dependencies in requirements.txt are compatible

### Database Data Persists But Service Won't Start
- **Solution**: 
  - Check database logs
  - Verify init.sql has correct SQL syntax
  - Confirm credentials match environment variables

---

## Deployment Checklist

- [ ] Database service deployed and running
- [ ] Backend service deployed and connected to database
- [ ] Frontend service deployed and connected to backend
- [ ] All services accessible from outside (if needed)
- [ ] Environment variables set correctly for each service
- [ ] Logs showing no errors for all services
- [ ] Test frontend at `http://<server>:5000`
- [ ] Test backend API at `http://<server>:8000/docs`

---

## Production Considerations

1. **Change Database Password**: Don't use `0000` in production
2. **Update SECRET_KEY**: Generate a secure key for Flask
3. **Use HTTPS**: Configure reverse proxy (nginx/caddy) for SSL
4. **Database Backups**: Set up automated backup strategy
5. **Monitoring**: Enable Coolify's monitoring/logging features
6. **Resource Limits**: Set CPU and memory limits per service
7. **Auto-restart**: Enable restart policies for services

---

## Next Steps

1. Deploy database service first
2. Verify database is healthy
3. Deploy backend service
4. Verify backend connects to database
5. Deploy frontend service
6. Verify all services communicate correctly
