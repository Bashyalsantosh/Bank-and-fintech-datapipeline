from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health_check_endpoint():
    """Test health check endpoint for system uptime and configuration status."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "app_name" in data

def test_predict_credit_risk_valid_payload():
    """Test credit risk prediction endpoint with valid loan parameters."""
    payload = {
        "application_id": "APP-TEST-999",
        "dti": 0.40,
        "ltv": 0.65,
        "p_instances": 0
    }
    response = client.post("/api/v1/predict-risk", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    assert data["application_id"] == "APP-TEST-999"
    assert "rc_score" in data
    assert "risk_category" in data
    assert data["risk_category"] in ["CRITICAL DEFAULT RISK", "WATCHLIST ELEVATED", "PASSABLE LOW RISK"]

def test_predict_credit_risk_invalid_payload():
    """Test validation error handling when invalid DTI or LTV bounds are provided."""
    payload = {
        "application_id": "APP-INVALID",
        "dti": 1.5,  # Invalid: should be <= 1.0 based on validation rules
        "ltv": 0.5,
        "p_instances": 1
    }
    response = client.post("/api/v1/predict-risk", json=payload)
    assert response.status_code == 422  # Unprocessable Entity (Pydantic validation failure)
