"""Validation helpers shared by routes and services."""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

from fastapi import HTTPException


def validate_coordinates(latitude: float, longitude: float) -> None:
    if not (-90.0 <= latitude <= 90.0):
        raise HTTPException(
            status_code=400,
            detail={"status": "error", "message": "latitude must be between -90 and 90"},
        )
    if not (-180.0 <= longitude <= 180.0):
        raise HTTPException(
            status_code=400,
            detail={"status": "error", "message": "longitude must be between -180 and 180"},
        )


def validate_date_range(start_date: date, end_date: date, max_days: int) -> None:
    if start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail={"status": "error", "message": "start_date must be <= end_date"},
        )
    if (end_date - start_date).days + 1 > max_days:
        raise HTTPException(
            status_code=400,
            detail={
                "status": "error",
                "message": f"date range must be at most {max_days} days",
            },
        )


def parse_date(value: str) -> date:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=400,
            detail={
                "status": "error",
                "message": f"invalid date {value!r}, expected YYYY-MM-DD",
            },
        )


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def make_timestamp(dt: datetime | None = None) -> str:
    """Compact UTC timestamp safe for object names, e.g. 20260601T153042Z."""
    dt = dt or utc_now()
    return dt.strftime("%Y%m%dT%H%M%SZ")
