from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    app_name: str = "Nepal Bank Loan Credit Risk Analytics Engine"
    environment: str = Field(default="development", validation_alias="ENVIRONMENT")
    
    # Algorithmic Risk Weights (ω1, ω2, ω3)
    weight_dti: float = Field(default=0.40, description="Debt-to-Income Weight")
    weight_ltv: float = Field(default=0.35, description="Loan-to-Value Weight")
    weight_p_instances: float = Field(default=0.25, description="Past-due Instances Weight")
    
    # Regulatory Thresholds (NRB Guidelines Mapping)
    threshold_critical: float = Field(default=0.75, description="Critical Default Risk Threshold")
    threshold_watchlist: float = Field(default=0.45, description="Watchlist Elevated Risk Threshold")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
