from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db import Base

# Define User table
class User(Base):
    __tablename__ = 'users'
    username = Column(String, primary_key=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    consent = Column(Boolean, default=False)
    diagnostics = relationship("Diagnostic", back_populates="user")

# Diagnostics table (common metadata)
class Diagnostic(Base):
    __tablename__ = 'diagnostics'
    diagnostic_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, ForeignKey('users.username'), nullable=False)
    diagnostic_type = Column(String, nullable=False)  # 'stroke', 'diabetes', 'heart_disease'
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="diagnostics")

# Diabetes diagnostics
class DiabetesDiagnostic(Base):
    __tablename__ = 'diabetes_diagnostics'
    diagnostic_id = Column(Integer, ForeignKey('diagnostics.diagnostic_id'), primary_key=True)
    pregnancies = Column(String)
    glucose = Column(String)
    blood_pressure = Column(String)
    skin_thickness = Column(String)
    insulin = Column(String)
    bmi = Column(String)
    diabetes_pedigree_function = Column(String)
    age = Column(String)

# Stroke diagnostics
class StrokeDiagnostic(Base):
    __tablename__ = 'stroke_diagnostics'
    diagnostic_id = Column(Integer, ForeignKey('diagnostics.diagnostic_id'), primary_key=True)
    gender = Column(String)
    age = Column(String)
    hypertension = Column(String)
    heart_disease = Column(String)
    ever_married = Column(String)
    work_type = Column(String)
    residence_type = Column(String)
    avg_glucose_level = Column(String)
    bmi = Column(String)
    smoking_status = Column(String)

# Heart Disease diagnostics
class HeartDiseaseDiagnostic(Base):
    __tablename__ = 'heart_disease_diagnostics'
    diagnostic_id = Column(Integer, ForeignKey('diagnostics.diagnostic_id'), primary_key=True)
    age = Column(String)
    sex = Column(String)
    chest_pain_type = Column(String)
    resting_bp = Column(String)
    cholesterol = Column(String)
    fasting_bs = Column(String)
    resting_ecg = Column(String)
    max_hr = Column(String)
    exercise_angina = Column(String)
    oldpeak = Column(String)
    st_slope = Column(String)