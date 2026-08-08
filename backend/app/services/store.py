"""Service layer: orchestrates fetching from Open-Meteo and storing the result."""

from __future__ import annotations

from datetime import date

from ..config import settings
from ..storage import StorageBackend
from ..validation import (
    make_timestamp,
    validate_coordinates,
    validate_date_range,
)
from .openmeteo import OpenMeteoClient, OpenMeteoError

OPENMETEO_VARIABLES = [
    "temperature_2m_max",
    "temperature_2m_min",
    "apparent_temperature_max",
    "apparent_temperature_min",
]


def _build_file_name(
    latitude: float, longitude: float, start: date, end: date, ts: str
) -> str:
    # Fixed decimal precision keeps file names predictable and sortable.
    lat = f"{latitude:.4f}"
    lon = f"{longitude:.4f}"
    return f"weather_{lat}_{lon}_{start}_{end}_{ts}.json"


class StoreService:
    def __init__(self, storage: StorageBackend, client: OpenMeteoClient | None = None) -> None:
        self._storage = storage
        self._client = client or OpenMeteoClient(timeout=settings.openmeteo_timeout)

    def store_weather(
        self,
        latitude: float,
        longitude: float,
        start_date: date,
        end_date: date,
    ) -> str:
        validate_coordinates(latitude, longitude)
        validate_date_range(start_date, end_date, settings.max_date_range_days)

        payload = {
            "latitude": latitude,
            "longitude": longitude,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "daily": OPENMETEO_VARIABLES,
            "timezone": "auto",
        }

        try:
            raw = self._client.fetch_daily_history(payload)
        except OpenMeteoError as exc:
            raise exc.to_http_exception()

        file_name = _build_file_name(
            latitude, longitude, start_date, end_date, make_timestamp()
        )
        self._storage.put(file_name, raw)
        return file_name
