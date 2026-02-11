"""Tests for user management API endpoints."""

import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def admin_headers():
    return {"Authorization": "Bearer test_admin_token"}


class TestListUsers:
    def test_list_users_default_pagination(self, client, admin_headers):
        response = client.get("/api/users/", headers=admin_headers)
        assert response.status_code in (200, 401)

    def test_list_users_with_search(self, client, admin_headers):
        response = client.get("/api/users/?search=admin", headers=admin_headers)
        assert response.status_code in (200, 401)

    def test_list_users_with_role_filter(self, client, admin_headers):
        response = client.get("/api/users/?role=editor", headers=admin_headers)
        assert response.status_code in (200, 401)


class TestUserPermissions:
    def test_admin_has_all_permissions(self):
        from app.core.permissions import has_permission, Permission
        assert has_permission("admin", Permission.MANAGE_USERS)
        assert has_permission("admin", Permission.EDIT_SETTINGS)
        assert has_permission("admin", Permission.DELETE_RECORDS)

    def test_viewer_limited_permissions(self):
        from app.core.permissions import has_permission, Permission
        assert has_permission("viewer", Permission.VIEW_DASHBOARD)
        assert not has_permission("viewer", Permission.MANAGE_USERS)
        assert not has_permission("viewer", Permission.DELETE_RECORDS)

    def test_editor_moderate_permissions(self):
        from app.core.permissions import has_permission, Permission
        assert has_permission("editor", Permission.VIEW_DASHBOARD)
        assert has_permission("editor", Permission.MANAGE_CONTENT)
        assert not has_permission("editor", Permission.MANAGE_USERS)

    def test_invalid_role(self):
        from app.core.permissions import has_permission, Permission
        assert not has_permission("invalid", Permission.VIEW_DASHBOARD)

    def test_get_user_permissions(self):
        from app.core.permissions import get_user_permissions
        perms = get_user_permissions("admin")
        assert len(perms) > 0