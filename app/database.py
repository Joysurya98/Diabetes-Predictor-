from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ✅ SQLite file path (adjust if needed)
SQLALCHEMY_DATABASE_URL= "sqlite:///D:/python_practice/DiabetesPredictor//diabetes.db"

# ✅ Connect to SQLite (check_same_thread is needed for SQLite with FastAPI)
engine= create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# ✅ Create a session factory (used for DB access)
SessionLocal= sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Base class used to define tables
Base= declarative_base()