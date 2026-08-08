# Cloud Run compatible image for the Weather Explorer backend.
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

# Cloud Run / Render inject PORT at runtime.
EXPOSE 8000
CMD ["sh", "-c", "uvicorn app.app_factory:app --host 0.0.0.0 --port ${PORT:-8000}"]
