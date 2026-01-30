#!/usr/bin/env python3
"""
Generate secrets and keys for Your Brief web app.

Generates:
- FLASK_SECRET_KEY: For Flask session security
- ENCRYPTION_KEY: For encrypting OAuth tokens

Usage:
    python scripts/generate_keys.py
    or
    uv run python scripts/generate_keys.py
"""
import secrets
from cryptography.fernet import Fernet


def generate_flask_secret_key(length: int = 32) -> str:
    """
    Generate a secure random secret key for Flask.

    Args:
        length: Length of the key in bytes (default 32)

    Returns:
        Hex-encoded secret key
    """
    return secrets.token_hex(length)


def generate_encryption_key() -> str:
    """
    Generate a Fernet encryption key.

    Returns:
        Base64-encoded Fernet key
    """
    return Fernet.generate_key().decode()


def main():
    """Generate and display all required keys."""
    print("=" * 70)
    print("Your Brief - Key Generator")
    print("=" * 70)
    print("\nGenerating secure keys for your .env file...\n")

    # Generate keys
    flask_secret = generate_flask_secret_key()
    encryption_key = generate_encryption_key()

    # Display results
    print("Copy these values to your .env file:")
    print("-" * 70)
    print()
    print(f"FLASK_SECRET_KEY={flask_secret}")
    print()
    print(f"ENCRYPTION_KEY={encryption_key}")
    print()
    print("-" * 70)
    print()
    print("⚠️  IMPORTANT:")
    print("  - Keep these keys secret and never commit them to git")
    print("  - Store them securely in your .env file")
    print("  - If you change ENCRYPTION_KEY, existing encrypted tokens will be invalid")
    print()
    print("✅ Keys generated successfully!")
    print()


if __name__ == '__main__':
    main()
