"""
Encryption utilities for Your Brief.

Uses Fernet (symmetric encryption) to encrypt/decrypt user OAuth tokens
before storing them in the database.
"""
import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def get_cipher():
    """
    Get Fernet cipher instance using encryption key from environment.

    Returns:
        Fernet: Cipher instance

    Raises:
        ValueError: If ENCRYPTION_KEY not found in environment
    """
    encryption_key = os.getenv('ENCRYPTION_KEY')
    if not encryption_key:
        raise ValueError(
            "ENCRYPTION_KEY not found in environment. "
            "Run 'python scripts/generate_keys.py' to generate one."
        )

    return Fernet(encryption_key.encode())


def encrypt_token(token: str) -> str:
    """
    Encrypt a token string.

    Args:
        token: Plain text token to encrypt

    Returns:
        Encrypted token as string

    Example:
        >>> encrypted = encrypt_token("my-secret-token")
        >>> encrypted
        'gAAAAABh...'
    """
    cipher = get_cipher()
    encrypted_bytes = cipher.encrypt(token.encode())
    return encrypted_bytes.decode()


def decrypt_token(encrypted: str) -> str:
    """
    Decrypt an encrypted token.

    Args:
        encrypted: Encrypted token string

    Returns:
        Decrypted plain text token

    Example:
        >>> token = decrypt_token(encrypted)
        >>> token
        'my-secret-token'
    """
    cipher = get_cipher()
    decrypted_bytes = cipher.decrypt(encrypted.encode())
    return decrypted_bytes.decode()


def generate_encryption_key() -> str:
    """
    Generate a new Fernet encryption key.

    Returns:
        Base64-encoded encryption key

    Example:
        >>> key = generate_encryption_key()
        >>> print(key)
        'gAAAAABh1234567890abcdef...'
    """
    return Fernet.generate_key().decode()


if __name__ == '__main__':
    """Quick test of encryption utilities."""
    # Generate a test key
    test_key = generate_encryption_key()
    print(f"Generated test encryption key: {test_key}")

    # Set it temporarily for testing
    os.environ['ENCRYPTION_KEY'] = test_key

    # Test encryption/decryption
    original = "test-oauth-token-12345"
    encrypted = encrypt_token(original)
    decrypted = decrypt_token(encrypted)

    print(f"\nOriginal:  {original}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"\nEncryption working: {original == decrypted}")
