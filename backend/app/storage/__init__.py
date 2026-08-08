"""Storage backends for weather JSON files.

Three implementations share one interface (StorageBackend):

* LocalStorage  - plain filesystem, used for development and tests
* GcsStorage    - Google Cloud Storage
* S3Storage     - AWS S3

The factory (get_storage) picks a backend from settings so the app layer never
needs to know which cloud it is talking to.
"""

from __future__ import annotations

from .base import StorageBackend, StoredFile
from .factory import get_storage

__all__ = ["StorageBackend", "StoredFile", "get_storage"]
