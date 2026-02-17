# Database Setup

## PostgreSQL Database - coolify_db

This folder contains the database configuration and initialization scripts for the Coolify App.

## Database Setup (Local PostgreSQL)

The database has already been created on your local PostgreSQL instance.

### Database Connection Details

- **Host:** localhost
- **Port:** 5432
- **Database:** coolify_db
- **Username:** postgres
- **Password:** 0000

### Connection String

```
postgresql://postgres:0000@localhost:5432/coolify_db
```

### Recreate Database (if needed)

If you need to recreate the database:

```bash
# Drop existing database (if exists)
$env:PGPASSWORD='0000'; psql -U postgres -h localhost -c "DROP DATABASE IF EXISTS coolify_db;"

# Create new database
$env:PGPASSWORD='0000'; psql -U postgres -h localhost -c "CREATE DATABASE coolify_db;"

# Initialize schema and data
$env:PGPASSWORD='0000'; psql -U postgres -h localhost -d coolify_db -f init.sql
```

## Files

- `init.sql` - Database initialization script
- `schema.sql` - Database schema documentation



## Database Schema

### Users Table

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key |
| first_name | VARCHAR(100) | User's first name |
| last_name | VARCHAR(100) | User's last name |
| date_of_birth | DATE | User's date of birth |
| created_at | TIMESTAMP | Record creation timestamp |

## Accessing the Database

### Using psql (Command Line)

```bash
$env:PGPASSWORD='0000'; psql -U postgres -h localhost -d coolify_db
```

### View tables:
```bash
$env:PGPASSWORD='0000'; psql -U postgres -h localhost -d coolify_db -c "\dt"
```

### View data:
```bash
$env:PGPASSWORD='0000'; psql -U postgres -h localhost -d coolify_db -c "SELECT * FROM users;"
```

### Using pgAdmin or other GUI tools

- Host: localhost
- Port: 5432
- Database: coolify_db
- Username: postgres
- Password: 0000