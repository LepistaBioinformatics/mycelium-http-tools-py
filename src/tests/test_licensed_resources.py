"""
Tests for LicensedResources class
"""

import base64
import pytest
from uuid import UUID

from myc_http_tools.models.licensed_resources import (
    LicensedResource,
    LicensedResources,
)
from myc_http_tools.models.permission import Permission


class TestLicensedResources:
    """Test cases for LicensedResources class"""

    def test_to_licenses_vector_with_records(self):
        """Test to_licenses_vector when records are provided"""
        # Create test records
        resource1 = LicensedResource(
            tenant_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
            acc_id=UUID("987fcdeb-51a2-43d1-9f12-345678901234"),
            role_id=UUID("456e7890-e89b-12d3-a456-426614174567"),
            role="admin",
            perm=Permission.READ,
            sys_acc=True,
            acc_name="Admin User",
            verified=True,
        )

        resource2 = LicensedResource(
            tenant_id=UUID("223e4567-e89b-12d3-a456-426614174001"),
            acc_id=UUID("887fcdeb-51a2-43d1-9f12-345678901235"),
            role_id=UUID("556e7890-e89b-12d3-a456-426614174568"),
            role="editor",
            perm=Permission.WRITE,
            sys_acc=False,
            acc_name="Editor User",
            verified=False,
        )

        licensed_resources = LicensedResources(records=[resource1, resource2])

        result = licensed_resources.to_licenses_vector()

        assert len(result) == 2
        assert result[0] == resource1
        assert result[1] == resource2

    def test_to_licenses_vector_with_urls(self):
        """Test to_licenses_vector when URLs are provided"""
        # Create test URLs
        tenant_id1 = "123e4567-e89b-12d3-a456-426614174000"
        account_id1 = "987fcdeb-51a2-43d1-9f12-345678901234"
        role_id1 = "456e7890-e89b-12d3-a456-426614174567"
        role_name1 = "admin"
        permission_code1 = "0"  # READ
        sys_value1 = "1"  # True
        verified_value1 = "1"  # True
        account_name1 = "Admin User"

        name_encoded1 = base64.b64encode(account_name1.encode("utf-8")).decode(
            "ascii"
        )
        url1 = f"t/{tenant_id1}/a/{account_id1}/r/{role_id1}?p={role_name1}:{permission_code1}&s={sys_value1}&v={verified_value1}&n={name_encoded1}"

        tenant_id2 = "223e4567-e89b-12d3-a456-426614174001"
        account_id2 = "887fcdeb-51a2-43d1-9f12-345678901235"
        role_id2 = "556e7890-e89b-12d3-a456-426614174568"
        role_name2 = "editor"
        permission_code2 = "1"  # WRITE
        sys_value2 = "0"  # False
        verified_value2 = "0"  # False
        account_name2 = "Editor User"

        name_encoded2 = base64.b64encode(account_name2.encode("utf-8")).decode(
            "ascii"
        )
        url2 = f"t/{tenant_id2}/a/{account_id2}/r/{role_id2}?p={role_name2}:{permission_code2}&s={sys_value2}&v={verified_value2}&n={name_encoded2}"

        licensed_resources = LicensedResources(urls=[url1, url2])

        result = licensed_resources.to_licenses_vector()

        assert len(result) == 2
        assert result[0].tenant_id == UUID(tenant_id1)
        assert result[0].acc_id == UUID(account_id1)
        assert result[0].role_id == UUID(role_id1)
        assert result[0].role == role_name1
        assert result[0].perm == Permission.READ
        assert result[0].sys_acc is True
        assert result[0].acc_name == account_name1
        assert result[0].verified is True

        assert result[1].tenant_id == UUID(tenant_id2)
        assert result[1].acc_id == UUID(account_id2)
        assert result[1].role_id == UUID(role_id2)
        assert result[1].role == role_name2
        assert result[1].perm == Permission.WRITE
        assert result[1].sys_acc is False
        assert result[1].acc_name == account_name2
        assert result[1].verified is False

    def test_to_licenses_vector_with_both_records_and_urls(self):
        """Test to_licenses_vector when both records and URLs are provided (should prefer records)"""
        # Create test record
        resource = LicensedResource(
            tenant_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
            acc_id=UUID("987fcdeb-51a2-43d1-9f12-345678901234"),
            role_id=UUID("456e7890-e89b-12d3-a456-426614174567"),
            role="admin",
            perm=Permission.READ,
            sys_acc=True,
            acc_name="Admin User",
            verified=True,
        )

        # Create test URL
        tenant_id = "223e4567-e89b-12d3-a456-426614174001"
        account_id = "887fcdeb-51a2-43d1-9f12-345678901235"
        role_id = "556e7890-e89b-12d3-a456-426614174568"
        role_name = "editor"
        permission_code = "1"
        sys_value = "0"
        verified_value = "0"
        account_name = "Editor User"

        name_encoded = base64.b64encode(account_name.encode("utf-8")).decode(
            "ascii"
        )
        url = f"t/{tenant_id}/a/{account_id}/r/{role_id}?p={role_name}:{permission_code}&s={sys_value}&v={verified_value}&n={name_encoded}"

        licensed_resources = LicensedResources(records=[resource], urls=[url])

        result = licensed_resources.to_licenses_vector()

        # Should return records, not URLs
        assert len(result) == 1
        assert result[0] == resource

    def test_to_licenses_vector_with_none_records_and_urls(self):
        """Test to_licenses_vector when both records and URLs are None"""
        licensed_resources = LicensedResources(records=None, urls=None)

        result = licensed_resources.to_licenses_vector()

        assert result == []

    def test_to_licenses_vector_with_empty_records_and_urls(self):
        """Test to_licenses_vector when both records and URLs are empty lists"""
        licensed_resources = LicensedResources(records=[], urls=[])

        result = licensed_resources.to_licenses_vector()

        assert result == []

    def test_to_licenses_vector_with_none_records_but_urls(self):
        """Test to_licenses_vector when records is None but URLs are provided"""
        tenant_id = "123e4567-e89b-12d3-a456-426614174000"
        account_id = "987fcdeb-51a2-43d1-9f12-345678901234"
        role_id = "456e7890-e89b-12d3-a456-426614174567"
        role_name = "admin"
        permission_code = "0"
        sys_value = "1"
        verified_value = "1"
        account_name = "Admin User"

        name_encoded = base64.b64encode(account_name.encode("utf-8")).decode(
            "ascii"
        )
        url = f"t/{tenant_id}/a/{account_id}/r/{role_id}?p={role_name}:{permission_code}&s={sys_value}&v={verified_value}&n={name_encoded}"

        licensed_resources = LicensedResources(records=None, urls=[url])

        result = licensed_resources.to_licenses_vector()

        assert len(result) == 1
        assert result[0].tenant_id == UUID(tenant_id)
        assert result[0].acc_name == account_name

    def test_to_licenses_vector_with_records_but_none_urls(self):
        """Test to_licenses_vector when records are provided but URLs is None"""
        resource = LicensedResource(
            tenant_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
            acc_id=UUID("987fcdeb-51a2-43d1-9f12-345678901234"),
            role_id=UUID("456e7890-e89b-12d3-a456-426614174567"),
            role="admin",
            perm=Permission.READ,
            sys_acc=True,
            acc_name="Admin User",
            verified=True,
        )

        licensed_resources = LicensedResources(records=[resource], urls=None)

        result = licensed_resources.to_licenses_vector()

        assert len(result) == 1
        assert result[0] == resource

    def test_to_licenses_vector_with_invalid_urls(self):
        """Test to_licenses_vector when URLs contain invalid data"""
        licensed_resources = LicensedResources(urls=["invalid-url"])

        with pytest.raises(ValueError):
            licensed_resources.to_licenses_vector()

    def test_to_licenses_vector_with_mixed_valid_invalid_urls(self):
        """Test to_licenses_vector when some URLs are valid and some are invalid"""
        tenant_id = "123e4567-e89b-12d3-a456-426614174000"
        account_id = "987fcdeb-51a2-43d1-9f12-345678901234"
        role_id = "456e7890-e89b-12d3-a456-426614174567"
        role_name = "admin"
        permission_code = "0"
        sys_value = "1"
        verified_value = "1"
        account_name = "Admin User"

        name_encoded = base64.b64encode(account_name.encode("utf-8")).decode(
            "ascii"
        )
        valid_url = f"t/{tenant_id}/a/{account_id}/r/{role_id}?p={role_name}:{permission_code}&s={sys_value}&v={verified_value}&n={name_encoded}"

        licensed_resources = LicensedResources(urls=[valid_url, "invalid-url"])

        with pytest.raises(ValueError):
            licensed_resources.to_licenses_vector()

    def test_licenses_resources_creation_with_records_only(self):
        """Test creating LicensedResources with only records"""
        resource = LicensedResource(
            tenant_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
            acc_id=UUID("987fcdeb-51a2-43d1-9f12-345678901234"),
            role_id=UUID("456e7890-e89b-12d3-a456-426614174567"),
            role="admin",
            perm=Permission.READ,
            sys_acc=True,
            acc_name="Admin User",
            verified=True,
        )

        licensed_resources = LicensedResources(records=[resource])

        assert licensed_resources.records == [resource]
        assert licensed_resources.urls is None

    def test_licenses_resources_creation_with_urls_only(self):
        """Test creating LicensedResources with only URLs"""
        tenant_id = "123e4567-e89b-12d3-a456-426614174000"
        account_id = "987fcdeb-51a2-43d1-9f12-345678901234"
        role_id = "456e7890-e89b-12d3-a456-426614174567"
        role_name = "admin"
        permission_code = "0"
        sys_value = "1"
        verified_value = "1"
        account_name = "Admin User"

        name_encoded = base64.b64encode(account_name.encode("utf-8")).decode(
            "ascii"
        )
        url = f"t/{tenant_id}/a/{account_id}/r/{role_id}?p={role_name}:{permission_code}&s={sys_value}&v={verified_value}&n={name_encoded}"

        licensed_resources = LicensedResources(urls=[url])

        assert licensed_resources.records is None
        assert licensed_resources.urls == [url]

    def test_licenses_resources_creation_with_both(self):
        """Test creating LicensedResources with both records and URLs"""
        resource = LicensedResource(
            tenant_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
            acc_id=UUID("987fcdeb-51a2-43d1-9f12-345678901234"),
            role_id=UUID("456e7890-e89b-12d3-a456-426614174567"),
            role="admin",
            perm=Permission.READ,
            sys_acc=True,
            acc_name="Admin User",
            verified=True,
        )

        tenant_id = "223e4567-e89b-12d3-a456-426614174001"
        account_id = "887fcdeb-51a2-43d1-9f12-345678901235"
        role_id = "556e7890-e89b-12d3-a456-426614174568"
        role_name = "editor"
        permission_code = "1"
        sys_value = "0"
        verified_value = "0"
        account_name = "Editor User"

        name_encoded = base64.b64encode(account_name.encode("utf-8")).decode(
            "ascii"
        )
        url = f"t/{tenant_id}/a/{account_id}/r/{role_id}?p={role_name}:{permission_code}&s={sys_value}&v={verified_value}&n={name_encoded}"

        licensed_resources = LicensedResources(records=[resource], urls=[url])

        assert licensed_resources.records == [resource]
        assert licensed_resources.urls == [url]

    def test_licenses_resources_creation_with_none_values(self):
        """Test creating LicensedResources with None values"""
        licensed_resources = LicensedResources(records=None, urls=None)

        assert licensed_resources.records is None
        assert licensed_resources.urls is None
