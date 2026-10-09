
import hashlib
import secrets


def generate_refresh_token() -> str:
    """
    Generate a cryptographically secure opaque refresh token.
    """
    return secrets.token_urlsafe(64)


def hash_refresh_token(refresh_token: str) -> str:
    """
    Return the SHA-256 hash of a refresh token.
    """
    return hashlib.sha256(
        refresh_token.encode("utf-8")
    ).hexdigest()
