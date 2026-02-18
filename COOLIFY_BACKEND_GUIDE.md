# Backend Service Deployment Guide for Coolify

## Overview
This document provides step-by-step instructions for deploying the FastAPI backend service in Coolify. This service depends on the PostgreSQL database, so ensure the database is deployed and running first.

**Prerequisites**: 
- PostgreSQL database deployed in Coolify (see `COOLIFY_DATABASE_GUIDE.md`)
- Database service named `coolify-db`
- Database is healthy and accessible

---

## Backend Service Overview

| Component | Details |
|-----------|---------|
| **Framework** | FastAPI (Python) |
| **Port** | 8000 |
| **Container** | `python:3.11-slim` |
| **Dependencies** | See `backend/requirements.txt` |
| **Database** | PostgreSQL (coolify-db) |

---

## Step 1: Verify Backend Files

Check your backend directory structure:

```
backend/
├── main.py              # FastAPI application
├── models.py            # Database models
├── schemas.py           # Pydantic schemas
├── database.py          # Database configuration
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker build file
└── README.md           # Backend documentation
```

### Key Files:

**`backend/Dockerfile`:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**`backend/requirements.txt`:**
Should contain all Python dependencies:
- fastapi
- uvicorn
- sqlalchemy
- psycopg2-binary
- pydantic
- (and others as needed)

---

## Step 2: Prepare Backend Configuration

### Backend `database.py` Configuration

Your `backend/database.py` is already configured to support Coolify deployment. It automatically builds the database URL from individual environment variables:

```python
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Database configuration
# Try to build from individual components first (Coolify friendly)
if all([os.getenv('POSTGRES_USER'), os.getenv('POSTGRES_PASSWORD'), 
        os.getenv('POSTGRES_HOST'), os.getenv('POSTGRES_DB')]):
    DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT', '5432')}/{os.getenv('POSTGRES_DB')}"
else:
    # Fall back to DATABASE_URL or local default
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:0000@localhost:5432/coolify_db"
    )

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

**This approach:**
- ✅ Uses individual `POSTGRES_*` env vars when available (Coolify-friendly)
- ✅ Falls back to `DATABASE_URL` if set
- ✅ Uses local dev defaults as last resort

### Update `backend/main.py`

Ensure your FastAPI app is configured to run with Uvicorn:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Your routes here...

if __name__ == "__main__":
    # Note: Uvicorn will run this via CMD in Dockerfile
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

---

## Step 3: Deploy Backend Service in Coolify

### In Coolify Dashboard:

1. **Open your project** (`coolify-app`)

2. **Click Add Service** → Select **Docker**

### Configuration:

#### Basic Settings

| Setting | Value | Notes |
|---------|-------|-------|
| Service Name | `coolify-backend` | Internal hostname for other services |
| Container Name | `birth_game_backend` | Display name |
| Port | `8000` | FastAPI runs on this port |
| Public Port | `8001` | Make accessible externally (optional) |

#### Docker Configuration

| Setting | Value | Notes |
|---------|-------|-------|
| Dockerfile Path | `backend/Dockerfile` | Relative to repo root |
| Build Context | `backend/` | Directory to build from |
| Image Name | `coolify-backend` | Auto-generated |

#### Git/Source (if using Git)

| Setting | Value | Notes |
|---------|-------|-------|
| Repository URL | Your GitHub URL | The full project repo |
| Branch | `main` | Or your default branch |
| Build Type | `Docker` | Use Dockerfile |

Or if uploading manually:
- Upload the entire project or just the backend folder
- Ensure paths are preserved

#### Environment Variables

**Click Add Environment Variable for each:**

**Required Database Variables:**
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<your-database-password>
POSTGRES_HOST=coolify-db
POSTGRES_PORT=5432
POSTGRES_DB=coolify_db
```

**Replace `<your-database-password>`** with the exact password from your `coolify-db` service.

**Optional Application Settings:**
```
PYTHON_ENV=production
LOG_LEVEL=info
```

