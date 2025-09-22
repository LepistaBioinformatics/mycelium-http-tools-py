from enum import Enum


class VerboseStatus(Enum):
    UNVERIFIED = "unverified"
    VERIFIED = "verified"
    INACTIVE = "inactive"
    ARCHIVED = "archived"
    DELETED = "deleted"
    UNKNOWN = "unknown"
