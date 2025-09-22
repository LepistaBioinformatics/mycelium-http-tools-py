from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class Owner(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    id: UUID
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    is_principal: bool
