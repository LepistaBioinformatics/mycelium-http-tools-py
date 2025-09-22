#!/usr/bin/env python3
"""
Test runner script for mycelium-http-tools
"""
import subprocess
import sys
from pathlib import Path


def run_tests():
    """Run all tests using pytest"""
    project_root = Path(__file__).parent
    test_dir = project_root / "src" / "tests"

    print("Running tests for mycelium-http-tools...")
    print(f"Test directory: {test_dir}")
    print("-" * 50)

    try:
        # Run pytest with verbose output
        subprocess.run(
            ["poetry", "run", "pytest", str(test_dir), "-v", "--tb=short"],
            cwd=project_root,
            check=True,
        )

        print("-" * 50)
        print("✅ All tests passed!")
        return 0

    except subprocess.CalledProcessError as e:
        print("-" * 50)
        print(f"❌ Tests failed with exit code {e.returncode}")
        return e.returncode
    except FileNotFoundError:
        print("❌ Error: poetry not found. Please install poetry first.")
        return 1


if __name__ == "__main__":
    sys.exit(run_tests())
