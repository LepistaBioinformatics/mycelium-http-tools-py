"""
Tests for LicensedResource class
"""

import base64
import pytest

from myc_http_tools.models.licensed_resources import LicensedResource
from myc_http_tools.models.permission import Permission


class TestLicensedResourceFromStr:
    """Test cases for LicensedResource.from_str method"""

    def test_valid_url_parsing_read_permission(self):
        """Test parsing a valid URL with READ permission"""
        tenant_id = "123e4567-e89b-12d3-a456-426614174000"
        account_id = "987fcdeb-51a2-43d1-9f12-345678901234"
        role_id = "456e7890-e89b-12d3-a456-426614174567"
        role_name = "admin"
        permission_code = "0"  # READ
        sys_value = "1"  # True
        verified_value = "1"  # True
        account_name = "Test Account"

        # Encode account name
        name_encoded = base64.b64encode(account_name.encode("utf-8")).decode("ascii")

        # Construct URL path
        url_path = f"t/{tenant_id}/a/{account_id}/r/{role_id}?p={role_name}:{permission_code}&s={sys_value}&v={verified_value}&n={name_encoded}"

        resource = LicensedResource.from_str(url_path)

        assert str(resource.tenant_id) == tenant_id
        assert str(resource.acc_id) == account_id
        assert str(resource.role_id) == role_id
        assert resource.role == role_name
        assert resource.perm == Permission.READ
        assert resource.sys_acc is True
        assert resource.acc_name == account_name
        assert resource.verified is True

    def test_valid_url_parsing_write_permission(self):
        """Test parsing a valid URL with WRITE permission"""
        tenant_id = "123e4567-e89b-12d3-a456-426614174000"
        account_id = "987fcdeb-51a2-43d1-9f12-345678901234"
        role_id = "456e7890-e89b-12d3-a456-426614174567"
        role_name = "editor"
        permission_code = "1"  # WRITE
        sys_value = "0"  # False
        verified_value = "0"  # False
        account_name = "Editor User"

        # Encode account name
        name_encoded = base64.b64encode(account_name.encode("utf-8")).decode("ascii")

        # Construct URL path
        url_path = f"t/{tenant_id}/a/{account_id}/r/{role_id}?p={role_name}:{permission_code}&s={sys_value}&v={verified_value}&n={name_encoded}"

        resource = LicensedResource.from_str(url_path)

        assert str(resource.tenant_id) == tenant_id
        assert str(resource.acc_id) == account_id
        assert str(resource.role_id) == role_id
        assert resource.role == role_name
        assert resource.perm == Permission.WRITE
        assert resource.sys_acc is False
        assert resource.acc_name == account_name
        assert resource.verified is False

    def test_valid_url_with_special_characters_in_name(self):
        """Test parsing URL with special characters in account name"""
        tenant_id = "123e4567-e89b-12d3-a456-426614174000"
        account_id = "987fcdeb-51a2-43d1-9f12-345678901234"
        role_id = "456e7890-e89b-12d3-a456-426614174567"
        role_name = "user"
        permission_code = "0"
        sys_value = "0"
        verified_value = "1"
        account_name = "Test User with Special Chars: @#$%^&*()"

        # Encode account name
        name_encoded = base64.b64encode(account_name.encode("utf-8")).decode("ascii")

        # Construct URL path
        url_path = f"t/{tenant_id}/a/{account_id}/r/{role_id}?p={role_name}:{permission_code}&s={sys_value}&v={verified_value}&n={name_encoded}"

        resource = LicensedResource.from_str(url_path)

        assert resource.acc_name == account_name

    def test_invalid_path_format_missing_t(self):
        """Test error when path doesn't start with t"""
        url_path = "a/123e4567-e89b-12d3-a456-426614174000/r/456e7890-e89b-12d3-a456-426614174567?p=admin:0&s=1&v=1&n=dGVzdA=="

        with pytest.raises(ValueError, match="Invalid path format"):
            LicensedResource.from_str(url_path)

    def test_invalid_path_format_missing_a(self):
        """Test error when path doesn't have a"""
        url_path = "t/123e4567-e89b-12d3-a456-426614174000/r/456e7890-e89b-12d3-a456-426614174567?p=admin:0&s=1&v=1&n=dGVzdA=="

        with pytest.raises(ValueError, match="Invalid path format"):
            LicensedResource.from_str(url_path)

    def test_invalid_path_format_missing_r(self):
        """Test error when path doesn't have r"""
        url_path = "t/123e4567-e89b-12d3-a456-426614174000/a/987fcdeb-51a2-43d1-9f12-345678901234?p=admin:0&s=1&v=1&n=dGVzdA=="

        with pytest.raises(ValueError, match="Invalid path format"):
            LicensedResource.from_str(url_path)

    def test_invalid_path_format_wrong_segment_count(self):
        """Test error when path has wrong number of segments"""
        url_path = "t/123e4567-e89b-12d3-a456-426614174000/a/987fcdeb-51a2-43d1-9f12-345678901234/r/456e7890-e89b-12d3-a456-426614174567/extra?p=admin:0&s=1&v=1&n=dGVzdA=="

        with pytest.raises(ValueError, match="Invalid path format"):
            LicensedResource.from_str(url_path)

    def test_invalid_tenant_uuid(self):
        """Test error when tenant_id is not a valid UUID"""
        url_path = "t/invalid-uuid/a/987fcdeb-51a2-43d1-9f12-345678901234/r/456e7890-e89b-12d3-a456-426614174567?p=admin:0&s=1&v=1&n=dGVzdA=="

        with pytest.raises(ValueError, match="Invalid tenant UUID"):
            LicensedResource.from_str(url_path)

    def test_invalid_account_uuid(self):
        """Test error when account_id is not a valid UUID"""
        url_path = "t/123e4567-e89b-12d3-a456-426614174000/a/invalid-uuid/r/456e7890-e89b-12d3-a456-426614174567?p=admin:0&s=1&v=1&n=dGVzdA=="

        with pytest.raises(ValueError, match="Invalid account UUID"):
            LicensedResource.from_str(url_path)

    def test_invalid_role_uuid(self):
        """Test error when role_id is not a valid UUID"""
        url_path = "t/123e4567-e89b-12d3-a456-426614174000/a/987fcdeb-51a2-43d1-9f12-345678901234/r/invalid-uuid?p=admin:0&s=1&v=1&n=dGVzdA=="

        with pytest.raises(ValueError, match="Invalid role UUID"):
            LicensedResource.from_str(url_path)

    def test_missing_p_parameter(self):
        """Test error when p parameter is missing"""
        url_path = "t/123e4567-e89b-12d3-a456-426614174000/a/987fcdeb-51a2-43d1-9f12-345678901234/r/456e7890-e89b-12d3-a456-426614174567?s=1&v=1&n=dGVzdA=="

        with pytest.raises(ValueError, match="Parameter permissions not found"):
            LicensedResource.from_str(url_path)

    def test_invalid_p_format(self):
        """Test error when p parameter has invalid format"""
        url_path = "t/123e4567-e89b-12d3-a456-426614174000/a/987fcdeb-51a2-43d1-9f12-345678901234/r/456e7890-e89b-12d3-a456-426614174567?p=admin&s=1&v=1&n=dGVzdA=="

        with pytest.raises(ValueError, match="Invalid permissioned role format"):
            LicensedResource.from_str(url_path)

    def test_missing_s_parameter(self):
        """Test error when s parameter is missing"""
        url_path = "t/123e4567-e89b-12d3-a456-426614174000/a/987fcdeb-51a2-43d1-9f12-345678901234/r/456e7890-e89b-12d3-a456-426614174567?p=admin:0&v=1&n=dGVzdA=="

        with pytest.raises(ValueError, match="Parameter sys not found"):
            LicensedResource.from_str(url_path)

    def test_invalid_s_value(self):
        """Test error when s parameter has invalid value"""
        url_path = "t/123e4567-e89b-12d3-a456-426614174000/a/987fcdeb-51a2-43d1-9f12-345678901234/r/456e7890-e89b-12d3-a456-426614174567?p=admin:0&s=2&v=1&n=dGVzdA=="

        with pytest.raises(ValueError, match="Invalid account standard"):
            LicensedResource.from_str(url_path)

    def test_invalid_s_parse(self):
        """Test error when s parameter cannot be parsed as integer"""
        url_path = "t/123e4567-e89b-12d3-a456-426614174000/a/987fcdeb-51a2-43d1-9f12-345678901234/r/456e7890-e89b-12d3-a456-426614174567?p=admin:0&s=invalid&v=1&n=dGVzdA=="

        with pytest.raises(ValueError, match="Failed to parse account standard"):
            LicensedResource.from_str(url_path)

    def test_missing_v_parameter(self):
        """Test error when v parameter is missing"""
        url_path = "t/123e4567-e89b-12d3-a456-426614174000/a/987fcdeb-51a2-43d1-9f12-345678901234/r/456e7890-e89b-12d3-a456-426614174567?p=admin:0&s=1&n=dGVzdA=="

        with pytest.raises(ValueError, match="Parameter v not found"):
            LicensedResource.from_str(url_path)

    def test_invalid_v_value(self):
        """Test error when v parameter has invalid value"""
        url_path = "t/123e4567-e89b-12d3-a456-426614174000/a/987fcdeb-51a2-43d1-9f12-345678901234/r/456e7890-e89b-12d3-a456-426614174567?p=admin:0&s=1&v=2&n=dGVzdA=="

        with pytest.raises(ValueError, match="Invalid account verification"):
            LicensedResource.from_str(url_path)

    def test_invalid_v_parse(self):
        """Test error when v parameter cannot be parsed as integer"""
        url_path = "t/123e4567-e89b-12d3-a456-426614174000/a/987fcdeb-51a2-43d1-9f12-345678901234/r/456e7890-e89b-12d3-a456-426614174567?p=admin:0&s=1&v=invalid&n=dGVzdA=="

        with pytest.raises(ValueError, match="Failed to parse account verification"):
            LicensedResource.from_str(url_path)

    def test_missing_n_parameter(self):
        """Test error when n parameter is missing"""
        url_path = "t/123e4567-e89b-12d3-a456-426614174000/a/987fcdeb-51a2-43d1-9f12-345678901234/r/456e7890-e89b-12d3-a456-426614174567?p=admin:0&s=1&v=1"

        with pytest.raises(ValueError, match="Parameter name not found"):
            LicensedResource.from_str(url_path)

    def test_invalid_base64_name(self):
        """Test error when n parameter contains invalid base64"""
        url_path = "t/123e4567-e89b-12d3-a456-426614174000/a/987fcdeb-51a2-43d1-9f12-345678901234/r/456e7890-e89b-12d3-a456-426614174567?p=admin:0&s=1&v=1&n=invalid-base64!"

        with pytest.raises(ValueError, match="Failed to decode account name"):
            LicensedResource.from_str(url_path)

    def test_invalid_permission_code(self):
        """Test error when permission code is invalid"""
        url_path = "t/123e4567-e89b-12d3-a456-426614174000/a/987fcdeb-51a2-43d1-9f12-345678901234/r/456e7890-e89b-12d3-a456-426614174567?p=admin:2&s=1&v=1&n=dGVzdA=="

        with pytest.raises(ValueError, match="Invalid permission code: 2"):
            LicensedResource.from_str(url_path)

    def test_invalid_permission_parse(self):
        """Test error when permission code cannot be parsed as integer"""
        url_path = "t/123e4567-e89b-12d3-a456-426614174000/a/987fcdeb-51a2-43d1-9f12-345678901234/r/456e7890-e89b-12d3-a456-426614174567?p=admin:invalid&s=1&v=1&n=dGVzdA=="

        with pytest.raises(ValueError):
            LicensedResource.from_str(url_path)

    def test_empty_string_input(self):
        """Test error when input string is empty"""
        with pytest.raises(ValueError):
            LicensedResource.from_str("")

    def test_malformed_url(self):
        """Test error when URL is malformed"""
        with pytest.raises(ValueError):
            LicensedResource.from_str("not-a-url")

    def test_unicode_account_name(self):
        """Test parsing URL with unicode characters in account name"""
        tenant_id = "123e4567-e89b-12d3-a456-426614174000"
        account_id = "987fcdeb-51a2-43d1-9f12-345678901234"
        role_id = "456e7890-e89b-12d3-a456-426614174567"
        role_name = "user"
        permission_code = "0"
        sys_value = "0"
        verified_value = "1"
        account_name = "Usuário com Acentos: ção, ñ, ü"

        # Encode account name
        name_encoded = base64.b64encode(account_name.encode("utf-8")).decode("ascii")

        # Construct URL path
        url_path = f"t/{tenant_id}/a/{account_id}/r/{role_id}?p={role_name}:{permission_code}&s={sys_value}&v={verified_value}&n={name_encoded}"

        resource = LicensedResource.from_str(url_path)

        assert resource.acc_name == account_name

    def test_long_account_name(self):
        """Test parsing URL with very long account name"""
        tenant_id = "123e4567-e89b-12d3-a456-426614174000"
        account_id = "987fcdeb-51a2-43d1-9f12-345678901234"
        role_id = "456e7890-e89b-12d3-a456-426614174567"
        role_name = "user"
        permission_code = "0"
        sys_value = "0"
        verified_value = "1"
        account_name = "A" * 1000  # Very long name

        # Encode account name
        name_encoded = base64.b64encode(account_name.encode("utf-8")).decode("ascii")

        # Construct URL path
        url_path = f"t/{tenant_id}/a/{account_id}/r/{role_id}?p={role_name}:{permission_code}&s={sys_value}&v={verified_value}&n={name_encoded}"

        resource = LicensedResource.from_str(url_path)

        assert resource.acc_name == account_name

    def test_uuid_helper_method(self):
        """Test the _is_uuid helper method"""
        # Valid UUIDs
        assert LicensedResource._is_uuid("123e4567-e89b-12d3-a456-426614174000") is True
        assert LicensedResource._is_uuid("00000000-0000-0000-0000-000000000000") is True
        assert LicensedResource._is_uuid("FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF") is True

        # Invalid UUIDs
        assert LicensedResource._is_uuid("invalid-uuid") is False
        assert LicensedResource._is_uuid("123") is False
        assert LicensedResource._is_uuid("") is False
        assert (
            LicensedResource._is_uuid("123e4567-e89b-12d3-a456-42661417400") is False
        )  # Too short
        assert (
            LicensedResource._is_uuid("123e4567-e89b-12d3-a456-4266141740000") is False
        )  # Too long
