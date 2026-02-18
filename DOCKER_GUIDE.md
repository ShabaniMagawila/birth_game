# Docker Compose Deployment Guide

## Quick Start with Docker Compose

### Prerequisites
- Docker installed
- Docker Compose installed

### Step 1: Clone the Repository
```bash
git clone https://github.com/ShabaniMagawila/birth_game.git
cd birth_game
```

### Step 2: Start All Services
```bash
docker-compose up -d
```

This will start:
- **PostgreSQL Database** on `localhost:5432`
- **FastAPI Backend** on `localhost:8001`
- **Flask Frontend** on `localhost:5000`

### Step 3: Access the Application
- Frontend: http://localhost:5000
- Backend API: http://localhost:8001
- API Docs: http://localhost:8001/docs

### Step 4: View Logs
```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

### Step 5: Stop Services
```bash
docker-compose down
```

### Step 6: Stop and Remove All Data
```bash
docker-compose down -v
```

---

## Service Details

### PostgreSQL Database
- **Host**: postgres (internal) or localhost:5432 (external)
- **Database**: coolify_db
- **Username**: postgres
- **Password**: 0000
- **Port**: 5432
- **Health Check**: Enabled - waits for database to be ready

### FastAPI Backend
- **Port**: 8000 (container), exposed as 8001
- **URL**: http://localhost:8001
- **Docs**: http://localhost:8001/docs
- **Database**: Connected to postgres service
- **Dependencies**: Waits for PostgreSQL health check

### Flask Frontend
- **Port**: 5000
- **URL**: http://localhost:5000
- **API URL**: http://backend:8000 (internal Docker network)
- **Dependencies**: Waits for backend service

---

## Common Docker Compose Commands

### Build Images
```bash
docker-compose build
```

### Build and Start
```bash
docker-compose up --build
```

### Start in Background
```bash
docker-compose up -d
```

### Stop All Services
```bash
docker-compose stop
```

### Remove All Services and Volumes
```bash
docker-compose down -v
```

### Execute Command in Container
```bash
# Access backend container
docker-compose exec backend bash

# Access frontend container
docker-compose exec frontend bash

# Access database
docker-compose exec postgres psql -U postgres -d coolify_db
```

---

## Environment Variables

### Backend (Automatic)
- `DATABASE_URL=postgresql://postgres:0000@postgres:5432/coolify_db`

### Frontend (Automatic)
- `API_URL=http://backend:8000`
- `SECRET_KEY=your-secret-key-change-in-production`

To change these, edit `docker-compose.yml` environment section.

---

## Database Initialization

The database is automatically initialized with:
- Users table with proper schema
- Indexes for performance
- Sample data (John Doe, Jane Smith, Bob Johnson)

To use your backup dump instead:
```bash
# Copy dump file to database folder
cp coolify_db.dump database/

# Create init script that restores from dump
# Then rebuild: docker-compose up --build
```

---

## Troubleshooting

### Port Already in Use
```bash
# Change port in docker-compose.yml
# For example, change 5000:5000 to 5001:5000
```

### Database Connection Failed
- Wait 10-15 seconds for PostgreSQL to start
- Check logs: `docker-compose logs postgres`
- Verify health check: `docker-compose ps`

### Cannot Access Frontend/Backend
- Ensure services are running: `docker-compose ps`
- Check logs: `docker-compose logs`
- Verify ports aren't blocked by firewall

### Reset Everything
```bash
docker-compose down -v
docker system prune -a
docker-compose up --build -d
```

---

## Production Deployment

For production with Coolify:
1. Update `SECRET_KEY` in docker-compose.yml
2. Update database credentials
3. Set proper `DATABASE_URL` with Coolify database
4. Deploy using Coolify's Docker Compose support

Or use the Coolify database credentials in docker-compose.yml:
```yaml
DATABASE_URL: postgresql://postgres:XNTpGsfRKNRJTtD6bh6HFVlm2m2KZaL54WyQdTv1eU9CHuBLEVnzY5JUvnQdVmNj@v4484o8gs0k04w4wswcs08ow:5432/coolify_db
```
