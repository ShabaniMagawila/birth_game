from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
# Build from individual components (Coolify friendly)
# Supports both DB_* and POSTGRES_* variable names
db_host = os.getenv('DB_HOST') or os.getenv('POSTGRES_HOST') or 'localhost'
db_port = os.getenv('DB_PORT') or os.getenv('POSTGRES_PORT') or '5432'
db_user = os.getenv('DB_USERNAME') or os.getenv('POSTGRES_USER') or 'postgres'
db_password = os.getenv('DB_PASSWORD') or os.getenv('POSTGRES_PASSWORD') or '0000'
db_name = os.getenv('DB_DATABASE') or os.getenv('POSTGRES_DB') or 'coolify_db'

# Build the connection URL
if all([db_host, db_port, db_user, db_password, db_name]):
    DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
else:
    # Fall back to explicit DATABASE_URL if provided
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()


# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
