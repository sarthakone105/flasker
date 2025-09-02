import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base



# Pull from env (set in docker-compose.yml for backend)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://myuser:mypassword@localhost:5432/myappdb")


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Add this function
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()