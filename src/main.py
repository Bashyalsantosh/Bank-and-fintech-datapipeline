from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
import pandas as pd
from src.config import settings
from src.pipelines.medallion_pipeline import MedallionRiskPipeline
import os

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Production-grade REST API for Nepal Bank Loan Credit Risk Analytics Engine"
)

# Request Body Model for Single/Batch Application
class LoanApplicationRequest(BaseModel):
    application_id: str = Field(..., example="APP-2026-001")
    dti: float = Field(..., ge=0.0, le=1.0, example=0.45, description="Debt-to-Income Ratio")
    ltv: float = Field(..., ge=0.0, le=2.0, example=0.70, description="Loan-to-Value Ratio")
    p_instances: int = Field(..., ge=0, example=1, description="Chronic past-due instances")

class RiskResponseModel(BaseModel):
    application_id: str
    rc_score: float
    risk_category: str
    environment: str

@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    """System Health and Status Check Endpoint."""
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "environment": settings.environment
    }

@app.post("/api/v1/predict-risk", response_model=RiskResponseModel, status_code=status.HTTP_200_OK)
def predict_credit_risk(payload: LoanApplicationRequest):
    """Calculates Sovereign Risk Coefficient Index (Rc) and assigns regulatory risk tiers."""
    try:
        # Convert incoming payload to DataFrame format for pipeline compatibility
        input_data = pd.DataFrame([{
            "application_id": payload.application_id,
            "dti": payload.dti,
            "ltv": payload.ltv,
            "p_instances": payload.p_instances
        }])
        
        # Temporary file path or direct processing (Here we use an ad-hoc dataframe run)
        w1, w2, w3 = settings.weight_dti, settings.weight_ltv, settings.weight_p_instances
        rc_score = (w1 * payload.dti) + (w2 * payload.ltv) + (w3 * payload.p_instances)
        
        # Regulatory Category Assignment
        if rc_score >= settings.threshold_critical:
            risk_category = "CRITICAL DEFAULT RISK"
        elif rc_score >= settings.threshold_watchlist:
            risk_category = "WATCHLIST ELEVATED"
        else:
            risk_category = "PASSABLE LOW RISK"
            
        return RiskResponseModel(
            application_id=payload.application_id,
            rc_score=round(rc_score, 4),
            risk_category=risk_category,
            environment=settings.environment
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing credit risk score: {str(e)}"
        )
