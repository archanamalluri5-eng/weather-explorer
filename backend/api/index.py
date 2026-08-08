"""Vercel entrypoint for the Weather Explorer backend.

Vercel's Python runtime detects ASGI apps by looking for an `app` variable at a
supported entrypoint (this file, inside the api/ directory). The parent dir is
added to sys.path so the `app` package is importable.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.app_factory import app  # noqa: E402
