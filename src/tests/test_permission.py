"""
Tests for Permission enum
"""

import pytest

from myc_http_tools.models.permission import Permission


class TestPermission:
    """Test cases for Permission enum"""

    def test_permission_values(self):
        """Test that Permission enum has correct values"""
        assert Permission.READ.value == "read"
        assert Permission.WRITE.value == "write"

    def test_permission_from_i32_read(self):
        """Test from_i32 method with READ permission code"""
        permission = Permission.from_i32(0)
        assert permission == Permission.READ

    def test_permission_from_i32_write(self):
        """Test from_i32 method with WRITE permission code"""
        permission = Permission.from_i32(1)
        assert permission == Permission.WRITE

    def test_permission_from_i32_invalid_code(self):
        """Test from_i32 method with invalid permission code"""
        with pytest.raises(ValueError, match="Invalid permission code: 2"):
            Permission.from_i32(2)

    def test_permission_from_i32_negative_code(self):
        """Test from_i32 method with negative permission code"""
        with pytest.raises(ValueError, match="Invalid permission code: -1"):
            Permission.from_i32(-1)

    def test_permission_from_i32_large_code(self):
        """Test from_i32 method with large permission code"""
        with pytest.raises(ValueError, match="Invalid permission code: 999"):
            Permission.from_i32(999)

    def test_permission_enum_membership(self):
        """Test that Permission enum members are correctly defined"""
        assert hasattr(Permission, "READ")
        assert hasattr(Permission, "WRITE")
        assert len(list(Permission)) == 2

    def test_permission_string_representation(self):
        """Test string representation of Permission enum"""
        assert str(Permission.READ) == "Permission.READ"
        assert str(Permission.WRITE) == "Permission.WRITE"

    def test_permission_equality(self):
        """Test equality comparison of Permission enum values"""
        assert Permission.READ == Permission.READ
        assert Permission.WRITE == Permission.WRITE
        assert Permission.READ != Permission.WRITE

    def test_permission_identity(self):
        """Test that Permission enum values are singletons"""
        assert Permission.READ is Permission.READ
        assert Permission.WRITE is Permission.WRITE
        assert Permission.READ is not Permission.WRITE
