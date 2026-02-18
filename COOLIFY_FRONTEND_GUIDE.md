# Frontend Service Deployment Guide for Coolify

## Overview
This document provides step-by-step instructions for deploying the Flask frontend service in Coolify. This service depends on the FastAPI backend, so ensure the backend is deployed and running first.

**Prerequisites**: 
- FastAPI backend deployed in Coolify (see `COOLIFY_BACKEND_GUIDE.md`)
- Backend service named `coolify-backend`
- Backend is healthy and accessible

---

## Frontend Service Overview

| Component | Details |
|-----------|---------|
| **Framework** | Flask (Python) |
| **Port** | 5000 |
| **Container** | `python:3.11-slim` |
| **Dependencies** | See `frontend/requirements.txt` |
| **Backend** | FastAPI (coolify-backend) |

---

## Step 1: Verify Frontend Files

Check your frontend directory structure:

```
frontend/
├── app.py              # Flask application
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker build file
├── .env                # Environment variables (local)
├── .dockerignore        # Docker ignore file
├── README.md           # Frontend documentation
└── templates/
    ├── index.html      # Main form page
    ├── result.html     # User result page
    └── users.html      # List all users page
```

### Key Files:

**`frontend/Dockerfile`:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
```

**`frontend/requirements.txt`:**
Should contain all Python dependencies:
- Flask
- requests
- python-dotenv
- (and others as needed)

---

## Step 2: Prepare Frontend Configuration

### Frontend `app.py` Configuration

Your `frontend/app.py` is already configured for Coolify deployment. It automatically uses the `API_URL` environment variable:

```python
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "your-secret-key-here")

# Backend API URL - loads from environment variable
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Routes use API_URL to connect to backend
@app.route('/submit', methods=['POST'])
def submit_user():
    response = requests.post(
        f"{API_URL}/users/",
        json={...}
    )
    # ... rest of code
```

**This approach:**
- ✅ Uses `API_URL` environment variable for backend connection
- ✅ Falls back to local development default (localhost:8000)
- ✅ Loads SECRET_KEY from environment for session security
- ✅ Error handling for backend connection failures

---

## Step 3: Deploy Frontend Service in Coolify

### In Coolify Dashboard:

1. **Open your project** (`coolify-app`)

2. **Click Add Service** → Select **Docker**

### Configuration:

#### Basic Settings

| Setting | Value | Notes |
|---------|-------|-------|
| Service Name | `coolify-frontend` | Internal hostname for other services |
| Container Name | `birth_game_frontend` | Display name |
| Port | `5000` | Flask runs on this port |
| Public Port | `5000` | Make accessible externally |

#### Docker Configuration

| Setting | Value | Notes |
|---------|-------|-------|
| Dockerfile Path | `frontend/Dockerfile` | Relative to repo root |
| Build Context | `frontend/` | Directory to build from |
| Image Name | `coolify-frontend` | Auto-generated |

#### Git/Source (Recommended - Use Your GitHub Repo)

**Since your code is on GitHub, use Git deployment for automatic updates:**

| Setting | Value | Notes |
|---------|-------|-------|
| Repository URL | `https://github.com/ShabaniMagawila/birth_game.git` | Your GitHub repo |
| Branch | `main` | Or your default branch |
| Build Type | `Docker` | Use Dockerfile |
| Dockerfile Path | `frontend/Dockerfile` | Relative to repo root |
| Build Context | `.` or `frontend/` | Use `.` for root context |

**Benefits:**
- 🔄 Click **Redeploy** to pull latest code from GitHub
- 📦 No manual file uploads needed
- 🔁 Easy rollbacks to previous commits

#### Environment Variables

**Click Add Environment Variable for each:**

**Required Backend Connection Variable:**
```
API_URL=http://coolify-backend:8000
```

**Optional but Recommended:**
```
SECRET_KEY=your-very-secure-secret-key-change-this-in-production
```

**Full Environment Variables List:**
```env
# Backend Connection (Required)
API_URL=http://coolify-backend:8000

# Flask Security (Required)
SECRET_KEY=your-very-secure-secret-key-change-this-in-production

# Flask Settings (Optional)
FLASK_ENV=production
DEBUG=False
```

**Important Notes:**
- `API_URL=http://coolify-backend:8000` uses internal hostname (works within Coolify network)
- `SECRET_KEY` should be a long random string for production
- Do NOT use debug mode in production

#### Health Check (Optional but Recommended)

| Setting | Value | Notes |
|---------|-------|-------|
| Health Check Enabled | `Yes` |  |
| Health Check Endpoint | `/` | Home page endpoint |
| Interval | `30s` | Check every 30 seconds |
| Timeout | `10s` | Wait 10s for response |
| Retries | `3` | Retry 3 times before marking unhealthy |

