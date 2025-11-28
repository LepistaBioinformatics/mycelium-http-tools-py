"""Decode and decompress profile from Base64.

This module provides a function to decode a Base64-encoded, ZSTD-compressed
profile string and return a Profile object.
"""

import base64
import json
from typing import Union

import zstandard as zstd

from myc_http_tools.exceptions import ProfileDecodingError
from myc_http_tools.models.profile import Profile


def decode_and_decompress_profile_from_base64(
    profile: Union[str, bytes],
) -> Profile:
    """Decode and decompress a profile from Base64.

    This function decodes a Base64-encoded string and decompresses it using ZSTD,
    then deserializes the resulting JSON into a Profile object.

    Args:
        profile: The Base64-encoded, ZSTD-compressed profile string or bytes.

    Returns:
        Profile: The decoded and decompressed profile.

    Raises:
        ProfileDecodingError: If there is an error during decoding, decompression,
            or deserialization.
    """
    # Decode from Base64
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

    # Decompress profile from ZSTD
    try:
        decompressor = zstd.ZstdDecompressor()
        decompressed_profile = decompressor.decompress(decoded_profile)
    except Exception as e:
        raise ProfileDecodingError(f"Failed to decompress profile: {e}") from e

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
