"""API routes: store weather, list files, read file content."""

from __future__ import annotations

import json

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from ..config import settings
from ..services.openmeteo import OpenMeteoClient
from ..services.store import StoreService
from ..storage import StorageBackend, get_storage
from ..validation import parse_date


class StoreWeatherRequest(BaseModel):
    latitude: float = Field(..., description="Latitude in [-90, 90]")
    longitude: float = Field(..., description="Longitude in [-180, 180]")
    start_date: str = Field(..., description="Inclusive start date YYYY-MM-DD")
    end_date: str = Field(..., description="Inclusive end date YYYY-MM-DD")


class StoreWeatherResponse(BaseModel):
    status: str
    file: str


class ErrorResponse(BaseModel):
    status: str
    message: str


router = APIRouter()


def _build_services() -> tuple[StorageBackend, StoreService]:
    storage = get_storage()
    store_service = StoreService(storage, OpenMeteoClient(timeout=settings.openmeteo_timeout))
    return storage, store_service


@router.post(
    "/store-weather-data",
    response_model=StoreWeatherResponse,
    status_code=status.HTTP_200_OK,
    responses={400: {"model": ErrorResponse}, 502: {"model": ErrorResponse}},
)
def store_weather_data(body: StoreWeatherRequest) -> StoreWeatherResponse:
    """Fetch historical weather from Open-Meteo and store the raw JSON."""
    start = parse_date(body.start_date)
    end = parse_date(body.end_date)
    _, store_service = _build_services()
    file_name = store_service.store_weather(body.latitude, body.longitude, start, end)
    return StoreWeatherResponse(status="ok", file=file_name)


@router.get("/list-weather-files")
def list_weather_files():
    """List all stored weather files with basic metadata."""
    storage, _ = _build_services()
    files = storage.list()
    return {
        "files": [
            {
                "name": f.name,
                "size": f.size,
                "created_at": f.created_at.isoformat() if f.created_at else None,
            }
            for f in files
        ]
    }


@router.get(
    "/weather-file-content/{file:path}",
    responses={404: {"model": ErrorResponse}},
)
def weather_file_content(file: str):
    """Return the stored JSON payload for a given file name."""
    storage, _ = _build_services()
    data = storage.get(file)
    if data is None:
        raise HTTPException(
            status_code=404,
            detail={"status": "error", "message": "not found"},
        )
    return JSONResponse(
        status_code=200,
        content={"file": file, "data": json.loads(data)},
    )
