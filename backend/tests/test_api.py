"""Integration tests for the HTTP API (storage = local filesystem)."""

from __future__ import annotations

import json

import pytest

SAMPLE_PAYLOAD = {
    "latitude": 51.5074,
    "longitude": -0.1278,
    "generationtime_ms": 0.5,
    "utc_offset_seconds": 0,
    "timezone": "GMT",
    "daily": {
        "time": ["2024-01-01", "2024-01-02"],
        "temperature_2m_max": [8.1, 9.2],
        "temperature_2m_min": [2.3, 3.1],
        "apparent_temperature_max": [6.0, 7.5],
        "apparent_temperature_min": [0.1, 1.2],
    },
}


class FakeOpenMeteoClient:
    def __init__(self, **kwargs):
        pass

    def fetch_daily_history(self, params):
        return json.dumps(SAMPLE_PAYLOAD).encode()


class FailingOpenMeteoClient:
    def __init__(self, **kwargs):
        pass

    def fetch_daily_history(self, params):
        from app.services.openmeteo import OpenMeteoError

        raise OpenMeteoError("Open-Meteo returned HTTP 500", status_code=502)


@pytest.fixture()
def fake_client(monkeypatch):
    monkeypatch.setattr("app.routes.weather.OpenMeteoClient", FakeOpenMeteoClient)


@pytest.fixture()
def failing_client(monkeypatch):
    monkeypatch.setattr("app.routes.weather.OpenMeteoClient", FailingOpenMeteoClient)


def _store(client, **overrides):
    body = {
        "latitude": 51.5074,
        "longitude": -0.1278,
        "start_date": "2024-01-01",
        "end_date": "2024-01-02",
    }
    body.update(overrides)
    return client.post("/api/store-weather-data", json=body)


class TestStoreWeather:
    def test_valid_request_stores_file(self, client, fake_client):
        response = _store(client)
        assert response.status_code == 200
        payload = response.json()
        assert payload["status"] == "ok"
        assert payload["file"].startswith("weather_51.5074_-0.1278_2024-01-01_2024-01-02_")
        assert payload["file"].endswith(".json")

        # File must actually be stored and contain the raw JSON.
        content_response = client.get(f"/api/weather-file-content/{payload['file']}")
        assert content_response.status_code == 200
        body = content_response.json()
        assert body["data"]["daily"]["temperature_2m_max"] == [8.1, 9.2]

    def test_invalid_latitude(self, client, fake_client):
        response = _store(client, latitude=95.0)
        assert response.status_code == 400
        assert response.json()["status"] == "error"

    def test_invalid_longitude(self, client, fake_client):
        response = _store(client, longitude=-200.0)
        assert response.status_code == 400
        assert response.json()["status"] == "error"

    def test_start_after_end(self, client, fake_client):
        response = _store(client, start_date="2024-02-01", end_date="2024-01-01")
        assert response.status_code == 400

    def test_range_too_long(self, client, fake_client):
        response = _store(client, start_date="2024-01-01", end_date="2024-02-10")
        assert response.status_code == 400

    def test_invalid_date_format(self, client, fake_client):
        response = _store(client, start_date="01-01-2024")
        assert response.status_code == 400

    def test_missing_fields(self, client, fake_client):
        response = client.post("/api/store-weather-data", json={})
        assert response.status_code == 422

    def test_upstream_failure_propagates(self, client, failing_client):
        response = _store(client)
        assert response.status_code == 502
        assert response.json()["status"] == "error"


class TestListFiles:
    def test_empty_bucket(self, client, fake_client):
        response = client.get("/api/list-weather-files")
        assert response.status_code == 200
        assert response.json()["files"] == []

    def test_lists_stored_file(self, client, fake_client):
        stored = _store(client).json()["file"]
        response = client.get("/api/list-weather-files")
        files = response.json()["files"]
        assert len(files) == 1
        assert files[0]["name"] == stored
        assert files[0]["size"] > 0
        assert files[0]["created_at"] is not None


class TestFileContent:
    def test_missing_file_returns_404(self, client):
        response = client.get("/api/weather-file-content/nope.json")
        assert response.status_code == 404
        assert response.json() == {"status": "error", "message": "not found"}

    def test_stored_file_roundtrip(self, client, fake_client):
        stored = _store(client).json()["file"]
        response = client.get(f"/api/weather-file-content/{stored}")
        assert response.status_code == 200
        assert response.json()["file"] == stored
        assert "daily" in response.json()["data"]
