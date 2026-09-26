import logging
import pandas as pd
from typing import Dict, Any
from src.config import settings

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class MedallionRiskPipeline:
    def __init__(self, raw_data_path: str):
        self.raw_data_path = raw_data_path

    def ingest_bronze(self) -> pd.DataFrame:
        """Bronze Layer: Asynchronous or batch ingestion of raw multi-source JSON records."""
        logger.info("Executing Bronze Layer: Ingesting raw JSON records...")
        df = pd.read_json(self.raw_data_path)
        return df

    def process_silver(self, df: pd.DataFrame) -> pd.DataFrame:
        """Silver Layer: Standardizing parameters, handling nulls, and building feature matrix."""
        logger.info("Executing Silver Layer: Cleaning and feature engineering...")
        
        # Handle missing values robustly
        df["dti"] = df["dti"].fillna(df["dti"].median())
        df["ltv"] = df["ltv"].fillna(df["ltv"].median())
        df["p_instances"] = df["p_instances"].fillna(0)
        
        # Normalization or scaling bounds if necessary
        return df

    def apply_gold_scoring(self, df: pd.DataFrame) -> pd.DataFrame:
        """Gold Layer: Calculating Sovereign Risk Coefficient Index (Rc) and assigning categories."""
        logger.info("Executing Gold Layer: Applying predictive inference scoring core...")
        
        w1, w2, w3 = settings.weight_dti, settings.weight_ltv, settings.weight_p_instances
        
        # Calculate Risk Coefficient Rc
        df["rc_score"] = (w1 * df["dti"]) + (w2 * df["ltv"]) + (w3 * df["p_instances"])
        
        # Assign Regulatory Categories
        def classify_risk(score: float) -> str:
            if score >= settings.threshold_critical:
                return "CRITICAL DEFAULT RISK"
            elif score >= settings.threshold_watchlist:
                return "WATCHLIST ELEVATED"
            else:
                return "PASSABLE LOW RISK"
                
        df["risk_category"] = df["rc_score"].apply(classify_risk)
        return df

    def run_pipeline(self) -> pd.DataFrame:
        raw_df = self.ingest_bronze()
        silver_df = self.process_silver(raw_df)
        gold_df = self.apply_gold_scoring(silver_df)
        logger.info("Medallion Pipeline executed successfully.")
        return gold_df
