"""Application configuration.

All settings are read from environment variables so the same code runs
identically in local development, CI, and on Cloud Run / Render / Lambda.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Settings:
    # Which storage backend to use: "local", "gcs", "s3" (auto-detected if blank).
    storage_backend: str = os.getenv("STORAGE_BACKEND", "").lower()
    # Directory used by the local backend (and dev default).
    local_data_dir: str = os.getenv("LOCAL_DATA_DIR", "data")
    # Bucket / container name for gcs or s3.
    bucket: str = os.getenv("STORAGE_BUCKET", "weather-explorer")
    # Google Cloud Storage settings.
    gcp_project: str = os.getenv("GOOGLE_CLOUD_PROJECT", "")
    # AWS S3 settings (boto3 picks up credentials from env / IAM role).
    s3_region: str = os.getenv("AWS_REGION", "us-east-1")
    # CORS: comma separated list of allowed origins. "*" allows all (dev default).
    cors_origins: list[str] = field(
        default_factory=lambda: [
            o.strip()
            for o in os.getenv("CORS_ORIGINS", "*").split(",")
            if o.strip()
        ]
    )
    # Timeout for upstream Open-Meteo calls, in seconds.
    openmeteo_timeout: float = float(os.getenv("OPENMETEO_TIMEOUT", "15"))
    # Maximum date range allowed per request (per spec).
    max_date_range_days: int = 31


def get_settings() -> Settings:
    return Settings()


settings = get_settings()
