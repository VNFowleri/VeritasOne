import ssl
import sys
import subprocess
import time
import requests
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from datetime import datetime, timezone


# Ensure necessary packages are installed
def ensure_installed(package):
    try:
        __import__(package)
    except ImportError:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])


# Required packages
required_packages = ["pg8000", "fastapi", "sqlalchemy", "requests"]
for package in required_packages:
    ensure_installed(package)

# Ensure SSL module is available
try:
    ssl.create_default_context()
except AttributeError:
    raise ImportError("SSL module is required but missing. Ensure Python is installed with SSL support.")

# Update database URL for Neon Tech PostgreSQL
DATABASE_URL = "postgresql://neondb_owner:npg_n6q9MyOcXUDi@ep-dawn-heart-a5xge8c0-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require"


def create_db_engine_with_retries(url, retries=5, delay=3):
    for attempt in range(retries):
        try:
            db_engine = create_engine(url, pool_pre_ping=True)
            with db_engine.connect() as conn:
                conn.close()
            print("✅ Successfully connected to the database!")
            return db_engine
        except Exception as e:
            print(f"Database connection failed (attempt {attempt + 1}/{retries}): {e}")
            time.sleep(delay)
    raise ConnectionError("Failed to connect to the database after multiple attempts.")


engine = create_db_engine_with_retries(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Database Models
class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    dob = Column(String, nullable=False)
    consent_status = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class MedicalRecord(Base):
    __tablename__ = "medical_records"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    record_type = Column(String, nullable=False)  # FHIR or OCR-based
    record_content = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    patient = relationship("Patient")


# Initialize DB
def init_db():
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables are set up and ready!")


# FastAPI App Setup
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def health_check():
    return {"message": "✅ FastAPI server is running!"}


# FHIR API Connection
FHIR_BASE_URL = "https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4"
FHIR_PATIENT_ENDPOINT = f"{FHIR_BASE_URL}/Patient"
FHIR_ACCESS_TOKEN = "YOUR_EPIC_SANDBOX_ACCESS_TOKEN"


@app.get("/fhir/patient/{patient_id}")
def get_fhir_patient(patient_id: str):
    headers = {"Authorization": f"Bearer {FHIR_ACCESS_TOKEN}"}
    response = requests.get(f"{FHIR_PATIENT_ENDPOINT}/{patient_id}", headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=f"Failed to fetch FHIR data: {response.text}")


if __name__ == "__main__":
    init_db()
    print("🚀 FastAPI application is running! Access the API at http://127.0.0.1:8000")
