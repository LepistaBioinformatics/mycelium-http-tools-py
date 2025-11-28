from typing import Union, Literal
from uuid import UUID

from pydantic import BaseModel, Field


class AllowedAccounts(BaseModel):
    """Represents accounts that are allowed access."""

    type: Literal["allowed_accounts"] = Field(
        default="allowed_accounts", alias="type"
    )
    accounts: list[UUID] = Field(alias="accounts")


class HasTenantWidePrivileges(BaseModel):
    """Represents tenant-wide privileges for a specific tenant."""

    type: Literal["has_tenant_wide_privileges"] = Field(
        default="has_tenant_wide_privileges", alias="type"
    )
    tenant_id: UUID = Field(alias="tenant_id")


class HasStaffPrivileges(BaseModel):
    """Represents staff privileges."""

    type: Literal["has_staff_privileges"] = Field(
        default="has_staff_privileges", alias="type"
    )


class HasManagerPrivileges(BaseModel):
    """Represents manager privileges."""

    type: Literal["has_manager_privileges"] = Field(
        default="has_manager_privileges", alias="type"
    )


def get_discriminator_value(
    v: Union[
        AllowedAccounts,
        HasTenantWidePrivileges,
        HasStaffPrivileges,
        HasManagerPrivileges,
    ],
) -> str:
    """Discriminator function for the union type."""
    return v.type


RelatedAccounts = Union[
    AllowedAccounts,
    HasTenantWidePrivileges,
    HasStaffPrivileges,
    HasManagerPrivileges,
]
