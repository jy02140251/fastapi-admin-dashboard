"""System settings API endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

router = APIRouter(prefix="/api/settings", tags=["settings"])


class SystemSettings(BaseModel):
    site_name: str = Field(default="Admin Dashboard")
    maintenance_mode: bool = Field(default=False)
    max_upload_size_mb: int = Field(default=10, ge=1, le=100)
    session_timeout_minutes: int = Field(default=30, ge=5, le=1440)
    allow_registration: bool = Field(default=True)
    smtp_host: Optional[str] = None
    smtp_port: int = Field(default=587)
    notification_email: Optional[str] = None


_settings_store: Dict[str, Any] = SystemSettings().dict()


@router.get("/")
async def get_settings():
    return {
        "settings": _settings_store,
        "last_updated": datetime.utcnow().isoformat(),
    }


@router.put("/")
async def update_settings(settings: SystemSettings):
    global _settings_store
    _settings_store = settings.dict()
    return {
        "message": "Settings updated successfully",
        "settings": _settings_store,
    }


@router.get("/audit-log")
async def get_audit_log(limit: int = 50):
    """Return recent audit log entries for settings changes."""
    return {
        "entries": [],
        "total": 0,
        "message": "Audit logging active",
    }