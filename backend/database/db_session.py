from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.database.db_models import Base

# DATABASE_URL
DATABASE_URL = "mysql+mysqlconnector://user:password@localhost:3307/resume_matcher?charset=utf8mb4"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
Base.metadata.create_all(bind=engine)