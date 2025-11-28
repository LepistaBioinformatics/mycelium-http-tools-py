"""
Tests for decode_and_decompress_profile_from_base64 function
"""

import base64
import json
from pathlib import Path

import pytest
import zstandard as zstd

from myc_http_tools.exceptions import ProfileDecodingError
from myc_http_tools.functions import decode_and_decompress_profile_from_base64
from myc_http_tools.models.profile import Profile


def load_large_profile() -> dict:
    """Load large profile from JSON file."""
    mock_path = Path(__file__).parent / "mock" / "large-profile.json"
    with open(mock_path, "r", encoding="utf-8") as f:
        return json.load(f)


def compress_and_encode_profile_to_base64(profile: Profile) -> str:
    """Compress and encode a profile to Base64.

    This is the inverse operation of decode_and_decompress_profile_from_base64.
    Used for testing roundtrip operations.
    """
    # Serialize profile to JSON
    profile_json = profile.model_dump_json(by_alias=True)

    # Compress with ZSTD
    compressor = zstd.ZstdCompressor()
    compressed = compressor.compress(profile_json.encode("utf-8"))

    # Encode to Base64
    encoded = base64.standard_b64encode(compressed).decode("ascii")

    return encoded


class TestDecodeAndDecompressProfileFromBase64:
    """Test cases for decode_and_decompress_profile_from_base64 function"""

    def test_decode_and_decompress_profile_roundtrip(self):
        """Test roundtrip: compress -> encode -> decode -> decompress"""
        # Load large profile from JSON file
        profile_dict = load_large_profile()
        original_profile = Profile.model_validate(profile_dict)

        # Compress and encode the profile
        encoded = compress_and_encode_profile_to_base64(original_profile)

        assert encoded, "Encoded profile should not be empty"

        # Decode and decompress the profile
        decoded_profile = decode_and_decompress_profile_from_base64(encoded)

        # Verify that the decoded profile matches the original
        assert (
            original_profile.acc_id == decoded_profile.acc_id
        ), "Account ID should match"

        assert len(original_profile.owners) == len(
            decoded_profile.owners
        ), "Number of owners should match"

        assert (
            original_profile.is_subscription == decoded_profile.is_subscription
        ), "Subscription status should match"

        assert (
            original_profile.is_manager == decoded_profile.is_manager
        ), "Manager status should match"

        assert (
            original_profile.is_staff == decoded_profile.is_staff
        ), "Staff status should match"

        # Compare the full profiles by serializing to JSON
        original_json = original_profile.model_dump_json(by_alias=True)
        decoded_json = decoded_profile.model_dump_json(by_alias=True)

        assert original_json == decoded_json, "Full profile JSON should match exactly"

    def test_decode_and_decompress_profile_with_bytes_input(self):
        """Test that the function accepts bytes input"""
        profile_dict = load_large_profile()
        original_profile = Profile.model_validate(profile_dict)

        # Compress and encode the profile
        encoded = compress_and_encode_profile_to_base64(original_profile)

        # Pass as bytes instead of string
        encoded_bytes = encoded.encode("utf-8")

        # Decode and decompress the profile
        decoded_profile = decode_and_decompress_profile_from_base64(encoded_bytes)

        assert (
            original_profile.acc_id == decoded_profile.acc_id
        ), "Account ID should match"

    def test_decode_and_decompress_profile_invalid_base64(self):
        """Test error when input is not valid Base64"""
        invalid_base64 = "not-valid-base64!!!"

        with pytest.raises(ProfileDecodingError) as exc_info:
            decode_and_decompress_profile_from_base64(invalid_base64)

        assert "Failed to decode base64 profile" in exc_info.value.message
        assert exc_info.value.code == "MYC00020"

    def test_decode_and_decompress_profile_invalid_zstd(self):
        """Test error when Base64 content is not valid ZSTD compressed data"""
        # Valid Base64 but not ZSTD compressed
        invalid_zstd = base64.standard_b64encode(b"not zstd data").decode("ascii")

        with pytest.raises(ProfileDecodingError) as exc_info:
            decode_and_decompress_profile_from_base64(invalid_zstd)

        assert "Failed to decompress profile" in exc_info.value.message
        assert exc_info.value.code == "MYC00020"

    def test_decode_and_decompress_profile_invalid_json(self):
        """Test error when decompressed content is not valid JSON"""
        # Create valid ZSTD compressed data but with invalid JSON content
        compressor = zstd.ZstdCompressor()
        compressed = compressor.compress(b"not valid json {{{")
        encoded = base64.standard_b64encode(compressed).decode("ascii")

        with pytest.raises(ProfileDecodingError) as exc_info:
            decode_and_decompress_profile_from_base64(encoded)

        assert "Failed to deserialize profile" in exc_info.value.message
        assert exc_info.value.code == "MYC00020"

    def test_decode_and_decompress_profile_invalid_profile_schema(self):
        """Test error when JSON does not match Profile schema"""
        # Create valid ZSTD compressed JSON but with wrong schema
        invalid_profile = {"invalid_field": "value"}
        compressor = zstd.ZstdCompressor()
        compressed = compressor.compress(json.dumps(invalid_profile).encode("utf-8"))
        encoded = base64.standard_b64encode(compressed).decode("ascii")

        with pytest.raises(ProfileDecodingError) as exc_info:
            decode_and_decompress_profile_from_base64(encoded)

        assert "Failed to deserialize profile" in exc_info.value.message
        assert exc_info.value.code == "MYC00020"

    def test_decode_and_decompress_profile_empty_string(self):
        """Test error when input is empty string"""
        with pytest.raises(ProfileDecodingError) as exc_info:
            decode_and_decompress_profile_from_base64("")

        # Empty string will fail at decompression since empty base64 decodes to empty bytes
        assert exc_info.value.code == "MYC00020"

    def test_decode_and_decompress_profile_preserves_licensed_resources(self):
        """Test that licensed resources are preserved after roundtrip"""
        profile_dict = load_large_profile()
        original_profile = Profile.model_validate(profile_dict)

        # Compress and encode the profile
        encoded = compress_and_encode_profile_to_base64(original_profile)

        # Decode and decompress the profile
        decoded_profile = decode_and_decompress_profile_from_base64(encoded)

        # Verify licensed resources
        assert decoded_profile.licensed_resources is not None
        assert original_profile.licensed_resources is not None

        original_records = original_profile.licensed_resources.to_licenses_vector()
        decoded_records = decoded_profile.licensed_resources.to_licenses_vector()

        assert len(original_records) == len(
            decoded_records
        ), "Number of licensed resources should match"

        # Check first and last record
        assert (
            original_records[0].acc_id == decoded_records[0].acc_id
        ), "First record acc_id should match"
        assert (
            original_records[0].acc_name == decoded_records[0].acc_name
        ), "First record acc_name should match"
        assert (
            original_records[-1].acc_id == decoded_records[-1].acc_id
        ), "Last record acc_id should match"
        assert (
            original_records[-1].acc_name == decoded_records[-1].acc_name
        ), "Last record acc_name should match"

    def test_decode_and_decompress_profile_preserves_owners(self):
        """Test that owners are preserved after roundtrip"""
        profile_dict = load_large_profile()
        original_profile = Profile.model_validate(profile_dict)

        # Compress and encode the profile
        encoded = compress_and_encode_profile_to_base64(original_profile)

        # Decode and decompress the profile
        decoded_profile = decode_and_decompress_profile_from_base64(encoded)

        # Verify owners
        assert len(original_profile.owners) == len(decoded_profile.owners)

        for i, (original_owner, decoded_owner) in enumerate(
            zip(original_profile.owners, decoded_profile.owners)
        ):
            assert (
                original_owner.id == decoded_owner.id
            ), f"Owner {i} id should match"
            assert (
                original_owner.email == decoded_owner.email
            ), f"Owner {i} email should match"
            assert (
                original_owner.first_name == decoded_owner.first_name
            ), f"Owner {i} first_name should match"
            assert (
                original_owner.last_name == decoded_owner.last_name
            ), f"Owner {i} last_name should match"
            assert (
                original_owner.username == decoded_owner.username
            ), f"Owner {i} username should match"
            assert (
                original_owner.is_principal == decoded_owner.is_principal
            ), f"Owner {i} is_principal should match"

    def test_decode_and_decompress_profile_preserves_tenants_ownership(self):
        """Test that tenants ownership is preserved after roundtrip"""
        profile_dict = load_large_profile()
        original_profile = Profile.model_validate(profile_dict)

        # Compress and encode the profile
        encoded = compress_and_encode_profile_to_base64(original_profile)

        # Decode and decompress the profile
        decoded_profile = decode_and_decompress_profile_from_base64(encoded)

        # Verify tenants ownership
        assert decoded_profile.tenants_ownership is not None
        assert original_profile.tenants_ownership is not None
        assert decoded_profile.tenants_ownership.records is not None
        assert original_profile.tenants_ownership.records is not None

        assert len(original_profile.tenants_ownership.records) == len(
            decoded_profile.tenants_ownership.records
        ), "Number of tenants ownership records should match"

        for i, (original_record, decoded_record) in enumerate(
            zip(
                original_profile.tenants_ownership.records,
                decoded_profile.tenants_ownership.records,
            )
        ):
            assert (
                original_record.id == decoded_record.id
            ), f"Tenant ownership {i} id should match"
            assert (
                original_record.name == decoded_record.name
            ), f"Tenant ownership {i} name should match"

