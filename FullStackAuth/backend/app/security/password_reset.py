
import hashlib
import secrets


def generate_otp() -> str:
    """
    Generate a cryptographically secure six-digit OTP.
    """
    return f"{secrets.randbelow(1_000_000):06d}"


def hash_otp(otp: str) -> str:
    """
    Hash the OTP using SHA-256 before storing it.
    """
    return hashlib.sha256(otp.encode("utf-8")).hexdigest()
