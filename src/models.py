from sqlalchemy import create_engine, Column, String, Float, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/loan_risk_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class LoanRiskRecord(Base):
    __tablename__ = "loan_risk_records"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(String, unique=True, index=True, nullable=False)
    dti = Column(Float, nullable=False)
    ltv = Column(Float, nullable=False)
    p_instances = Column(Integer, nullable=False)
    rc_score = Column(Float, nullable=False)
    risk_category = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

def init_db():
    """Initializes database tables."""
    Base.metadata.create_all(bind=engine)