#### Service Dependencies

| Setting | Value | Notes |
|---------|-------|-------|
| Depends On | `coolify-backend` | Wait for backend before starting |

3. **Click Deploy**

---

## Step 4: Monitor Deployment

### Check Build Progress

1. Open the `coolify-frontend` service
2. Go to **Logs** tab
3. Watch for:
   - ✅ `Building image...`
   - ✅ `Installing dependencies from requirements.txt`
   - ✅ `Build successful`
   - ✅ `Starting container...`
   - ✅ `Running on http://0.0.0.0:5000`

### Common Startup Messages

**Expected successful logs:**
```
WARNING in app.run() This is a development server. Do not use it in a production deployment.
 * Running on http://0.0.0.0:5000
```

**Issues to watch for:**
```
ERROR: ModuleNotFoundError: No module named 'flask'
→ Solution: Ensure requirements.txt is being installed

ERROR: Could not connect to backend
→ Solution: Backend service not running or API_URL is incorrect

ERROR: Connection refused on coolify-backend:8000
→ Solution: Backend service may not be ready, wait a bit
```

---

## Step 5: Verify Frontend Service

### Status Check

1. Check service is **Running** (green status)
2. Logs show no errors
3. Container is healthy

### Web Application Tests

#### From External (Your Browser)

Visit the application:
```
http://<coolify-server-ip>:5000
```

Or use your domain:
```
http://<your-coolify-domain>:5000
```

**Expected Page:** You should see the user form with fields for:
- First Name
- Last Name
- Date of Birth

#### Test the Form Submission

1. **Fill out the form:**
   - First Name: John
   - Last Name: Doe
   - Date of Birth: 1990-01-15

2. **Click Submit**

3. **Verify Result:**
   - Should display the user data
   - Should show calculated age
   - Should show day of week born

4. **If it fails:**
   - Check backend is accessible
   - Check backend logs for errors
   - Verify API_URL is correct

---

## Step 6: Verify Backend Connection

### Test Backend Connectivity

The frontend should connect to the backend on startup and when handling requests.

**In Logs, look for:**
```
✅ Frontend started successfully
✅ Backend connection working
```

**Or if there's an error:**
```
❌ ERROR: Cannot connect to backend API
❌ errno: Connection refused
```

### Manual Backend Test

From your Coolify machine or locally:

```bash
# Test if backend is accessible from frontend container
curl http://coolify-backend:8000/

# Should return: {"message":"Welcome to User Birthday API"}
```

---

## Frontend Service Summary

### Access Points

| Access Path | Used By | Details |
|-------------|---------|---------|
| `http://<server-ip>:5000` | End users | Public IP address |
| `coolify-backend:8000` | Frontend service | Internal Docker network |
| `http://<domain>:5000` | End users | Your domain/CNAME |

### Service Details

```
Service Name: coolify-frontend
Hostname: coolify-frontend
Port: 5000
Backend: coolify-backend:8000
Status: Should show "Running" in Coolify
```

### Environment Variables Used

```env
API_URL=http://coolify-backend:8000
SECRET_KEY=your-very-secure-secret-key-change-this-in-production
FLASK_ENV=production
DEBUG=False
```

---

## Troubleshooting

### Issue: Frontend Container Crashes Immediately

**Symptoms**: Service crashes after a few seconds

**Solutions**:
```bash
# 1. Check logs for Python errors
# Look for ImportError, SyntaxError, etc.

# 2. Verify requirements.txt exists and is formatted correctly
# Each dependency on a new line, no empty lines

# 3. Test build locally first
docker build -f frontend/Dockerfile -t test-frontend frontend/
docker run -p 5000:5000 test-frontend
```

### Issue: Can't Access Frontend Website

**Error**: `Cannot reach http://server:5000` or connection timeout

**Solutions**:
1. ✅ Verify frontend service is deployed and running (green status)
2. ✅ Check frontend service logs for errors
3. ✅ Verify firewall allows port 5000
4. ✅ Check if address is correct:
   - Your Coolify domain or IP
   - Port 5000
5. ✅ Try accessing from Coolify server directly:
   ```bash
   curl http://localhost:5000
   ```

### Issue: Frontend Page Loads But Form Buttons Don't Work

**Symptoms**: Page displays but submitting form hangs or fails

**Solutions**:
1. ✅ Check that backend service is running and healthy
2. ✅ Verify `API_URL` environment variable is set correctly:
   - Should be: `http://coolify-backend:8000`
   - NOT `http://localhost:8000`
   - NOT `http://<server-ip>:8001`
