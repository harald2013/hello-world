"""ASGI entry point: uvicorn app:app."""

from reports.api import app

__all__ = ["app"]
