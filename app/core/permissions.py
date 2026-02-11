"""Role-based access control (RBAC) permission system."""

from enum import Enum
from typing import Set, Dict
from functools import wraps
from fastapi import HTTPException, Depends


class Permission(str, Enum):
    VIEW_DASHBOARD = "view_dashboard"
    MANAGE_USERS = "manage_users"
    EDIT_SETTINGS = "edit_settings"
    VIEW_LOGS = "view_logs"
    MANAGE_CONTENT = "manage_content"
    EXPORT_DATA = "export_data"
    DELETE_RECORDS = "delete_records"
    MANAGE_ROLES = "manage_roles"


class Role(str, Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"


ROLE_PERMISSIONS: Dict[Role, Set[Permission]] = {
    Role.ADMIN: set(Permission),
    Role.EDITOR: {
        Permission.VIEW_DASHBOARD,
        Permission.MANAGE_CONTENT,
        Permission.VIEW_LOGS,
        Permission.EXPORT_DATA,
    },
    Role.VIEWER: {
        Permission.VIEW_DASHBOARD,
        Permission.VIEW_LOGS,
    },
}


def has_permission(role: str, permission: Permission) -> bool:
    """Check if a role has a specific permission."""
    try:
        role_enum = Role(role)
    except ValueError:
        return False
    return permission in ROLE_PERMISSIONS.get(role_enum, set())


def get_user_permissions(role: str) -> Set[Permission]:
    """Get all permissions for a given role."""
    try:
        role_enum = Role(role)
    except ValueError:
        return set()
    return ROLE_PERMISSIONS.get(role_enum, set())


def require_permission(permission: Permission):
    """Dependency that checks if the current user has the required permission."""
    def dependency(current_user=Depends()):
        if not has_permission(current_user.role, permission):
            raise HTTPException(
                status_code=403,
                detail=f"Permission denied: {permission.value} required",
            )
        return current_user
    return dependency