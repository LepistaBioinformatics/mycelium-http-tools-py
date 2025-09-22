"""FastAPI integration for mycelium-http-tools."""

try:
    from .middleware import get_profile_from_request, profile_middleware

    __all__ = ["get_profile_from_request", "profile_middleware"]

except ImportError as e:
    # FastAPI dependencies not installed
    def _raise_import_error():
        raise ImportError(
            "FastAPI dependencies not installed. "
            "Install with: pip install mycelium-http-tools[fastapi]"
        ) from e

    def get_profile_from_request(*args, **kwargs):
        _raise_import_error()

    def profile_middleware(*args, **kwargs):
        _raise_import_error()

    __all__ = ["get_profile_from_request", "profile_middleware"]