**Full Environment Variables List:**
```env
# Database Configuration (Required)
# These must match your database service settings
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<your-database-password>
POSTGRES_HOST=coolify-db
POSTGRES_PORT=5432
POSTGRES_DB=coolify_db

# Application Settings (Optional)
PYTHON_ENV=production
LOG_LEVEL=info

# Alternative: Use DATABASE_URL instead of individual variables
# DATABASE_URL=postgresql://postgres:<password>@coolify-db:5432/coolify_db
```

**Note:** The backend automatically builds the database connection URL from the individual `POSTGRES_*` variables. This is more Coolify-friendly than manually constructing the `DATABASE_URL`.

#### Health Check (Optional but Recommended)

| Setting | Value | Notes |
|---------|-------|-------|
| Health Check Enabled | `Yes` |  |
| Health Check Endpoint | `/docs` or `/health` | FastAPI docs endpoint |
| Interval | `30s` | Check every 30 seconds |
| Timeout | `10s` | Wait 10s for response |
| Retries | `3` | Retry 3 times before marking unhealthy |

#### Service Dependencies

| Setting | Value | Notes |
|---------|-------|-------|
| Depends On | `coolify-db` | Wait for database before starting |

3. **Click Deploy**

---

## Step 4: Monitor Deployment

### Check Build Progress

1. Open the `coolify-backend` service
2. Go to **Logs** tab
3. Watch for:
   - ✅ `Building image...`
   - ✅ `Installing dependencies from requirements.txt`
   - ✅ `Build successful`
   - ✅ `Starting container...`
   - ✅ `Uvicorn running on 0.0.0.0:8000`

### Common Startup Messages

**Expected successful logs:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Application startup complete
```

**Issues to watch for:**
```
ERROR: ModuleNotFoundError: No module named 'fastapi'
→ Solution: Ensure requirements.txt is being installed

ERROR: could not translate host name "coolify-db" to address
→ Solution: Database service not running or not healthy

ERROR: connection refused (postgres)
→ Solution: Database service may not be ready, wait a bit

ERROR: Database URL not set
→ Solution: Verify DATABASE_URL environment variable
```

---

## Step 5: Verify Backend Service

### Status Check

1. Check service is **Running** (green status)
2. Logs show no errors
3. Container is healthy

### API Connectivity Test

#### From Coolify Interface:

Within Coolify, test the API endpoint:
```
http://coolify-backend:8000
```

#### From Another Service (Frontend will do this):

Frontend will use:
```
http://coolify-backend:8000
```

#### From External (Your Computer):

```bash
# Test if API is accessible
curl http://<coolify-server-ip>:8001/docs

# Should return HTML of the Swagger UI documentation page
```

#### Using Python:

```python
import requests

response = requests.get("http://<coolify-server-ip>:8000/docs")
if response.status_code == 200:
    print("✅ Backend is accessible!")
else:
    print(f"❌ Backend returned {response.status_code}")
```

### Access API Documentation

Visit in your browser:
```
http://<coolify-server-ip>:8001/docs
```

This shows:
- All API endpoints
- Request/response schemas
- Ability to test endpoints
- OpenAPI/Swagger documentation

---

## Step 6: Verify Database Connection

### Check Database Connection in Backend

The backend should establish a connection to the database on startup.

**In Logs, look for:**
```
✅ Connected to PostgreSQL database
✅ Database tables initialized
```

**Or if there's an error:**
```
❌ ERROR: Connection failed to database
❌ ERROR: password authentication failed for user "postgres"
```

### Test Database Connectivity (Optional)

Add a test endpoint to verify the connection:

**In `backend/main.py`:**

```python
from sqlalchemy import text
from database import engine

@app.get("/health")
async def health_check():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}, 500
```

Then test:
```bash
curl http://<coolify-server-ip>:8000/health
# Should return: {"status":"healthy","database":"connected"}
```

---

## Backend Service Summary

### Access Points

| Access Path | Used By | Details |
|-------------|---------|---------|
| `coolify-backend:8000` | Frontend service | Internal Docker network |
| `http://<server-ip>:8001` | External users | Public IP address |
| `http://<server-ip>:8001/docs` | Developers | Swagger UI documentation |

