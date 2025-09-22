"""Custom exceptions for mycelium-http-tools."""

from typing import Optional


class MyceliumError(Exception):
    """Base exception for Mycelium HTTP Tools."""

    def __init__(
        self, message: str, code: Optional[str] = None, exp_true: bool = False
    ):
        self.message = message
        self.code = code
        self.exp_true = exp_true
        super().__init__(self.message)


class InsufficientPrivilegesError(MyceliumError):
    """Raised when there are insufficient privileges to perform an action."""

    def __init__(self, message: str, filtering_state: Optional[list[str]] = None):
        self.filtering_state = filtering_state or []
        super().__init__(message=message, code="MYC00019", exp_true=True)


class InsufficientLicensesError(MyceliumError):
    """Raised when there are insufficient licenses to perform an action."""

    def __init__(self, message: str = "Insufficient licenses to perform these action"):
        super().__init__(message=message, code="MYC00019", exp_true=True)
