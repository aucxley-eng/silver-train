import base64
import hashlib
import hmac
import json
import uuid
from datetime import datetime, timezone
from flask import current_app

def _secret() -> str:
    return current_app.config["SECRET_KEY"]
 
 
def _expiry() -> int:
    return int(current_app.config.get("TOKEN_EXPIRY_SECONDS", 3600))
 
 
def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")
 
 
def _b64url_decode(s: str) -> bytes:
    pad = 4 - len(s) % 4
    if pad != 4:
        s += "=" * pad
    return base64.urlsafe_b64decode(s)
 
 
def _sign(message: str) -> str:
    """HMAC-SHA256 over message; returns base64url-encoded digest."""
    raw = hmac.new(
        _secret().encode(),
        message.encode(),
        hashlib.sha256,
    ).digest()
    return _b64url_encode(raw)
 
 
# ── Public JWT API ────────────────────────────────────────────────────────────
 
def create_token(user_id: int, role: str, username: str) -> str:
    """
    Issue a signed JWT.
 
    Claims
    ──────
    sub      — user primary key (integer stored as int)
    username — convenience claim, not security-critical
    role     — "guest" | "member" | "admin"
    jti      — UUID4, used to revoke individual tokens on logout
    iat      — issued-at  (UTC unix timestamp)
    exp      — expiry     (UTC unix timestamp)
    """
    now = int(datetime.now(timezone.utc).timestamp())
 
    header = _b64url_encode(
        json.dumps({"alg": "HS256", "typ": "JWT"}, separators=(",", ":")).encode()
    )
    payload = _b64url_encode(
        json.dumps(
            {
                "sub":      user_id,
                "username": username,
                "role":     role,
                "jti":      str(uuid.uuid4()),
                "iat":      now,
                "exp":      now + _expiry(),
            },
            separators=(",", ":"),
        ).encode()
    )
 
    return f"{header}.{payload}.{_sign(f'{header}.{payload}')}"
 
 
def decode_token(token: str) -> dict:
    """
    Verify signature + expiry and return the payload dict.
 
    Raises ValueError (with a user-safe message) on any failure.
    The middleware catches ValueError and returns HTTP 401.
    """
    try:
        parts = token.split(".")
        if len(parts) != 3:
            raise ValueError("Malformed token")
 
        header_b64, payload_b64, provided_sig = parts
 
        if not hmac.compare_digest(provided_sig, _sign(f"{header_b64}.{payload_b64}")):
            raise ValueError("Invalid token signature")
 
        payload = json.loads(_b64url_decode(payload_b64))
 
        if payload.get("exp", 0) < int(datetime.now(timezone.utc).timestamp()):
            raise ValueError("Token has expired — please log in again")
 
        return payload
 
    except (KeyError, json.JSONDecodeError) as exc:
        raise ValueError("Malformed token") from exc
    