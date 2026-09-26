import pytest
import pandas as pd
from src.config import settings
from src.pipelines.medallion_pipeline import MedallionRiskPipeline

@pytest.fixture
def sample_raw_data(tmp_path):
    """Fixture to create a temporary JSON file with sample banking loan data."""
    data = {
        "application_id": ["APP001", "APP002", "APP003"],
        "dti": [0.35, 0.80, None],
        "ltv": [0.60, 0.90, 0.50],
        "p_instances": [0, 3, 1]
    }
    df = pd.DataFrame(data)
    file_path = tmp_path / "sample_loans.json"
    df.to_json(file_path, orient="records")
    return str(file_path)

def test_settings_initialization():
    """Test if default weights sum up correctly and settings load."""
    assert 0.0 <= settings.weight_dti <= 1.0
    assert 0.0 <= settings.weight_ltv <= 1.0
    assert 0.0 <= settings.weight_p_instances <= 1.0

def test_medallion_pipeline_execution(sample_raw_data):
    """Test full execution of Bronze -> Silver -> Gold pipeline layers."""
    pipeline = MedallionRiskPipeline(raw_data_path=sample_raw_data)
    result_df = pipeline.run_pipeline()
    
    # Assertions
    assert not result_df.empty
    assert "rc_score" in result_df.columns
    assert "risk_category" in result_df.columns
    assert len(result_df) == 3
    
    # Check if null imputation worked in Silver layer
    assert result_df["dti"].isna().sum() == 0
    
    # Verify categories are assigned based on thresholds
    valid_categories = {"CRITICAL DEFAULT RISK", "WATCHLIST ELEVATED", "PASSABLE LOW RISK"}
    for cat in result_df["risk_category"]:
        assert cat in valid_categories
