import hashlib
import hmac
import os

# ── Password hashing ──────────────────────────────────────────────────────────
 
def hash_password(plain: str) -> str:
    """
    PBKDF2-HMAC-SHA256 with a random 16-byte salt.
 
    Storage format: "hex_salt$hex_digest"
 
    PBKDF2 is a key-stretching function: it runs SHA-256 260 000 times
    deliberately so that brute-forcing one hash costs real CPU time.
    The salt ensures two users with the same password produce completely
    different stored values.
    """
    salt   = os.urandom(16)
    digest = hashlib.pbkdf2_hmac(
        hash_name  = "sha256",
        password   = plain.encode(),
        salt       = salt,
        iterations = 260_000,        # NIST SP 800-132 recommended minimum (2023)
    )
    return f"{salt.hex()}${digest.hex()}"
 
 
def verify_password(plain: str, stored: str) -> bool:
    """
    Re-derive the hash using the stored salt and compare timing-safely.
 
    hmac.compare_digest prevents timing attacks: the comparison always
    takes the same amount of time regardless of where the strings differ.
    """
    try:
        salt_hex, hash_hex = stored.split("$", 1)
        salt     = bytes.fromhex(salt_hex)
        expected = bytes.fromhex(hash_hex)
    except (ValueError, AttributeError):
        return False
 
    candidate = hashlib.pbkdf2_hmac(
        hash_name  = "sha256",
        password   = plain.encode(),
        salt       = salt,
        iterations = 260_000,
    )
    return hmac.compare_digest(candidate, expected)
