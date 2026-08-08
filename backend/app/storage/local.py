"""Filesystem-backed storage. Used for local development and tests."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from .base import StorageBackend, StoredFile


class LocalStorage(StorageBackend):
    def __init__(self, directory: str) -> None:
        self._dir = Path(directory)
        self._dir.mkdir(parents=True, exist_ok=True)

    def _path(self, name: str) -> Path:
        # Prevent path traversal: reject names that escape the data directory.
        candidate = (self._dir / name).resolve()
        if not candidate.is_relative_to(self._dir.resolve()):
            raise ValueError(f"invalid object name: {name!r}")
        return candidate

    def put(self, name: str, data: bytes) -> None:
        self._path(name).write_bytes(data)

    def get(self, name: str) -> bytes | None:
        path = self._path(name)
        if not path.exists() or not path.is_file():
            return None
        return path.read_bytes()

    def list(self) -> list[StoredFile]:
        files: list[StoredFile] = []
        for path in self._dir.iterdir():
            if not path.is_file():
                continue
            stat = path.stat()
            created = datetime.fromtimestamp(stat.st_ctime, tz=timezone.utc)
            files.append(StoredFile(name=path.name, size=stat.st_size, created_at=created))
        files.sort(key=lambda f: f.created_at, reverse=True)
        return files

    def exists(self, name: str) -> bool:
        path = self._path(name)
        return path.exists() and path.is_file()
