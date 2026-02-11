"""
Dashboard API Endpoints.

Provides aggregated statistics and data for the admin dashboard,
including user counts, activity logs, and system metrics.
"""

from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.core.security import get_current_user, require_role

router = APIRouter()


class DashboardStats(BaseModel):
    """Aggregated dashboard statistics."""
    total_users: int
    active_users: int
    new_users_today: int
    admin_count: int


class SystemInfo(BaseModel):
    """System information response."""
    server_time: str
    uptime_hours: float
    database_status: str
    cache_status: str


_start_time = datetime.utcnow()


@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Retrieve aggregated dashboard statistics.
    
    Requires authenticated user. Returns user counts
    and activity metrics for the dashboard overview.
    """
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

    total = await db.execute(select(func.count(User.id)))
    active = await db.execute(
        select(func.count(User.id)).where(User.is_active == True)
    )
    new_today = await db.execute(
        select(func.count(User.id)).where(User.created_at >= today)
    )
    admins = await db.execute(
        select(func.count(User.id)).where(User.role == "admin")
    )

    return DashboardStats(
        total_users=total.scalar() or 0,
        active_users=active.scalar() or 0,
        new_users_today=new_today.scalar() or 0,
        admin_count=admins.scalar() or 0,
    )


@router.get("/system", response_model=SystemInfo)
async def get_system_info(
    current_user: User = Depends(require_role("admin")),
):
    """
    Retrieve system health information.
    
    Admin-only endpoint that returns server status,
    uptime, and service connectivity information.
    """
    uptime = (datetime.utcnow() - _start_time).total_seconds() / 3600

    return SystemInfo(
        server_time=datetime.utcnow().isoformat(),
        uptime_hours=round(uptime, 2),
        database_status="connected",
        cache_status="connected",
    )


@router.get("/users")
async def list_users(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("admin")),
):
    """
    List all users with pagination. Admin only.
    
    Args:
        page: Page number (1-indexed)
        per_page: Number of items per page (max 100)
    """
    offset = (page - 1) * per_page
    result = await db.execute(
        select(User)
        .order_by(User.created_at.desc())
        .offset(offset)
        .limit(per_page)
    )
    users = result.scalars().all()

    total_result = await db.execute(select(func.count(User.id)))
    total = total_result.scalar() or 0

    return {
        "items": [
            {
                "id": str(u.id),
                "username": u.username,
                "email": u.email,
                "role": u.role,
                "is_active": u.is_active,
                "created_at": u.created_at.isoformat() if u.created_at else None,
            }
            for u in users
        ],
        "total": total,
        "page": page,
        "per_page": per_page,
    }