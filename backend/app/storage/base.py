"""Storage interface used by the rest of the application."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class StoredFile:
    """Metadata about a single stored object."""

    name: str
    size: int
    created_at: datetime


class StorageBackend(ABC):
    """Minimal, cloud-agnostic object-storage interface."""

    @abstractmethod
    def put(self, name: str, data: bytes) -> None:
        """Write ``data`` under key ``name``."""

    @abstractmethod
    def get(self, name: str) -> bytes | None:
        """Read object ``name``; return None if it does not exist."""

    @abstractmethod
    def list(self) -> list[StoredFile]:
        """Return metadata for every stored object."""

    @abstractmethod
    def exists(self, name: str) -> bool:
        """Whether object ``name`` exists."""