### Service Details

```
Service Name: coolify-backend
Hostname: coolify-backend
Port: 8000
Database: coolify-db
Status: Should show "Running" in Coolify
```

### Environment Variables Used

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<your-database-password>
POSTGRES_HOST=coolify-db
POSTGRES_PORT=5432
POSTGRES_DB=coolify_db
PYTHON_ENV=production
```

---

## Troubleshooting

### Issue: Backend Container Crashes Immediately

**Symptoms**: Service crashes after a few seconds

**Solutions**:
```bash
# 1. Check logs for Python errors
# Look for ImportError, SyntaxError, etc.

# 2. Verify requirements.txt exists and is formatted correctly
# Each dependency on a new line, no empty lines

# 3. Test build locally first
docker build -f backend/Dockerfile -t test-backend backend/
docker run test-backend
```

### Issue: Can't Connect to Database

**Error**: `could not translate host name "coolify-db" to address` or `password authentication failed`

**Solutions**:
1. ✅ Verify database service is deployed and running
2. ✅ Check database service name is exactly `coolify-db`
3. ✅ Verify all `POSTGRES_*` environment variables are set correctly:
   - `POSTGRES_USER=postgres`
   - `POSTGRES_PASSWORD=<exact-match-with-database>`
   - `POSTGRES_HOST=coolify-db`
   - `POSTGRES_PORT=5432`
   - `POSTGRES_DB=coolify_db`
4. ✅ **Password must exactly match database password** - check for typos!
5. ✅ Wait for database to be fully healthy before backend starts
6. ✅ Add dependency: backend depends on `coolify-db`
7. ✅ After updating env vars, click **Update** then **Restart**/**Redeploy**

### Issue: API Endpoints Return 500 Error

**Symptoms**: `/docs` loads but other endpoints fail

**Solutions**:
1. Check backend logs for stack trace
2. Verify database migrations ran successfully
3. Check database has correct schema
4. Verify environment variables are set correctly
5. Look for import errors or configuration issues

### Issue: API Documentation Loads But Endpoints Don't Work

**Symptoms**: FastAPI Swagger UI loads but GET/POST requests fail

**Solutions**:
```bash
# 1. Check CORS configuration in main.py
# 2. Verify database connection
# 3. Check request payloads match schemas
# 4. Review error response body for details
```

### Issue: Port 8000 Already in Use

**Solutions**:
1. Change port in Coolify service config (e.g., 8001)
2. Or kill existing process on port 8000
3. Update frontend API_URL to match new port

### Issue: Dependency Installation Fails

**Error**: `ERROR: Could not find a version that satisfies...`

**Solutions**:
1. Review `backend/requirements.txt` for typos
2. Ensure versions are compatible with Python 3.11
3. Remove version pins and let pip find compatible versions
4. Test requirements locally:
   ```bash
   python -m pip install -r backend/requirements.txt
   ```

---

## Performance Considerations

### Resource Limits (Optional)

In Coolify, you can set:
- **CPU Limit**: `0.5` - `1` CPU core
- **Memory Limit**: `512MB` - `1GB`
- **Storage**: Depends on how much data you store

### Scaling

For production with multiple requests:
- Monitor CPU and memory usage in Coolify
- If hitting limits, increase resource allocation
- Consider horizontal scaling (multiple instances) if needed

---

## Production Checklist

- [ ] Database service is running and healthy
- [ ] Backend service is running without errors
- [ ] API documentation page loads (`/docs`)
- [ ] Test endpoint responds correctly
- [ ] Database connection is established
- [ ] Environment variables are set correctly
- [ ] CORS is configured properly
- [ ] API is accessible from frontend service
- [ ] Logs show no errors
- [ ] Health check endpoint responds

---

## Next Steps

After Backend is Successfully Deployed:

1. ✅ Database deployed
2. ✅ Backend deployed and connected
3. → Move to **Frontend Service Deployment** in `COOLIFY_FRONTEND_DEPLOYMENT_GUIDE.md`

For detailed multi-service setup, see: `COOLIFY_DEPLOYMENT_GUIDE.md`
