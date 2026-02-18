# Database Service Deployment Guide for Coolify

## Overview
This document provides step-by-step instructions for deploying the PostgreSQL database as the first service in your Coolify project.

---

## Prerequisites
- Coolify instance running and accessible
- Access to Coolify dashboard
- The database initialization files ready (`database/init.sql` and `database/schema.sql`)

---

## Step 1: Verify Database Files

Check that your database initialization files exist and are correct:

### Current Database Files:
- `database/init.sql` - Initialization commands
- `database/schema.sql` - Schema definition
- `database/coolify_db.dump` - Database dump (optional backup)

These files contain the SQL needed to set up your database structure.

---

## Step 2: Create Project in Coolify

1. **Log in to Coolify Dashboard**
   - Navigate to your Coolify instance
   - Go to **Projects**

2. **Create New Project:**
   - Click **Create New Project** button
   - **Project Name**: `coolify-app`
   - **Description**: Multi-service application (Database, Backend, Frontend)
   - Click **Create**

---

## Step 3: Deploy PostgreSQL Database Service

### In Coolify Dashboard:

1. **Click into your new project** (`coolify-app`)

2. **Add Database Service:**
   - Click **Add Service**
   - Select **PostgreSQL** from the database options
   - Or select **Docker** if PostgreSQL isn't directly available

### Configuration:

**If PostgreSQL is directly available:**

| Setting | Value | Notes |
|---------|-------|-------|
| Service Name | `coolify-db` | This is the internal hostname |
| Container Name | `coolify_postgres` | Display name |
| Database Name | `coolify_db` | Your main database |
| Username | `postgres` | Default PostgreSQL user |
| Password | `0000` | Change in production! |
| Port | `5432` | Standard PostgreSQL port |
| Image | `postgres:15-alpine` | Lightweight PostgreSQL image |

**Environment Variables:**
```
POSTGRES_DB=coolify_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=0000
```

**Volumes/Storage:**
- **Mount Point**: `/var/lib/postgresql/data`
- **Volume Name**: `postgres_data` or let Coolify auto-create
- **Purpose**: Persist database data between restarts

3. **Click Deploy**

### Waiting for Deployment:
- The service will build and start
- Check the **Logs** tab to monitor progress
- Wait until you see: `PostgreSQL is ready` or `server started`
- Status should show **Running** (green)

---

## Step 4: Apply Database Schema

After the PostgreSQL service is running:

### Option A: Using Coolify's Database Shell

1. Click on the `coolify-db` service
2. Look for **Console** or **Shell** tab
3. Access the PostgreSQL shell:
   ```bash
   psql -U postgres -d coolify_db
   ```
4. Execute your schema:
   ```sql
   \i /path/to/database/schema.sql
   ```

### Option B: Using Docker Exec (if available in Coolify)

1. Upload or ensure `database/schema.sql` is accessible to the container
2. Execute via Coolify's exec function:
   ```bash
   psql -U postgres -d coolify_db -f /docker-entrypoint-initdb.d/schema.sql
   ```

### Option C: Using Local PostgreSQL Client

If you have `psql` installed locally:

```bash
# First, get your Coolify server's IP
# Then run:
psql -h <coolify-server-ip> -U postgres -d coolify_db -f database/schema.sql
```

**Password when prompted**: `0000`

### Option D: Via Docker Volume Mount (Recommended)

In Coolify, configure the service with a volume mount:

**Volume Binding:**
- **Host Path**: `./database/init.sql`
- **Container Path**: `/docker-entrypoint-initdb.d/init.sql`
- **Purpose**: Automatically runs on container startup

This will automatically execute your initialization SQL when PostgreSQL starts.

---

## Step 5: Verify Database Setup

### Check Database Status:

1. **In Coolify:**
   - Open the `coolify-db` service
   - Check **Logs** section
   - Look for message indicating database is ready

2. **Connection Test (from local machine):**
   ```bash
   # Install psql if needed (on Windows: use WSL or PostgreSQL installer)
   psql -h <coolify-server-ip> -U postgres -d coolify_db
   ```

3. **Verify Tables Created:**
   ```sql
   \dt
   ```
   Should show your tables if schema was applied correctly.

### Connection Information

**For services in same Coolify project (internal):**
```
Host: coolify-db
Port: 5432
Database: coolify_db
User: postgres
Password: 0000
URL: postgresql://postgres:0000@coolify-db:5432/coolify_db
```

**For external access (from your machine):**
```
Host: <your-coolify-server-ip>
Port: 5432
Database: coolify_db
User: postgres
Password: 0000
URL: postgresql://postgres:0000@<coolify-server-ip>:5432/coolify_db
```

---

## Database Service Summary

### Service Details:
- **Service Name in Coolify**: `coolify-db`
- **Internal Hostname**: `coolify-db`
- **Port**: `5432`
- **Database**: `coolify_db`
- **User**: `postgres`
- **Password**: `0000`
- **Image**: `postgres:15-alpine`

### What Other Services Will Use:
When you deploy the Backend and Frontend services, they will reference:
```
DATABASE_URL=postgresql://postgres:0000@coolify-db:5432/coolify_db
```

The hostname `coolify-db` works automatically because Coolify creates an internal network for services in the same project.

---

## Troubleshooting

### Database Service Won't Start
- **Check Logs**: Look for PostgreSQL error messages
- **Verify Password**: Ensure `POSTGRES_PASSWORD` is set correctly
- **Check Storage**: Ensure volume has enough space
- **Review Image**: Confirm `postgres:15-alpine` image can be pulled

### Can't Connect to Database
- **From Coolify Service**: Use `coolify-db:5432`
- **From External**: Use `<your-server-ip>:5432`
- **Verify Port**: Is 5432 exposed/available?
- **Check Credentials**: Username `postgres`, password `0000`

### Database Data Lost After Restart
- **Issue**: Volume not properly configured
- **Solution**: Ensure volume mount is set for `/var/lib/postgresql/data`
- **Check**: Verify `postgres_data` volume exists in Coolify storage

### Tables Not Created After Initialization
- **Re-initialize**: Check `database/init.sql` for syntax errors
- **Manual Setup**: Run schema script manually through psql
- **Verify File**: Ensure init.sql is in correct location `/docker-entrypoint-initdb.d/`

---

## Next Steps

After confirming the database is running:

1. ✅ Database deployed and healthy
2. → Move to **Backend Service Deployment** in `COOLIFY_BACKEND_DEPLOYMENT_GUIDE.md`
3. → Then **Frontend Service Deployment**

---

## Security Notes for Production

⚠️ **IMPORTANT**: The configuration above is for development only!

For production:
- [ ] Change password from `0000` to a strong password
- [ ] Use environment variables for sensitive data
- [ ] Enable SSL/TLS for database connections
- [ ] Restrict database access to only required services
- [ ] Set up automated backups
- [ ] Monitor database logs for suspicious activity
- [ ] Use secrets management system (Coolify Secrets)
