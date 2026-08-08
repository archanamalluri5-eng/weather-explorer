"""Unit tests for validation helpers."""

from __future__ import annotations

import pytest
from fastapi import HTTPException

from app.validation import (
    parse_date,
    validate_coordinates,
    validate_date_range,
)


class TestCoordinates:
    def test_valid_values(self):
        validate_coordinates(0.0, 0.0)
        validate_coordinates(-90.0, -180.0)
        validate_coordinates(90.0, 180.0)

    @pytest.mark.parametrize("lat", [-90.01, 90.01, 1000, -1000])
    def test_invalid_latitude(self, lat):
        with pytest.raises(HTTPException) as exc:
            validate_coordinates(lat, 0.0)
        assert exc.value.status_code == 400

    @pytest.mark.parametrize("lon", [-180.01, 180.01, 1000, -1000])
    def test_invalid_longitude(self, lon):
        with pytest.raises(HTTPException) as exc:
            validate_coordinates(0.0, lon)
        assert exc.value.status_code == 400


class TestDateRange:
    def test_valid_range(self):
        validate_date_range(parse_date("2024-01-01"), parse_date("2024-01-31"), 31)

    def test_start_after_end(self):
        with pytest.raises(HTTPException) as exc:
            validate_date_range(parse_date("2024-02-01"), parse_date("2024-01-01"), 31)
        assert exc.value.status_code == 400

    def test_range_too_long(self):
        with pytest.raises(HTTPException) as exc:
            validate_date_range(parse_date("2024-01-01"), parse_date("2024-02-10"), 31)
        assert exc.value.status_code == 400

    @pytest.mark.parametrize("bad", ["2024-13-01", "01/02/2024", "yesterday", "", None])
    def test_invalid_date_string(self, bad):
        with pytest.raises(HTTPException) as exc:
            parse_date(bad)
        assert exc.value.status_code == 400
