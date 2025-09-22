"""
Tests for Profile class
"""

from uuid import UUID

import pytest

from myc_http_tools.models.licensed_resources import LicensedResource, LicensedResources
from myc_http_tools.models.owner import Owner
from myc_http_tools.models.permission import Permission
from myc_http_tools.models.profile import Profile
from myc_http_tools.models.tenants_ownership import TenantOwnership, TenantsOwnership
from myc_http_tools.models.verbose_status import VerboseStatus


class TestProfile:
    """Test cases for Profile class"""

    def test_profile_creation_minimal(self):
        """Test creating a Profile with minimal required fields"""
        profile = Profile(
            acc_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
            is_subscription=True,
            is_admin=False,
            is_staff=False,
            owner_is_active=True,
            account_is_active=True,
            account_was_approved=True,
            account_was_archived=False,
            account_was_deleted=False,
        )

        assert profile.acc_id == UUID("123e4567-e89b-12d3-a456-426614174000")
        assert profile.is_subscription is True
        assert profile.is_admin is False
        assert profile.is_staff is False
        assert profile.owner_is_active is True
        assert profile.account_is_active is True
        assert profile.account_was_approved is True
        assert profile.account_was_archived is False
        assert profile.account_was_deleted is False
        assert profile.owners == []
        assert profile.verbose_status is None
        assert profile.licensed_resources is None
        assert profile.tenants_ownership is None
        assert profile.meta is None
        assert profile.filtering_state is None

    def test_profile_creation_with_all_fields(self):
        """Test creating a Profile with all fields populated"""
        owner = Owner(
            id=UUID("987fcdeb-51a2-43d1-9f12-345678901234"),
            email="test@example.com",
            first_name="John",
            last_name="Doe",
            username="johndoe",
            is_principal=True,
        )

        tenant_ownership = TenantOwnership(
            id=UUID("456e7890-e89b-12d3-a456-426614174567"),
            name="Test Tenant",
            since="2024-01-01T00:00:00Z",
        )

        tenants_ownership = TenantsOwnership(records=[tenant_ownership])

        licensed_resource = LicensedResource(
            tenant_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
            acc_id=UUID("987fcdeb-51a2-43d1-9f12-345678901234"),
            role_id=UUID("456e7890-e89b-12d3-a456-426614174567"),
            role="admin",
            perm=Permission.READ,
            sys_acc=True,
            acc_name="Test Account",
            verified=True,
        )

        licensed_resources = LicensedResources(records=[licensed_resource])

        profile = Profile(
            owners=[owner],
            acc_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
            is_subscription=True,
            is_admin=True,
            is_staff=True,
            owner_is_active=True,
            account_is_active=True,
            account_was_approved=True,
            account_was_archived=False,
            account_was_deleted=False,
            verbose_status=VerboseStatus.VERIFIED,
            licensed_resources=licensed_resources,
            tenants_ownership=tenants_ownership,
            meta={"key": "value", "number": 42},
            filtering_state=["filter1", "filter2"],
        )

        assert len(profile.owners) == 1
        assert profile.owners[0] == owner
        assert profile.acc_id == UUID("123e4567-e89b-12d3-a456-426614174000")
        assert profile.is_subscription is True
        assert profile.is_admin is True
        assert profile.is_staff is True
        assert profile.owner_is_active is True
        assert profile.account_is_active is True
        assert profile.account_was_approved is True
        assert profile.account_was_archived is False
        assert profile.account_was_deleted is False
        assert profile.verbose_status == VerboseStatus.VERIFIED
        assert profile.licensed_resources == licensed_resources
        assert profile.tenants_ownership == tenants_ownership
        assert profile.meta == {"key": "value", "number": 42}
        assert profile.filtering_state == ["filter1", "filter2"]

    def test_profile_creation_with_multiple_owners(self):
        """Test creating a Profile with multiple owners"""
        owner1 = Owner(
            id=UUID("987fcdeb-51a2-43d1-9f12-345678901234"),
            email="owner1@example.com",
            first_name="John",
            last_name="Doe",
            username="johndoe",
            is_principal=True,
        )

        owner2 = Owner(
            id=UUID("887fcdeb-51a2-43d1-9f12-345678901235"),
            email="owner2@example.com",
            first_name="Jane",
            last_name="Smith",
            username="janesmith",
            is_principal=False,
        )

        profile = Profile(
            owners=[owner1, owner2],
            acc_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
            is_subscription=True,
            is_admin=False,
            is_staff=False,
            owner_is_active=True,
            account_is_active=True,
            account_was_approved=True,
            account_was_archived=False,
            account_was_deleted=False,
        )

        assert len(profile.owners) == 2
        assert profile.owners[0] == owner1
        assert profile.owners[1] == owner2

    def test_profile_creation_with_different_verbose_status(self):
        """Test creating a Profile with different VerboseStatus values"""
        for status in VerboseStatus:
            profile = Profile(
                acc_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
                is_subscription=True,
                is_admin=False,
                is_staff=False,
                owner_is_active=True,
                account_is_active=True,
                account_was_approved=True,
                account_was_archived=False,
                account_was_deleted=False,
                verbose_status=status,
            )

            assert profile.verbose_status == status

    def test_profile_creation_with_meta_data(self):
        """Test creating a Profile with various meta data types"""
        meta_data = {
            "string": "test",
            "number": 42,
            "float": 3.14,
            "boolean": True,
            "list": [1, 2, 3],
            "dict": {"nested": "value"},
            "null": None,
        }

        profile = Profile(
            acc_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
            is_subscription=True,
            is_admin=False,
            is_staff=False,
            owner_is_active=True,
            account_is_active=True,
            account_was_approved=True,
            account_was_archived=False,
            account_was_deleted=False,
            meta=meta_data,
        )

        assert profile.meta == meta_data

    def test_profile_creation_with_filtering_state(self):
        """Test creating a Profile with filtering state"""
        filtering_state = ["filter1", "filter2", "filter3"]

        profile = Profile(
            acc_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
            is_subscription=True,
            is_admin=False,
            is_staff=False,
            owner_is_active=True,
            account_is_active=True,
            account_was_approved=True,
            account_was_archived=False,
            account_was_deleted=False,
            filtering_state=filtering_state,
        )

        assert profile.filtering_state == filtering_state

    def test_profile_creation_with_empty_optional_fields(self):
        """Test creating a Profile with empty optional fields"""
        profile = Profile(
            acc_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
            is_subscription=True,
            is_admin=False,
            is_staff=False,
            owner_is_active=True,
            account_is_active=True,
            account_was_approved=True,
            account_was_archived=False,
            account_was_deleted=False,
            verbose_status=None,
            licensed_resources=None,
            tenants_ownership=None,
            meta=None,
            filtering_state=None,
        )

        assert profile.verbose_status is None
        assert profile.licensed_resources is None
        assert profile.tenants_ownership is None
        assert profile.meta is None
        assert profile.filtering_state is None

    def test_profile_validation_missing_required_fields(self):
        """Test Profile validation with missing required fields"""
        with pytest.raises(Exception):  # Pydantic validation error
            Profile()

        with pytest.raises(Exception):
            Profile(acc_id=UUID("123e4567-e89b-12d3-a456-426614174000"))

        with pytest.raises(Exception):
            Profile(
                acc_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
                is_subscription=True,
            )

    def test_profile_validation_invalid_uuid(self):
        """Test Profile validation with invalid UUID"""
        with pytest.raises(Exception):
            Profile(
                acc_id="invalid-uuid",
                is_subscription=True,
                is_admin=False,
                is_staff=False,
                owner_is_active=True,
                account_is_active=True,
                account_was_approved=True,
                account_was_archived=False,
                account_was_deleted=False,
            )

    def test_profile_validation_invalid_boolean_fields(self):
        """Test Profile validation with invalid boolean fields"""
        with pytest.raises(Exception):
            Profile(
                acc_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
                is_subscription="not-a-boolean",
                is_admin=False,
                is_staff=False,
                owner_is_active=True,
                account_is_active=True,
                account_was_approved=True,
                account_was_archived=False,
                account_was_deleted=False,
            )

    def test_with_read_access_without_licensed_resources(self):
        """Test with_read_access when licensed_resources is None"""
        profile = Profile(
            acc_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
            is_subscription=True,
            is_admin=False,
            is_staff=False,
            owner_is_active=True,
            account_is_active=True,
            account_was_approved=True,
            account_was_archived=False,
            account_was_deleted=False,
            licensed_resources=None,
        )

        result = profile.with_read_access()

        # Should return the same profile when licensed_resources is None
        assert result == profile
        assert result.licensed_resources is None

    def test_with_write_access_without_licensed_resources(self):
        """Test with_write_access when licensed_resources is None"""
        profile = Profile(
            acc_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
            is_subscription=True,
            is_admin=False,
            is_staff=False,
            owner_is_active=True,
            account_is_active=True,
            account_was_approved=True,
            account_was_archived=False,
            account_was_deleted=False,
            licensed_resources=None,
        )

        result = profile.with_write_access()

        # Should return the same profile when licensed_resources is None
        assert result == profile
        assert result.licensed_resources is None

    def test_with_read_access_with_licensed_resources(self):
        """Test with_read_access when licensed_resources is present"""
        read_resource = LicensedResource(
            tenant_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
            acc_id=UUID("987fcdeb-51a2-43d1-9f12-345678901234"),
            role_id=UUID("456e7890-e89b-12d3-a456-426614174567"),
            role="admin",
            perm=Permission.READ,
            sys_acc=True,
            acc_name="Read Account",
            verified=True,
        )

        write_resource = LicensedResource(
            tenant_id=UUID("223e4567-e89b-12d3-a456-426614174001"),
            acc_id=UUID("887fcdeb-51a2-43d1-9f12-345678901235"),
            role_id=UUID("556e7890-e89b-12d3-a456-426614174568"),
            role="editor",
            perm=Permission.WRITE,
            sys_acc=False,
            acc_name="Write Account",
            verified=False,
        )

        licensed_resources = LicensedResources(records=[read_resource, write_resource])

        profile = Profile(
            acc_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
            is_subscription=True,
            is_admin=False,
            is_staff=False,
            owner_is_active=True,
            account_is_active=True,
            account_was_approved=True,
            account_was_archived=False,
            account_was_deleted=False,
            licensed_resources=licensed_resources,
        )

        result = profile.with_read_access()

        # Should return a copy of the profile
        assert result != profile  # Different objects
        assert result.acc_id == profile.acc_id
        assert result.is_subscription == profile.is_subscription
        assert result.licensed_resources is not None

        # Should only contain READ permission resources
        assert len(result.licensed_resources.records) == 1
        assert result.licensed_resources.records[0].perm == Permission.READ
        assert result.licensed_resources.records[0].acc_name == "Read Account"

    def test_with_write_access_with_licensed_resources(self):
        """Test with_write_access when licensed_resources is present"""
        read_resource = LicensedResource(
            tenant_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
            acc_id=UUID("987fcdeb-51a2-43d1-9f12-345678901234"),
            role_id=UUID("456e7890-e89b-12d3-a456-426614174567"),
            role="admin",
            perm=Permission.READ,
            sys_acc=True,
            acc_name="Read Account",
            verified=True,
        )

        write_resource = LicensedResource(
            tenant_id=UUID("223e4567-e89b-12d3-a456-426614174001"),
            acc_id=UUID("887fcdeb-51a2-43d1-9f12-345678901235"),
            role_id=UUID("556e7890-e89b-12d3-a456-426614174568"),
            role="editor",
            perm=Permission.WRITE,
            sys_acc=False,
            acc_name="Write Account",
            verified=False,
        )

        licensed_resources = LicensedResources(records=[read_resource, write_resource])

        profile = Profile(
            acc_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
            is_subscription=True,
            is_admin=False,
            is_staff=False,
            owner_is_active=True,
            account_is_active=True,
            account_was_approved=True,
            account_was_archived=False,
            account_was_deleted=False,
            licensed_resources=licensed_resources,
        )

        result = profile.with_write_access()

        # Should return a copy of the profile
        assert result != profile  # Different objects
        assert result.acc_id == profile.acc_id
        assert result.is_subscription == profile.is_subscription
        assert result.licensed_resources is not None

        # Should only contain WRITE permission resources
        assert len(result.licensed_resources.records) == 1
        assert result.licensed_resources.records[0].perm == Permission.WRITE
        assert result.licensed_resources.records[0].acc_name == "Write Account"

    def test_profile_equality(self):
        """Test Profile equality comparison"""
        profile1 = Profile(
            acc_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
            is_subscription=True,
            is_admin=False,
            is_staff=False,
            owner_is_active=True,
            account_is_active=True,
            account_was_approved=True,
            account_was_archived=False,
            account_was_deleted=False,
        )

        profile2 = Profile(
            acc_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
            is_subscription=True,
            is_admin=False,
            is_staff=False,
            owner_is_active=True,
            account_is_active=True,
            account_was_approved=True,
            account_was_archived=False,
            account_was_deleted=False,
        )

        profile3 = Profile(
            acc_id=UUID("223e4567-e89b-12d3-a456-426614174001"),
            is_subscription=True,
            is_admin=False,
            is_staff=False,
            owner_is_active=True,
            account_is_active=True,
            account_was_approved=True,
            account_was_archived=False,
            account_was_deleted=False,
        )

        assert profile1 == profile2
        assert profile1 != profile3

    def test_profile_string_representation(self):
        """Test Profile string representation"""
        profile = Profile(
            acc_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
            is_subscription=True,
            is_admin=False,
            is_staff=False,
            owner_is_active=True,
            account_is_active=True,
            account_was_approved=True,
            account_was_archived=False,
            account_was_deleted=False,
        )

        profile_str = str(profile)
        # Pydantic doesn't include class name in string representation by default
        assert "123e4567-e89b-12d3-a456-426614174000" in profile_str
        assert "is_subscription=True" in profile_str
        assert "is_admin=False" in profile_str

    def test_profile_model_copy(self):
        """Test Profile model_copy method"""
        profile = Profile(
            acc_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
            is_subscription=True,
            is_admin=False,
            is_staff=False,
            owner_is_active=True,
            account_is_active=True,
            account_was_approved=True,
            account_was_archived=False,
            account_was_deleted=False,
        )

        profile_copy = profile.model_copy()

        assert profile_copy == profile
        assert profile_copy is not profile  # Different objects

    def test_profile_model_copy_with_updates(self):
        """Test Profile model_copy with updates"""
        profile = Profile(
            acc_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
            is_subscription=True,
            is_admin=False,
            is_staff=False,
            owner_is_active=True,
            account_is_active=True,
            account_was_approved=True,
            account_was_archived=False,
            account_was_deleted=False,
        )

        profile_copy = profile.model_copy(update={"is_admin": True})

        assert profile_copy.is_admin is True
        assert profile.is_admin is False  # Original unchanged
        assert profile_copy.acc_id == profile.acc_id  # Other fields unchanged

    def test_profile_with_complex_meta_data(self):
        """Test Profile with complex nested meta data"""
        complex_meta = {
            "user": {
                "id": 123,
                "name": "John Doe",
                "preferences": {
                    "theme": "dark",
                    "notifications": True,
                    "language": "en",
                },
                "permissions": ["read", "write", "admin"],
            },
            "system": {
                "version": "1.0.0",
                "environment": "production",
                "features": {
                    "feature1": True,
                    "feature2": False,
                },
            },
            "timestamps": {
                "created": "2024-01-01T00:00:00Z",
                "updated": "2024-01-02T12:00:00Z",
            },
        }

        profile = Profile(
            acc_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
            is_subscription=True,
            is_admin=False,
            is_staff=False,
            owner_is_active=True,
            account_is_active=True,
            account_was_approved=True,
            account_was_archived=False,
            account_was_deleted=False,
            meta=complex_meta,
        )

        assert profile.meta == complex_meta
        assert profile.meta["user"]["id"] == 123
        assert profile.meta["user"]["preferences"]["theme"] == "dark"
        assert profile.meta["system"]["features"]["feature1"] is True

    def test_profile_with_empty_lists(self):
        """Test Profile with empty lists for optional fields"""
        profile = Profile(
            acc_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
            is_subscription=True,
            is_admin=False,
            is_staff=False,
            owner_is_active=True,
            account_is_active=True,
            account_was_approved=True,
            account_was_archived=False,
            account_was_deleted=False,
            owners=[],  # Empty list
            filtering_state=[],  # Empty list
        )

        assert profile.owners == []
        assert profile.filtering_state == []

    def test_profile_boolean_combinations(self):
        """Test Profile with various boolean field combinations"""
        boolean_fields = [
            "is_subscription",
            "is_admin",
            "is_staff",
            "owner_is_active",
            "account_is_active",
            "account_was_approved",
            "account_was_archived",
            "account_was_deleted",
        ]

        # Test all True
        profile_all_true = Profile(
            acc_id=UUID("123e4567-e89b-12d3-a456-426614174000"),
            is_subscription=True,
            is_admin=True,
            is_staff=True,
            owner_is_active=True,
            account_is_active=True,
            account_was_approved=True,
            account_was_archived=True,
            account_was_deleted=True,
        )

        for field in boolean_fields:
            assert getattr(profile_all_true, field) is True

        # Test all False
        profile_all_false = Profile(
            acc_id=UUID("223e4567-e89b-12d3-a456-426614174001"),
            is_subscription=False,
            is_admin=False,
            is_staff=False,
            owner_is_active=False,
            account_is_active=False,
            account_was_approved=False,
            account_was_archived=False,
            account_was_deleted=False,
        )

        for field in boolean_fields:
            assert getattr(profile_all_false, field) is False
