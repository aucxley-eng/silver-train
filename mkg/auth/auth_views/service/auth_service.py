"""
Business logic for authentication.

Returns plain Python objects / tuples — no Flask objects.
Routes are responsible for turning these into HTTP responses.
"""

from mkg.auth.auth_models.domain_entity.auth_domain import Member
from mkg.auth.auth_models.repo_layer.sqlalchemy_repo import MemberRepository
from mkg.auth.auth_models.schema.auth_schema import MemberSchema
from ...utils.cryptographic_operations.tokens.blcklist import blacklist_jti
from ...utils.cryptographic_operations.tokens.jwt import create_token, decode_token

member_schema = MemberSchema()


class AuthService:

    def __init__(self):
        self.repo = MemberRepository()

    # ── register ──────────────────────────────────────────────────

    def register(self, data: dict) -> tuple[dict | None, dict | None]:
        """
        Validate, create, and persist a new Member.

        Returns (serialized_member, errors).
        Exactly one of the two will be None.
        """
        # Unique-field checks before hitting the DB
        if self.repo.get_by_email(data.get("email", "")):
            return None, {"email": ["A member with that email already exists."]}

        if self.repo.get_by_username(data.get("username", "")):
            return None, {"username": ["That username is already taken."]}

        # Marshmallow validation + object hydration
        from marshmallow import ValidationError
        try:
            member: Member = member_schema.load(data)
        except ValidationError as exc:
            return None, exc.messages

        member.set_password(data["password"])
        
        self.repo.save(member)

        return member_schema.dump(member), None

    # ── login ─────────────────────────────────────────────────────

    def login(self, email: str, password: str) -> tuple[dict | None, str | None]:
        """
        Verify credentials and issue a token.

        Returns (token_payload, error_message).
        """
        member = self.repo.get_by_email(email)

        # Deliberate: same error message for unknown email and wrong password
        # so an attacker cannot enumerate registered emails.
        if not member or not member.verify_password(password):
            return None, "Invalid email or password."

        token = create_token(
            user_id  = member.id,
            role     = member.role.value,
            username = member.username,
        )

        return {
            "access_token": token,
            "member": {
                "id":       member.id,
                "username": member.username,
                "role":     member.role.value,
            },
        }, None

    # ── logout ────────────────────────────────────────────────────

    def logout(self, token: str) -> str | None:
        """
        Revoke the token by blacklisting its jti.

        Returns an error message string on failure, None on success.
        The middleware already verified the token before this runs,
        but we decode again to pull the jti cleanly.
        """
        try:
            payload = decode_token(token)
        except ValueError as exc:
            return str(exc)

        if jti := payload.get("jti"):
            blacklist_jti(jti)

        return None

