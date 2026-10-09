from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import (
    DB_SERVER,
    DB_NAME,
    DB_DRIVER,
    DB_TRUSTED_CONNECTION
)


# ==========================================
# Database Connection URL
# ==========================================

DATABASE_URL = (
    f"mssql+pyodbc://@{DB_SERVER}/{DB_NAME}"
    f"?driver={DB_DRIVER.replace(' ', '+')}"
    f"&Trusted_Connection={DB_TRUSTED_CONNECTION}"
    f"&TrustServerCertificate=yes"
)


# ==========================================
# SQLAlchemy Engine
# ==========================================

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=False
)


# ==========================================
# SQLAlchemy Session Factory
# ==========================================

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


# ==========================================
# SQLAlchemy Declarative Base
# ==========================================

Base = declarative_base()


# ==========================================
# Database Dependency
# ==========================================

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# ==========================================
# Database Connection Test
# ==========================================

def test_database_connection():

    try:

        with engine.connect() as connection:

            result = connection.execute(
                text("SELECT 1")
            )

            print("Database connection successful.")

            print(
                "Test result:",
                result.scalar()
            )

    except Exception as e:

        print("Database connection failed.")

        print("Error:", e)

if __name__ == "__main__":

    test_database_connection()