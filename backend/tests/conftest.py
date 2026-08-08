"""Shared test fixtures."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.storage.local import LocalStorage


@pytest.fixture()
def client(tmp_path, monkeypatch):
    """App wired to a throwaway local storage directory."""
    storage = LocalStorage(str(tmp_path))
    monkeypatch.setattr("app.routes.weather.get_storage", lambda: storage)
    with TestClient(app) as test_client:
        yield test_client
