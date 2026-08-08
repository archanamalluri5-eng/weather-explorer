"""Google Cloud Storage backend (lazy-imported so dev/test need no GCS SDK)."""

from __future__ import annotations

from datetime import timezone

from .base import StorageBackend, StoredFile


class GcsStorage(StorageBackend):
    def __init__(self, bucket: str, project: str | None = None) -> None:
        from google.cloud import storage  # optional dependency

        self._client = storage.Client(project=project) if project else storage.Client()
        self._bucket = self._client.bucket(bucket)

    def _normalise_time(self, dt) -> str:
        if dt is None:
            return ""
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc).isoformat()
        return dt.isoformat()

    def put(self, name: str, data: bytes) -> None:
        blob = self._bucket.blob(name)
        blob.upload_from_string(data, content_type="application/json")

    def get(self, name: str) -> bytes | None:
        blob = self._bucket.blob(name)
        if not blob.exists():
            return None
        return blob.download_as_bytes()

    def list(self) -> list[StoredFile]:
        files: list[StoredFile] = []
        # Generator-based listing avoids loading all objects into memory.
        for blob in self._client.list_blobs(self._bucket, page_size=1000):
            files.append(
                StoredFile(
                    name=blob.name,
                    size=blob.size,
                    created_at=blob.time_created.replace(tzinfo=timezone.utc)
                    if blob.time_created else None,
                )
            )
        files.sort(key=lambda f: f.created_at, reverse=True)
        return files

    def exists(self, name: str) -> bool:
        return self._bucket.blob(name).exists()
