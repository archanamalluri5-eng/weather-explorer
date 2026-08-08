"""Storage backend factory.

Priority:
1. Explicit STORAGE_BACKEND env var ("local", "gcs", "s3").
2. Otherwise auto-detect: GCS if GOOGLE_CLOUD_PROJECT is set, else S3 if
   AWS credentials exist, else local filesystem.
"""

from __future__ import annotations

import os

from .base import StorageBackend
from .gcs import GcsStorage
from .local import LocalStorage
from .s3 import S3Storage


def get_storage() -> StorageBackend:
    from ..config import settings

    backend = settings.storage_backend

    if not backend:
        if settings.gcp_project:
            backend = "gcs"
        elif os.getenv("AWS_ACCESS_KEY_ID") or os.getenv("AWS_PROFILE"):
            backend = "s3"
        else:
            backend = "local"

    if backend == "local":
        return LocalStorage(settings.local_data_dir)
    if backend == "gcs":
        return GcsStorage(settings.bucket, settings.gcp_project or None)
    if backend == "s3":
        return S3Storage(settings.bucket, settings.s3_region)
    raise ValueError(f"unsupported storage backend: {backend!r}")
