from extensions import db
from datetime import datetime, timezone

from ..domain_entity.roles import Role
from ...utils.cryptographic_operations.password_security.password_hash import hash_password, verify_password


class Member(db.Model):
    __tablename__ = "members"

    id           = db.Column(db.Integer, primary_key=True)
    email        = db.Column(db.String(100))
    username     = db.Column(db.String(100))
    password     = db.Column(db.Text)

    role         = db.Column(
        db.Enum(Role),
        nullable=False,
        default=Role.GUEST
        )
    created_at   = db.Column(
        db.DateTime(timezone=True),
        nullable=False, 
        default=lambda: datetime.now(timezone.utc)
        )


    def set_password(self, raw: str) -> None:
        self.password = hash_password(raw)
 
    def verify_password(self, raw: str) -> bool:
        return verify_password(raw, self.password)
 
    def __repr__(self) -> str:
        return f"<Member {self.username} [{self.role.value}]>"

    