3. ✅ Check frontend logs for connection errors
4. ✅ Check backend logs for request errors
5. ✅ Test backend directly:
   ```bash
   curl http://coolify-backend:8000/
   ```

### Issue: Backend Connection Refused

**Error**: `Cannot connect to backend API` or `Connection refused`

**Solutions**:
1. ✅ Verify backend service is deployed and running
2. ✅ Check backend service name is exactly `coolify-backend`
3. ✅ Verify `API_URL` uses `coolify-backend` hostname (not IP)
4. ✅ Wait for backend to be fully healthy before frontend starts
5. ✅ Add dependency: frontend depends on `coolify-backend`
6. ✅ After updating env vars, click **Update** then **Restart**/**Redeploy**
7. ✅ Check if backend has correct DATABASE_URL set

### Issue: Form Data Not Being Saved

**Error**: Form submits but user not created, or 500 error

**Solutions**:
1. Check backend logs for database errors
2. Verify backend can connect to database
3. Verify database tables exist
4. Check backend logs for any Python errors
5. Test backend directly:
   ```bash
   curl -X POST http://coolify-backend:8000/users/ \
     -H "Content-Type: application/json" \
     -d '{"first_name":"John","last_name":"Doe","date_of_birth":"1990-01-15"}'
   ```

### Issue: Seeing "Secret Key" or Session Errors

**Error**: `BadSignature` or session errors in logs

**Solutions**:
1. Verify `SECRET_KEY` is set in environment
2. Use a complex random string (at least 32 characters)
3. Don't use same SECRET_KEY on multiple instances (unless intended)
4. Restart frontend after changing SECRET_KEY

### Issue: Static Files or Templates Not Loading

**Error**: 404 on CSS/JS/images, or blank page

**Solutions**:
1. Verify `templates/` directory is in Docker build context
2. Verify Dockerfile copies all files:
   ```dockerfile
   COPY . .  # This should copy everything including templates/
   ```
3. Check frontend logs for template loading errors
4. Verify your templates are in `frontend/templates/` folder

### Issue: Too Many Requests / Rate Limiting

**Error**: 429 or service sluggish

**Solutions**:
1. Check if backend is slow or struggling
2. Increase backend resource limits in Coolify
3. Add caching in frontend if applicable
4. Check backend database connections aren't maxed out

---

## Performance Considerations

### Resource Limits (Optional)

In Coolify, you can set:
- **CPU Limit**: `0.25` - `0.5` CPU core (frontend is lightweight)
- **Memory Limit**: `256MB` - `512MB` (Flask is very low memory)
- **Storage**: Minimal (just application files)

### Scaling

For production with many users:
- Frontend is lightweight, scales easily
- Monitor backend performance instead
- If backend is bottleneck, increase backend resources
- Frontend can handle many concurrent users with minimal resources

---

## Production Checklist

- [ ] Backend service is running and healthy
- [ ] Frontend service is running without errors
- [ ] Website loads at `http://<your-domain>:5000`
- [ ] Form page displays correctly
- [ ] Form submission works (test with sample data)
- [ ] User list page works (`/users`)
- [ ] `API_URL` is set to `http://coolify-backend:8000`
- [ ] `SECRET_KEY` is set to a secure random string
- [ ] `FLASK_ENV=production` is set
- [ ] `DEBUG=False` is set
- [ ] Logs show no errors
- [ ] Backend is accessible from frontend

---

## Next Steps

After Frontend is Successfully Deployed:

1. ✅ Database deployed
2. ✅ Backend deployed and connected
3. ✅ Frontend deployed and connected
4. → **Full Application Stack is Ready!** 🎉

### Final Verification:

1. Visit frontend at `http://<domain>:5000`
2. Create a new user
3. View list of users
4. Check backend logs show user was created
5. Check database has new user record

---

## Security Notes for Production

⚠️ **IMPORTANT**: The configuration above requires security hardening for production!

For production:
- [ ] Change `SECRET_KEY` to a long random string (32+ characters)
- [ ] Use HTTPS/SSL (configure in reverse proxy)
- [ ] Set `FLASK_ENV=production`
- [ ] Set `DEBUG=False`
- [ ] Use environment variables for all secrets
- [ ] Restrict `API_URL` to your domain only (no localhost)
- [ ] Set up CORS properly in backend
- [ ] Implement rate limiting
- [ ] Use secrets management system (Coolify Secrets)
- [ ] Set up monitoring and alerts
- [ ] Use strong database passwords
- [ ] Keep dependencies updated

---

For detailed multi-service setup, see: [COOLIFY_DEPLOYMENT_GUIDE.md](COOLIFY_DEPLOYMENT_GUIDE.md)
