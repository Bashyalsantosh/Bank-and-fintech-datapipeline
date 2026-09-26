# 🏦 Nepal Bank Loan Credit Risk Analytics Engine
> **A Production-Ready Medallion Data Pipeline and Risk Telemetry Platform Framework Engineered to Mitigate Non-Performing Assets (NPAs) and Automate Credit Default Predictions.**

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Architecture](https://img.shields.io/badge/Architecture-Medallion%20Pipeline-0EA5E9.svg)]()

---

## 🎯 Central Banking Bottleneck & Business Logic
Commercial and retail lending operations in developing financial ecosystems face heavy baseline exposures due to unstandardized scoring mechanisms and systemic macroeconomic volatility. Manual risk assessments delay liquidity provisioning and heighten default frequencies.

This repository implements a **Decoupled ETL / Analytics Pipeline** that ingests raw banking client application schemas, normalizes multi-variate risk parameters, and applies an algorithmic scoring engine to output a precise **Sovereign Risk Coefficient Index ($R_c$)** served via a glassmorphic command console.

nepal-bank-loan-risk-analytics/
├── .github/workflows/ci.yml             # GitHub Actions CI/CD Pipeline
├── helm/nepal-bank-risk/                 # Enterprise Helm Chart for K8s
├── k8s/                                 # Kubernetes Deployment Manifests
├── frontend/index.html                   # Glassmorphic Command Console UI
├── src/
│   ├── config.py                       # Pydantic Configuration
│   ├── main.py                         # FastAPI REST API (with JWT & Prometheus)
│   ├── models.py                       # SQLAlchemy PostgreSQL Models
│   ├── auth.py                        # JWT Authentication Middleware
│   ├── monitoring.py                    # Prometheus Observability Setup
│   ├── pipelines/
│   │   └── medallion_pipeline.py  # Bronze, Silver, Gold Data Pipeline
│   └── ml/
│       └── train_model.py         # XGBoost MLOps Training Pipeline
├── tests/
│   ├── test_pipeline.py           # Pipeline & Config Unit Tests
│   └── test_api.py                # End-to-End FastAPI Integration Tests
├── Dockerfile                     # Multi-stage Docker Build
├── docker-compose.yml             # Local Multi-container Orchestration
├── requirements.txt               # Pinned Python Dependencies
└── README.md                      # Professional Project Documentation


















---

## 📐 Algorithmic Risk Formulation

The default classification core relies on mapping structural lending vulnerabilities across linear boundaries using the following multi-variate formulation:

$$R_c = (\omega_1 \times DTI) + (\omega_2 \times LTV) + (\omega_3 \times P_{instances})$$

* **DTI:** Debt-to-Income Calculation Metric.
* **LTV:** Loan-to-Value Structural Collateral Coverage Ratio.
* **P_instances:** Chronic occurrences of historical past-due indicators.
* **Operational Weights:** Configured dynamically at $\omega_1 = 0.40, \omega_2 = 0.35, \omega_3 = 0.25$.

---

## 🏗️ Medallion Data Flow Integration
1. **Bronze Layer (Ingestion):** Seamless asynchronous collection of multi-source unstructured json banking records including collateral valuations and demographic bounds.
2. **Silver Layer (Feature Engineering):** Standardizes local script parameters, addresses multi-collinearity errors, transforms text classes into ordinal categories, and builds the static feature matrix.
3. **Gold Layer (Predictive Inference Core):** Matches live application profiles against central bank regulatory risk thresholds to instantly assign credit categories: `CRITICAL DEFAULT RISK`, `WATCHLIST ELEVATED`, or `PASSABLE LOW RISK`.

---

## 🛠️ Repository Setup & Execution Commands

1. Initialize repository and activate the virtual ecosystem block:
   ```bash
   git clone [https://github.com/YourNewName/nepal-bank-loan-risk-analytics.git](https://github.com/YourNewName/nepal-bank-loan-risk-analytics.git)
   cd nepal-bank-loan-risk-analytics
   python3 -m venv venv
   source venv/bin/activate
