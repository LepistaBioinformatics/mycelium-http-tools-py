"""FastAPI middleware for extracting profile from HTTP headers."""

import json
import os
from typing import Optional

try:
    from fastapi import HTTPException, Request
    from fastapi.responses import JSONResponse

    FASTAPI_AVAILABLE = True
except ImportError:
    # FastAPI not available - define placeholder types
    FASTAPI_AVAILABLE = False

    class Request:
        """Placeholder for Request when FastAPI is not available."""

        def __init__(self, *args, **kwargs):
            raise ImportError(
                "FastAPI dependencies not installed. "
                "Install with: pip install mycelium-http-tools[fastapi]"
            )

    class HTTPException(Exception):
        """Placeholder for HTTPException when FastAPI is not available."""

        def __init__(self, *args, **kwargs):
            raise ImportError(
                "FastAPI dependencies not installed. "
                "Install with: pip install mycelium-http-tools[fastapi]"
            )

    class JSONResponse:
        """Placeholder for JSONResponse when FastAPI is not available."""

        def __init__(self, *args, **kwargs):
            raise ImportError(
                "FastAPI dependencies not installed. "
                "Install with: pip install mycelium-http-tools[fastapi]"
            )


from myc_http_tools.models.profile import Profile


def get_profile_from_request(request: Request) -> Optional[Profile]:
    """Extract profile from HTTP headers.

    This function extracts the profile from the 'x-mycelium-profile' header
    in the HTTP request. The header should contain a JSON string representation
    of the Profile object.

    Args:
        request: The FastAPI Request object

    Returns:
        Profile object if successfully parsed, None if in development mode
        and header is missing

    Raises:
        HTTPException: If required header is missing in production environment
        or if the JSON parsing fails
        ImportError: If FastAPI dependencies are not installed
    """
    if not FASTAPI_AVAILABLE:
        raise ImportError(
            "FastAPI dependencies not installed. "
            "Install with: pip install mycelium-http-tools[fastapi]"
        )
    environment = os.getenv("ENVIRONMENT", "development")
    incoming_headers = dict(request.headers)

    if environment != "development":
        if "x-mycelium-profile" not in incoming_headers:
            raise HTTPException(
                status_code=403,
                detail="Required header 'x-mycelium-profile' missing in production environment.",
            )

        try:
            # Parse the JSON from the header
            profile_json = json.loads(incoming_headers["x-mycelium-profile"])
            # Create Profile instance using Pydantic
            return Profile.model_validate(profile_json)
        except json.JSONDecodeError as e:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid JSON in 'x-mycelium-profile' header: {str(e)}",
            )
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Failed to parse profile from header: {str(e)}"
            )

    # In development mode, try to parse if header exists, otherwise return None
    if "x-mycelium-profile" in incoming_headers:
        try:
            profile_json = json.loads(incoming_headers["x-mycelium-profile"])
            return Profile.model_validate(profile_json)
        except (json.JSONDecodeError, Exception):
            # In development, we're more lenient with errors
            return None

    return None


async def profile_middleware(request: Request, call_next):
    """FastAPI middleware to extract and attach profile to request state.

    This middleware extracts the profile from the 'x-mycelium-profile' header
    and attaches it to the request state for easy access in route handlers.

    Usage:
        app.add_middleware(BaseHTTPMiddleware, dispatch=profile_middleware)

    Then in your route handlers:
        profile = request.state.profile

    Raises:
        ImportError: If FastAPI dependencies are not installed
    """
    if not FASTAPI_AVAILABLE:
        raise ImportError(
            "FastAPI dependencies not installed. "
            "Install with: pip install mycelium-http-tools[fastapi]"
        )
    try:
        profile = get_profile_from_request(request)
        request.state.profile = profile
    except HTTPException:
        # Re-raise HTTP exceptions as they are
        raise
    except Exception as e:
        # Handle any other unexpected errors
        return JSONResponse(
            status_code=500, content={"detail": f"Internal server error: {str(e)}"}
        )

    response = await call_next(request)
    return response
