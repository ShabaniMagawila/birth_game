-- Database schema for coolify_db

-- Table: users
-- Description: Stores user information including names and date of birth
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_users_dob ON users(date_of_birth);
CREATE INDEX idx_users_names ON users(first_name, last_name);

-- Comments
COMMENT ON TABLE users IS 'Stores user personal information';
COMMENT ON COLUMN users.id IS 'Unique identifier for each user';
COMMENT ON COLUMN users.first_name IS 'User first name';
COMMENT ON COLUMN users.last_name IS 'User last name';
COMMENT ON COLUMN users.date_of_birth IS 'User date of birth';
COMMENT ON COLUMN users.created_at IS 'Timestamp when user was added to the system';
