from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

def setup_monitoring(app: FastAPI):
    """Initializes Prometheus metrics instrumentation for FastAPI."""
    Instrumentator().instrument(app).expose(app, endpoint="/metrics")
