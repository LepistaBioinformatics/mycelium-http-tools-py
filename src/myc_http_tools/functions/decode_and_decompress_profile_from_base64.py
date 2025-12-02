"""Decode and decompress profile from Base64.

This module provides a function to decode a Base64-encoded, ZSTD-compressed
profile string and return a Profile object.
"""

import base64
import json
import logging
from typing import Union

from myc_http_tools.exceptions import ProfileDecodingError
from myc_http_tools.models.profile import Profile

try:
    import zstandard as zstd

    ZSTD_AVAILABLE = True
except ImportError:
    ZSTD_AVAILABLE = False
    zstd = None  # type: ignore[assignment]


logger = logging.getLogger(__name__)


def decode_and_decompress_profile_from_base64_robust(
    profile: Union[str, bytes],
) -> Profile:
    """Decode and decompress a profile from Base64 with fallback support.

    This function first tries to decode and decompress using ZSTD (the expected
    format). If that fails, it falls back to trying plain Base64 decoding,
    which is useful for development or when profiles are sent without compression.

    Args:
        profile: The Base64-encoded profile string or bytes. May be ZSTD-compressed
            or plain Base64.

    Returns:
        Profile: The decoded and decompressed profile.

    Raises:
        ProfileDecodingError: If there is an error during decoding, decompression,
            or deserialization, and all fallback methods have been exhausted.
    """
    # Decode from Base64 first
    try:
        if isinstance(profile, str):
            profile_bytes = profile.encode("utf-8")
        else:
            profile_bytes = profile

        decoded_profile = base64.standard_b64decode(profile_bytes)
    except Exception as e:
        raise ProfileDecodingError(
            f"Failed to decode base64 profile: {e}"
        ) from e

    # Try ZSTD decompression first (expected format)
    if ZSTD_AVAILABLE:
        try:
            decompressor = zstd.ZstdDecompressor()
            decompressed_profile = decompressor.decompress(decoded_profile)
            logger.debug("Successfully decompressed profile using ZSTD")
        except Exception as zstd_error:
            # If ZSTD fails, try treating as plain Base64 (fallback for development)
            # This handles cases where profiles are sent without ZSTD compression
            error_msg = str(zstd_error)
            logger.info(
                f"ZSTD decompression failed ({error_msg}), "
                "trying plain Base64 decoding as fallback"
            )
            # Use decoded_profile directly (already Base64-decoded bytes)
            decompressed_profile = decoded_profile
    else:
        # ZSTD not available, use plain Base64
        logger.debug("ZSTD not available, using plain Base64 decoding")
        decompressed_profile = decoded_profile

    # Deserialize from JSON
    try:
        profile_string = decompressed_profile.decode("utf-8")
    except Exception as e:
        raise ProfileDecodingError(
            f"Failed to convert decompressed profile to string: {e}"
        ) from e

    try:
        profile_dict = json.loads(profile_string)
        return Profile.model_validate(profile_dict)
    except Exception as e:
        raise ProfileDecodingError(f"Failed to deserialize profile: {e}") from e
