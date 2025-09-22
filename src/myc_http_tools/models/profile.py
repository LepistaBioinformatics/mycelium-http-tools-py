from typing import Optional, Self
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from myc_http_tools.models.licensed_resources import LicensedResources
from myc_http_tools.models.owner import Owner
from myc_http_tools.models.permission import Permission
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
