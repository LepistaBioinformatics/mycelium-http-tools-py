from typing import Optional, Self, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from myc_http_tools.exceptions import (
    InsufficientLicensesError,
    InsufficientPrivilegesError,
)
from myc_http_tools.models.licensed_resources import LicensedResources
from myc_http_tools.models.owner import Owner
from myc_http_tools.models.permission import Permission
from myc_http_tools.models.related_accounts import (
    RelatedAccounts,
    AllowedAccounts,
    HasStaffPrivileges,
    HasManagerPrivileges,
)
from myc_http_tools.models.tenants_ownership import TenantsOwnership
from myc_http_tools.models.verbose_status import VerboseStatus


class Profile(BaseModel):
    """Profile model"""

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    # --------------------------------------------------------------------------
    # PUBLIC ATTRIBUTES
    # --------------------------------------------------------------------------

    owners: list[Owner] = Field(default_factory=list)
    acc_id: UUID = Field()
    is_subscription: bool
    is_admin: bool
    is_staff: bool
    is_manager: bool = Field(default=False)
    owner_is_active: bool
    account_is_active: bool
    account_was_approved: bool
    account_was_archived: bool
    account_was_deleted: bool
    verbose_status: Optional[VerboseStatus] = None
    licensed_resources: Optional[LicensedResources] = None
    tenants_ownership: Optional[TenantsOwnership] = None
    meta: Optional[dict] = None
    filtering_state: Optional[list[str]] = None

    # --------------------------------------------------------------------------
    # PUBLIC METHODS
    # --------------------------------------------------------------------------

    def with_read_access(self) -> Self:
        return self.__with_permission(Permission.READ)

    def with_write_access(self) -> Self:
        return self.__with_permission(Permission.WRITE)

    def on_tenant(self, tenant_id: UUID) -> Self:
        """Filter the licensed resources to the tenant.

        This method should be used to filter licensed resources to the tenant
        that the profile is currently working on.

        Args:
            tenant_id: The UUID of the tenant to filter by

        Returns:
            A new Profile instance with filtered licensed resources
        """
        # Filter the licensed resources to the tenant
        licensed_resources = None
        if self.licensed_resources is not None:
            # Get all licensed resources
            all_resources = self.licensed_resources.to_licenses_vector()

            # Filter by tenant_id
            filtered_resources = [
                resource
                for resource in all_resources
                if resource.tenant_id == tenant_id
            ]

            # Create new LicensedResources if we have filtered results
            if filtered_resources:
                licensed_resources = LicensedResources(records=filtered_resources)

        # Update filtering state to track the tenant filter (incremental)
        updated_filtering_state = (
            self.filtering_state.copy() if self.filtering_state else []
        )

        # Get the next filter number
        next_filter_number = len(updated_filtering_state) + 1
        tenant_filter = f"{next_filter_number}:tenantId:{tenant_id}"

        # Add the new filter (incremental behavior)
        updated_filtering_state.append(tenant_filter)

        # Return the new profile
        return self.model_copy(
            update={
                "licensed_resources": licensed_resources,
                "filtering_state": updated_filtering_state,
            }
        )

    def with_roles(self, roles: list[str]) -> Self:
        """Filter the licensed resources to the specified roles.

        This method should be used to filter licensed resources to only include
        those that match any of the specified roles.

        Args:
            roles: List of role names to filter by

        Returns:
            A new Profile instance with filtered licensed resources
        """
        # Filter the licensed resources to the roles
        licensed_resources = None
        if self.licensed_resources is not None:
            # Get all licensed resources
            all_resources = self.licensed_resources.to_licenses_vector()

            # Filter by roles (any role that matches any of the specified roles)
            filtered_resources = [
                resource for resource in all_resources if resource.role in roles
            ]

            # Create new LicensedResources if we have filtered results
            if filtered_resources:
                licensed_resources = LicensedResources(records=filtered_resources)

        # Update filtering state to track the role filter (incremental)
        updated_filtering_state = (
            self.filtering_state.copy() if self.filtering_state else []
        )

        # Get the next filter number
        next_filter_number = len(updated_filtering_state) + 1
        roles_str = ",".join(roles)
        role_filter = f"{next_filter_number}:role:{roles_str}"

        # Add the new filter (incremental behavior)
        updated_filtering_state.append(role_filter)

        # Return the new profile
        return self.model_copy(
            update={
                "licensed_resources": licensed_resources,
                "filtering_state": updated_filtering_state,
            }
        )

    def get_related_account_or_error(self) -> RelatedAccounts:
        """Get related accounts based on profile privileges.

        This method determines the appropriate RelatedAccounts variant based on
        the profile's privileges and available licensed resources.

        Returns:
            RelatedAccounts: The appropriate variant based on privileges

        Raises:
            InsufficientLicensesError: When there are no licensed resources
            InsufficientPrivilegesError: When there are insufficient privileges
        """
        # Check for staff privileges first
        if self.is_staff:
            return HasStaffPrivileges()

        # Check for manager privileges
        if self.is_manager:
            return HasManagerPrivileges()

        # Check for licensed resources
        if self.licensed_resources is not None:
            records = self.licensed_resources.to_licenses_vector()

            if not records:
                raise InsufficientLicensesError()

            # Extract account IDs from licensed resources
            account_ids = [record.acc_id for record in records]
            return AllowedAccounts(accounts=account_ids)

        # No privileges available
        filtering_state_str = (
            ", ".join(self.filtering_state) if self.filtering_state else ""
        )
        raise InsufficientPrivilegesError(
            f"Insufficient privileges to perform these action (no accounts): {filtering_state_str}",
            filtering_state=self.filtering_state,
        )

    # --------------------------------------------------------------------------
    # PRIVATE METHODS
    # --------------------------------------------------------------------------

    def __with_permission(self, permission: Permission) -> Self:
        if self.licensed_resources is None:
            return self

        licensed_resources = self.licensed_resources.model_copy()

        licensed_resources.records = list(
            filter(
                lambda x: x.perm.to_int() >= permission.to_int(),
                licensed_resources.to_licenses_vector(),
            )
        )

        licensed_resources.urls = None

        return self.model_copy(update={"licensed_resources": licensed_resources})
