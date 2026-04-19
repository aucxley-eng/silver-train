"""
One job: verify tokens and enforce RBAC on every protected route.

Usage
─────
    from app.middleware.auth_middleware import require_role

    @books_bp.route("/api/books", methods=["POST"])
    @require_role("member", "admin")
    def create_book():
        user_id = g.current_user["sub"]
        ...

After the decorator passes, g.current_user holds the full JWT payload:
    {
        "sub":      1,
        "username": "alice",
        "role":     "member",
        "jti":      "uuid-string",
        "iat":      1234567890,
        "exp":      1234571490,
    }

HTTP responses
──────────────
  401 — no token / bad signature / expired / revoked
  403 — valid token but role not in allowed set
"""

import functools
from flask import g, jsonify, request

from ..cryptographic_operations.tokens.jwt import decode_token
from ..cryptographic_operations.tokens.blcklist import is_blacklisted


def _extract_bearer() -> str | None:
    """Parse 'Authorization: Bearer <token>' → token string or None."""
    header = request.headers.get("Authorization", "")
    parts  = header.split(" ", 1)
    if len(parts) == 2 and parts[0].lower() == "bearer":
        return parts[1]
    return None


def require_role(*allowed_roles: str):
    """
    Decorator factory.  Pass one or more role strings that may access the route.

        @require_role("admin")                   # admin only
        @require_role("member", "admin")         # member OR admin
    """
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):

            # 1 — token present?
            token = _extract_bearer()
            if not token:
                return jsonify({"error": "Authentication required"}), 401

            # 2 — signature valid and not expired?
            try:
                payload = decode_token(token)
            except ValueError as exc:
                return jsonify({"error": str(exc)}), 401

            # 3 — not revoked?
            if is_blacklisted(payload.get("jti", "")):
                return jsonify({"error": "Token has been revoked — please log in again"}), 401

            # 4 — role allowed?
            if payload.get("role") not in allowed_roles:
                return jsonify({
                    "error": (
                        f"Access denied. Required: {' or '.join(allowed_roles)}. "
                        f"Your role: {payload.get('role', 'none')}"
                    )
                }), 403

            # 5 — attach to request context and proceed
            g.current_user = payload
            return fn(*args, **kwargs)

        return wrapper
    return decorator
