"""Thin client around the Open-Meteo Historical Weather API.

Docs: https://open-meteo.com/en/docs/historical-weather-api
"""

from __future__ import annotations

import json
import time
from typing import Any

import httpx

OPENMETEO_URL = "https://archive-api.open-meteo.com/v1/archive"

# Cap how many files (in storage) we inspect to generate a unique name if the
# first attempt collides (should essentially never happen).
MAX_NAME_UNIQUE_ATTEMPTS = 5


class OpenMeteoError(Exception):
    """Wraps an upstream Open-Meteo failure with a user-facing message."""

    def __init__(self, message: str, status_code: int = 502) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code

    def to_http_exception(self):
        from fastapi import HTTPException

        return HTTPException(
            status_code=self.status_code,
            detail={"status": "error", "message": self.message},
        )


class OpenMeteoClient:
    def __init__(self, timeout: float = 15.0, max_retries: int = 2) -> None:
        self._timeout = timeout
        self._max_retries = max_retries

    def fetch_daily_history(self, params: dict[str, Any]) -> bytes:
        last_error: OpenMeteoError | None = None
        for attempt in range(self._max_retries + 1):
            if attempt:
                time.sleep(0.5 * attempt)
            try:
                with httpx.Client(timeout=self._timeout) as client:
                    response = client.get(OPENMETEO_URL, params=params)
            except httpx.HTTPError as exc:
                last_error = OpenMeteoError(
                    f"Open-Meteo request failed: {exc.__class__.__name__}"
                )
                continue

            if response.status_code == 200:
                # Validate the body is JSON before storing it.
                try:
                    response.json()
                except json.JSONDecodeError:
                    raise OpenMeteoError(
                        "Open-Meteo returned an unreadable response", status_code=502
                    )
                return response.content

            last_error = OpenMeteoError(
                f"Open-Meteo returned HTTP {response.status_code}",
                status_code=502 if response.status_code >= 500 else 502,
            )

        assert last_error is not None
        raise last_error
