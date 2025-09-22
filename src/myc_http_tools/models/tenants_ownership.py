from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class TenantOwnership(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    id: UUID
    name: str
    since: str


class TenantsOwnership(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    records: Optional[list[TenantOwnership]] = Field(default=None)
    urls: Optional[list[str]] = Field(default=None)
