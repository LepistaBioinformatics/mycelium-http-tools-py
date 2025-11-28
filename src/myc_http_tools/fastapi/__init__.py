"""FastAPI integration for mycelium-http-tools."""

try:
    from .middleware import (
        get_profile_from_header,
        get_profile_from_header_required,
        get_profile_from_request,
        profile_middleware,
    )

    __all__ = [
        "get_profile_from_header",
        "get_profile_from_header_required",
        "get_profile_from_request",
        "profile_middleware",
    ]

except ImportError:
    # FastAPI dependencies not installed
    def _raise_import_error():
        raise ImportError(
            "FastAPI dependencies not installed. "
            "Install with: pip install mycelium-http-tools[fastapi]"
        )

    def get_profile_from_request(*args, **kwargs):  # type: ignore[misc]
        _raise_import_error()

    def profile_middleware(*args, **kwargs):  # type: ignore[misc]
        _raise_import_error()

    def get_profile_from_header(*args, **kwargs):  # type: ignore[misc]
        _raise_import_error()

    def get_profile_from_header_required(*args, **kwargs):  # type: ignore[misc]
        _raise_import_error()

    __all__ = [
        "get_profile_from_header",
        "get_profile_from_header_required",
        "get_profile_from_request",
        "profile_middleware",
    ]
