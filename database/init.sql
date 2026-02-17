-- Initialize coolify_db database

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index on date_of_birth for faster queries
CREATE INDEX IF NOT EXISTS idx_users_dob ON users(date_of_birth);

-- Sample data (optional)
INSERT INTO users (first_name, last_name, date_of_birth) VALUES
    ('John', 'Doe', '1990-01-15'),
    ('Jane', 'Smith', '1985-06-23'),
    ('Bob', 'Johnson', '1995-12-05')
ON CONFLICT DO NOTHING;
